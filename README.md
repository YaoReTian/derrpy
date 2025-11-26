# derrpy
Library for python for scientific values, including uncertainties and units  

## Run-time dependencies
- Numpy

## Usage
Note: before I figure out how to publish this to PyPI, this can be built locally and the .so file could be copied to any directory where it is needed, see instructions in [Build instructions](#Build-instructions)

This library can be used to represent values which require uncertainty and units.

### Using DataErr
Below shows an example of using the `derrpy.DataErr` class to multiply 2 unitless values together

```
import derrpy as dp

data1 = dp.DataErr(50,2)
data2 = dp.DataErr(30, 5)

data3 = data1 * data2
print(data3)
```

The above code outputs:

```
Null / unitless : 1.50E3 +/- 2E2
```

`Null` is the default name for any DataErr object, which can be changed either during instantiation or during runtime using `DataErr.setName()`. Similarly, all values are set to 3 significant figures by default, which can also be changed in the same way as the name using `DataErr.setSigFig()` or during instantiation

`derrpy.DataErr` can be used to calculate addition/subtraction in the case (when the units of both values are equal), multiplication/division (for any units) and exponentiation (given that the exponent is unitless) using the default python operators

When a `float` or `int` is operated on with a DataErr object, they are assumed to be of the same units for addition/subtraction, and to be unitless for multiplication, division and exponentiation
### Using Unit
Below shows an example of using `derrpy.Unit` to define the units of `data1` from the above example

```
u1 = dp.Unit([0,1])
data1.setUnits(u1)
print(data1)
```

The above code outputs:

```
Null / m : 5.00E1 +/- 2E0
```

The `dp.Unit` class takes in an array of 7 elements at maximum, in which an index represents the exponent of the below dimensions in SI units:  
    0 = M/Mass (kg)  
    1 = L/Length (m)  
    2 = T/Time (s)  
    3 = K/Temperature (K)  
    4 = I/Current (A)  
    5 = N/Amount of substance (mol)  
    6 = J/luminous intensity (cd)  
    
Similarly to `derrpy.DataErr`, Units can be multiplied together to form compound units, it is also possible to define a scale and symbol for a user-defined unit as long as the dimensions of the value and the user-defined unit is the same, for example:

```
u2 = dp.Unit([0,1])
u2.setSymScale("km",1000)
data1.convertUnitTo(u2)
print(data1)
```

The above code outputs

```
Null / km : 5.00E-2 +/- 2E-3
```

### Using derrpy with matplotlib or numpy
As derrpy.DataErr types are not directly compatible with matplotlib, derrpy has a built in function `derrpy.parseDerrList()`, which would take in any array-like data structure of `derrpy.DataErr` types, and parse that into a tuple of a list of values and a list of errors. This is useful for cases in numpy or matplotlib when it is needed to separate values and errors

```
data = [dp.DataErr(50,2), dp.DataErr(45,3), dp.DataErr(55,7)]
print(dp.parseDerrList(data))
```

Output:
```
([50, 45, 55], [2, 3, 7])

```

## Build instructions
Build-time dependencies:  
 - Setuptools
 - Cython
 
Instructions:  
Copy and run the below code in the command line  
#####
    git clone https://github.com/YaoReTian/derrpy.git
    cd derrpy
    python3 setup.py build_ext --inplace

This creates a `.so` file which is the library, and can be copied into any directory to be used.

## To be added
 - Support for more standard functions, e.g. sin(x) or log(x)