import json
from typing import Annotated, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from geolysis.core.soil_classifier import ClfType, create_soil_classifier


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


def _soil_classification(soil_param: SoilParam, clf_type: ClfType):
    params = json.loads(soil_param.model_dump_json())
    clf = create_soil_classifier(**params, clf_type=clf_type)
    return {"classification": clf.classify(), "description": clf.description()}


@app.get("/aashto/")
async def aashto(soil_param: Annotated[SoilParam, Query()]):
    return _soil_classification(soil_param=soil_param, clf_type=ClfType.AASHTO)


@app.get("/uscs/")
async def uscs(soil_param: Annotated[SoilParam, Query()]):
    return _soil_classification(soil_param=soil_param, clf_type=ClfType.USCS)
