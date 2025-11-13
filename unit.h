#ifndef UNIT_H
#define UNIT_H

/*
 * @author: YaoReTian
 * Data structure for SI base units
 * 0 = M/Mass
 * 1 = L/Length
 * 2 = T/Time
 * 3 = K/Temperature
 * 4 = I/Current
 * 5 = N/Amount of substance
 * 6 = J/luminous intensity
 */

#include <string>

class Unit
{
public:
    Unit(float MExp = 0, float LExp = 0, float TExp = 0, float KExp = 0, float CExp = 0, float NExp = 0, float JExp = 0);
    Unit(float exps[7]);
    ~Unit();
    bool operator==(Unit other);
    Unit operator*(Unit other);
    Unit operator/(Unit other);
    Unit operator^(float num);

    // Setter
    void setUnit(float MExp = 0, float LExp = 0, float TExp = 0, float KExp = 0, float CExp = 0, float NExp = 0, float JExp = 0);
    void setUnit(float exps[7]);
    void setExpOf(int index, float exp);
    void defineUnit(std::string name);

    // Getters
    std::string dimensions();
    std::string units();
    std::string latex();
    float expOf(int index);
    std::string unitSymbol();
    bool unitless();

private:
    std::string formatExp(int index);

    float m_exps[7];
    std::string m_unitSymbol;
    std::string DIMENSION[7] = {"M","L","T","K","I","N","J"};

    std::string SI_BASE_UNIT[7] = {"kg", "m", "s","K","A","mol","cd"};
};

#endif // UNIT_H
