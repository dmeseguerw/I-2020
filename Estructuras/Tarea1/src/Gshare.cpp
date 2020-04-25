#ifndef GSHARE_H
#define GSHARE_H
#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>

#include "Methods.cpp"



using namespace std;

/**
 * @file Gshare.cpp
 * @brief La clas Gshare contiene los métodos para ejecutar un predictor Gshare. Encontramos make_Gpred para realizar una sola predicción, y use_Gpred para leer todo un archivo de entrada e instanciar por cada línea a make_Gpred. Tenemos atributos para los contadores (BHT), un registro de historia, y la predicción y el estado de la predicción (Correcto o incorrecto), además de guardar el outcome real.
 * @class Gshare
 * @author Daniel Meseguer Wong
 * @brief La clas Gshare contiene los métodos para ejecutar un predictor Gshare. Encontramos make_Gpred para realizar una sola predicción, y use_Gpred para leer todo un archivo de entrada e instanciar por cada línea a make_Gpred. Tenemos atributos para los contadores (BHT), un registro de historia, y la predicción y el estado de la predicción (Correcto o incorrecto), además de guardar el outcome real.
 */
class Gshare{
    public:

        /**
         * @brief Realiza una predicción al obtener el índice de la tabla de contadores mediante un registro de historia, convertir ese estado a taken o not taken, y comparar con el outcome real. Hace un llamado a otros métodos de la clase Methods.
         * @param ln: cada instruccion con su respectivo outcome
         * @param s: parametro ingresado por el usuario para calcular el tamaño de los arreglos de contadores.
         * @param bp: parámetro ingresado por el usuario para definir cual predictor se usa, en este caso debería ser 0.
         * @param o: parámetro ingresado por el usuario para decidir si se escribe o no a un archivo .txt.
         * @param gh: parámetro ingresado por el usuario para definir la cantidad de bits del registro de historia.
         */
        void make_Gpred(string ln, int bp, int s, int gh, int o){
            int index;
            string real;
            int mask_for_h = (int)(pow(2.0,(double)gh)) - 1; //Esta mascara es para que el registro de historia quede siempre con gh bits.
            index = Gshare::met.get_state(ln, bp, history, s); // Se obtiene el indice para el arreglo de contadores.
            real = ln.back(); //Se obtiene el outcome real del branch.
            Gshare::prediction = Gshare::met.convert_state(Gshare::contadores[index]); //Se convierte el estado a T o N
            Gshare::pred_status = Gshare::met.make_prediction(Gshare::prediction, real); //Se realiza comparacion de prediccion

            //Se escribe a archivo de texto
            string txt_input = ln.substr(0, ln.find(" ")) + " | " + Gshare::prediction + " | " + real + " | " + Gshare::pred_status;
            met.create_txt(bp, txt_input, o);

            //Se hace update al arreglo de contadores y al registro de historia.
            Gshare::contadores = Gshare::met.update_contadores(Gshare::contadores, index, real);
            Gshare::history = Gshare::met.update_history(Gshare::history, mask_for_h, real);

        }


        /**
         * @brief Se inicializan los contadores del BHT en Strongly Not Taken (00), y también los counters de branches y de predicciones correctas o incorrectas. Se inicializa el registro de historia en cero. Se encarga de realizar las predicciones de todo un archivo mediante un llamado a make_Gpred enciclado. Suma a los counters y al final imprime los resultados.
         * @param gh: parámetro ingresado por el usuario para definir la cantidad de bits del registro de historia del predictor global.
         * @param ph: parámetro ingresado por el usuario para definir la cantidad de bits de historia de cada entrada de la tabla pht.
         * @param s: parametro ingresado por el usuario para calcular el tamaño de los arreglos de contadores.
         * @param bp: parámetro ingresado por el usuario para definir cual predictor se usa, en este caso debería ser 0.
         * @param o: parámetro ingresado por el usuario para decidir si se escribe o no a un archivo .txt.
        */
        void use_Gpredictor(int bp, int s, int gh, int ph, int o){
            string ln;
            //Se inicializa el arreglo de contadores y el registro de historia.
            vector<int> contadores((int)(pow(2.0,(double)s)),00);
            Gshare::contadores = contadores;
            Gshare::history = 0;

            //Se inicializan los contadores de resultados.
            int branch_counter = 0;
            int c_taken = 0;
            int i_taken = 0;
            int c_ntaken = 0;
            int i_ntaken = 0;

            while(getline(cin,ln)){ //Se lee el trace linea por linea

                make_Gpred(ln, bp, s, gh, o); //Se realiza una prediccion
                if(met.condition) break;

                //Se hace update a los contadores de resultados.
                if(prediction == "T" & pred_status == "Correct") c_taken++;
                else if(prediction == "T" & pred_status == "Incorrect") i_taken++;
                else if(prediction == "N" & pred_status == "Correct") c_ntaken++;
                else if(prediction == "N" & pred_status == "Incorrect") i_ntaken++;
                branch_counter++;
            }
            met.print_results("Gshare", contadores.size(), gh, ph, branch_counter, c_taken, i_taken, c_ntaken, i_ntaken); //Se imprimen los resultados finales.
        }

        vector<int> contadores;
        int history; //registro de historia
        string prediction, pred_status;
        Methods met;
};

#endif