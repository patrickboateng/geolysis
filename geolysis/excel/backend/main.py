from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from geolysis.core.soil_classifier import (
    AASHTO,
    PSD,
    USCS,
    AtterbergLimits,
    SizeDistribution,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/aashto/")
async def aashto(
    liquidLimit: float,
    plasticityIndex: float,
    fines: float,
    addGroupIndex: bool,
):
    clf = AASHTO(
        liquid_limit=liquidLimit,
        plasticity_index=plasticityIndex,
        fines=fines,
        add_group_idx=addGroupIndex,
    )

    return {"classification": clf.classify(), "description": clf.description()}


@app.get("/uscs/")
async def uscs(
    liquidLimit: float,
    plasticLimit: float,
    fines: float,
    sand: float,
    d_10: float,
    d_30: float,
    d_60: float,
    organic: bool,
):
    al = AtterbergLimits(liquid_limit=liquidLimit, plastic_limit=plasticLimit)
    size_dist = SizeDistribution(d_10=d_10, d_30=d_30, d_60=d_60)
    psd = PSD(fines=fines, sand=sand, size_dist=size_dist)
    clf = USCS(atterberg_limits=al, psd=psd, organic=organic)

    return {"classification": clf.classify(), "description": clf.description()}
