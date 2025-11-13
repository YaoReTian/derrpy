#include <iostream>
#include <iomanip>
#include "unit.h"

int main()
{
    Unit u1(1,0,-1);
    Unit u2(1);

    std::cout << u1.dimensions() << std::endl;
    std::cout << u2.units() << std::endl;

    Unit u3 = u1 * u2 * u2;

    std::cout << u3.dimensions() << std::endl;
    std::cout << u3.units() << std::endl;
    std::cout << u3.latex() << std::endl;

    u3.defineUnit("J");
    std::cout << u3.unitSymbol() << std::endl;
    return 0;
}
