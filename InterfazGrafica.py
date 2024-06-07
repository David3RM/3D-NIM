from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, Point3, WindowProperties
import panda3d.bullet as bullet
import numpy as np
from Tablero import Tablero_3Dimensiones
from Agentes import Agente, AgenteAleatorio, AgenteBasadoEnReglas, AgenteAlfaBeta

class Nim_3D(ShowBase):
    
    def __init__(self, turnoJugadorHumano, tablero: Tablero_3Dimensiones, adversario: Agente):
        ShowBase.__init__(self)
        self.disableMouse()
        self.tablero = tablero
        self.adversario = adversario
        self.notmoving = True
        self.turnoJugadorHumano = turnoJugadorHumano
        self.world = bullet.BulletWorld()
        self.cameraMove = False
        self.cubos_elegidos = []
        self.cubos_permitidos = []
        self.distance = self.tablero.size
        self.size = self.tablero.size
        self.cubo = self.generarCubo()
        if turnoJugadorHumano != self.tablero.turno and self.adversario is not None:
            update_coords = adversario.realizarMovimiento()
            self.actualizarCoordenadas(update_coords)
        self.setCamera()
        self.setupControls()
        self.lastMouseX = 0
        self.lastMouseY = 0
        self.taskMgr.add(self.updateCamera,'updateCamera')

        

    # Preparamos los controles para el jugador
    def setupControls(self):
        self.accept("mouse1", self.elegirCubos)
        self.accept("mouse3", self.moverCamara)
        self.accept("mouse3-up", self.noMoverCamara)
        self.accept("wheel_down",self.zoom)
        self.accept("wheel_up",self.unZoom)

    def zoom(self):
        self.distance += 0.25

    def unZoom(self):
        self.distance -= 0.25

    def moverCamara(self):
        self.cameraMove=True
        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()
        properties = WindowProperties()
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def noMoverCamara(self):
        self.cameraMove=False
        properties = WindowProperties()
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    # Colocamos la camara del jugador
    def setCamera(self):
        self.camera.setPos(self.size/2-0.5,self.size/2-0.5,self.size/2-0.5)
        self.camera.setHpr(0,0,0)
        self.camera.setPos(self.camera,0,-self.size*5,0)

    # Colocamos la camara del jugador
    def updateCamera(self, task):
        dt = self.clock.getDt()
        if self.cameraMove:
            # Estamos moviendo la camara con nuestro ratón
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 45

            currentH = self.camera.getH()
            currentP = self.camera.getP()
            self.camera.setPos(self.size/2-0.5,self.size/2-0.5,self.size/2-0.5)

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )
        
            self.camera.setPos(self.camera,0,-self.distance*5,0)

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY
        else:
            # Hemos dejado de mover nuestra camara con el ratón
            self.camera.setPos(self.size/2-0.5,self.size/2-0.5,self.size/2-0.5)
            # El jugador tiene libertad de movimiento completa, si ha elegido una pieza para realizar su movimiento.
            # Si no ha seleccionado todavía ninguna pieza para empezar a realizar su movimiento se introduce la restriccion de movimiento de la camara
            if self.notmoving:
                h,p,_ = self.camera.getHpr()
                h = round(h/90)*90
                p = round(p/90)*90
                self.camera.setHpr(h,p,0)
            self.camera.setPos(self.camera,0,-self.distance*5,0)
        
        return task.cont


        

    # Funcion que permite al jugador elegir los cubos que va a eliminar.
    def elegirCubos(self):
        pMouse = self.mouseWatcherNode.getMouse()
        pFrom = Point3()
        pTo = Point3()
        self.camLens.extrude(pMouse, pFrom, pTo)

        pFrom = self.render.getRelativePoint(self.camera, pFrom)
        pTo = self.render.getRelativePoint(self.camera, pTo)
        result = self.world.rayTestClosest(pFrom, pTo)
        node = result.getNode()
        if node:
            node_coord = node.getTransform().getPos()
            x,y,z = int(node_coord.x),int(node_coord.y),int(node_coord.z)
            if len(self.cubos_elegidos)==0:
                # Guardamos el primer cubo elegido
                self.cubos_elegidos.append([x,y,z])
                # El cubo elegido se volvera un color más oscuro para permitir al jugador recordar desde donde esta el comienzo.
                self.cubo[x,y,z][0].setColorScale(0.5, 0.5, 0.5, 1)
                # Mostramos solo los cubos que cumplen las restricciones para ser elegidos y hacemos invisibles todos los demás.
                self.notmoving = False
                self.cubos_permitidos = self.tablero.coordenadasAccesibles([x,y,z])
                self.cubos_permitidos.append([x,y,z])
                for i in range(self.size):
                    for j in range(self.size):
                        for k in range(self.size):
                            if [i,j,k] not in self.cubos_permitidos and self.tablero.piezas[i,j,k]==1:
                                # Sacamos los cubos 3D, no validos para selección, del renderizado para que no se vean.
                                self.cubo[i,j,k][0].detachNode()
                                # Eliminamos la collision de los cubos que no estan siendo renderizados.
                                self.world.remove(self.cubo[i,j,k][1])
            else:
                # El segundo cubo ha sido elegido así que cogeremos todos los cubos permitidos, que se encuentren entre estos dos.
                self.cubos_elegidos.append([x,y,z])
                update_coords = self.tablero.tomarPiezas(self.cubos_elegidos[0],self.cubos_elegidos[1])
                if self.tablero.finPartida():
                    print("-------------------------------\n---¡Ha ganado el Jugador %d!" % (self.tablero.turno+1)+"---\n-------------------------------")
                    self.finalizeExit()
                self.cubos_elegidos=[]
                self.actualizarCoordenadas(update_coords)
                for i in range(self.size):
                    for j in range(self.size):
                        for k in range(self.size):
                            if [i,j,k] not in self.cubos_permitidos and self.tablero.piezas[i,j,k]==1:
                                # Volvemos a introducir el cubo 3D en el renderizado para que vuelva a ser visible.
                                self.render.attachNewNode(self.cubo[i,j,k][1])
                                # Añadimos su colision de nuevo, para que el jugador pueda interactuar con él.
                                self.world.attach(self.cubo[i,j,k][1])
                self.cubos_permitidos=[]
                # Realizamos el movimiento del adversario, ya que nuestro turno ya lo hemos realizado
                # Actualizamos el estado gráfico del cubo.
                if not self.tablero.finPartida() and self.adversario is not None:
                    update_coords = self.adversario.realizarMovimiento()
                    if self.tablero.finPartida():
                        print("-------------------------------\n---¡Ha ganado el Adversario!---\n-------------------------------")
                        self.finalizeExit()
                    self.actualizarCoordenadas(update_coords)
                self.notmoving = True

    def actualizarCoordenadas(self,update_coords):
        for coord in update_coords:
            #Actualizamos los cubos seleccionados, para que sean eliminados del cubo.
            x,y,z = coord
            #Eliminamos la colision de los cubos seleccionados.
            self.world.remove(self.cubo[x,y,z][1])
            #Eliminamos el modelo 3D de los cubos seleccionados, para que dejen de ser renderizados.
            self.cubo[x,y,z][0].removeNode()
            self.cubo[x,y,z]=tuple()


    def generarCubo(self):
        # Creamos un nuevo array que nos permitira acceder a los elementos gráficos de panda3d.
        cubos_tablero = np.empty((self.size,self.size,self.size),dtype=tuple)
        # Cargamos el modelo de cubo
        cubo = self.loader.loadModel("modelos/cubo.gltf")
        cubo.setScale(0.5,0.5,0.5)
        shape = bullet.BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    # Comprobamos si en el tablero hay una pieza en dicha posición.
                    if self.tablero.piezas[i,j,k]==1:
                        # Creamos el objeto de colision que nos permitira detectarlo con clics.
                        # shape = bullet.BulletBoxShape(Vec3(0.5, 0.5, 0.5))
                        node_collision = bullet.BulletRigidBodyNode('Box')
                        node_collision.addShape(shape)
                        node_render = self.render.attachNewNode(node_collision)
                        node_render.setPos(i, j, k)
                        self.world.attach(node_collision)
                        cubo.instanceTo(node_render)
                        # Introducimos el objeto 3D del cubo que se renderiza en pantalla ('node_render') y el objeto que da colision al objeto 3D ('node_collision')
                        # Le asignamos una coordenada para poder trabajar con ellas más adelante.
                        cubos_tablero[i,j,k] = (node_render, node_collision)
                    else:
                        cubos_tablero[i,j,k] = tuple()
        return cubos_tablero

semilla = None
tablero = Tablero_3Dimensiones(3,1,semilla)
agentes = [AgenteAleatorio(tablero,semilla),AgenteBasadoEnReglas(tablero,semilla),AgenteAlfaBeta(tablero,semilla,2)]

# Argumentos (Turno del jugador humano, el tablero, el adversario (puede ser None) )
app = Nim_3D(0, tablero, agentes[1])
app.run()