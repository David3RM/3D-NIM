# Diseño de estrategias basadas en inteligencia artificial para jugar a 3D-Nim.

Para usar la interfaz gráfica, se ejecuta el fichero "InterfazGrafica.py". Si se desea cambiar el tipo de agente del adversario, hay que modificar la línea 216 y pasar el tipo de adversario deseado. Si se desea cambiar el tamaño del tablero, hay que modificar la línea 212.

Para modificar la profundidad de los agentes AlphaBeta, solo es necesario modificar los parámetros que se pasan a su constructor.

La ejecución del fichero "AgenteVSAgente.py" permite la simulación de partidas y el almacenamiento de los resultados en un fichero "resultados_simulacion.csv".

Por defecto, en el programa predefinido, el almacenamiento de los resultados en el fichero está activado. Para desactivarlo, hay que cambiar el parámetro "guardarResultados" a "False".

Los diferentes archivos .csv presentes en este repositorio contienen los resultados de los experimentos realizados en el proyecto. Sus nombres indican el tipo de agentes que se enfrentan en los resultados:
- AA = Agente Aleatorio
- ABR = Agente Basado en Reglas
- AAB = Agente Alfa-Beta
