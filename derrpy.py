#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 11:10:09 2025

@author: YaoReTian / Martin Yiu 

derrpy.py
"""

import numpy as np

# Static functions
def formatSciNum(num : float, sigfig : int) -> str:
    """Formats a number in standard form with significant figures"""
    if num == 0:
        return "0."+'0'*(sigfig-1)
    
    mag = int(np.floor(np.log10(np.abs(num))))
    val = str(num / (10**mag))
    val = val[0:sigfig+1]
    
    return val + "E" + str(mag)

def parseDerrList(lst):
    """Converts a list of DataErr types to a list of values and a list of errors"""
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
    """
    Scale: float - dimensionless constant multiplier for the units
    Exps: list[float] - exponents of dimensions in SI units:
        0 = M/Mass (kg)
        1 = L/Length (m)
        2 = T/Time (s)
        3 = K/Temperature (K)
        4 = I/Current (A)
        5 = N/Amount of substance (mol)
        6 = J/luminous intensity (cd)
    Symbol: str - parameter defines the symbol of a self-defined unit, e.g. N
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
        """Exps: arr[float] - exponents of dimensions in SI units:
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
        """Symbol: str - parameter defines the symbol of a self-defined unit, e.g. N
        scale: int - constant multiplier between user defined symbol and SI units"""
        self.__sym = symbol
        self.__scale = scale
        
    def setExpOf(self, dimension : str, exp : float):
        self.__exps[DIMENSION.index(dimension)] = exp
        
    # Getters
    def scale(self) -> float:
        return self.__scale
    
    def expOf(self, dimension : str) -> float:
        return self.__exps[DIMENSION.index(dimension)]
    
    def exps(self) -> float:
        return self.__exps
    
    def sym(self) -> str:
        return self.__sym
    
    def unitless(self) -> bool:
        if self.__exps == [0]*7:
            return True
        return False
    
    def dimensions(self) -> str:
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
        if self.__sym != "":
            return self.__sym
        elif self.unitless():
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
        if self.__sym != "":
            return "$"+self.__sym+"$"
        elif self.unitless():
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
    """Data type including both the value and uncertainty"""
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
        self.__val = val
    
    def setErr(self, err : float):
        self.__err = err
    
    def setUnits(self, unit : Unit):
        self.__unit = Unit

    def setRelErr(self, relErr : float):
        """Set relative error in decimal"""
        self.__err = np.abs(self.__val*relErr)
    
    def setSigFig(self, sigfig : int):
        """Set number of significant figures to output the value with"""
        self.__sigfig = sigfig
    
    def setName(self, name : str):
        self.__name = name
        
    def convertUnitTo(self, unit : Unit):
        """Converts value from one unit to another of the same dimension"""
        if (unit != self.__unit):
            print("Invalid conversion, unit to be converted is not of same dimension")
            return 0
    
        self.__val = self.__val / unit.scale() * self.__unit.scale()
        self.__err = self.__val / unit.scale() * self.__unit.scale()
        self.__unit = unit        
        
    # Getters
    def val(self) -> float:
        return self.__val;
    
    def err(self) -> float:
        return self.__err
    
    def relErr(self) -> float:
        """returns relative error in decimal"""
        return np.abs(self.__err/self.__val)
    
    def units(self) -> Unit:
        return self.__unit
    
    def dimensions(self) -> str:
        return self.__unit.dimensions()
    
    def top(self) -> float:
        """Returns maximum value in the error range (val + err)"""
        return self.__top
    
    def bottom(self) -> float:
        """Returns minimum value in error range (val - err)"""
        return self.__bottom
    
    def name(self) -> str:
        return self.__name

    def sigfig(self) -> int:
        return self.__sigfig
    
    def show(self) -> str:
        """Returns string of data, error and units in scientific format"""
        v = formatSciNum(self.__val, self.__sigfig);
        e = formatSciNum(self.__err, self.__sigfig);

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

