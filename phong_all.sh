#!/bin/bash

for ((i=0; i<=100000; i+=1000)); do
    blender phong.blend --background --python phong.py -- $i $(($i+999))
done
