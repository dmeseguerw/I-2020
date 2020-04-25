
#include <iostream>
#include <fstream>
#include <math.h>
#include <vector>
#include "Methods.cpp"
#include "Gshare.cpp"
#include "Pshare.cpp"

using namespace std;

/**
 * @file Tournament.cpp
 * @brief La clase Tournament posee los métodos para utilizar un predictor Tournament. Hereda de las clases Gshare y Pshare. Tiene atributos para guardar la predicción y su comparación, además de crear objetos de las clases Gshare, Pshare, y Methods.
 * @class Tournament
 * @brief La clase Tournament posee los métodos para utilizar un predictor Tournament. Hereda de las clases Gshare y Pshare. 
 * @author Daniel Meseguer Wong
 */



class Tournament{

    public:
        /**
         * @brief Realiza una predicción al obtener el índice del metapredictor, convertir ese estado a P o G, y comparar cada prediccion con el outcome real.
         * @param ln: cada instruccion con su respectivo outcome
         * @param s: parametro ingresado por el usuario para calcular el tamaño de los arreglos de contadores.
         * @param bp: parámetro ingresado por el usuario para definir cual predictor se usa, en este caso debería ser 0.
         * @param gh: parámetro ingresado por el usuario para definir la cantidad de bits del registro de historia del Gshare.
         * @param ph: parámetro ingresado por el usuario para definir la cantidad de bits de historia de cada entrada del PHT.
         * @param o: parámetro ingresado por el usuario para decidir si se escribe o no a un archivo .txt.
         */
        void make_Tournament(string ln, int bp, int s, int gh, int ph, int o){
            string real;
            int meta_index = met.get_state(ln, 0, 0, s); //Obtengo indice del metapredictor con ultimos s bits de PC
            string p_prediction, g_prediction;
            gpred.make_Gpred(ln, 2, s, gh, o); //Realizo prediccion usando el Gshare
            g_prediction = gpred.prediction;
            ppred.make_Ppred(ln, 1, s, ph, o); //Realizo prediccion usando el Pshare
            p_prediction = ppred.prediction;

            real = ln.back(); //Obtengo el outcome real del branch
            string pred_in_use = convert_state(MetaPredictor[meta_index]); //Obtengo el predictor a ser utilizado segun el Meta
            comparePred(pred_in_use, g_prediction, p_prediction, real); //Comparo prediccion

            //Escribo a archivo de texto
            string txt_input = ln.substr(0, ln.find(" ")) + " | " + Tournament::prediction + " | " + real + " | " + Tournament::pred_status;
            met.create_txt(bp, txt_input, o);

            //Hago update al MetaPredictor
            updateMeta(real, p_prediction, g_prediction, meta_index);
        }

        /**
         * @brief Según la predicción realizada y el predictor utilizado, hace update al metapredictor cambiando de estado.
         * @param real: Outcome real del branch.
         * @param p_prediction: Predicción realizada por el Pshare.
         * @param g_prediction: Predicción realizada por el Gshare.
         * @param meta_index: Índice utilizado de Metapredictor que indica a un contador específico.
         */
        void updateMeta(string real, string p_prediction, string g_prediction, int meta_index){
            //Si ambos son correctos no se hace update, si Gshare es correcto se aumenta, si Pshare es correcto se disminuye.
            if(g_prediction == real){
                if(p_prediction != real){
                    if(Tournament::MetaPredictor[meta_index]<3) Tournament::MetaPredictor[meta_index]++;
                }
            }
            else if(p_prediction == real){
                if(Tournament::MetaPredictor[meta_index]>0) Tournament::MetaPredictor[meta_index] = Tournament::MetaPredictor[meta_index]-1;
            }
        }

        /**
         * @brief Define si la predicción es correcta o incorrecta según el predictor que se utilice en el branch.
         * @param pred_in_use: el predictor que estamos utilizando.
         * @param g_prediction: predicción realizada por el Gshare.
         * @param p_prediction: predicción realizada por el Pshare.
         * @param real: outcome real.
         */
        void comparePred(string pred_in_use, string g_prediction, string p_prediction, string real){
            //Se determina si la predicción es correcta o incorrecta segun el predictor siendo utilizado.
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

        /**
         * @brief Convierte de strongly o weakly a un solo estado de P o G.
         * @param number: estado del contador (00, 01, 10, 11)
         */
        string convert_state(int number){ //Convierte estados en binario a P o G.
            string real_state;
            if (number >= 2){real_state = "G";}
            else{real_state = "P";}
            return real_state;
        }

        /**
         * @brief
         * @param bp: ingresado por el usuario para definir cual predictor se usa.
         * @param s: ingresado por el usuario para calcular el tamaño de los arreglos de contadores.
         * @param gh: ingresado por el usuario para definir la cantidad de bits del registro de historia de Gshare.
         * @param ph: ingresado por el usuario para definir la cantidad de bits de cada entrada de la tabla PHT del Pshare.
         * @param o: define si se escribe o no un archivo de texto con las predicciones.
         */
        void use_Tournament(int bp, int s, int gh, int ph, int o){
            string ln;
            //Se inicializan los predictores Gshare y Pshare, el MetaPredictor y los contadores de resultados.
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

            while(getline(cin, ln)){//Se lee el trace linea por linea
                make_Tournament(ln, bp, s, gh, ph, o); //Se realiza la eleccion de predictor y la prediccion
                if(met.condition) break;
                
                //Se hace update a los contadores de resultados.
                if(prediction == "T" & pred_status == "Correct") c_taken++;
                else if(prediction == "T" & pred_status == "Incorrect") i_taken++;
                else if(prediction == "N" & pred_status == "Correct") c_ntaken++;
                else if(prediction == "N" & pred_status == "Incorrect") i_ntaken++;
                branch_counter++;
            }
            met.print_results("Tournament", gpred.contadores.size(), gh, ph, branch_counter, c_taken, i_taken, c_ntaken, i_ntaken); //Se imprime tabla con resultados finales.
        }

    private:
        vector<int>MetaPredictor;
        Methods met;
        Gshare gpred;
        Pshare ppred;
        string prediction;
        string pred_status;



};
