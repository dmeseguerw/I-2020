#include <iostream>
#include <fstream>


using namespace std;

int main(int argc, char **argv){

    int op, qty;
    ifstream Traces;

// Se determina la operacion a realizar.
    op = atoi(argv[1]); 
    // Traces.open("mcf.trace", ios::in);
    string ln;


    while(getline(cin, ln)){
        if (atoi(&ln[2]) == op) qty++; 
    }

    cout << "La cantidad de op es: " << qty << endl;
    
    return 0;






}