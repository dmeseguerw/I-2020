#ifndef METHODS_H
#define METHODS_H
#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>

using namespace std;

/**
 * @file Methods.cpp
 * @brief Contiene los métodos comúnes para todos los predictores como: obtener el estado del contador, convertir a T o N, realizar predicción y comparación, update a la historia y update al arreglo de contadores. 
 * @class Methods
 * @author Daniel Meseguer Wong
 * @brief Contiene los métodos comúnes para todos los predictores como: obtener el estado del contador, convertir a T o N, realizar predicción y comparación, update a la historia y update al arreglo de contadores. 
 */

class Methods{
    public:
        int txt_counter;
        bool condition;
        /**
         * @brief Constructor de la clase Methods que inicializa un bool y un contador de lineas en la escritura de archivos.
         */
        Methods(){
            txt_counter = 0;
            condition = false;
        }

        /**
         * @brief Convierte estado de un contador de (SN, WN, WT, ST) a T o N.
         * @param number: estado del contador.
         */
        string convert_state(int number){ //Convierte estados en binario a taken o not taken
            string real_state;
            if (number >= 2){real_state = "T";}
            else{real_state = "N";}
            return real_state;
        }

        /**
         * @brief Imprime los estados del arreglo de contadores.
         * @param contadores: es un arreglo con todos los contadores.
         */
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


        /**
         * @brief Obtener el índice adecuado para el arreglo de contadores, según el tipo de predictor.
         * @param line: línea de archivo de entrada con PC y outcome
         * @param bp: ingresado por el usuario para definir el tipo de predictor a usar.
         * @param history: registro de historia.
         * param s: ingresado por el usuario para definir tamaño de las tablas.
         */
        int get_state(string line, int bp, int history, int s){ //Obtiene el estado que se debe utilizar
            int state;
            int mask = (int)(pow(2.0,(double)s)) - 1;
            //Segun bp, se obtienen ultimos s bits.
            if(bp == 0) state =  (stol(line.substr(0, line.find(" ")))) & mask;
            else if(bp == 2) state = (stol(line.substr(0, line.find(" "))) ^ history) & mask;
            else if(bp==1) state = (stol(line.substr(0, line.find(" "))) ^ history) & mask;
            return state;
        }

        /**
         * @brief Compara predicción con outcome y determina si es Correct o Incorrect.
         * @param predicted: predicción realizada
         * @param real: outcome real
         */
        string make_prediction(string predicted, string real){
            string prediction;
            if(predicted == real) prediction = "Correct";
            else prediction = "Incorrect";
            return prediction;
        }


        /**
         * @brief Hace un update al arreglo de contadores según el outcome real. Si es taken, aumenta; si es not taken, disminuye.
         * @param contadores: arreglo de contadores
         * @param index: indice en el que se encuentra el contador siendo utilizado. 
         * @param real: outcome real
         */
        vector<int> update_contadores(vector<int> contadores, int index, string real){//Hace update a los contadores de dos bits
            //Si el branch es taken, se suma al contador; si es not taken, se resta al contador.
            if(real == "T"){
                if(contadores[index]<3) contadores[index]++;
            }

            if(real == "N"){
                if(contadores[index]>0) contadores[index] = contadores[index]-1;
            }

            return contadores;
        }


        /**
         * @brief Actualiza el registro de historia según el outcome real y mantiene este registro del tamaño adecuado.
         * @param history: registro de historia
         * @param mask: máscara para que el registro de historia quede con la cantidad de bits que se requiere.
         * @param real: outcome real.
         */
        int update_history(int history, int mask, string real){//Hace update a los bits de historia para el global share
            if(real == "T") history = ((history<<1) | 1) & mask;
            else if(real == "N") history = (history<<1) & mask;
            return history;
        }

        /**
         * @brief Escribe un archivo de texto con los resultados de cada predicción realizada, si es correcta o incorrecta, según el tipo de predictor utilizado.
         * @param bp: ingresado por el usuario para determinar cual predictor se utiliza.
         * @param input: string de entrada a ser guardado en un archivo. Contiene distintos resultados como predicción, comparación, PC address, etc.
         * @param o: define si se escribe el archivo de texto o no.
         */
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

        /**
         * @brief Imprime una tabla de resultados para el predictor utilizado, con los tamaños de registro de historia, cantidad de entradas, el tipo de predictor, cantidad de branches y desglose según su predicción. Además muestra un porcentaje de branches predecidos correctamente.
         * @param bp_choice: un string que dice cual predictor se está utilizando.
         * @param bht_size: la cantidad de entradas de la tabla BHT. Dado por 2^s.
         * @param gh: ingresado por el usuario determina la cantidad de bits del registro de historia.
         * @param ph: ingresado por el usuario determina la cantidad de bits de cada entrada de la tabla PHT.
         * @param branch_nmbr: cantidad de branches leídas.
         * @param correct_taken: cantidad de branches que se toman y se predijeron correctamente.
         * @param incorret_taken: cantidad de branches que se toman y se predijeron incorrectamente.
         * @param correct_ntaken: cantidad de branches que no se toman y se predijeron correctamente.
         * @param incorrect_ntaken: cantidad de branches que no se toman y se predijeron incorrectamente.
         */
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