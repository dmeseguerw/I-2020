#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>
#include "Methods.cpp"


using namespace std;


class Gshare{
    public:
        Gshare(){

        };
        void make_Gpred(string ln, int bp, int s, int gh){
            int index;
            string real;
            int mask_for_h = (int)(pow(2.0,(double)gh)) - 1;
            index = Gshare::met.get_state(ln, bp, history, s);
            real = ln.back();
            Gshare::predicted = Gshare::met.convert_state(Gshare::contadores[index]);
            Gshare::prediction = Gshare::met.make_prediction(Gshare::predicted, real);
            cout << Gshare::met.print_states(Gshare::contadores) << " | " << Gshare::predicted << " | " << real << " | " << Gshare::prediction << endl;
            Gshare::contadores = Gshare::met.update_contadores(Gshare::contadores, index, real);
            Gshare::history = Gshare::met.update_history(Gshare::history, mask_for_h, real);

        }

        void use_Gpredictor(int bp, int s, int gh){
            string ln;
            vector<int> contadores((int)(pow(2.0,(double)s)),00);
            Gshare::contadores = contadores;
            int counter = 0;
            Gshare::history = 0;
            while(getline(cin,ln)){
                counter++;
                if(counter == 100){break;}
                make_Gpred(ln, bp, s, gh);
            }
        }

    private:
        vector<int> contadores;
        int history;
        string predicted, prediction;
        Methods met;
};