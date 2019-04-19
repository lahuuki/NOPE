# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:48:12 2019

@author: akarami
"""

def tf_input_make(cubes,tags):
    tf_in = []
    for cube in range(len(cubes)):
        if cube+1 in tags:
            tf_in.append(cube,1)
        else:
            tf_in.append(cube,0)
    return tf_in
