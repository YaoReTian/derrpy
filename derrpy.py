#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 11:10:09 2025

@author: YaoReTian

derrpy.py
"""

import numpy as np

# Static functions
def formatSciNum(num : float, sigfig : int) -> str:
    """formatSciNum(num : float, sigfig : int) -> str
    
    Returns a string after converting a number into scientific format (standard form)
    
    Parameters
    ----------
    num : float
        Number to be converted to scientific form
    sigfig : int
        Number of significant figures the number will be returned to"""
    if num == 0:
        return "0."+'0'*(sigfig-1)
    
    mag = int(np.floor(np.log10(np.abs(num))))
    val = str(num / (10**mag))
    val += "0"*sigfig
    val = val[0:sigfig+1]
    
    return val + "E" + str(mag)

def parseDerrList(lst):
    """parseDerrList(lst) -> (array-like, array_like)
    
    Converts a list of DataErr types to a tuple of a list of values and a list of errors 
    
    Parameters
    ----------
    lst : array-like
        An array of DataErr types"""
    valLst = []
    errLst = []
    
    for i in lst:
        valLst.append(i.val())
        errLst.append(i.err())
        
    return (valLst,errLst)

# Constants
DIMENSION= ["M","L","T","K","I","N","J"]
SI_BASE_UNIT = ["kg", "m", "s","K","A","mol","cd"]

class Unit:
    """Unit(exps = [0]*7)
    
    Creates a Unit data structure
    
    Parameters
    ----------
    exps: list[float]
        exponents of dimensions in SI units:
            0 = M/Mass (kg)
            1 = L/Length (m)
            2 = T/Time (s)
            3 = K/Temperature (K)
            4 = I/Current (A)
            5 = N/Amount of substance (mol)
            6 = J/luminous intensity (cd)
    """
    def __init__(self, exps = [0]*7):
        
        self.__exps = [0]*7
        for i in range(len(exps)):
            self.__exps[i] = exps[i]
            
        self.__scale = 1
        self.__sym = ""
    
    def __repr__(self):
        return self.units()
    
    # Setters
        
    def setExps(self, exps):
        """u.setExps(exps) 
        
        Sets the exponents of `u`
        
        Parameters
        ----------
        exps: list[float]
            exponents of dimensions in SI units:
                0 = M/Mass (kg)
                1 = L/Length (m)
                2 = T/Time (s)
                3 = K/Temperature (K)
                4 = I/Current (A)
                5 = N/Amount of substance (mol)
                6 = J/luminous intensity (cd)"""
            
        self.__exps = [0]*7
        for i in range(len(exps)):
            self.__exps[i] = exps[i]
        
    def setSymScale(self, symbol : str, scale : float = 1):
        """u.setSymScale(symbol : str, scale : float = 1) 
        
        Sets a user-defined symbol and a conversion factor (scale) for `u`
        
        Parameters
        ----------
        symbol: str
            defines the symbol of a self-defined unit, e.g. N
        scale: int
            constant multiplier between user defined symbol and SI units"""
            
        self.__sym = symbol
        self.__scale = scale
                
    def setExpOf(self, dimension : str, exp : float):
        """u.setExpOf(dimension : str, exp : float) 
        
        Sets the exponent of a specific dimension of `u`
        
        Parameters
        ----------
        dimension : str
            the dimension whose exponent is to be changed (M,L,T,K,I,N,J)
        exp : float
            exponent to be changed to
        """
        self.__exps[DIMENSION.index(dimension)] = exp
        
    # Getters
    def scale(self) -> float:
        """u.scale() -> float
        
        Returns the conversion factor of `u` relative to SI base units if there exists a user defined symbol
        Returns 1 if no user-defined symbol exists
        """
        return self.__scale
    
    def expOf(self, dimension : str) -> float:
        """u.expOf(dimension : str) -> float
        
        Returns the exponent of a dimension of `u`
        """
        return self.__exps[DIMENSION.index(dimension)]
    
    def exps(self):
        """u.exps()
        
        Returns a list of exponents for every dimension of `u`
        """
        return self.__exps
    
    def sym(self) -> str:
        """u.sym() -> str
        
        Returns a user-defined symbol if one exists"""
        return self.__sym
    
    def unitless(self) -> bool:
        """u.unitless() -> bool
        
        Returns True if all the exponents of `u` is 0, False otherwise"""
        if self.__exps == [0]*7:
            return True
        return False
    
    def dimensions(self) -> str:
        """u.dimensions() -> str
        
        Returns a string detailing the dimensions of `u`"""
        if self.unitless():
            return "unitless"
        
        dim = ""
        for i in range(7):
            if self.__exps[i] == 1:
                dim += DIMENSION[i] + " "
            elif self.__exps[i] != 0:
                dim += f"{DIMENSION[i]}^{self.__exps[i]} "
            
        dim = dim[0:len(dim)-1]
        return dim
    
    def units(self) -> str:
        """u.units() -> str
        
        Returns a string detailing the units of `u`
        Returns a user-defined symbol if it exists, otherwise returns SI units"""
        if self.__sym != "":
            return self.__sym
        elif self.unitless():
            return "unitless"
        
        return self.SIunits()
    
    def SIunits(self) -> str:
        """u.SIunits() -> str
        
        Returns a string detailing the units of `u` in SI units"""
        if self.unitless():
            return "unitless"
        units = ""
        for i in range(7):
            if self.__exps[i] == 1:
                units += SI_BASE_UNIT[i] + " "
            elif self.__exps[i] != 0:
                units += f"{SI_BASE_UNIT[i]}^{self.__exps[i]} "
    
        units = units[0:len(units)-1]
        return units
    
    def latex(self) -> str:
        """u.latex() -> str
        
        Returns the results of u.units() in LaTeX form"""
        if self.__sym != "":
            return "$"+self.__sym+"$"
        return self.SIlatex()
    
    def SIlatex(self) -> str:
        """u.SIlatex() -> str
        
        Returns the results of u.SIunits() in LaTeX form"""
        if self.unitless():
            return "$unitless$"
        
        units = "$"
        for i in range(7):
            if self.__exps[i] == 1:
                units += SI_BASE_UNIT[i] + " "
            elif self.__exps[i] != 0:
                units += f"{SI_BASE_UNIT[i]}^" + "{" + f"{self.__exps[i]}" + "} " 
        
        units = units[0:len(units)-1]
        units += "$"
        return units
        
    # Operators
    def __eq__(self, other):
        if self.__scale == other.scale() and self.__exps == other.exps():
            return True
        
        return False
    
    def __ne__(self, other):
        if self.__scale == other.scale() and self.__exps == other.exps():
            return False
        
        return True
    
    def __mul__(self, other):
        if isinstance(other, Unit):
            exps = []
            for i in range(7):
                exps.append(self.__exps[i] + other.exps()[i])
                
            u = Unit(exps)
            sym = ""
            if other.sym() != "":
                sym += other.sym() + " "
            elif self.__sym != "":
                sym += self.__sym
            
            if sym != "":
                scale = self.__scale * other.scale()
                u.setSymScale(sym, scale)
                
            return u
        
    def __truediv__(self, other):
        if isinstance(other, Unit):
            exps = []
            for i in range(7):
                exps.append(self.__exps[i] - other.exps()[i])
            
            u = Unit(exps)
            sym = ""
            if other.sym() != "":
                sym += other.sym() + " "
            elif self.__sym != "":
                sym += self.__sym
            
            if sym != "":
                scale = self.__scale * other.scale()
                u.setSymScale(sym, scale)
                
            return u
        
    def __pow__(self, other):
        if isinstance(other, (int, float)):
            scale = self.__scale**other
            sym = ""
            if self.__sym != "":
                sym = self.__sym + f"^{other}"
            exps=[]
            for i in range(7):
                exps.append(self.__exps[i]*other)
            return Unit(scale, sym, exps)

class DataErr:
    """DataErr(val : float = 0, err : float = 0, unit : Unit = Unit(), name : str = "Null", sigfig : int = 3)\
    
    Creates a DataErr data structure
    
    Parameters
    ----------
    val : float
        Value of the data
    err : float
        Uncertainty / error / standard deviation in the value
    unit : Unit
        Units of the value
    name : str
        Name of the value, e.g. Distance
    sigfig: int
        Number of significant figures of numbers printed from this data structure is set to
    """
    def __init__(self, val : float = 0,
                 err : float = 0,
                 unit : Unit = Unit(),
                 name : str = "Null",
                 sigfig : int = 3):
        self.__val = val
        self.__err = err
        self.__name = name
        self.__unit = unit
        self.__sigfig = sigfig
    
    def __repr__(self):
        return self.show()
    
    # Setters
    def setVal(self, val : float):
        """derr.setVal(val : float)
        
        Sets the value of `derr`
        
        Parameters
        ----------
        val : float
            Value of the data"""
        self.__val = val
    
    def setErr(self, err : float):
        """derr.setErr(err : float)
        
        Sets the uncertainty in `derr`
        
        Parameters
        ----------
        err : float
            Uncertainty / error / standard deviation in the value"""
        self.__err = err
    
    def setUnits(self, unit : Unit):
        """derr.setUnits(unit : Unit)
        
        Sets the units of `derr`
        
        Parameters
        ----------
        unit : Unit
            Units of the value"""
        self.__unit = unit

    def setRelErr(self, relErr : float):
        """derr.setRelErr(relErr : float)
        
        Sets the relative uncertainty of `derr` in DECIMAL
        
        Parameters
        ----------
        relErr : float
            Relative uncertainty in DECIMAL"""
        self.__err = np.abs(self.__val*relErr)
    
    def setSigFig(self, sigfig : int):
        """derr.setSigFig(sigfig : int)
        
        Sets the number of significant figures of values printed from `derr`
        
        Parameters
        ----------
        sigfig : int
            Number of significant figures of numbers printed from this data structure is set to"""
        self.__sigfig = sigfig
    
    def setName(self, name : str):
        """derr.setName(name : str)
        
        Sets the Nnme of the value, e.g. Distance
        
        Parameters
        ----------
        name : str
            Name of the value, e.g. Distance"""
        self.__name = name
        
    def convertUnitTo(self, unit : Unit):
        """derr.convertUnitTo(unit : Unit)
        
        Converts value and error of `derr` from one unit to another of the same dimension
        
        Parameters
        ----------
        unit : Unit
            Units of `derr` after conversion, needs to have same dimensions as `derr`"""
        if (unit.exps() != self.__unit.exps()):
            print("Invalid conversion, unit to be converted is not of same dimension")
            return 0
    
        self.__val = self.__val / unit.scale() * self.__unit.scale()
        self.__err = self.__err / unit.scale() * self.__unit.scale()
        self.__unit = unit        
        
    # Getters
    def val(self) -> float:
        """derr.val() -> float
        
        Returns the value of `derr`"""
        return self.__val;
    
    def err(self) -> float:
        """derr.err() -> float
        
        Returns the error in `derr`"""
        return self.__err
    
    def relErr(self) -> float:
        """derr.relErr() -> float
        
        Returns relative error in `derr` in DECIMAL"""
        return np.abs(self.__err/self.__val)
    
    def units(self) -> Unit:
        """derr.units() -> Unit
        
        Returns the Unit data structure of `derr`"""
        return self.__unit
    
    def dimensions(self) -> str:
        """derr.dimensions() -> str
        
        Returns the dimensions of `derr`"""
        return self.__unit.dimensions()
    
    def top(self) -> float:
        """derr.top() -> float
        
        Returns maximum value in the error range (val + err)"""
        return self.__top
    
    def bottom(self) -> float:
        """derr.bottom() -> float
        
        Returns minimum value in error range (val - err)"""
        return self.__bottom
    
    def name(self) -> str:
        """derr.name() -> str
        
        Returns the name of `derr`"""
        return self.__name

    def sigfig(self) -> int:
        """derr.sigfig() -> int
        
        Returns the number of sigfigs `derr` would be displayed to when printed"""
        return self.__sigfig
    
    def show(self) -> str:
        """derr.show() -> str
        
        Returns a string of the name, value, error and units of `derr` in scientific format"""
        v = formatSciNum(self.__val, self.__sigfig);
        e = formatSciNum(self.__err, 1);

        return f"{self.__name} / {self.__unit.units()} : {v} +/- {e}"
            
    # Operators
    def __add__(self, other):
        if isinstance(other, DataErr):
            if self.__unit != other.units():
                print("Error: cannot add data of different units")
                return DataErr()
            
            val = self.__val + other.val()
            err = np.sqrt(self.__err**2 + other.err()**2)
            
            sf = other.sigfig()
            if self.__sigfig < sf:
                sf = self.__sigfig
            
            return DataErr(val, err, self.__unit, sigfig=sf)
        
        if isinstance(other, (int, float)):
            val = self.__val + other
            return DataErr(val, self.__err, self.__unit, sigfig=self.__sigfig)
        
    def __sub__(self, other):
        if isinstance(other, DataErr):
            if self.__unit != other.units():
                print("Error: cannot take away data of different units")
                return DataErr()
            
            val = self.__val - other.val()
            err = np.sqrt(self.__err**2 + other.err()**2)
            
            sf = other.sigfig()
            if self.__sigfig < sf:
                sf = self.__sigfig
            
            return DataErr(val, err, self.__unit, sigfig=sf)
        
        if isinstance(other, (int, float)):
            val = self.__val - other
            return DataErr(val, self.__err, self.__unit, sigfig=self.__sigfig)
        
    def __mul__(self, other):
        if isinstance(other, DataErr):
            val = self.__val * other.val()
            relErr = np.sqrt(self.relErr()**2 + other.relErr()**2)
            unit = self.__unit*other.units()
            
            sf = other.sigfig()
            if self.__sigfig < sf:
                sf = self.__sigfig
            
            derr = DataErr(val, unit = unit, sigfig = sf)
            derr.setRelErr(relErr)
            return derr
        
        if isinstance(other, (int, float)):
            val = self.__val * other
            derr = DataErr(val, unit = self.__unit, sigfig = self.__sigfig)
            derr.setRelErr(self.relErr())
            return derr
        
    def __truediv__(self, other):
        if isinstance(other, DataErr):
            val = self.__val / other.val()
            relErr = np.sqrt(self.relErr()**2 + other.relErr()**2)
            unit = self.__unit*other.units()
            
            sf = other.sigfig()
            if self.__sigfig < sf:
                sf = self.__sigfig
            
            derr = DataErr(val, unit = unit, sigfig = sf)
            derr.setRelErr(relErr)
            return derr
        
        if isinstance(other, (int, float)):
            val = self.__val / other
            derr = DataErr(val, unit = self.__unit, sigfig = self.__sigfig)
            derr.setRelErr(self.relErr())
            return derr
            
    def __pow__(self, other):
        if isinstance(other, DataErr):
            if not other.unitless():
                print("Error: cannot raise to an exponent with units")
                return DataErr()
            
            val = self.__val ** other.val()
            relErr = np.sqrt((other.val()*self.relErr())**2 +
                             (np.log(self.__val)*other.err())**2)
            derr = DataErr(val, unit=self.__unit**other.val(),sigfig=self.__sigfig)
            derr.setRelErr(relErr)
            return derr
        
        if isinstance(other, (int, float)):
            val = self.__val**other
            derr = DataErr(val, unit = self.__unit**other, sigfig = self.__sigfig)
            derr.setRelErr(other*self.relErr())
            return derr
        
    def __neg__(self):
        return DataErr(-self.__val, self.__err, self.__unit, self.__name, self.__sigfig)

