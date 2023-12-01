#include <vector>
#include <iostream>
#include <random>
#include <time.h>
#include <cmath>

class secret
{
public:
    double x;
    double secret;
};

class secretSharing
{
public:
    secretSharing(int, int);
    void generatePoly();
    void splitSecret(double);
    double polyCalculate(double); // calculate the polynomial

    void outputSecret();
    double calculateSecret();
    double calculateSecret(std::vector<secret> &);
    double floatRandom();

    std::vector<secret> &getSecrets()
    {
        return secrets;
    }

// private:
    int N;
    int T;
    std::vector<secret> secrets;
    std::vector<double> polynomial;
};

secretSharing::secretSharing(int n, int t)
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

    generatePoly();
}

void secretSharing::generatePoly()
{
    // generate secret sharing polynomial
    polynomial.push_back(0);
    for (int i = 1; i < T; i++)
    {
        polynomial.push_back((rand() % T)+1);
    }
}

double secretSharing::polyCalculate(double x)
{
    // calculate the polynomial
    double y = 0;
    for (int i = 0; i < polynomial.size(); i++)
    {
        y += polynomial[i] * pow(x, i);
    }
    return y;
}

void secretSharing::splitSecret(double inputSecret)
{
    polynomial[0] = inputSecret;

    // calculate secret from x = 1 to N
    for (int i = 1; i <= N; i++)
    {
        secret temp;

        // temp.secret = polyCalculate((double)i/N);
        temp.secret = polyCalculate(i);
        temp.x = i;
        secrets.push_back(temp);
    }
}

double secretSharing::calculateSecret(std::vector<secret> &inputSecrets)
{
    if (inputSecrets.size() < T)
    {
        std::cerr << "splits not enough to calculate secret" << std::endl;
        exit(1);
    }
    // using Lagrange polynomial to calculate back secret
    long double output = 0;

    // calculate f(0)
    for (int i = 0; i < inputSecrets.size(); i++)
    {
        double y = inputSecrets[i].secret;
        long double L = 1;

        // calculate L_i
        for (int j = 0; j < inputSecrets.size(); j++)
        {

            double x = inputSecrets[i].x;

            if (i == j)
                continue;

            L *= (0 - inputSecrets[j].x) / (x - inputSecrets[j].x);
        }

        // f(x) = sigma[ y_i * L_i(x) ]
        output += y * L;
    }
    return output;
}

double secretSharing::calculateSecret()
{

    // using Lagrange polynomial to calculate back secret
    double output = 0;

    // calculate f(0)
    for (int i = 0; i < secrets.size(); i++)
    {
        double y = secrets[i].secret;
        double L = 1;

        // calculate L_i
        for (int j = 0; j < secrets.size(); j++)
        {

            double x = secrets[i].x;

            if (i == j)
                continue;

            L *= (0 - secrets[j].x) / (x - secrets[j].x);
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
        std::cout << a.x << " " << a.secret << std::endl;
    }
}

double secretSharing::floatRandom()
{
    return (double)rand() / (RAND_MAX);
}