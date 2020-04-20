#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>

using namespace std;

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
    return state;
}

//Decide si la prediccion es correcta o incorrecta
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
}





void gshare_and_bimodal(int s, int gh, int bp){
    string ln;
    vector<int> contadores((int)(pow(2.0,(double)s)), 00);
    string real;
    string predicted, prediction;
    int state;
    int mask_for_h = (int)(pow(2.0,(double)gh)) - 1;
    int mask = (int)(pow(2.0,(double)s)) - 1;
    int history = 0*gh;
    int counter = 0;
    while(getline(cin,ln)){
        counter++;
        if(counter == 100){break;}

        state = get_state(ln, bp, history, s);
        real = ln.back();
        predicted = convert_state(contadores[state]);
        prediction = make_prediction(predicted, real);
        cout << print_states(contadores) << " | " << predicted << " | " << real << " | " << prediction << endl;
        
        
        contadores = update_contadores(contadores, state, real);
        if(bp == 2) history = update_history(history, mask_for_h, real);
    }


}

void tournament(){}

void pshare(){}



void create_table(){}

void print_results(){}



int main(int argc, char **argv){

    // Obtencion de parametros
    int s, bp, gh, ph, o;
    s = atoi(argv[2]);
    bp = atoi(argv[4]);
    gh = atoi(argv[6]);
    gshare_and_bimodal(s, gh, bp);
    // ph = atoi(argv[8]);
    // o = atoi(argv[10]);


}