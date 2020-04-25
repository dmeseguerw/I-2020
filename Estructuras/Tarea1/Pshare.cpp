#ifndef PSHARE_H
#define PSHARE_H
#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>


#include "Methods.cpp"


using namespace std;


class Pshare{
    public:
        void make_Ppred(string ln, int bp, int s, int ph, int o){
            unsigned int mask = (int)(pow(2.0,(double)s)) - 1;
            int mask_for_h = (int)(pow(2.0,(double)ph)) - 1;
            string real;
            unsigned int PHT_index = (stol(ln.substr(0,ln.find(" ")))) & mask; //Obtengo los ultimos s bits del PC
            unsigned int PHT_current_reg = PHT[PHT_index];
            unsigned int BHT_index = met.get_state(ln, bp, PHT_current_reg, s);
            Pshare::prediction = met.convert_state(Pshare::BHT[BHT_index]);
            real = ln.back();
            Pshare::pred_status = met.make_prediction(Pshare::prediction, real);

            string txt_input = ln.substr(0, ln.find(" ")) + " | " + Pshare::prediction + " | " + real + " | " + Pshare::pred_status;
            met.create_txt(bp, txt_input, o);

            Pshare::BHT = met.update_contadores(Pshare::BHT, BHT_index, real);
            Pshare::PHT[PHT_index] = met.update_history(PHT_current_reg, mask_for_h, real);

        }

        void use_Ppredictor(int bp, int s, int ph, int gh, int o){
            string ln;
            vector<int> PHT((int)(pow(2.0,(double)s)),00);
            vector<int> BHT((int)(pow(2.0,(double)s)),00);
            Pshare::PHT = PHT;
            Pshare::BHT = BHT;
            int branch_counter = 0;
            int c_taken = 0;
            int i_taken = 0;
            int c_ntaken = 0;
            int i_ntaken = 0;
            while(getline(cin,ln)){

                make_Ppred(ln, bp, s, ph, o);
                if(met.condition) break;
                if(prediction == "T" & pred_status == "Correct") c_taken++;
                else if(prediction == "T" & pred_status == "Incorrect") i_taken++;
                else if(prediction == "N" & pred_status == "Correct") c_ntaken++;
                else if(prediction == "N" & pred_status == "Incorrect") i_ntaken++;
                branch_counter++;
            }
            met.print_results("Pshare", BHT.size(), gh, ph, branch_counter, c_taken, i_taken, c_ntaken, i_ntaken);
 
        }

        vector<int> PHT, BHT;
        string prediction, pred_status;
        Methods met;
};

#endif