import numpy as np
import random
import time

class Tablero_3Dimensiones():

    def __init__(self, m, p, seed):
        self.turno = 0 # Turno 0 corresponde al jugador 1 y el turno 1 al jugador 2.
        self.size = m # Tamaño del tablero
        self.seed = seed # semilla para el random
        self.p = p # Porcentaje de piezas
        self.dict_coords = dict()
        # Construimos el tablero/cubo con todas las piezas o con solo un porcentaje de ellas.
        if self.seed: random.seed(self.seed)
        if self.p<1:
            self.piezas = np.zeros((self.size,self.size,self.size))
            for i in range(self.size):
                for j in range(self.size):
                    for k in range(self.size):
                        if random.random()<=self.p:
                            self.piezas[i,j,k] = 1
        else:
            self.piezas = np.ones((self.size,self.size,self.size))
        self.filasX,self.filasY,self.columnas = self.columnas_filas_Minimas()
        
    # Funcion que permite restablecer el cubo a su estado original para volver a comenzar una partida
    # Necesaria para poder repetir la misma partida varias veces.
    def restaurarTablero(self):
        self.turno = 0
        self.dict_coords = dict()
        if self.seed: random.seed(self.seed)
        if self.p<1:
            self.piezas = np.zeros((self.size,self.size,self.size))
            for i in range(self.size):
                for j in range(self.size):
                    for k in range(self.size):
                        if random.random()<=self.p:
                            self.piezas[i,j,k] = 1
        else:
            self.piezas = np.ones((self.size,self.size,self.size))
        self.filasX,self.filasY,self.columnas = self.columnas_filas_Minimas()

    # Devolvera el número minimo columnas, filasX y filasY del cubo.
    # Esta funcion se realizara solo una vez al construir el cubo y se ira actualizando las columnas, filasX y filasY a las que pertenecia la coordenada eliminada en la función tomarPiezas
    def columnas_filas_Minimas(self):
        columnas,filasX,filasY = [],[],[]
        columna,filaX,filaY = [],[],[]
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    if self.piezas[i,j,k]==1:
                        columna.append([i,j,k])
                    else: # Si la columna esta partida en dos o más cachos que hay que considerar columnas independientes
                        if len(columna)>0:
                            # Para que la primera columna de la lista de columnas sea la más larga
                            columnas.append(columna)
                            for coord in columna:
                                # Utilizamos un diccionario con las coordenadas, para ser capaz de encontrar la columna, filaX y filaY a la que pertenece la coordenada, rápidamente.
                                i,j,k = coord
                                str_coord = str(i)+","+str(j)+","+str(k)
                                if str_coord in self.dict_coords.keys():
                                    self.dict_coords[str_coord]["columna"] = columna
                                else:
                                    self.dict_coords[str_coord] = {"columna": columna}
                            columna = []
                        
                    if self.piezas[k,j,i]==1:
                        filaX.append([k,j,i])
                    else: # Si la filaX esta partida en dos o más cachos que hay que considerar filasX independientes
                        if len(filaX)>0:
                            # Para que la primera columna de la lista de filasX sea la más larga
                            filasX.append(filaX)
                            for coord in filaX:
                                # Utilizamos un diccionario con las coordenadas, para ser capaz de encontrar la columna, filaX y filaY a la que pertenece la coordenada, rápidamente.
                                i,j,k = coord
                                str_coord = str(i)+","+str(j)+","+str(k)
                                if str_coord in self.dict_coords.keys():
                                    self.dict_coords[str_coord]["filaX"] = filaX
                                else:
                                    self.dict_coords[str_coord] = {"filaX": filaX}
                            filaX = []
                        
                    if self.piezas[i,k,j]==1:
                        filaY.append([i,k,j])
                    else: # Si la filaY esta partida en dos o más cachos que hay que considerar filasY independientes
                        if len(filaY)>0:
                            # Para que la primera columna de la lista de filasY sea la más larga
                            filasY.append(filaY)
                            for coord in filaY:
                                # Utilizamos un diccionario con las coordenadas, para ser capaz de encontrar la columna, filaX y filaY a la que pertenece la coordenada, rápidamente.
                                i,j,k = coord
                                str_coord = str(i)+","+str(j)+","+str(k)
                                if str_coord in self.dict_coords.keys():
                                    self.dict_coords[str_coord]["filaY"] = filaY
                                else:
                                    self.dict_coords[str_coord] = {"filaY": filaY}
                            filaY = []

                # Para asegurarnos que cogemos la columna, filaX y filaY, si esta no estaba partida en trozos.

                if len(columna)>0:
                    # Para que la primera columna de la lista de columnas sea la más larga
                    columnas.append(columna)
                    for coord in columna:
                        # Utilizamos un diccionario con las coordenadas, para ser capaz de encontrar la columna, filaX y filaY a la que pertenece la coordenada, rápidamente.
                        i,j,k = coord
                        str_coord = str(i)+","+str(j)+","+str(k)
                        if str_coord in self.dict_coords.keys():
                            self.dict_coords[str_coord]["columna"] = columna
                        else:
                            self.dict_coords[str_coord] = {"columna": columna}

                if len(filaX)>0:
                    # Para que la primera columna de la lista de filasX sea la más larga
                    filasX.append(filaX)
                    for coord in filaX:
                        # Utilizamos un diccionario con las coordenadas, para ser capaz de encontrar la columna, filaX y filaY a la que pertenece la coordenada, rápidamente.
                        i,j,k = coord
                        str_coord = str(i)+","+str(j)+","+str(k)
                        if str_coord in self.dict_coords.keys():
                            self.dict_coords[str_coord]["filaX"] = filaX
                        else:
                            self.dict_coords[str_coord] = {"filaX": filaX}

                if len(filaY)>0:
                    # Para que la primera columna de la lista de filasY sea la más larga
                    filasY.append(filaY)
                    for coord in filaY:
                        # Utilizamos un diccionario con las coordenadas, para ser capaz de encontrar la columna, filaX y filaY a la que pertenece la coordenada, rápidamente.
                        i,j,k = coord
                        str_coord = str(i)+","+str(j)+","+str(k)
                        if str_coord in self.dict_coords.keys():
                            self.dict_coords[str_coord]["filaY"] = filaY
                        else:
                            self.dict_coords[str_coord] = {"filaY": filaY}

                columna,filaX,filaY = [],[],[]

        filasX.sort(reverse=True, key = self.priorizarfilaX)
        filasY.sort(reverse=True, key = self.priorizarfilaY)
        columnas.sort(reverse=True, key = self.priorizarcolumna)

        return filasX, filasY, columnas
    

    #Funciones para permitir ordenar la lista para que la primera fila/columna sea la que tenga más piezas pegadas a otras filas/columnas.
    def priorizarfilaX(self,filaX):
        compartidas = 0
        for coord in filaX:
            i,j,k = coord
            if j-1>0:
                compartidas+=self.piezas[i,j-1,k]
            if j+1<self.size:
                compartidas+=self.piezas[i,j+1,k]
            if k-1>0:
                compartidas+=self.piezas[i,j,k-1]
            if k+1<self.size:
                compartidas+=self.piezas[i,j,k+1]
        return (compartidas,len(filaX))

    def priorizarfilaY(self,filaY):
        compartidas = 0
        for coord in filaY:
            i,j,k = coord
            if i-1>0:
                compartidas+=self.piezas[i-1,j,k]
            if i+1<self.size:
                compartidas+=self.piezas[i+1,j,k]
            if k-1>0:
                compartidas+=self.piezas[i,j,k-1]
            if k+1<self.size:
                compartidas+=self.piezas[i,j,k+1]
        return (compartidas,len(filaY))

    def priorizarcolumna(self,columna):
        compartidas = 0
        for coord in columna:
            i,j,k = coord
            if i-1>0:
                compartidas+=self.piezas[i-1,j,k]
            if i+1<self.size:
                compartidas+=self.piezas[i+1,j,k]
            if j-1>0:
                compartidas+=self.piezas[i,j-1,k]
            if j+1<self.size:
                compartidas+=self.piezas[i,j+1,k]
        return (compartidas,len(columna))
        

    #Cambia el turno, es decir, el jugador que esta cogiendo piezas en el momento.
    def cambiarTurno(self):
        if not self.finPartida():
            if self.turno==0:
                self.turno=1
            else:
                self.turno=0

    # Devuelve las coordenas que se han eliminado con el movimiento.
    def tomarPiezas(self,coord1,coord2):
        x,y,z = coord1
        coords_eliminadas = []
        if coord1==coord2 and self.coordenadaEsValida(coord1):
            coords_eliminadas.append([x,y,z])
            self.piezas[x,y,z] = 0
        elif self.movimientoValido(coord1,coord2):
            coords_piezas_eliminar = self.coordenadasEntre(coord1,coord2)
            for coord in coords_piezas_eliminar:
                x,y,z = coord
                if self.piezas[x,y,z]==1:
                    coords_eliminadas.append([x,y,z])
                    self.piezas[x,y,z] = 0
                else:
                    #Si hay algún hueco vacío entre los dos elementos elegidos, se para de eliminar piezas.
                    break
        else:
            # Solo se dispara si uno de los jugadores ha intentado realizar un movimiento imposible de realizar.
            raise Exception("Movimiento no válido")
        self.cambiarTurno()
        # Actualizamos solo las columnas, filasX y filasY a la que pertenecia la coordenada eliminada
        # Todo este código permite al agente basado en reglas trabajar mucho más rápido, al ahorarse recalcular todo de nuevo cada vez que quiere realizar un movimiento 
        for coord in coords_eliminadas:
            x,y,z = coord
            str_coord = str(x)+","+str(y)+","+str(z)
            # Buscamos en el diccionario de coordenadas, la columna, filaX y filaY a la que pertenece la coordenada eliminada, para poder actualizarla.
            # También se actualizaran las otras coordenadas que formaban parte de la columna, filaX y filaY a la que pertenecia la coordenada eliminada.
            columna_e, filaX_e, filaY_e = self.dict_coords[str_coord]["columna"], self.dict_coords[str_coord]["filaX"], self.dict_coords[str_coord]["filaY"]
            if columna_e:
                i = columna_e.index(coord)
                if len(columna_e)==1:
                    self.columnas.remove(columna_e)
                elif i == 0 or i==len(columna_e)-1:
                    columna_e.pop(i)
                else:
                    self.columnas.remove(columna_e)
                    new_col1 = columna_e[0:columna_e.index(coord)]
                    new_col2 = columna_e[columna_e.index(coord)+1:]
                    for coord1 in new_col1:
                        if coord1 != coord:
                            x1,y1,z1 = coord1
                            str_coord1 = str(x1)+","+str(y1)+","+str(z1)
                            self.dict_coords[str_coord1]["columna"] = new_col1
                    for coord1 in new_col2:
                        if coord1 != coord:
                            x1,y1,z1 = coord1
                            str_coord1 = str(x1)+","+str(y1)+","+str(z1)
                            self.dict_coords[str_coord1]["columna"] = new_col2
                    self.columnas.append(new_col1)
                    self.columnas.append(new_col2)
                del self.dict_coords[str_coord]["columna"]
                self.columnas.sort(reverse=True, key=self.priorizarcolumna)
            if filaX_e:
                i = filaX_e.index(coord)
                if len(filaX_e)==1:
                    self.filasX.remove(filaX_e)
                elif i == 0 or i==len(filaX_e)-1:
                    filaX_e.pop(i)
                else:
                    self.filasX.remove(filaX_e)
                    new_filaX1 = filaX_e[0:filaX_e.index(coord)]
                    new_filaX2 = filaX_e[filaX_e.index(coord)+1:]
                    for coord1 in new_filaX1:
                        if coord1 != coord:
                            x1,y1,z1 = coord1
                            str_coord1 = str(x1)+","+str(y1)+","+str(z1)
                            self.dict_coords[str_coord1]["filaX"] = new_filaX1
                    for coord1 in new_filaX2:
                        if coord1 != coord:
                            x1,y1,z1 = coord1
                            str_coord1 = str(x1)+","+str(y1)+","+str(z1)
                            self.dict_coords[str_coord1]["filaX"] = new_filaX2
                    self.filasX.append(new_filaX1)
                    self.filasX.append(new_filaX2)
                del self.dict_coords[str_coord]["filaX"]
                self.filasX.sort(reverse=True, key=self.priorizarfilaX)
            if filaY_e:
                i = filaY_e.index(coord)
                if len(filaY_e)==1:
                    self.filasY.remove(filaY_e)
                elif i == 0 or i==len(filaY_e)-1:
                    filaY_e.pop(i)
                else:
                    self.filasY.remove(filaY_e)
                    new_filaY1 = filaY_e[0:filaY_e.index(coord)]
                    new_filaY2 = filaY_e[filaY_e.index(coord)+1:]
                    for coord1 in new_filaY1:
                        if coord1 != coord:
                            x1,y1,z1 = coord1
                            str_coord1 = str(x1)+","+str(y1)+","+str(z1)
                            self.dict_coords[str_coord1]["filaY"] = new_filaY1
                    for coord1 in new_filaY2:
                        if coord1 != coord:
                            x1,y1,z1 = coord1
                            str_coord1 = str(x1)+","+str(y1)+","+str(z1)
                            self.dict_coords[str_coord1]["filaY"] = new_filaY2
                    self.filasY.append(new_filaY1)
                    self.filasY.append(new_filaY2)
                del self.dict_coords[str_coord]["filaY"]
                self.filasY.sort(reverse=True, key=self.priorizarfilaY)
        return coords_eliminadas

    # Indica si la partida ha finalizado (se ha cogido la última pieza del tablero).
    def finPartida(self):
        return np.sum(self.piezas)==0

    # Comprobamos que las dos coordenadas elegidas no rompen las restricciones del juego (No permite diagonales).
    def movimientoValido(self,coord1,coord2):
        x1,y1,z1 = coord1
        x2,y2,z2 = coord2
        # Comprobamos si las piezas elegidas estan en la misma fila o en la misma columna, impidiendo que escojan diagonales.
        # También comprobamos si en las coordenadas elegidas hay piezas, es decir, las coordenadas no estan vacías.
        return (x1==x2)+(y1==y2)+(z1==z2) == 2 and self.coordenadaEsValida(coord1) and self.coordenadaTienePieza(coord2)
    
    def coordenadaEsValida(self,coord):
        visible = self.coordenadaEsVisible(coord)
        return self.coordenadaTienePieza(coord) and np.sum(visible)>0
        
    def coordenadaTienePieza(self,coord):
        x,y,z = coord
        return self.piezas[x,y,z]==1
    
    # Indicamos si la coordenada elegida es visible y en que direcciones.
    def coordenadaEsVisible(self,coord):
        visibleX1, visibleX2 = True, True
        visibleY1, visibleY2 = True, True
        visibleZ1, visibleZ2 = True, True
        x,y,z = coord
        for i in range(x+1,self.size):
            if self.piezas[i,y,z]==1:
                visibleX1 = False
                break
        # Recorremos el eje X hacia la izquierda para ver si hay alguna coordenada bloqueando la visibilidad.
        for i in reversed(range(0,x)):
            if self.piezas[i,y,z]==1:
                visibleX2 = False
                break
        # Recorremos el eje Y hacia la derecha para ver si hay alguna coordenada bloqueando la visibilidad.
        for i in range(y+1,self.size):
            if self.piezas[x,i,z]==1:
                visibleY1 = False
                break
        # Recorremos el eje Y hacia la derecha para ver si hay alguna coordenada bloqueando la visibilidad.
        for i in reversed(range(0,y)):
            if self.piezas[x,i,z]==1:
                visibleY2 = False
                break
        # Recorremos el eje Z hacia la derecha para ver si hay alguna coordenada bloqueando la visibilidad.
        for i in range(z+1,self.size):
            if self.piezas[x,y,i]==1:
                visibleZ1 = False
                break
        # Recorremos el eje Z hacia la derecha para ver si hay alguna coordenada bloqueando la visibilidad.
        for i in reversed(range(0,z)):
            if self.piezas[x,y,i]==1:
                visibleZ2 = False
                break
        return [visibleX1 or visibleX2, visibleY1 or visibleY2, visibleZ1 or visibleZ2]
        
    # Devuelve todas las otras coordenadas que puede elegir, sin romper restricciones, al elegir una coordenada.
    def coordenadasAccesibles(self, coord):
        visibleX,visibleY,visibleZ = self.coordenadaEsVisible(coord)
        coord_validas = [coord]
        x,y,z = coord
        # Recorremos el eje X hacia la derecha para encontrar todas las coordenadas válidas.
        for i in range(x+1,self.size):
            coord_visible = self.coordenadaEsVisible([i,y,z])
            if self.piezas[i,y,z]==1 and (visibleX or coord_visible[1] or coord_visible[2]):
                coord_validas.append([i,y,z])
            else:
                break
        # Recorremos el eje X hacia la izquierda para encontrar todas las coordenadas válidas.
        for i in reversed(range(0,x)):
            coord_visible = self.coordenadaEsVisible([i,y,z])
            if self.piezas[i,y,z]==1 and (visibleX or coord_visible[1] or coord_visible[2]):
                coord_validas.append([i,y,z])
            else:
                break
        # Recorremos el eje Y hacia la derecha para encontrar todas las coordenadas válidas.
        for i in range(y+1,self.size):
            coord_visible = self.coordenadaEsVisible([x,i,z])
            if self.piezas[x,i,z]==1 and (coord_visible[0] or visibleY or coord_visible[2]):
                coord_validas.append([x,i,z])
            else:
                break
        # Recorremos el eje Y hacia la derecha para encontrar todas las coordenadas válidas.
        for i in reversed(range(0,y)):
            coord_visible = self.coordenadaEsVisible([x,i,z])
            if self.piezas[x,i,z]==1 and (coord_visible[0] or visibleY or coord_visible[2]):
                coord_validas.append([x,i,z])
            else:
                break
        # Recorremos el eje Z hacia la derecha para encontrar todas las coordenadas válidas.
        for i in range(z+1,self.size):
            coord_visible = self.coordenadaEsVisible([x,y,i])
            if self.piezas[x,y,i]==1 and (coord_visible[0] or coord_visible[1] or visibleZ):
                coord_validas.append([x,y,i])
            else:
                break
        # Recorremos el eje Z hacia la derecha para encontrar todas las coordenadas válidas.
        for i in reversed(range(0,z)):
            coord_visible = self.coordenadaEsVisible([x,y,i])
            if self.piezas[x,y,i]==1 and (coord_visible[0] or coord_visible[1] or visibleZ):
                coord_validas.append([x,y,i])
            else:
                break
        # Devolvemos las coordenadas encontradas.
        return coord_validas
        
    #Devuelve todas las coordenadas validas que se encuentran entre las dos coordenadas dadas (Incluyendo las elegidas).
    def coordenadasEntre(self,coord1,coord2):
        x1,y1,z1 = coord1
        x2,y2,z2 = coord2
        coords_piezas = []
        if x1-x2!=0:
            rango = range(x1,x2+1)
            if x1-x2>0: rango = reversed(range(x2,x1+1))# Importante invertir el orden de recorrido para empezar desde la primera posición elegida.
            for i in rango:
                coords_piezas.append([i,y1,z1])
        elif y1-y2!=0:
            rango = range(y1,y2+1)
            if y1-y2>0: rango = reversed(range(y2,y1+1))# Importante invertir el orden de recorrido para empezar desde la primera posición elegida.
            for i in rango:
                coords_piezas.append([x1,i,z1])
        else:
            rango = range(z1,z2+1)
            if z1-z2>0: rango = reversed(range(z2,z1+1))# Importante invertir el orden de recorrido para empezar desde la primera posición elegida.
            for i in rango:
                coords_piezas.append([x1,y1,i])
        return coords_piezas