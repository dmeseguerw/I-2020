all: compile bimodal gshare pshare tournament doxy

compile:
	g++ src/main.cpp

bimodal:
	gunzip -c ~/Downloads/branch-trace-gcc.trace.gz | ./a.out -s 3 -bp 0 -gh 4 -ph 3 -o 1

gshare:
	gunzip -c ~/Downloads/branch-trace-gcc.trace.gz | ./a.out -s 4 -bp 2 -gh 3 -ph 3 -o 1

pshare:
	gunzip -c ~/Downloads/branch-trace-gcc.trace.gz | ./a.out -s 5 -bp 1 -gh 3 -ph 2 -o 1

tournament:	
	gunzip -c ~/Downloads/branch-trace-gcc.trace.gz | ./a.out -s 3 -bp 3 -gh 4 -ph 3 -o 1

doxy:
	doxygen doc/Doxyfile