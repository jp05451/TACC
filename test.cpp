#include "SecretSharing.hpp"

using namespace std;

int main()
{

    for (int i = 1; i < 50; i++)
    {
        for (int j = 1; j < i; j++)
        {
            secretSharing s(i, j);
            s.splitSecret(10);

            // s.getSecrets().erase(s.getSecrets().begin(), s.getSecrets().end() - i);

            // s.outputSecret();

            cout << i << " " << j << " ";
            double temp = s.calculateSecret(s.getSecrets());
            cout << temp;
            if (temp == 10)
                cout << "*";
            cout << endl;
            s.secrets.clear();
            s.polynomial.clear();
        }
    }
}