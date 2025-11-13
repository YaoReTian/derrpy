#include "unit.h"

Unit::Unit(float MExp, float LExp, float TExp, float KExp, float CExp, float NExp, float JExp)
{
    setUnit(MExp, LExp, TExp, KExp, CExp, NExp, JExp);
}

Unit::Unit(float exp[7])
{
    setUnit(exp);
}

Unit::~Unit()
{}

// Operators

void Unit::operator=(Unit other)
{
    for (int i = 0; i < 7; i++)
    {
        m_exps[i] = other.expOf(i);
    }
}

bool Unit::operator==(Unit other)
{
    for (int i = 0; i < 7; i++)
    {
        if (m_exps[i] != other.expOf(i))
        {
            return false;
        }
    }
    return true;
}

bool Unit::operator!=(Unit other)
{
    for (int i = 0; i < 7; i++)
    {
        if (m_exps[i] != other.expOf(i))
        {
            return true;
        }
    }
    return false;
}

Unit Unit::operator*(Unit other)
{
    float exp[7];
    for (int i = 0; i < 7; i++)
    {
        exp[i] = m_exps[i] + other.expOf(i);
    }

    Unit u(exp);

    return u;
}

Unit Unit::operator/(Unit other)
{
    float exp[7];
    for (int i = 0; i < 7; i++)
    {
        exp[i] = m_exps[i] - other.expOf(i);
    }

    Unit u(exp);

    return u;
}

Unit Unit::operator^(float num)
{
    float exp[7];
    for (int i = 0; i < 7; i++)
    {
        exp[i] = m_exps[i]*num;
    }

    Unit u(exp);

    return u;
}

// Setters
void Unit::setUnit(float MExp, float LExp, float TExp, float KExp, float CExp, float NExp, float JExp)
{
    float exp[7] = {MExp, LExp, TExp, KExp, CExp, NExp, JExp};
    for (int i = 0; i < 7 ; i++)
    {
        m_exps[i] = exp[i];
    }
}

void Unit::setUnit(float exp[7])
{
    for (int i = 0; i < 7; i++)
    {
        m_exps[i] = exp[i];
    }
}

void Unit::setExpOf(int index, float exp)
{
    m_exps[index] = exp;
}

void Unit::defineUnit(std::string unitSymbol)
{
    m_unitSymbol = unitSymbol;
}

// Getters

std::string Unit::dimensions()
{
    std::string str = "";
    for (int i = 0; i < 7; i++)
    {
        if (m_exps[i] == 1.0f)
        {
            str += DIMENSION[i] + " ";
        }
        else if (m_exps[i] != 0)
        {
            str += DIMENSION[i] + "^" + formatExp(i) + " ";
        }
    }

    if (str == "")
    {
        str = "unitless";
    }

    return str;
}

std::string Unit::units()
{
    std::string str = "";
    for (int i = 0; i < 7; i++)
    {
        if (m_exps[i] == 1.0f)
        {
            str += SI_BASE_UNIT[i] + " ";
        }
        else if (m_exps[i] != 0)
        {
            str += SI_BASE_UNIT[i] + "^" + formatExp(i) + " ";
        }
    }

    if (str == "")
    {
        str = "unitless";
    }

    return str;
}

std::string Unit::latex()
{
    std::string str = "$";
    for (int i = 0; i < 7; i++)
    {
        if (m_exps[i] == 1.0f)
        {
            str += SI_BASE_UNIT[i] + " ";
        }
        else if (m_exps[i] != 0)
        {
            str += SI_BASE_UNIT[i] + "^{" + formatExp(i) + "} ";
        }
    }

    if (str == "")
    {
        str = "unitless";
    }

    str += "$";
    return str;
}

float Unit::expOf(int index)
{
    return m_exps[index];
}

std::string Unit::unitSymbol()
{
    return m_unitSymbol;
}

std::string Unit::formatExp(int index)
{
    std::string pm = "";
    float e = m_exps[index];
    if (e < 0)
    {
        pm = "-";
        e *= -1;
    }

    std::string val = std::to_string(e);

    int i = 1;
    while (i < 3 && val[i] != 0)
    {
        i++;
    }
    i--;
    if (val[i-1] == '.')
    {
        i--;
    }

    return pm + val.substr(0,i);
}

bool Unit::unitless()
{
    for (auto i : m_exps)
    {
        if (i != 0.0f)
        {
            return true;
        }
    }

    return false;
}
