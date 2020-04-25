#ifndef METHODS_H
#define METHODS_H
#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>

using namespace std;

class Methods{
    public:
        int txt_counter;
        bool condition;
        Methods(){
            txt_counter = 0;
            condition = false;
        }

        string convert_state(int number){ //Convierte estados en binario a taken o not taken
            string real_state;
            if (number >= 2){real_state = "T";}
            else{real_state = "N";}
            return real_state;
        }

        string print_states(vector<int> contadores){ //Imprime estados en weakly y strongly
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

        int get_state(string line, int bp, int history, int s){ //Obtiene el estado que se debe utilizar
            int state;
            int mask = (int)(pow(2.0,(double)s)) - 1;
            if(bp == 0) state =  (stol(line.substr(0, line.find(" ")))) & mask;
            else if(bp == 2) state = (stol(line.substr(0, line.find(" "))) ^ history) & mask;
            else if(bp==1) state = (stol(line.substr(0, line.find(" "))) ^ history) & mask;
            return state;
        }

        string make_prediction(string predicted, string real){
            string prediction;
            if(predicted == real) prediction = "Correct";
            else prediction = "Incorrect";
            return prediction;
        }

        vector<int> update_contadores(vector<int> contadores, int state, string real){//Hace update a los contadores de dos bits
            if(real == "T"){
                if(contadores[state]<3) contadores[state]++;
            }

            if(real == "N"){
                if(contadores[state]>0) contadores[state] = contadores[state]-1;
            }

            return contadores;
        }

        int update_history(int history, int mask, string real){//Hace update a los bits de historia para el global share
            if(real == "T") history = ((history<<1) | 1) & mask;
            else if(real == "N") history = (history<<1) & mask;
            return history;
        }


        void create_txt(int bp, string input, int o){
            Methods::txt_counter++;
                if(Methods::txt_counter <= 5000){
                    if(o==1){
                        string predictor;
                        if(bp == 0){predictor = "bimodal";}
                        else if(bp == 2){predictor = "gshare";}
                        else if(bp == 1){predictor = "pshare";}
                        else if(bp == 3){predictor = "tournament";}
                        ofstream txt_file;
                        txt_file.open(predictor+".txt", ios::out | ios::app);
                        txt_file << input << endl; 
                        txt_file.close();
                    }
                }
                else{Methods::condition = true;}
        }


        void print_results(string bp_choice, int bht_size, int gh, int ph, int branch_nmbr, int correct_taken, int incorrect_taken, int correct_ntaken, int incorrect_ntaken){
            double corr_perc = ((double)(correct_taken + correct_ntaken)/(double)(branch_nmbr))*100.0;
            


            cout << "______________________________________________________________" << endl << "Prediction parameters: " << endl << "______________________________________________________________" << endl
            << "Branch Prediction type:                                " << bp_choice << endl
            << "BHT size (entries):                                    " << bht_size << endl
            << "Global history register size:                          " << gh << endl
            << "Private history register size:                         " << ph << endl
            << "______________________________________________________________" << endl
            << "Simulation results: " << endl << "______________________________________________________________" << endl
            << "Number of branch:                                      " << branch_nmbr << endl
            << "Number of correct prediction of taken branches:        " << correct_taken << endl
            << "Number of incorrect prediction of taken branches:      " << incorrect_taken << endl
            << "Number of correct prediction of not taken branches:    " << correct_ntaken << endl
            << "Number of incorrect prediction of not taken branches:  " << incorrect_ntaken << endl
            << "Percentage of correct predictions                      " << corr_perc << "%" << endl
            << "______________________________________________________________" << endl;
        }
};

#endif