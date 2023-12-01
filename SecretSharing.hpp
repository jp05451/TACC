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
    void splitSecret(double);
    double calculate(double);
    void outputSecret();
    double calculateSecret();

    int N;
    int T;
    std::vector<secret> secrets;
    std::vector<double> polynomial;
};

secretSharing::secretSharing(int n, int t)
{
    srand(time(NULL));
    if (t > n)
    {
        std::cerr << "T must smaller or equal to N" << std::endl;
        return;
    }

    N = n;
    T = t;

    polynomial.push_back(0);
    for (int i = 1; i < T; i++)
    {
        polynomial.push_back(rand() % 10);
    }
}

double secretSharing::calculate(double x)
{
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
    for (int i = 0; i < N; i++)
    {
        secret temp;
        // int r = rand();
        temp.secret = calculate(i);
        temp.x = i;
        secrets.push_back(temp);
    }
}

double secretSharing::calculateSecret()
{



    double output = 0;
    for (int i = 0; i < secrets.size(); i++)
    {
        double y = secrets[i].secret;
        double L = 1;
        for (int j = 0; j < secrets.size(); j++)
        {

            double x = secrets[i].x;

            if (i == j)
                continue;
            double t = (0 - secrets[j].x) / (x - secrets[j].x);
            L *= t;
        }
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