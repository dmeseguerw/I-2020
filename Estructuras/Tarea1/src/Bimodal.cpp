#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>
#include "Methods.cpp"


using namespace std;

/**
 * @file Bimodal.cpp
 * @brief La clase Bimodal contiene los métodos para utilizar un predictor bimodal. make_Bipred realiza una predicción una por una, y use_Bipred realiza todas las predicciones. Existen variables de clase para almacenar los contadores, el estado de predicción, la predicción, y el outcome real. 
 * @class Bimodal
 * @author Daniel Meseguer Wong
 * @brief La clase Bimodal contiene los métodos para utilizar un predictor bimodal. make_Bipred realiza una predicción una por una, y use_Bipred realiza todas las predicciones. Existen variables de clase para almacenar los contadores, el estado de predicción, la predicción, y el outcome real. 
 */
class Bimodal{
    public:
        /**
         * @brief Realiza una predicción al obtener el índice de la tabla de contadores, convertir ese estado a taken o not taken, y comparar con el outcome real.
         * @param ln: cada instruccion con su respectivo outcome
         * @param s: parametro ingresado por el usuario para calcular el tamaño de los arreglos de contadores.
         * @param bp: parámetro ingresado por el usuario para definir cual predictor se usa, en este caso debería ser 0.
         * @param o: parámetro ingresado por el usuario para decidir si se escribe o no a un archivo .txt.
         */
        void make_Bipred(string ln, int s, int bp, int o){
            string txt_input;
            int index = met.get_state(ln, bp, 0, s); //Obtiene el indice para el arreglo de contadores según su bp
            Bimodal::real = ln.back(); //Se obtiene el outcome real del branch.
            Bimodal::prediction = met.convert_state(Bimodal::contadores[index]); //Convierte de weak o strong a T o N
            Bimodal::pred_status = met.make_prediction(Bimodal::prediction, Bimodal::real); //Se compara si es correcta o incorrecta
            txt_input = ln.substr(0, ln.find(" ")) + " | " + Bimodal::prediction + " | " + Bimodal::real + " | " + Bimodal::pred_status; //String a ingresar en el archivo de texto.
            met.create_txt(bp, txt_input, o); //Se crea el archivo de texto si o es 1.
            Bimodal::contadores = met.update_contadores(Bimodal::contadores, index, real); //Se hace update al arreglo de contadores.
        }

        /**
         * @brief Inicializa los contadores en Strongly Not Taken, e inicializa los counter respectivos a la cantidad de branches y predicciones correctas e incorrectas. Recorre todo el archivo de entrada y realiza predicciones utilizando make_Bipred. Agrega a los counters de resultados según la predicción realizada.
         * @param gh: parámetro ingresado por el usuario para definir la cantidad de bits del registro de historia del predictor global.
         * @param ph: parámetro ingresado por el usuario para definir la cantidad de bits de historia de cada entrada de la tabla pht.
         * @param s: parametro ingresado por el usuario para calcular el tamaño de los arreglos de contadores.
         * @param bp: parámetro ingresado por el usuario para definir cual predictor se usa, en este caso debería ser 0.
         * @param o: parámetro ingresado por el usuario para decidir si se escribe o no a un archivo .txt.
         */
        void use_Bipred(int bp, int s, int gh, int ph, int o){
            string ln;
            vector<int> contadores((int)(pow(2.0,(double)s)),00); //Se inicializa el arreglo de contadores en SN.
            Bimodal::contadores = contadores;
            //Se inicializann contadores para los resultados en cero.
            int branch_counter = 0;
            int c_taken = 0;
            int i_taken = 0;
            int c_ntaken = 0;
            int i_ntaken = 0;
            while(getline(cin,ln)){ //Se hace lectura linea por linea del archivo de entrada

                make_Bipred(ln, s, bp, o); //Se realiza la prediccion segun el branch actual
                if(met.condition) break; 

                //Se actualizan los contadores de resultados segun el estado de la prediccion.
                if(prediction == "T" & pred_status == "Correct") c_taken++;
                else if(prediction == "T" & pred_status == "Incorrect") i_taken++;
                else if(prediction == "N" & pred_status == "Correct") c_ntaken++;
                else if(prediction == "N" & pred_status == "Incorrect") i_ntaken++;
                branch_counter++;
            }

            met.print_results("Bimodal", contadores.size(), gh, ph, branch_counter, c_taken, i_taken, c_ntaken, i_ntaken); // Imprime los resultados finales del predictor
        }



        vector<int> contadores; //Arreglo de contadores
        string prediction, pred_status, real;
        Methods met;
};