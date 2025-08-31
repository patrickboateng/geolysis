# Python Style Guide

We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style 
guide for formatting Python code. Docstrings follow
[PEP 257](https://www.python.org/dev/peps/pep-0257/). We use sphinx 
documentation format for documenting objects. (`packages`, `modules`, 
`classes`, `methods`, `functions` and `GLOBAL variables` if necessary)

The rest of the document describes additions and clarifications to the **PEP**
documents that we follow.

## Indentation

Use 4 spaces (no tabs) for indentation.

## Import conventions

Except in cases of circular imports, all imports should be at the top of the
file, grouped into three sections and separated by blanklines. The sections
should be, imports from the **standard library**, followed by
**third party libraries**, and then imports from **geolysis** itself.

- **Bearing Capacity**

    - **Allowable Bearing Capacity (ABC)**
     
      ```python
      from geolysis.bearing_capacity.abc import create_abc_4_cohesionless_soils
      ```
        
    - **Ultimate Bearing Capacity (UBC)**
     
      ```python
      from geolysis.bearing_capacity.ubc import create_ubc_4_all_soil_types
      ```

- **Foundation**
 
  ```python
  from geolysis.foundation import create_foundation
  ```
  
- **Soil Classification**
 
  ```python
  from geolysis.soil_classifier import create_uscs_classifier
  from geolysis.soil_classifier import create_aashto_classifier
  ```
 
- **Standard Penetration Test (SPT) Analysis**
 
  ```python
  from geolysis.spt import DilatancyCorrection
  from geolysis.spt import EnergyCorrection
  from geolysis.spt import SPT
  from geolysis.spt import create_overburden_pressure_correction
  ```
    
## Code Documentation

### Documenting Classes

```python

class ClassName:

    """Short description of class.
    
    Long description of class.
    
    Example usage and other informations.
    
    """
    
    def __init__(self, arg_1: str, arg_2: int) -> None:
        """
        :param arg_1: Argument 1 description.
        
        :param arg_2: Argument 2 description.
        
        :raises ExcetionType: Description of why exception occurs.
     
        """
        
```

**_There is no need to provide additional types in docstrings_**

Objects in a class should be arranged in the following order:

- Class Variables
- Dunder Methods (eg. ``__init__``, ``__str__``, etc)
- Properties
- Public/Private Properties
- Instance Methods
- Class Methods
- Static Methods

**_It is best to define private methods closest to their intended use_**

### Documenting Functions

```text

def function_name(arg_1: str, arg_2: int) -> ReturnType:
    """Short description of function.
    
    Long description of function.
    
    Example Usage and other informations.
    
    :param arg_1: Argument 1 description.
        
    :param arg_2: Argument 2 description.
        
    :raises ExcetionType: Description of why exception occurs.
    
    :return: Description of what is returned.
     
    """
    
```

**_Method docstrings use the same format as function docstrings, as always
`self` is not documented._**

### Documenting Constants

```text

CONSTANT_NAME = value
"""Short constant description.

Long constant description if any.

Any other information if any.

"""

```

**_Docstrings for constants (or primitive types) will not be visible in text 
terminals because they are not natively supported in python, but will appear 
in the documentation built with mkdocs._**
