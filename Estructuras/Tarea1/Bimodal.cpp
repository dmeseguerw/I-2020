#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>
#include "Methods.cpp"


using namespace std;


class Bimodal{
    public:
        void make_Bipred(string ln, int s, int bp, int o){
            string txt_input;
            int index = met.get_state(ln, bp, 0, s);
            Bimodal::real = ln.back();
            Bimodal::prediction = met.convert_state(Bimodal::contadores[index]);
            Bimodal::pred_status = met.make_prediction(Bimodal::prediction, Bimodal::real);
            txt_input = ln.substr(0, ln.find(" ")) + " | " + Bimodal::prediction + " | " + Bimodal::real + " | " + Bimodal::pred_status;
            met.create_txt(bp, txt_input, o);
            Bimodal::contadores = met.update_contadores(Bimodal::contadores, index, real);
        }

        void use_Bipred(int bp, int s, int gh, int ph, int o){
            string ln;
            vector<int> contadores((int)(pow(2.0,(double)s)),00);
            Bimodal::contadores = contadores;
            int branch_counter = 0;
            int c_taken = 0;
            int i_taken = 0;
            int c_ntaken = 0;
            int i_ntaken = 0;
            while(getline(cin,ln)){

                make_Bipred(ln, s, bp, o);
                if(met.condition) break;
                if(prediction == "T" & pred_status == "Correct") c_taken++;
                else if(prediction == "T" & pred_status == "Incorrect") i_taken++;
                else if(prediction == "N" & pred_status == "Correct") c_ntaken++;
                else if(prediction == "N" & pred_status == "Incorrect") i_ntaken++;
                branch_counter++;
            }

            met.print_results("Bimodal", contadores.size(), gh, ph, branch_counter, c_taken, i_taken, c_ntaken, i_ntaken);
        }



        vector<int> contadores;
        string prediction, pred_status, real;
        Methods met;
};