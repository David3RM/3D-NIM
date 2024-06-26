from Tablero import Tablero_3Dimensiones
import random
from abc import ABC, abstractmethod
import numpy as np
import copy
import time
import itertools

# Clase abstracta para que todos los agentes tengan que implementar los métodos básicos
class Agente(ABC):
    @abstractmethod
    def __init__(self, tablero):
        self.tablero = tablero

    @abstractmethod
    def nombre(self):
        return "Agente vacío"

    @abstractmethod
    def realizarMovimiento(self):
        return []


class AgenteAleatorio(Agente):

    # Es necesario poner una semilla al agente aleatorio para que se puedan reproducir sus movimientos.
    def __init__(self, tablero: Tablero_3Dimensiones, seed):
        self.tablero = tablero
        self.randomstate = random.Random(seed)

    def nombre(self):
        return "Agente Aleatorio"

    def realizarMovimiento(self):
        coord_aleatoria = [self.randomstate.randint(0,self.tablero.size-1),self.randomstate.randint(0,self.tablero.size-1),self.randomstate.randint(0,self.tablero.size-1)]
        # Impedimos que eliga una coordenada que no tiene pieza
        while not self.tablero.coordenadaEsValida(coord_aleatoria):
            coord_aleatoria = [self.randomstate.randint(0,self.tablero.size-1),self.randomstate.randint(0,self.tablero.size-1),self.randomstate.randint(0,self.tablero.size-1)]
        coords_a_elegir = self.tablero.coordenadasAccesibles(coord_aleatoria)
        # No comprobamos si la coordenada_2, elegida aleatoriamente, tiene pieza o cumple las condiciones, ya que las coordenadas devueltas en "coords_a_elegir" tienen piezas y son validas
        coord_elegida = coords_a_elegir[self.randomstate.randint(0,len(coords_a_elegir)-1)]
        coords_eliminadas = self.tablero.tomarPiezas(coord_aleatoria,coord_elegida)
        return coords_eliminadas
    
class AgenteBasadoEnReglas(Agente):

    def __init__(self, tablero: Tablero_3Dimensiones, seed):
        self.tablero = tablero
        self.randomstate = random.Random(seed)

    def nombre(self):
        return "Agente Basado en Reglas"
    
    def realizarMovimiento(self):
        # Vamos a elegir si comprobamos la filasX, filasY o columnas,
        comprobando = None
        eje = None
        # Elegimos el eje que menos filas completas tenga.
        if len(self.tablero.filasX) < len(self.tablero.filasY) and len(self.tablero.filasX) < len(self.tablero.columnas):
            comprobando = self.tablero.filasX
            eje = "X"
        elif len(self.tablero.filasY) < len(self.tablero.filasX) and len(self.tablero.filasY) < len(self.tablero.columnas):
            comprobando = self.tablero.filasY
            eje = "Y"
        elif len(self.tablero.columnas) < len(self.tablero.filasX) and len(self.tablero.columnas) < len(self.tablero.filasY):
            comprobando = self.tablero.columnas
            eje = "Z"
        else:
            # Elegimos un eje aleatorio, ya que todos tienen el mismo número de filas.
            probability = self.randomstate.random()
            probability_division = 1/3
            if probability<=probability_division:
                comprobando = self.tablero.filasX
                eje = "X"
            elif probability>probability_division and probability<=probability_division*2:
                comprobando = self.tablero.filasY
                eje = "Y"
            else:
                comprobando = self.tablero.columnas
                eje = "Z"
        # Una vez elegido lo que vamos a comprobar realizamos las reglas. Se comprobaran filas o columnas segun lo que se haya elegido.
        # Si hay un número impar de filas/columnas, borramos una entera para dejar un número par priorizando la que este pegada a las otras columnas
        if len(comprobando)%2==1:
            columna_fila = comprobando[0]
            coord1,coord2 = columna_fila[0],columna_fila[len(columna_fila)-1]
            i=1
            while not self.tablero.coordenadaEsValida(coord1): 
                columna_fila = comprobando[i]
                coord1,coord2 = columna_fila[0],columna_fila[len(columna_fila)-1]
                i+=1
        # Si hay solo dos filas/columnas, intentaremos, con nuestro movimiento, dejar un número par de movimientos para ser capaces de ganar.
        elif len(comprobando)==2:
            columna_fila1, columna_fila2 = comprobando[0],comprobando[1]
            # Si una de las filas/columnas es más grande que la otra, intentaremos que se conviertan en dos filasX iguales.
            if len(columna_fila1)>len(columna_fila2):
                x1,y1,z1 = columna_fila1[len(columna_fila1)-len(columna_fila2)]
                x2,y2,z2 = columna_fila2[0]
                # Eliminamos al sentido contrario para impedir que dos columnas que estan juntas sigan unidas una vez que eliminamos sus piezas para asegurar que dejamos un movimiento par
                if eje=="X" and x1==x2 and z1==z2 or eje=="Y" and y1==y2 and z1==z2 or eje=="Z" and z1==z2 and x1==x2:
                    coord1,coord2 = columna_fila1[len(columna_fila1)-len(columna_fila2)-1],columna_fila1[len(columna_fila1)-1]
                else:
                    coord1,coord2 = columna_fila1[0],columna_fila1[len(columna_fila1)-len(columna_fila2)-1]
            elif len(columna_fila1)<len(columna_fila2):
                x1,y1,z1 = columna_fila2[len(columna_fila2)-len(columna_fila1)]
                x2,y2,z2 = columna_fila1[0]
                if eje=="X" and x1==x2 and z1==z2 or eje=="Y" and y1==y2 and z1==z2 or eje=="Z" and z1==z2 and x1==x2:
                    coord1,coord2 = columna_fila2[len(columna_fila2)-len(columna_fila1)-1],columna_fila2[len(columna_fila2)-1]
                else:
                    coord1,coord2 = columna_fila2[0],columna_fila2[len(columna_fila2)-len(columna_fila1)-1]
            # Si son iguales en tamaño, parte una de ellas en dos trozos de tamaño uno o si es posible parte ambas al mismo tiempo.
            else:
                corte1 = np.clip(1,0,len(columna_fila1)-1)
                corte2 = np.clip(len(columna_fila1)-2,0,len(columna_fila1)-1)
                if corte1>corte2:
                    corte1,corte2 = 0,0
                coord1,coord2 = columna_fila1[corte1],columna_fila1[corte2]
                coord3,coord4 = columna_fila2[corte1],columna_fila2[corte2]
                if len(columna_fila1)>2:
                    if self.tablero.movimientoValido(coord1,coord3):
                        coord1, coord2 = coord1, coord3
                    elif self.tablero.movimientoValido(coord2,coord4):
                        coord1, coord2 = coord2, coord4
        # Si el número par es mayor que dos, entonces convertimos la fila/columna más grande en una fila/columna de un elemento
        else:
            columna_fila = comprobando[0]
            #centro = round(len(columna_fila)/2)-1
            coord1, coord2 = columna_fila[0],columna_fila[max(len(columna_fila)-2,0)]
            i=1
            while not self.tablero.coordenadaEsValida(coord1): 
                columna_fila = comprobando[i]
                #centro = round(len(columna_fila)/2)-1
                coord1, coord2 = columna_fila[0],columna_fila[max(len(columna_fila)-2,0)]
                i+=1
        coords_eliminadas = self.tablero.tomarPiezas(coord1,coord2)
        return coords_eliminadas
    
class AgenteAlfaBeta(Agente):

    def __init__(self, tablero: Tablero_3Dimensiones, semilla, p):
        self.tablero = tablero
        self.profundidad = p
        self.arbol = None
        self.randomstate = random.Random(semilla)
        self.ramificacionmax = 0

    def nombre(self):
        return "Agente Alfa-Beta"
    
    def realizarMovimiento(self):
        turnoAgente = self.tablero.turno
        self.arbol = ArbolAlfaBeta(self.tablero,self.profundidad,turnoAgente,self.randomstate)
        self.arbol.generarHijos()
        mejor_accion = None
        mejor_valor = -float("inf")
        # La raíz del arbol siempre tendra la mayor cantidad de hijos, asi que siempre sera el que realice la ramificación máxima.
        self.ramificacionmax = max(self.ramificacionmax,self.arbol.ramificacionmax)
        for hijo in self.arbol.hijos:
            if mejor_valor<hijo.valor:
                mejor_valor = hijo.valor
                mejor_accion = hijo.accion
        if mejor_accion==None:
            mejor_accion = self.arbol.hijos[0].accion
        coords_eliminadas = self.tablero.tomarPiezas(mejor_accion[0],mejor_accion[1])
        return coords_eliminadas

# Clase que utilizaremos para representar un árbol
class ArbolAlfaBeta():

    def __init__(self, tablero: Tablero_3Dimensiones, p, turnoAgente,randomstate):
        self.estado = tablero
        self.turnoAgente = turnoAgente
        self.randomstate = randomstate
        self.accion = None
        self.pasos = p
        self.hijos = []
        self.ramificacionmax = 0
        self.estadosgenerados = 1
        # Set que utilizaremos para comprobar rápidamente si un estado equivalente ya ha sido comprobado.
        self.estados_repetidos=set()
        if self.turnoAgente==self.estado.turno:
            self.valor = float("inf")
        else:
            self.valor = -float("inf")
        self.alfabeta = [-float("inf"),float("inf")]
    
    # Evalua el estado del arbol actual.
    def funcionEvaluacion(self):
        movimientosMax=0
        if len(self.estado.filasX)<=len(self.estado.filasY) and len(self.estado.filasX)<=len(self.estado.columnas):
            movimientosMin = len(self.estado.filasX)
            for element in self.estado.filasX:
                movimientosMax = max(movimientosMax,len(element))
        elif len(self.estado.filasY)<=len(self.estado.filasX) and len(self.estado.filasY)<=len(self.estado.columnas):
            movimientosMin = len(self.estado.filasY)
            for element in self.estado.filasX:
                movimientosMax = max(movimientosMax,len(element))
        else:
            movimientosMin = len(self.estado.columnas)
            for element in self.estado.filasX:
                movimientosMax = max(movimientosMax,len(element))
        valormax = 1000/np.sum(self.estado.piezas)
        if movimientosMin%2==0 and movimientosMax<=2 and np.sum(self.estado.piezas)%2==0:
            valor = valormax
        else:
            valor = -valormax
        return valor 
    
    # Comprueba si el nuevo hijo es un estado equivalente a otro ya explorado anteriormente, ya que no aporta nueva información.
    def repetido(self, arbol):
        repetido = False
        lista = (len(arbol.estado.filasX),len(arbol.estado.filasY), len(arbol.estado.columnas))
        for permutacion in set(itertools.permutations(lista)):
            if permutacion in self.estados_repetidos and np.sum(self.estado.piezas)==np.sum(self.estado.piezas):
                repetido=True
            else:
                self.estados_repetidos.add(permutacion)
        return repetido
    
    def ordenacionMovimientos(self, coord1, coord2):
        diferenciacoords = [coord1[0]-coord2[0],coord1[1]-coord2[1],coord1[2]-coord2[2]]
        piezas_a_elimnar = 1+abs(sum(diferenciacoords))
        # Añadimos aleatoriedad para permitir que movimientos que eliminan el mismo número de piezas sean seleccionados y no siempre se realice la misma ordenación.
        # Devolvemos el numero de piezas que eliman dicho movimiento
        return piezas_a_elimnar+self.randomstate.random()*0.5

    def generarHijos(self):
        if not self.estado.finPartida() and self.pasos>0:
            for i in range(self.estado.size):
                for j in range(self.estado.size):
                    for k in range(self.estado.size):
                        if self.estado.coordenadaEsValida([i,j,k]):
                            # Se barajea los movimientos de forma aleatoria para permitir a alfa beta realizar diferentes movimientos que considera equivalentes.
                            # Incluso ayudandonos a conseguir la reducción de complejidad más fácilmente.
                            movimientos = self.estado.coordenadasAccesibles([i,j,k])
                            # Lo ordenamos de forma que los primeros movimientos sean los que más piezas eliminan, ya que permiten a alfa conseguir valores superiores rapidamente permitiendo realizar la poda antes.
                            movimientos.sort(key=lambda movimiento: self.ordenacionMovimientos([i,j,k],movimiento),reverse=True)
                            for coord in movimientos:
                                nuevo_tablero = copy.deepcopy(self.estado)
                                nuevo_hijo = ArbolAlfaBeta(nuevo_tablero,self.pasos-1,self.turnoAgente,self.randomstate)
                                nuevo_hijo.alfabeta=self.alfabeta
                                nuevo_hijo.estado.tomarPiezas([i,j,k],coord)
                                nuevo_hijo.accion = ([i,j,k],coord)
                                if not self.repetido(nuevo_hijo):
                                    self.hijos.append(nuevo_hijo)
                                    nuevo_hijo.generarHijos()
                                    self.ramificacionmax=max(len(self.hijos),nuevo_hijo.ramificacionmax)
                                    self.estadosgenerados += nuevo_hijo.estadosgenerados
                                    if self.estado.turno==self.turnoAgente:
                                        self.valor = max(self.valor, nuevo_hijo.valor)
                                        self.alfabeta[0] = max(self.alfabeta[0], self.valor)
                                        if self.alfabeta[0]>=self.alfabeta[1]:
                                            break
                                    else:
                                        self.valor = min(self.valor, nuevo_hijo.valor)
                                        self.alfabeta[1] = min(self.alfabeta[1], self.valor)
                                        if self.alfabeta[0]>=self.alfabeta[1]:
                                            break
            #El set ya ha sido utilizado completamente, no es necesario tenerlo en memoria
            self.estados_repetidos=None

        # Damos valor al nodo, ya que es un nodo hoja.
        elif self.estado.finPartida():
            valor = float("inf")
            # Si mi movimiento dejo el tablero vacío damos un valor positivo
            if self.estado.turno!=self.turnoAgente:
                self.valor = valor
            else:
                self.valor = -valor
        # Estimamos el valor del estado, ya que no es un nodo hoja, pero se ha alcanzado la profundidad máxima.
        else:
            # Si mi movimiento dejo el tablero en una posición desfavorable para el adversario, la valoración de la función es positiva
            if self.estado.turno!=self.turnoAgente:
                self.valor = self.funcionEvaluacion()
            else:
                self.valor = -self.funcionEvaluacion()

# Prueba para comprobar cuantos estados hay en el espacio de busqueda completo en un tablero 2x2x2
# Antes de ejecutarlo hay que eliminar la poda y la comprobación de estados equivalentes.
# tablero = Tablero_3Dimensiones(2,1,None)
# arbol = ArbolAlfaBeta(tablero,float("inf"),0,random.Random())
# arbol.generarHijos()
# print(arbol.estadosgenerados)