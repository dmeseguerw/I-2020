#ifndef PSHARE_H
#define PSHARE_H
#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>


#include "Methods.cpp"


using namespace std;

/**
 * @file Pshare.cpp
 * @brief La clase Pshare contiene métodos para realizar una sola predicción y otro para realizar todas las predicciones de un archivo instanciando al primer método. Posee atributos para guardar la tabla PHT y el BHT, la predicción, su estado, y el outcome real. Además de un objeto de la clase Methods para poder invocar los métodos necesarios de esa clase. 
 * @class Pshare
 * @author Daniel Meseguer Wong
 * @brief La clase Pshare contiene métodos para realizar una sola predicción y otro para realizar todas las predicciones de un archivo instanciando al primer método. Posee atributos para guardar la tabla PHT y el BHT, la predicción, su estado, y el outcome real. Además de un objeto de la clase Methods para poder invocar los métodos necesarios de esa clase.
 */

class Pshare{
    public:

        /**
         * @brief Obtiene un índice de la tabla PHT, realiza una XOR con el PC, e indexa al BHT para realizar la predicción con el contador correspondiente.
         * @param ln: cada instruccion con su respectivo outcome
         * @param s: parametro ingresado por el usuario para calcular el tamaño de los arreglos de contadores.
         * @param bp: parámetro ingresado por el usuario para definir cual predictor se usa, en este caso debería ser 0.
         * @param ph: parámetro ingresado por el usuario para definir la cantidad de bits de historia de cada entrada del PHT.
         * @param o: parámetro ingresado por el usuario para decidir si se escribe o no a un archivo .txt.
         */
        void make_Ppred(string ln, int bp, int s, int ph, int o){
            unsigned int mask = (int)(pow(2.0,(double)s)) - 1; //Mascara para obtener los ultimos s bits del PC
            int mask_for_h = (int)(pow(2.0,(double)ph)) - 1; //Mascara para retener cada registro de historia de tamano ph bits.
            string real;
            unsigned int PHT_index = (stol(ln.substr(0,ln.find(" ")))) & mask; //Obtengo los ultimos s bits del PC
            unsigned int PHT_current_reg = PHT[PHT_index]; //Obtengo el indice para el PHT
            unsigned int BHT_index = met.get_state(ln, bp, PHT_current_reg, s); //Obtengo el indice para el BHT
            Pshare::prediction = met.convert_state(Pshare::BHT[BHT_index]); //Convertir estado a T o N.
            real = ln.back(); //Obtengo outcome real del branch.
            Pshare::pred_status = met.make_prediction(Pshare::prediction, real); //Comparo prediccion con outcome

            //Escribe a archivo de texto si o es 1.
            string txt_input = ln.substr(0, ln.find(" ")) + " | " + Pshare::prediction + " | " + real + " | " + Pshare::pred_status;
            met.create_txt(bp, txt_input, o);

            //Hago update a BHT y a PHT.
            Pshare::BHT = met.update_contadores(Pshare::BHT, BHT_index, real);
            Pshare::PHT[PHT_index] = met.update_history(PHT_current_reg, mask_for_h, real);

        }

        /**
         * @brief Inicializa los contadores de BHT en Strongly Not Taken y el PHT en cero, e inicializa los counter respectivos a la cantidad de branches y predicciones correctas e incorrectas. Recorre todo el archivo de entrada y realiza predicciones utilizando make_Ppred. Agrega a los counters de resultados según la predicción realizada.
         * @param gh: parámetro ingresado por el usuario para definir la cantidad de bits del registro de historia del predictor global.
         * @param ph: parámetro ingresado por el usuario para definir la cantidad de bits de historia de cada entrada de la tabla pht.
         * @param s: parametro ingresado por el usuario para calcular el tamaño de los arreglos de contadores.
         * @param bp: parámetro ingresado por el usuario para definir cual predictor se usa, en este caso debería ser 0.
         * @param o: parámetro ingresado por el usuario para decidir si se escribe o no a un archivo .txt.
         */
        void use_Ppredictor(int bp, int s, int ph, int gh, int o){
            string ln;
            //Inicializo PHT y BHT y los contadores de resultados.
            vector<int> PHT((int)(pow(2.0,(double)s)),00);
            vector<int> BHT((int)(pow(2.0,(double)s)),00);
            Pshare::PHT = PHT;
            Pshare::BHT = BHT;
            int branch_counter = 0;
            int c_taken = 0;
            int i_taken = 0;
            int c_ntaken = 0;
            int i_ntaken = 0;
            while(getline(cin,ln)){//Leo el trace linea por linea

                make_Ppred(ln, bp, s, ph, o); //Realizo prediccion
                if(met.condition) break;

                //Update a los contadores de resultados.
                if(prediction == "T" & pred_status == "Correct") c_taken++;
                else if(prediction == "T" & pred_status == "Incorrect") i_taken++;
                else if(prediction == "N" & pred_status == "Correct") c_ntaken++;
                else if(prediction == "N" & pred_status == "Incorrect") i_ntaken++;
                branch_counter++;
            }
            met.print_results("Pshare", BHT.size(), gh, ph, branch_counter, c_taken, i_taken, c_ntaken, i_ntaken); //Imprimo tabla de resultados finales.
 
        }

        vector<int> PHT, BHT;
        string prediction, pred_status;
        Methods met;
};

#endif