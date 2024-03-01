.. currentmodule:: geolysis.estimators

*******************************
How to estimate soil parameters
*******************************

Importing objects
=================

.. code:: python

   >>> from geolysis.estimators import (
   ...      SoilUnitWeightEst, 
   ...      CompressionIndexEst, 
   ...      SoilFrictionAngleEst,
   ...      UndrainedShearStrengthEst,
   ... )


Soil Unit Weight
================

Estimate the moist unit weight of soil from ``SPT N60``: ::

   >>> suw_est = SoilUnitWeightEst(spt_n_60=13)
   >>> suw_est.moist_wgt
   17.3

Estimate the saturated unit weight of soil from ``SPT N60``: ::

   >>> suw_est = SoilUnitWeightEst(spt_n_60=13)
   >>> suw_est.saturated_wgt
   18.75

Estimate the submerged unit weight of soil from ``SPT N60``: ::

   >>> suw_est = SoilUnitWeightEst(spt_n_60=13)
   >>> suw_est.submerged_wgt
   8.93

Compression Index
=================

Estimate compression index using relations given by, ``Terzaghi el al (1967)``
, ``Skempton (1994)``, and ``Hough (1957)`` respectively: ::

   >>> CompressionIndexEst.terzaghi_et_al_ci_1967(liquid_limit=35)
   0.225
   >>> CompressionIndexEst.skempton_ci_1994(liquid_limit=35)
   0.175
   >>> CompressionIndexEst.hough_ci_1957(void_ratio=0.78)
   0.148

Soil Internal Angle of Friction
===============================

Estimate soil internal angle of friction using relations given by, 
``Wolff (1989)``, and ``Kullhawy & Mayne (1990)`` respectively: ::

   >>> SoilFrictionAngleEst.wolff_sfa_1989(spt_n_60=50)
   40.75
   >>> SoilFrictionAngleEst.kullhawy_mayne_sfa_1990(
   ...        spt_n_60=40, 
   ...        eop=103.8, 
   ...        atm_pressure=101.325
   ... )
   46.874

Undrained Shear Strength 
========================

Estimate undrained shear strength of soil using relations given by,
``Stroud (1974)``, and ``Skempton (1974)`` respectively: ::

   >>> UndrainedShearStrengthEst.stroud_uss_1974(spt_n_60=40)
   140.0
   >>> UndrainedShearStrengthEst.skempton_uss_1957(eop=108.3, plasticity_index=12)
   16.722
