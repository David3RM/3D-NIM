# Permite a dos agentes jugar partidas. Tambien recogera información sobre las partidas.
from Tablero import Tablero_3Dimensiones
from Agentes import Agente, AgenteAleatorio, AgenteBasadoEnReglas, AgenteAlfaBeta
import time
import pandas as pd
import numpy as np

class AgenteVSAgente():

    def __init__(self,semilla, n, tableros, profundidad, Agentes, guardarResultados):
        self.guardarResultados = guardarResultados
        self.tableros = tableros
        self.Agentes = Agentes
        self.semilla = semilla
        self.dictionary = {"Jugador 1": [],"Victorias 1": [],"Jugador 2": [],"Victorias 2": [], "Profundidad 1": [], "Profundidad 2": [], "Ramificación máxima 1": [], "Ramificación máxima 2": [], "N.º Partidas": [], "Tamaño del Tablero": [], "Tiempo total": [], "Tiempo medio por partida": [],
                                        "Tiempo medio para mover 1": [], "Tiempo medio para mover 2": []}
        for tablero in tableros:
            for i in range(len(Agentes)-1):
                Agente1 = Agentes[i]
                Agente1 = self.PrepararAgente(Agente1,tablero,profundidad)
                for j in range(i+1,len(Agentes)):
                    Agente2 = Agentes[j]
                    Agente2 = self.PrepararAgente(Agente2,tablero,profundidad)
                    self.SimularNPartidas(n,tablero,Agente1,Agente2)
                    # Simulamos los partidas pero los agentes cambian de turno, para observar si el turno ofrece alguna ventaja.
                    self.SimularNPartidas(n,tablero,Agente2,Agente1)

        resultados = pd.DataFrame(self.dictionary)
        if self.guardarResultados:
            resultados.to_csv("./resultados_simulacion.csv")
        print(resultados[["Jugador 1","Victorias 1","Jugador 2","Victorias 2","N.º Partidas","Tamaño del Tablero", "Tiempo total", "Tiempo medio por partida","Tiempo medio para mover 1","Tiempo medio para mover 2"]])
        print("---------------------Resumen de las simulaciones---------------------\n")
        for index in resultados.index:
            row = resultados.iloc[index]
            print(f"---------------------Simulación {index+1}---------------------")
            print("\tTamaño del tablero: "+str(row["Tamaño del Tablero"])+" ("+str(row["Tamaño del Tablero"])+"x"+str(row["Tamaño del Tablero"])+"x"+str(row["Tamaño del Tablero"])+")" )
            print("\tNº de partidas simuladas: "+str(row["N.º Partidas"]))
            print("\t"+row["Jugador 1"]+" VS "+row["Jugador 2"]+" --> "+row["Jugador 1"]+str(row["Victorias 1"])+" "+row["Jugador 2"]+str(row["Victorias 2"]))
            print("\tTiempo total de la simulación: "+str(round(row["Tiempo total"],6))+ " segundos")
            print("\tTiempo medio de una partida: "+str(round(row["Tiempo medio por partida"],6))+ " segundos")
            print("\t---------------------"+row["Jugador 1"]+"---------------------")
            print("\tTiempo medio para mover: "+str(round(row["Tiempo medio para mover 1"],6))+ " segundos")
            if row["Profundidad 1"]>0:
                print("\tProfundidad de búsqueda: "+str(row["Profundidad 1"]))
                print("\tRamificación máxima: "+str(row["Ramificación máxima 1"]))
            print("\t---------------------"+row["Jugador 2"]+"---------------------")
            print("\tTiempo medio para mover: "+str(round(row["Tiempo medio para mover 2"],6))+ " segundos")
            if row["Profundidad 2"]>0:
                print("\tProfundidad de búsqueda: "+str(row["Profundidad 2"]))
                print("\tRamificación máxima: "+str(row["Ramificación máxima 2"]))
            print("\n")

    # Prepara los argumentos de los agentes especificados con los parametros indicados.
    def PrepararAgente(self,Agente: Agente,tablero: Tablero_3Dimensiones, profundidad):
        if Agente is AgenteAleatorio:
            Agente = Agente(tablero,tablero.seed)
        elif Agente is AgenteAlfaBeta:
            Agente = Agente(tablero,profundidad)
        else:
            Agente = Agente(tablero)
        return Agente

    # Se encarga de simular varias partidas entre los agentes especificados en un tablero dado.
    def SimularNPartidas(self,n,tablero: Tablero_3Dimensiones, Agente1: Agente, Agente2: Agente):
        A1_max_moves,A2_max_moves=0,0
        A1_min_moves,A2_min_moves = tablero.size**3,tablero.size**3
        A1_movetime_avg,A2_movetime_avg = 0,0
        A1_win, A2_win = 0,0
        gametime_avg = 0
        for i in range(n):
            print(f"Simulando: {i+1}/{n}", end = "\r")
            tstart = time.time()
            A1_moves, A2_moves = 0,0
            A1_movetime, A2_movetime = 0,0
            while not tablero.finPartida():
                ta = time.time()
                Agente1.realizarMovimiento()
                A1_movetime += time.time()-ta
                A1_moves+=1
                if tablero.finPartida():
                    A1_win+=1
                    # print("Gana agente "+Agente1.nombre())
                    break
                ta = time.time()
                Agente2.realizarMovimiento()
                A2_movetime += time.time()-ta
                A2_moves+=1
                if tablero.finPartida():
                    A2_win+=1
                    # print("Gana agente "+Agente2.nombre())
                    break
            tablero.restaurarTablero()

            gametime = time.time()-tstart
            gametime_avg += gametime

            A1_movetime = A1_movetime/A1_moves
            A2_movetime = A2_movetime/A2_moves

            A1_movetime_avg += A1_movetime
            A2_movetime_avg += A2_movetime

            if A1_max_moves<A1_moves:
                A1_max_moves=A1_moves

            if A2_max_moves<A2_moves:
                A2_max_moves=A2_moves
                
            if A1_min_moves>A1_moves:
                A1_min_moves=A1_moves

            if A2_min_moves>A1_moves:
                A2_min_moves=A1_moves

        A1_movetime_avg /= n
        A2_movetime_avg /= n

        self.dictionary["Tiempo total"].append(gametime_avg)
        
        A1_per = str(A1_win/n*100)+"%"
        A2_per = str(A2_win/n*100)+"%"

        self.dictionary["Jugador 1"].append(Agente1.nombre())
        self.dictionary["Jugador 2"].append(Agente2.nombre())
        self.dictionary["N.º Partidas"].append(n)
        self.dictionary["Tamaño del Tablero"].append(tablero.size)
        self.dictionary["Tiempo medio por partida"].append(gametime_avg/n)
        self.dictionary["Victorias 1"].append((A1_win,A1_per))
        self.dictionary["Victorias 2"].append((A2_win,A2_per))
        if type(Agente1) is AgenteAlfaBeta:
            self.dictionary["Profundidad 1"].append(Agente1.profundidad)
            self.dictionary["Ramificación máxima 1"].append(Agente1.ramifiacionmax)
        else:
            self.dictionary["Profundidad 1"].append(0)
            self.dictionary["Ramificación máxima 1"].append(0)
        if type(Agente2) is AgenteAlfaBeta:
            self.dictionary["Profundidad 2"].append(Agente2.profundidad)
            self.dictionary["Ramificación máxima 2"].append(Agente2.ramifiacionmax)
        else:
            self.dictionary["Profundidad 2"].append(0)
            self.dictionary["Ramificación máxima 2"].append(0)
        self.dictionary["Tiempo medio para mover 1"].append(A1_movetime_avg)
        self.dictionary["Tiempo medio para mover 2"].append(A2_movetime_avg)
        print("\n")

lista_agentes = [AgenteAleatorio,AgenteAlfaBeta] # Lista de agentes disponibles
tableros = [Tablero_3Dimensiones(2,1,None),Tablero_3Dimensiones(3,1,None)]# Lista de tableros que queremos probar
profundidad = 2
semilla = 10
num_simulaciones = 200
# Argumentos: semilla, nº simulaciones, lista tableros, lista agentes, guardar resultados
AgenteVSAgente(semilla, num_simulaciones, tableros, profundidad, lista_agentes, True)