import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.shortcuts import render
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from apps.registro.models import *
import mpld3
#import matplotlib as matplt

def getcreditsbytrandct(trimestre_dado, cohorte_dada):
    EstudiantesDeCohorteCT = Estudiante.objects.filter(cohorte_id = cohorte_dada)
    print(Estudiante.objects.first().cohorte_id)

    listadeCursaporEstdecohortect = []
    for estudianteCT in EstudiantesDeCohorteCT:
        listadeCursaporEstdecohortect.append(Cursa.objects.filter(estudiante = estudianteCT))

    if int(cohorte_dada) >= 68:
        apendboy = '19'
    else:
        apendboy = '20'


    trimestres = ['Sep-Dic ' + apendboy + str(int(cohorte_dada)), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+1), 'Abr-Jul '+ apendboy + str(int(cohorte_dada)+1), 'Sep-Dic ' + apendboy + str(int(cohorte_dada)+1), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+2), 
        'Abr-Jul '+ apendboy +str(int(cohorte_dada)+2), 'Sep-Dic ' + apendboy + str(int(cohorte_dada)+2), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+3), 'Abr-Jul '+ apendboy +str(int(cohorte_dada)+3), 'Sep-Dic ' + apendboy + str(int(cohorte_dada)+3), 
        'Ene-Mar '+ apendboy + str(int(cohorte_dada)+4), 'Abr-Jul '+ apendboy +str(int(cohorte_dada)+4),'Sep-Dic ' + apendboy + str(int(cohorte_dada)+4), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+5), 'Abr-Jul '+ apendboy +str(int(cohorte_dada)+5)]

    lista = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for cursa_est in listadeCursaporEstdecohortect:
        creditos = 0
        for i in trimestres:
            if cursa_est.filter(trimestre_id = i).count() > 0:

                creditos += cursa_est.filter(trimestre_id = i).first().creditosAprobados
                
            if i == trimestre_dado:
                break
        if creditos == 0:
            lista[0] += 1
        else:
            if creditos <= 240:
                lista[int((creditos -1)/ 16) + 1] += 1
            else:
                lista[-1] += 1
    print(lista)

    return lista

def obtenerMatriz(cohorte):
    matriz = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    EstudianteDeCohorte = Estudiante.objects.filter(cohorte_id = cohorte)
    print('id cohorte: ' + str(Estudiante.objects.first().cohorte_id))
    #for x in EstudianteDeCohorte:
     #   print(x.cohorte_id)
      #  print(x.carnet)
    cuenta = EstudianteDeCohorte.count()
    numeroTrimestres = 0
    trimestresVistos = []
    listaEstudiantes = []

    if int(cohorte) >= 68:
        apendboy = '19'
    else:
        apendboy = '20'
    cohorte_dada = cohorte

    trimestress = ['Sep-Dic ' + apendboy + str(int(cohorte_dada)), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+1), 'Abr-Jul '+ apendboy + str(int(cohorte_dada)+1), 'Sep-Dic ' + apendboy + str(int(cohorte_dada)+1), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+2),
        'Abr-Jul '+ apendboy +str(int(cohorte_dada)+2), 'Sep-Dic ' + apendboy + str(int(cohorte_dada)+2), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+3), 'Abr-Jul '+ apendboy +str(int(cohorte_dada)+3), 'Sep-Dic ' + apendboy + str(int(cohorte_dada)+3),
        'Ene-Mar '+ apendboy + str(int(cohorte_dada)+4), 'Abr-Jul '+ apendboy +str(int(cohorte_dada)+4),'Sep-Dic ' + apendboy + str(int(cohorte_dada)+4), 'Ene-Mar '+ apendboy + str(int(cohorte_dada)+5), 'Abr-Jul '+ apendboy +str(int(cohorte_dada)+5)]


    for estudianteAct in EstudianteDeCohorte:
        print(estudianteAct.nombre)
        CursasEsatudiante = Cursa.objects.filter(estudiante = estudianteAct)
        for cursaAct in CursasEsatudiante:
            trimestreVar = cursaAct.trimestre.id
            print(trimestreVar)
            if trimestreVar in trimestresVistos:
                posicion = trimestress.index(trimestreVar) + 1
                creditos = cursaAct.creditosAprobados
                print(creditos)
                if creditos <= 240:
                    matriz[posicion][int((creditos - 1)/ 16) + 1] += 1
                else:
                    matriz[posicion][16] += 1
            else:
                trimestresVistos.append(trimestreVar)
                temp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                matriz.append(temp)
    print(trimestresVistos)
    print(matriz)

    for i in matriz:
        for j in i:
            j = j * 100 / cuenta

    return [matriz, trimestresVistos]

def crear_grafica(cohorte, carrera, trimestre, total_estudiantes, lista):

    carrera = carrera
    total_de_estudiantes = total_estudiantes
    total_de_creditos_carrera = 240
    cohorte = cohorte
    trimestre = trimestre
    titulo = cohorte + '\n' + trimestre
    lista = lista

    # Statico
    datos = ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%', '']
    creditos = []

    # arreglo que contendra un % con respecto al 100 % de la cohorte
    y = []

    for i in lista:
        y.append(((float(i * 100)) / total_de_estudiantes) / 10)

    # creditos que estaran en el eje x (varia con respecto al total de creditos de la carrera)
    contador = 0
    string = ""
    creditos.append(str(contador))
    seguir = False
    while not (seguir):
        if total_de_creditos_carrera == contador:
            seguir = True

        else:
            contador += 1

            if contador == total_de_creditos_carrera:
                creditos.append(str(contador))
                seguir = True

            else:
                string += str(contador)
                valor_a_sumar = total_de_creditos_carrera - contador
                if valor_a_sumar >= 15:
                    string += "-"
                    contador += 15
                    string += str(contador)

                else:
                    string += "-"
                    contador += valor_a_sumar
                    string += str(contador)

        if len(string) != 0:
            creditos.append(string)
        else:
            pass
        string = ""

    creditos.append("240+")
    # OJO: La longitud de creditos debe ser igual a la longitud de la lista que contiene el numero de estudiantes por trimestre


    idsx = np.arange(len(creditos))
    idsy = np.arange(len(datos))

    # Formato de la figura
    fig = plt.figure(figsize=(22, 12), dpi=60, frameon=True)

    # 1 cuadro por imagen
    ax = fig.add_subplot(1, 1, 1)

    # Grafia barra
    plt.bar(idsx, y, width=0.5, color='c', align="center", label=carrera)

    # labels
    plt.yticks(idsy, datos, fontsize=14)
    plt.xticks(idsx, creditos, fontsize=14)  # labels del eje horizontal

    # nombres, titulos y leyenda y frontera del eje y
    plt.xlabel("Créditos", fontsize=18)
    plt.ylabel("% de Estudiantes", fontsize=18)
    plt.ylim(0, 11)

    plt.title(titulo, fontsize=20)
    plt.legend(bbox_to_anchor=(0, 0, 1, 1), fontsize=15, loc=2, shadow=True)  # loc= "lower left"
    #plt.savefig(fname="static/grafica.png", dpi=100)
    return mpld3.fig_to_html(fig)
