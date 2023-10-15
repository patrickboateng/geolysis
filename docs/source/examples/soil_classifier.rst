Classification of soil according to ``USCS``.

Single classification example:

.. doctest::

    >>> from geolysis.soil_classifier import USCS
    >>> uscs_classifier = USCS(liquid_limit=34.1, 
    ...                        plastic_limit=21.1, 
    ...                        plasticity_index=13,
    ...                        fines=47.88, 
    ...                        sand=37.84, 
    ...                        gravel=14.28)
    >>> uscs_classifier.classify()
    'SC'

Dual classification example:

.. doctest::

    >>> uscs_classifier = USCS(liquid_limit=30.8, 
    ...                        plastic_limit=20.7, 
    ...                        plasticity_index=10.1,
    ...                        fines=10.29, 
    ...                        sand=81.89, 
    ...                        gravel=7.83, 
    ...                        d10=0.07, 
    ...                        d30=0.3, 
    ...                        d60=0.8)
    >>> uscs_classifier.classify()
    'SW-SC'

Classification of soil using `AASHTO` classification system.

.. doctest::

    >>> from geolysis.soil_classifier import AASHTO
    >>> aashto_classifier = AASHTO(liquid_limit=37.7, 
    ...                            plasticity_index=13.9, 
    ...                            fines=47.44)
    >>> aashto_classifier.classify()
    'A-6(4)'