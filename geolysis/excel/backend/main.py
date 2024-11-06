import json
from typing import Annotated, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from geolysis.core.soil_classifier import SCType, SoilClassificationFactory


class SoilParam(BaseModel):
    liquid_limit: int | float
    plastic_limit: int | float
    fines: int | float
    sand: Optional[float] = None
    d_10: int | float = 0
    d_30: int | float = 0
    d_60: int | float = 0
    add_group_idx: bool = True
    organic: bool = False


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_soil_classification(soil_params: SoilParam, clf_type: SCType):
    params = json.loads(soil_params.model_dump_json())
    clf = SoilClassificationFactory.create_soil_classifier(
        **params,
        clf_type=clf_type,
    )
    return {"classification": clf.classify(), "description": clf.description()}


@app.get("/aashto/")
async def aashto(soil_param: Annotated[SoilParam, Query()]):
    return get_soil_classification(
        soil_params=soil_param,
        clf_type=SCType.AASHTO,
    )


@app.get("/uscs/")
async def uscs(soil_param: Annotated[SoilParam, Query()]):
    return get_soil_classification(
        soil_params=soil_param,
        clf_type=SCType.USCS,
    )
