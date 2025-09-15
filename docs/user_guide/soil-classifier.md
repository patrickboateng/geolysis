# Soil Classification

## AASHTO classification

```python

>>> from geolysis.soil_classifier import create_aashto_classifier
>>> aashto_clf = create_aashto_classifier(liquid_limit=30.2,
...                                       plastic_limit=23.9,
...                                       fines=11.18, )
>>> clf = aashto_clf.classify()
>>> clf.symbol
'A-2-4(0)'
>>> clf.symbol_no_group_idx
'A-2-4'
>>> clf.group_index
'0'
>>> clf.description
'Silty or clayey gravel and sand'

```

## USCS classification

Classification with soil grading

```python

>>> from geolysis.soil_classifier import create_uscs_classifier
>>> uscs_clf = create_uscs_classifier(liquid_limit=30.8,
...                                   plastic_limit=20.7,
...                                   fines=10.29,
...                                   sand=81.89,
...                                   d_10=0.07,
...                                   d_30=0.3,
...                                   d_60=0.8, )
>>> clf = uscs_clf.classify()
>>> clf.symbol
'SW-SC'
>>> clf.description
'Well graded sand with clay'

```

Classification without soil grading

```python

>>> uscs_clf = create_uscs_classifier(liquid_limit=34.1,
...                                   plastic_limit=21.1,
...                                   fines=47.88,
...                                   sand=37.84, )
>>> clf = uscs_clf.classify()
>>> clf.symbol
'SC'
>>> clf.description
'Clayey sands'

```
