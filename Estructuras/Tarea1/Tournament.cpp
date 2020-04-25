
#include <iostream>
#include <fstream>
#include <math.h>
#include <vector>
#include "Methods.cpp"
#include "Gshare.cpp"
#include "Pshare.cpp"





class Tournament{

    public:

        void make_Tournament(string ln, int bp, int s, int gh, int ph, int o){
            string real;
            int meta_index = met.get_state(ln, 0, 0, s);
            string p_prediction, g_prediction;
            gpred.make_Gpred(ln, 2, s, gh, o);
            g_prediction = gpred.prediction;
            ppred.make_Ppred(ln, 1, s, ph, o);
            p_prediction = ppred.prediction;
            real = ln.back();
            string pred_in_use = convert_state(MetaPredictor[meta_index]);
            comparePred(pred_in_use, g_prediction, p_prediction, real);

            string txt_input = ln.substr(0, ln.find(" ")) + " | " + Tournament::prediction + " | " + real + " | " + Tournament::pred_status;
            met.create_txt(bp, txt_input, o);

            updateMeta(real, p_prediction, g_prediction, meta_index);

        }

        void updateMeta(string real, string p_prediction, string g_prediction, int meta_index){
            if(g_prediction == real){
                if(p_prediction != real){
                    if(Tournament::MetaPredictor[meta_index]<3) Tournament::MetaPredictor[meta_index]++;
                }
            }
            else if(p_prediction == real){
                if(Tournament::MetaPredictor[meta_index]>0) Tournament::MetaPredictor[meta_index] = Tournament::MetaPredictor[meta_index]-1;
            }
        }

        void comparePred(string pred_in_use, string g_prediction, string p_prediction, string real){
            if(pred_in_use == "G") {
                Tournament::prediction = g_prediction;
                if(g_prediction == real) Tournament::pred_status = "Correct";
                else{Tournament::pred_status = "Incorrect";}
            }
            if(pred_in_use == "P"){
                Tournament::prediction = p_prediction;
                if(p_prediction == real) Tournament::pred_status = "Correct";
                else{Tournament::pred_status = "Incorrect";}
            }
        }

        string convert_state(int number){ //Convierte estados en binario a taken o not taken
            string real_state;
            if (number >= 2){real_state = "G";}
            else{real_state = "P";}
            return real_state;
        }

        void use_Tournament(int bp, int s, int gh, int ph, int o){
            string ln;
            vector<int> MetaPredictor((int)(pow(2.0,(double)s)),00);
            Tournament::MetaPredictor = MetaPredictor;

            vector<int> Gcounters((int)(pow(2.0,(double)s)),00);
            gpred.contadores = Gcounters;
            gpred.history = 0;
            
            vector<int> PHT((int)(pow(2.0,(double)s)),00);
            vector<int> BHT((int)(pow(2.0,(double)s)),00);
            ppred.PHT = PHT;
            ppred.BHT = BHT;

            int branch_counter = 0;
            int c_taken = 0;
            int i_taken = 0;
            int c_ntaken = 0;
            int i_ntaken = 0;

            while(getline(cin, ln)){
                make_Tournament(ln, bp, s, gh, ph, o);
                if(met.condition) break;
                if(prediction == "T" & pred_status == "Correct") c_taken++;
                else if(prediction == "T" & pred_status == "Incorrect") i_taken++;
                else if(prediction == "N" & pred_status == "Correct") c_ntaken++;
                else if(prediction == "N" & pred_status == "Incorrect") i_ntaken++;
                branch_counter++;
            }
            met.print_results("Tournament", gpred.contadores.size(), gh, ph, branch_counter, c_taken, i_taken, c_ntaken, i_ntaken);
        }

    private:
        vector<int>MetaPredictor;
        Methods met;
        Gshare gpred;
        Pshare ppred;
        string prediction;
        string pred_status;



};
