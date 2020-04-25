all: ex

ex:
	g++ main.cpp
	gunzip -c ~/Downloads/branch-trace-gcc.trace.gz | ./a.out -s 3 -bp 0 -gh 4 -ph 3 -o 1
	gunzip -c ~/Downloads/branch-trace-gcc.trace.gz | ./a.out -s 4 -bp 2 -gh 3 -ph 3 -o 1
	gunzip -c ~/Downloads/branch-trace-gcc.trace.gz | ./a.out -s 5 -bp 1 -gh 3 -ph 2 -o 1
	gunzip -c ~/Downloads/branch-trace-gcc.trace.gz | ./a.out -s 3 -bp 3 -gh 4 -ph 3 -o 1