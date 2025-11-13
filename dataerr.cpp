#include "dataerr.h"

#include <cmath>
#include <stdexcept>

DataErr::DataErr(float val, float err, Unit u, std::string name)
    : m_val(val), m_err(fabs(err)), m_unit(u), m_name(name)
{}

DataErr::DataErr(std::pair<float,float> val, Unit u,std::string name)
    : m_val(val.first), m_err(fabs(val.second)), m_unit(u), m_name(name)
{}

void DataErr::operator=(DataErr other)
{
    m_val = other.val();
    m_err = other.err();
    m_unit = other.unit();
}

void DataErr::operator=(std::pair<float,float> val)
{
    m_val = val.first;
    m_err = fabs(val.second);
    m_unit = Unit();
}

void DataErr::operator=(float val)
{
    m_val = val;
    m_err = 0;
    m_unit = Unit();
}

bool DataErr::operator==(DataErr other)
{
    if (m_unit == other.unit() &&
        max() >= other.min() &&
        other.max() >= min() )
    {
        return true;
    }
    return false;
}

bool DataErr::operator==(std::pair<float,float> val)
{
    if (max() >= val.first - val.second &&
        val.first + val.second >= min() )
    {
        return true;
    }
    return false;
}

bool DataErr::operator==(float val)
{
    if (m_val == val)
    {
        return true;
    }
    return false;
}

bool DataErr::operator!=(DataErr other)
{
    if (m_unit != other.unit() ||
        max() < other.min() ||
        other.max() < min() )
    {
        return true;
    }
    return false;
}

bool DataErr::operator!=(std::pair<float,float> val)
{
    if (max() < val.first - val.second ||
        val.first + val.second < min() )
    {
        return true;
    }
    return false;
}

bool DataErr::operator!=(float val)
{
    if (m_val != val)
    {
        return true;
    }
    return false;
}

bool DataErr::operator>(DataErr other)
{
    if (m_unit == other.unit() &&
        min() > other.max())
    {
        return true;
    }
    return false;
}

bool DataErr::operator>(std::pair<float,float> val)
{
    if (min() > val.first + val.second)
    {
        return true;
    }
    return false;
}

bool DataErr::operator>(float val)
{
    if (min() > val)
    {
        return true;
    }
    return false;
}

bool DataErr::operator<(DataErr other)
{
    if (m_unit == other.unit() &&
        max() < other.min())
    {
        return true;
    }
    return false;
}
bool DataErr::operator<(std::pair<float,float> val)
{
    if (max() < val.first - val.second)
    {
        return true;
    }
    return false;
}

bool DataErr::operator<(float val)
{
    if (max() < val)
    {
        return true;
    }
    return false;
}

bool DataErr::operator>=(DataErr other)
{
    if (m_unit == other.unit() &&
        min() >= other.max())
    {
        return true;
    }
    return false;
}

bool DataErr::operator>=(std::pair<float,float> val)
{
    if (min() >= val.first + val.second)
    {
        return true;
    }
    return false;
}
bool DataErr::operator>=(float val)
{
    if (min() >= val)
    {
        return true;
    }
    return false;
}

bool DataErr::operator<=(DataErr other)
{
    if (m_unit == other.unit() &&
        max() <= other.min())
    {
        return true;
    }
    return false;
}

bool DataErr::operator<=(std::pair<float,float> val)
{
    if (max() <= val.first - val.second)
    {
        return true;
    }
    return false;
}

bool DataErr::operator<=(float val)
{
    if (max() <= val)
    {
        return true;
    }
    return false;
}

DataErr DataErr::operator+(DataErr other)
{
    if (m_unit != other.unit())
    {
        throw std::invalid_argument("Cannot add values with different units "+m_unit.units() + " and " + other.unitsTxt());
        return 0;
    }
    DataErr var;
    var.setVal(m_val + other.val());
    var.setErr( std::sqrt( std::pow(m_err, 2) + std::pow(other.err(),2) ) );
    var.setUnit(m_unit);
    return var;
}

DataErr DataErr::operator+(std::pair<float,float> val)
{
    DataErr var;
    var.setVal(m_val + val.first);
    var.setErr( std::sqrt( std::pow(m_err, 2) + std::pow(val.second,2) ) );
    var.setUnit(m_unit);
    return var;
}
DataErr DataErr::operator+(float val)
{
    DataErr var;
    var.setVal(m_val + val);
    var.setErr(m_err);
    var.setUnit(m_unit);
    return var;
}


DataErr DataErr::operator-(DataErr other)
{
    if (m_unit != other.unit())
    {
        throw std::invalid_argument("Cannot add values with different units "+m_unit.units() + " and " + other.unitsTxt());
        return 0;
    }
    DataErr var;
    var.setVal(m_val - other.val());
    var.setErr( std::sqrt( std::pow(m_err, 2) + std::pow(other.err(),2) ) );
    var.setUnit(m_unit);
    return var;
}

DataErr DataErr::operator-(std::pair<float,float> val)
{
    DataErr var;
    var.setVal(m_val - val.first);
    var.setErr( std::sqrt( std::pow(m_err, 2) + std::pow(val.second,2) ) );
    var.setUnit(m_unit);
    return var;
}

DataErr DataErr::operator-(float val)
{
    DataErr var;
    var.setVal(m_val - val);
    var.setErr(m_err);
    var.setUnit(m_unit);
    return var;
}

DataErr DataErr::operator*(DataErr other)
{
    DataErr var;
    var.setVal(m_val * other.val());
    var.setRelErr(std::sqrt( pow(relErr(),2) + pow(other.relErr(),2)));
    var.setUnit(m_unit*other.unit());
    return var;
}
DataErr DataErr::operator*(std::pair<float,float>val)
{
    DataErr var;
    var.setVal(m_val * val.first);
    var.setRelErr(std::sqrt( pow(relErr(),2) + pow(val.second,2)));
    var.setUnit(m_unit);
    return var;
}

DataErr DataErr::operator*(float val)
{
    DataErr var;
    var.setVal(m_val * val);
    var.setRelErr(relErr());
    var.setUnit(m_unit);
    return var;
}
DataErr DataErr::operator/(DataErr other)
{
    DataErr var;
    var.setVal(m_val / other.val());
    var.setRelErr(std::sqrt( pow(relErr(),2) + pow(other.relErr(),2)));
    var.setUnit(m_unit*other.unit());
    return var;
}
DataErr DataErr::operator/(std::pair<float,float> val)
{
    DataErr var;
    var.setVal(m_val / val.first);
    var.setRelErr(std::sqrt( pow(relErr(),2) + pow(val.second,2)));
    var.setUnit(m_unit);
    return var;
}
DataErr DataErr::operator/(float val)
{
    DataErr var;
    var.setVal(m_val / val);
    var.setRelErr(relErr());
    var.setUnit(m_unit);
    return var;
}

DataErr DataErr::operator^(DataErr other)
{
    if (other.unit().unitless())
    {
        throw std::invalid_argument("Exponent not unitless: " + other.unitsTxt());
        return 0;
    }
    DataErr var;
    var.setVal( pow(m_val, other.val()));
    var.setRelErr(other.val() * std::sqrt( pow(relErr(),2) + pow(log(m_val) * other.relErr(),2) ) );
    var.setUnit(m_unit^other.val());
    return var;
}
DataErr DataErr::operator^(std::pair<float,float>val)
{
    DataErr var;
    var.setVal( pow(m_val, val.first));
    var.setRelErr(val.first * std::sqrt( pow(relErr(),2) + pow(log(m_val) * val.second / fabs(val.first),2) ) );
    var.setUnit(m_unit^val.first);
    return var;
}
DataErr DataErr::operator^(float val)
{
    DataErr var;
    var.setVal(pow(m_val,val));
    var.setRelErr(val * relErr());
    var.setUnit(m_unit^val);
    return var;
}

// getters
float DataErr::val()
{
    return m_val;
}

float DataErr::err()
{
    return m_err;
}


std::string DataErr::unitsTxt()
{
    return m_unit.units();
}

Unit DataErr::unit()
{
    return m_unit;
}

std::string DataErr::dimensions()
{
    return m_unit.dimensions();
}

float DataErr::relErr()
{
    return fabs(m_err/m_val);
}

float DataErr::max()
{
    return m_val + m_err;
}

float DataErr::min()
{
    return m_val - m_err;
}

std::string DataErr::show()
{
    std::string v = DataErr::formatSciNum(m_val, m_sigfig);
    std::string e = DataErr::formatSciNum(m_err, m_sigfig);

    return m_name + " / " + m_unit.units() + " : " + v + " +/- " + e;
}

std::string DataErr::name()
{
    return m_name;
}

// setters
void DataErr::setVal(float val)
{
    m_val = val;
}

void DataErr::setErr(float err)
{
    m_err = fabs(err);
}

void DataErr::setRelErr(float relErrDec)
{
    m_err = fabs(m_val * relErrDec);
}

void DataErr::setDataErr(float val, float err, Unit u)
{
    m_val = val;
    m_err = fabs(err);
    m_unit = u;
}

void DataErr::setDataErr(DataErr val)
{
    m_val = val.val();
    m_err = val.err();
    m_unit = val.unit();
}

void DataErr::setDataErr(std::pair<float,float> val, Unit u)
{
    m_val = val.first;
    m_val = fabs(val.second);
    m_unit = u;
}

void DataErr::setUnit(Unit u)
{
    m_unit = u;
}

void DataErr::setName(std::string name)
{
    m_name = name;
}

void DataErr::setSigFig(int sigfig)
{
    m_sigfig = sigfig;
}

std::string DataErr::formatSciNum(float num, int sigfig)
{
    if (num == 0.0f)
    {
        std::string s = "0.";
        for (int i = 0; i < sigfig -1; i++)
        {
            s += '0';
        }
        return s;
    }
    int n = floor(log10(fabs(num)));
    float val = num / (pow(10,n));
    std::string str = std::to_string(val).substr(0,sigfig+1) + "E" + std::to_string(n);
    return str;
}

std::pair<std::vector<float>, std::vector<float>> DataErr::parseDerrList(std::vector<DataErr> l)
{
    std::vector<float> val;
    std::vector<float> err;

    for (auto& i : l)
    {
        val.push_back(i.val());
        err.push_back(i.err());
    }

    return std::pair<std::vector<float>, std::vector<float>>(val, err);
}
