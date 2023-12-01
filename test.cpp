#include"SecretSharing.hpp"

int main()
{
    secretSharing s(10, 10);
    s.splitSecret(10);
    std::cout << std::endl;
    s.outputSecret();

    std::cout << s.calculateSecret() << std::endl;
}