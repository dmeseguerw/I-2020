all: ex

ex:
	g++ predictor.cpp
	gunzip -c ~/Downloads/branch-trace-gcc.trace.gz | ./a.out -s 3
	gunzip -c ~/Downloads/branch-trace-gcc.trace.gz | ./a.out -s 4 -bp 2 -gh 3 
	gunzip -c ~/Downloads/branch-trace-gcc.trace.gz | ./a.out -s 5 -bp 1 -gh 3 -ph 2 