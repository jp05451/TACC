#include "SecretSharing.hpp"
#include <iomanip>

using namespace std;

int main()
{

    secretSharing s(3,3);
    s.share(10);

    // s.getSecrets().erase(s.getSecrets().begin(), s.getSecrets().end() - i);

    // s.outputSecret();

    // cout << i << " " << j << " ";
    double temp = s.calculateSecret(s.getSecrets());
    
    cout << temp;

    cout << endl;

}