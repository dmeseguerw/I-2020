#!/bin/bash/
g++ reader.cpp -o tarea
gunzip -c mcf.trace.gz | ./tarea 0
