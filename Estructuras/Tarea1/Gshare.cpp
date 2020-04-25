#ifndef GSHARE_H
#define GSHARE_H
#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>

#include "Methods.cpp"



using namespace std;


class Gshare{
    public:

        void make_Gpred(string ln, int bp, int s, int gh, int o){
            int index;
            string real;
            int mask_for_h = (int)(pow(2.0,(double)gh)) - 1;
            index = Gshare::met.get_state(ln, bp, history, s);
            real = ln.back();
            Gshare::prediction = Gshare::met.convert_state(Gshare::contadores[index]);
            Gshare::pred_status = Gshare::met.make_prediction(Gshare::prediction, real);

            string txt_input = ln.substr(0, ln.find(" ")) + " | " + Gshare::prediction + " | " + real + " | " + Gshare::pred_status;
            met.create_txt(bp, txt_input, o);

            Gshare::contadores = Gshare::met.update_contadores(Gshare::contadores, index, real);
            Gshare::history = Gshare::met.update_history(Gshare::history, mask_for_h, real);

        }

        void use_Gpredictor(int bp, int s, int gh, int ph, int o){
            string ln;
            vector<int> contadores((int)(pow(2.0,(double)s)),00);
            Gshare::contadores = contadores;
            Gshare::history = 0;

            int branch_counter = 0;
            int c_taken = 0;
            int i_taken = 0;
            int c_ntaken = 0;
            int i_ntaken = 0;

            while(getline(cin,ln)){

                make_Gpred(ln, bp, s, gh, o);
                if(met.condition) break;
                if(prediction == "T" & pred_status == "Correct") c_taken++;
                else if(prediction == "T" & pred_status == "Incorrect") i_taken++;
                else if(prediction == "N" & pred_status == "Correct") c_ntaken++;
                else if(prediction == "N" & pred_status == "Incorrect") i_ntaken++;
                branch_counter++;
            }
            met.print_results("Gshare", contadores.size(), gh, ph, branch_counter, c_taken, i_taken, c_ntaken, i_ntaken);
        }

        vector<int> contadores;
        int history;
        string prediction, pred_status;
        Methods met;
};

#endif