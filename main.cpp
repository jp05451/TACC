#include"SecretSharing.hpp"

int main()
{
    secretSharing s(3, 3);
    s.splitSecret(10);
    s.outputSecret();
    std::cout << s.calculateSecret() << std::endl;
}