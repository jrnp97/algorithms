# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from execute import run
import codecs

home = Blueprint('home', __name__)

def file(Content):
    #Creando archivo *.utb
    file = open('program.utb', 'w')
    file.write(Content)
    file.close()

def file2(Content):
    # Creando archivo *.utb
    file = open('result.txt', 'w')
    file.write(Content)
    file.close()

def extract():
    file = open('result.txt', 'r')
    data = file.readlines()
    file.close()
    print type(data)
    return data

#Index
@home.route('/',  methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #extrayendo codigo
        Code = request.form['code']
        #creando archivo con el codigo
        file(Code)
        #executandolo
        Code = run()
        #generando archivo de salida
        file2(Code)
        #Extrayendo datos del archivo
        data = extract()

        return render_template('index.html', RESULT=data)
    else:
        return render_template('index.html', RESULT="Sin Compilar")