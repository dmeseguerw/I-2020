#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>
#include "Gshare.cpp"
#include "Bimodal.cpp"
#include "Pshare.cpp"
#include "Tournament.cpp"

using namespace std;

int main(int argc, char **argv){

    // Obtencion de parametros
    int s, bp, gh, ph, o;
    s = atoi(argv[2]);
    bp = atoi(argv[4]);
    gh = atoi(argv[6]);
    ph = atoi(argv[8]);
    o = atoi(argv[10]);

    if(bp==0){
        Bimodal bi;
        bi.use_Bipred(bp,s, gh, ph,o);
    }
    if(bp==1){
        Pshare p;
        p.use_Ppredictor(bp,s,ph,gh,o);
    }
    if(bp==2){
        Gshare g;
        g.use_Gpredictor(bp, s, gh, ph, o);
    }
    if(bp==3){
        Tournament t;
        t.use_Tournament(bp, s, gh, ph, o);
    }

}