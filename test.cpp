#include "SecretSharing.hpp"
#include <iomanip>

using namespace std;

int main()
{

    secretSharing s(10,10);
    s.splitSecret(10);

    // s.getSecrets().erase(s.getSecrets().begin(), s.getSecrets().end() - i);

    // s.outputSecret();

    // cout << i << " " << j << " ";
    double temp = s.calculateSecret(s.getSecrets());
    cout << setprecision(60) << fixed << temp;

    cout << endl;
    s.secrets.clear();
    s.polynomial.clear();
}