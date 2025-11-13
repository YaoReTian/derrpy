#ifndef DATAERR_H
#define DATAERR_H

/*
 * @author: YaoReTian
 *
 * Addition and subtraction: input assumed to have same unit if not provided
 * Multiplication and division: input assumed to be unitless if not provided
 *
 */

#include <vector>
#include "unit.h"

class DataErr
{
public:
    DataErr(float val = 0, float err = 0, Unit u = Unit(), std::string name = "NoName" );
    DataErr(std::pair<float,float> val,  Unit u = Unit(),std::string name = "NoName");

    // Operators
    void operator=(DataErr other);
    void operator=(std::pair<float,float> val);
    void operator=(float val);

    bool operator==(DataErr other);
    bool operator==(std::pair<float,float> val);
    bool operator==(float val);

    bool operator!=(DataErr other);
    bool operator!=(std::pair<float,float> val);
    bool operator!=(float val);

    bool operator>(DataErr other);
    bool operator>(std::pair<float,float> val);
    bool operator>(float val);

    bool operator<(DataErr other);
    bool operator<(std::pair<float,float> val);
    bool operator<(float val);

    bool operator>=(DataErr other);
    bool operator>=(std::pair<float,float> val);
    bool operator>=(float val);

    bool operator<=(DataErr other);
    bool operator<=(std::pair<float,float> val);
    bool operator<=(float val);

    DataErr operator+(DataErr other);
    DataErr operator+(std::pair<float,float> val);
    DataErr operator+(float val);

    DataErr operator-(DataErr other);
    DataErr operator-(std::pair<float,float> val);
    DataErr operator-(float val);

    DataErr operator*(DataErr other);
    DataErr operator*(std::pair<float,float>val);
    DataErr operator*(float val);

    DataErr operator/(DataErr other);
    DataErr operator/(std::pair<float,float> val);
    DataErr operator/(float val);

    DataErr operator^(DataErr other);
    DataErr operator^(std::pair<float,float>val);
    DataErr operator^(float val);

    void operator+=(DataErr other);
    void operator+=(std::pair<float,float> val);
    void operator+=(float val);

    void operator-=(DataErr other);
    void operator-=(std::pair<float,float> val);
    void operator-=(float val);

    void operator*=(DataErr other);
    void operator*=(std::pair<float,float>val);
    void operator*=(float val);

    void operator/=(DataErr other);
    void operator/=(std::pair<float,float> val);
    void operator/=(float val);

    void operator^=(DataErr other);
    void operator^=(std::pair<float,float>val);
    void operator^=(float val);

    // getters
    float val();
    float err();
    std::string unitsTxt();
    Unit unit();
    std::string dimensions();
    float relErr();
    float min();
    float max();
    std::string show();
    std::string name();

    // setters
    void setVal(float val);
    void setErr(float err);
    void setRelErr(float relErrDec);
    void setDataErr(float val, float err, Unit u = Unit());
    void setDataErr(DataErr val);
    void setDataErr(std::pair<float,float> val, Unit u = Unit());
    void setUnit(Unit u);
    void setName(std::string name);
    void setSigFig(int sigfig);

    // Static functions
    static std::string formatSciNum(float num, int sigfig) ;
    static std::pair<std::vector<float>, std::vector<float>> parseDerrList(std::vector<DataErr> l);
private:

    float m_val;
    float m_err;
    Unit m_unit;
    std::string m_name;
    int m_sigfig = 3;
};

#endif // DATAERR_H
