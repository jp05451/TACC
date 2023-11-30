#include <vector>
#include<iostream>
#include<random>
#include<time.h>



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
    void splitSecret(std::ostream &,double);

private:
    int N;
    int T;
    std::vector<secret> secretSplit;
    std::vector<double> polynomial;
};

secretSharing::secretSharing(int n,int t)
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
    for (int i = 1; i < t; i++)
    {
        polynomial.push_back(rand());
    }
}

void secretSharing::splitSecret(std::ostream &ostr,double secret)
{
    polynomial[0] = secret;
    for (int i = 0; i < N;i++)
    {
        
    }
}
