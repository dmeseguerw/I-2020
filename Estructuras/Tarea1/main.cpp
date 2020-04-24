#include <iostream>
#include <fstream>
#include <math.h> 
#include <vector>
// #include "Gshare.cpp"
// #include "Bimodal.cpp"
#include "Pshare.cpp"

using namespace std;

int main(int argc, char **argv){

    // Obtencion de parametros
    int s, bp, gh, ph, o;
    s = atoi(argv[2]);
    bp = atoi(argv[4]);
    gh = atoi(argv[6]);
    // gshare_and_bimodal(s, gh, bp);
    ph = atoi(argv[8]);
    // Gshare g;
    // g.use_Gpredictor(bp, s, gh);
    // Bimodal bi;
    // bi.use_Bipred(bp,s);
    Pshare p;
    p.use_Ppredictor(bp,s,ph);
    // o = atoi(argv[10]);


}