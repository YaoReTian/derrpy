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

bool Unit::operator==(Unit other)
{
    for (int i = 0; i < 7; i++)
    {
        if (m_exps[i] != other.units()[i])
        {
            return false;
        }
    }
    return true;
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
        if (m_exps[i] != 0)
        {
            str += DIMENSION[i] + "^" + std::to_string(m_exps[i]);
        }
    }

    return str;
}

std::string Unit::units()
{
    std::string str = "";
    for (int i = 0; i < 7; i++)
    {
        if (m_exps[i] != 0)
        {
            str += SI_BASE_UNIT[i] + "^" + std::to_string(m_exps[i]) + " ";
        }
    }

    return str;
}

std::string Unit::latex()
{
    std::string str = "$";
    for (int i = 0; i < 7; i++)
    {
        if (m_exps[i] != 0)
        {
            str += SI_BASE_UNIT[i] + "^{" + std::to_string(m_exps[i]) + "} ";
        }
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
