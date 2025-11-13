#include <iostream>
#include "dataerr.h"

int main()
{
    DataErr a(180, 60, Unit(0,1), "distance");

    // Testing
    DataErr t[5] = {
    DataErr(230, 20, Unit(0,0,1)),
    DataErr(3, 1),
    DataErr(150, 23, Unit(0,1)),
    DataErr(20, 0, Unit(1)),
    DataErr(2,0)};

    std::cout << a.show() << std::endl;

    for (int i = 0; i < 5; i++)
    {
        try
        {
            std::cout << "("+a.show() << ") + (" << t[i].show() +")" << std::endl;
            std::cout << (a+t[i]).show() << std::endl;
            std::cout << std::endl;
        }
        catch (std::invalid_argument)
        {
        }

        try
        {
            std::cout << "("+a.show() << ") - (" << t[i].show() +")" << std::endl;
            std::cout << (a-t[i]).show() << std::endl;
            std::cout << std::endl;
        }
        catch (std::invalid_argument){}

        try {
            std::cout << "("+a.show() << ") * (" << t[i].show() +")" << std::endl;
            std::cout << (a*t[i]).show() << std::endl;
            std::cout << std::endl;
        } catch (...) {
        }

        try {
            std::cout << "("+a.show() << ") / (" << t[i].show() +")" << std::endl;
            std::cout << (a/t[i]).show() << std::endl;
            std::cout << std::endl;

        } catch (...) {}

        try{
            std::cout << "("+a.show() << ") ^ (" << t[i].show() +")" << std::endl;
            std::cout << (a^t[i]).show() << std::endl;
            std::cout << std::endl;
        } catch(...) {}
    }
    return 0;
}
