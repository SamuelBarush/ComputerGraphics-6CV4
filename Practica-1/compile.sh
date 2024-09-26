#!/bin/bash

output="salida"

sdl_flags=$(sdl2-config --cflags --libs)


gcc -o "$output" *.c $sdl_flags -lm