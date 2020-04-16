# -*- coding: cp850 -*-
import subprocess
from subprocess import check_output

def run():
    #cmd = ["java -jar C:/Users/asus\Desktop/Java_Compiler/dist/Java_Compiler.jar"]
    p2 = subprocess.check_output(["java", "-jar", "C:/Users/asus\Desktop/Java_Compiler/dist/Java_Compiler.jar"])
    #print p2
    return p2