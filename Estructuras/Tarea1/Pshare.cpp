#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>
#include "Methods.cpp"


using namespace std;


class Pshare{
    public:
        void make_Ppred(string ln, int bp, int s, int ph){
            unsigned int mask = (int)(pow(2.0,(double)s)) - 1;
            int mask_for_h = (int)(pow(2.0,(double)ph)) - 1;
            string real;
            unsigned int PHT_index = (stol(ln.substr(0,ln.find(" ")))) & mask; //Obtengo los ultimos s bits del PC
            unsigned int PHT_current_reg = PHT[PHT_index];
            unsigned int BHT_index = met.get_state(ln, bp, PHT_current_reg, s);
            // BHT_index = (PC_adrs ^ PHT_current_reg) & mask;
            Pshare::predicted = met.convert_state(Pshare::BHT[BHT_index]);
            real = ln.back();
            Pshare::prediction = met.make_prediction(Pshare::predicted, real);
            cout << met.print_states(Pshare::BHT) << " | " << Pshare::predicted << " | " << real << " | " << Pshare::prediction << endl;

            Pshare::BHT = met.update_contadores(Pshare::BHT, BHT_index, real);
            Pshare::PHT[PHT_index] = met.update_history(PHT_current_reg, mask_for_h, real);

        }

        void use_Ppredictor(int bp, int s, int ph){
            string ln;
            int counter = 0;
            vector<int> PHT((int)(pow(2.0,(double)s)),00);
            vector<int> BHT((int)(pow(2.0,(double)s)),00);
            Pshare::PHT = PHT;
            Pshare::BHT = BHT;

            while(getline(cin,ln)){
                counter++;
                if(counter == 100){break;}
                make_Ppred(ln, bp, s, ph);
            }
        }





    private:
        vector<int> PHT, BHT;
        string predicted, prediction;
        Methods met;
};