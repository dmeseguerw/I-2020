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
    else if(bp==1) state = (stol(line.substr(0, line.find(" "))) ^ history) & mask;
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
    return history;
}



// NECESITO CAMBIAR TODOS LOS METODOS DE PREDICTOR PARA PODER USAR EL TOURNAMENT
// ENTONCES QUIERO SACAR EL CICLO Y PODER USARLAS PARA REALIZAR SOLO UNA PREDICCION
// CADA VEZ QUE LLAME A GSHARE OCUPO LOS CONTADORES, LA HISTORIA.
// CADA VEZ QUE LLAME A PSHARE OCUPO EL PHT, EL BHT


void bimodal(int s, int bp){
    string ln;
    vector<int> contadores((int)(pow(2.0,(double)s)), 00);
    string real;
    string predicted, prediction;
    int state;
    int mask = (int)(pow(2.0,(double)s)) - 1;
    int history = 0;
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
    }
}

void gshare(int s, int gh, int bp){
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
        history = update_history(history, mask_for_h, real);
    }


}

void pshare(int s, int ph, int bp){
    string ln;
    string real, prediction;
    unsigned int PHT_index;
    unsigned int PC_adrs;
    unsigned int mask = (int)(pow(2.0,(double)s)) - 1;
    int mask_for_h = (int)(pow(2.0,(double)ph)) - 1;
    vector<int> PHT((int)(pow(2.0,(double)s)), 00);
    vector<int> BHT((int)(pow(2.0,(double)s)), 00);
    string predicted;
    int counter = 0;
    unsigned int BHT_index;
    int PHT_current_reg;
    while(getline(cin,ln)){
        counter++;
        if(counter == 100){break;}

        PC_adrs = (stol(ln.substr(0,ln.find(" "))));
        PHT_index = PC_adrs & mask; //Obtengo los ultimos s bits del PC
        PHT_current_reg = PHT[PHT_index];
        BHT_index = get_state(ln, bp, PHT_current_reg, s);
        // BHT_index = (PC_adrs ^ PHT_current_reg) & mask;
        predicted = convert_state(BHT[BHT_index]);
        real = ln.back();
        prediction = make_prediction(predicted, real);
        cout << print_states(BHT) << " | " << predicted << " | " << real << " | " << prediction << endl;

        BHT = update_contadores(BHT, BHT_index, real);
        PHT[PHT_index] = update_history(PHT_current_reg, mask_for_h, real);

    }


}
















void tournament(int s, int ph, int bp, int gh){
    string ln;
    string real1, prediction1;
    string real2, prediction2;
    unsigned int PHT_index;
    unsigned int PC_adrs;
    unsigned int mask = (int)(pow(2.0,(double)s)) - 1;
    int mask_for_h = (int)(pow(2.0,(double)ph)) - 1;
    vector<int> PHT((int)(pow(2.0,(double)s)), 00);
    vector<int> BHT((int)(pow(2.0,(double)s)), 00);
    vector<int> contadores((int)(pow(2.0,(double)s)), 00);
    vector<int> MetaPredictor((int)(pow(2.0,(double)s)), 00);
    string predicted1, predicted2;
    unsigned int meta_index;
    int history = 0*gh;
    int counter = 0;
    int state;
    unsigned int BHT_index;
    int PHT_current_reg;
    int which;
    cout << "G Predictions | P Predictions | REAL " << endl;
    while(getline(cin,ln)){
        counter++;
        if(counter == 100){break;}

        //Correr ambos predictores y pbtener sus predicciones correspondientes

        meta_index = (stol(ln.substr(0, ln.find(" ")))) & mask;
        which = check_predictions(predicted1, predicted2, real1);
        if(which == 1){
            //Uso el Gshare
            if(MetaPredictor[meta_index]<3) MetaPredictor[meta_index]++;
        }
        if(which==2){
            //Uso el Pshare
            if(MetaPredictor[meta_index]>0) MetaPredictor[meta_index] = MetaPredictor[meta_index] - 1;
        }

        
        

    }

}

int check_predictions(string pred1, string pred2, string real){
    if(pred1==real){
        if(pred2!=real){
            //Update al Gshare
            return 1;
        }
        else{return 0;}
    }
    else{
        if(pred2==real){
            //Update al Pshare
            return 2;
        }
    }
}


void create_table(){
}

void print_results(){

}



int main(int argc, char **argv){

    // Obtencion de parametros
    int s, bp, gh, ph, o;
    s = atoi(argv[2]);
    bp = atoi(argv[4]);
    gh = atoi(argv[6]);
    // gshare_and_bimodal(s, gh, bp);
    ph = atoi(argv[8]);
    // pshare(s, ph, bp);
    // tournament(s, ph, bp, gh);
    // o = atoi(argv[10]);


}