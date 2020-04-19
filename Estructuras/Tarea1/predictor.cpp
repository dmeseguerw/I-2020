#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>

using namespace std;

string convert_state(int number){
    string real_state;
    if (number >= 2){real_state = "T";}
    else{real_state = "N";}
    return real_state;
}

string print_states(vector<int> contadores){
    string states = "";
    string current = "";
    for (int i=0;i<contadores.size();i++){
        if(contadores[i] == 00){current = "N";}
        if(contadores[i] == 01){current = "n";}
        if(contadores[i] == 2){current = "t";}
        if(contadores[i] == 3){current = "T";}
        states = states + current;
    }

    return states;
}

void bimodal(int s){

    string ln;
    vector<int> contadores((int)(pow(2.0,(double)s)), 00);
    string prediccion;
    int mask = (int)(pow(2.0,(double)s)) - 1;
    int last_bits;
    int state;
    string real;
    string pred;
    string taken = "T";
    string ntaken = "N";
    string CorI = "";
    int counter = 0;
    while(getline(cin, ln)){
        counter++;
        if(counter == 100){break;}
        last_bits = atoi(&ln[0]) & mask;
        real = &ln[11];
        pred = convert_state(contadores[last_bits]);
        if(pred == real){CorI = "Correct";}
        else{CorI = "Incorrect";}
        cout << last_bits << " | " << print_states(contadores) << " | " << pred << " | " << real << " | " << CorI << endl;

        if(real == "T"){
            if(contadores[last_bits]<3)
            {contadores[last_bits]++;}
        }
        if(real == "N"){
            if(contadores[last_bits]>0){
                contadores[last_bits] = contadores[last_bits]-1;
            }
        }

        cout << contadores[last_bits] << endl;
    }
}



void tournament(){}

void pshare(){}

void gshare(){}

void create_table(){}

void print_results(){}



int main(int argc, char **argv){

    // Obtencion de parametros
    int s, bp, gh, ph, o;
    s = atoi(argv[2]);
    bimodal(s);
    // bp = atoi(argv[4]);
    // gh = atoi(argv[6]);
    // ph = atoi(argv[8]);
    // o = atoi(argv[10]);


}