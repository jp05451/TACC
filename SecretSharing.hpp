#include <vector>
#include <iostream>
#include <random>
#include <time.h>
#include <cmath>

#define MODULUS_DEFAULT (2 ^ 32 - 1)

class secret
{
public:
    int index;
    int value;
};

class secretSharing
{
public:
    secretSharing(int, int, unsigned int);
    void generatePoly();
    void share(int);
    unsigned int polyCalculate(int); // calculate the polynomial

    void outputSecret();
    int calculateSecret();
    long calculateSecret(std::vector<secret> &);
    int floatRandom();

    std::vector<secret> &getSecrets()
    {
        return secrets;
    }

    // private:
    int N;
    int T;

    unsigned int modulus;

    std::vector<secret> secrets;
    std::vector<int> polynomial;
};

secretSharing::secretSharing(int n, int t, unsigned int modulus = MODULUS_DEFAULT)
{
    // check if N and T is available
    srand(time(NULL));
    if (t > n)
    {
        std::cerr << "T must smaller or equal to N" << std::endl;
        exit(1);
    }

    // initialize N and T
    N = n;
    T = t;

    this->modulus = modulus;
}

void secretSharing::generatePoly()
{
    // generate secret sharing polynomial
    polynomial.push_back(0);
    for (int i = 1; i < T; i++)
    {
        polynomial.push_back((rand() % modulus) + 1);
    }
}

unsigned int secretSharing::polyCalculate(int x)
{
    // calculate the polynomial
    unsigned int y = 0;
    for (int i = 0; i < polynomial.size(); i++)
    {
        y += (polynomial[i] * (int)pow(x, i)) % modulus;
        y %= modulus;
    }
    return y;
}

void secretSharing::share(int inputSecret)
{

    generatePoly();
    polynomial[0] = inputSecret;

    // calculate secret from x = 1 to N
    for (int i = 1; i <= N; i++)
    {
        secret temp;

        temp.value = polyCalculate(i);
        temp.index = i;
        secrets.push_back(temp);
    }
}

long secretSharing::calculateSecret(std::vector<secret> &inputSecrets)
{
    if (inputSecrets.size() < T)
    {
        std::cerr << "splits not enough to calculate secret" << std::endl;
        exit(1);
    }
    // using Lagrange polynomial to calculate back secret
    long int output = 0;

    // calculate f(0)
    for (int i = 0; i < inputSecrets.size(); i++)
    {
        int y = inputSecrets[i].value;
        long int L = 1;

        // calculate L_i
        for (int j = 0; j < inputSecrets.size(); j++)
        {

            int x = inputSecrets[i].index;

            if (i == j)
                continue;

            L *= (0 - inputSecrets[j].index) / (x - inputSecrets[j].index);
            L %= modulus;
        }

        // f(x) = sigma[ y_i * L_i(x) ]
        output += y * L;
    }
    return output;
}

int secretSharing::calculateSecret()
{

    // using Lagrange polynomial to calculate back secret
    int output = 0;

    // calculate f(0)
    for (int i = 0; i < secrets.size(); i++)
    {
        int y = secrets[i].value;
        int L = 1;

        // calculate L_i
        for (int j = 0; j < secrets.size(); j++)
        {

            int x = secrets[i].index;

            if (i == j)
                continue;

            L *= (0 - secrets[j].index) / (x - secrets[j].index);
        }

        // f(x) = sigma[ y_i * L_i(x) ]
        output += y * L;
    }
    return output;
}

void secretSharing::outputSecret()
{
    for (auto &a : polynomial)
    {
        std::cout << a << " " << std::endl;
    }
    for (auto &a : secrets)
    {
        std::cout << a.index << " " << a.value << std::endl;
    }
}

int secretSharing::floatRandom()
{
    return (int)rand() / (RAND_MAX);
}