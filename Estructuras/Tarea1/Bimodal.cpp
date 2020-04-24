#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>
#include "Methods.cpp"


using namespace std;


class Bimodal{
    public:
        void make_Bipred(string ln, int s, int bp){
            string real;
            int index = met.get_state(ln, bp, 0, s);
            real = ln.back();
            Bimodal::predicted = met.convert_state(Bimodal::contadores[index]);
            Bimodal::prediction = met.make_prediction(Bimodal::predicted, real);
            cout << met.print_states(Bimodal::contadores) << " | " << Bimodal::predicted << " | " << real << " | " << Bimodal::prediction << endl;
            Bimodal::contadores = met.update_contadores(Bimodal::contadores, index, real);
        }

        void use_Bipred(int bp, int s){
            string ln;
            int counter = 0;
            vector<int> contadores((int)(pow(2.0,(double)s)),00);
            Bimodal::contadores = contadores;
            while(getline(cin,ln)){
                counter++;
                if(counter == 100){break;}
                make_Bipred(ln, s, bp);
            }
        }



    private:
        vector<int> contadores;
        string predicted, prediction;
        Methods met;
};