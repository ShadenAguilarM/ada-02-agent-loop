# Preguntas Obligatorias

## ¿Qué es tool calling?
Tool Calling es la capacidad de un modelo de IA para utilizar herramientas externas para realizar acciones o acceder a información que no puede obtener únicamente generando texto. Por ejemplo, en esta actividad el agente utilizó herramientas como Read, Edit y Bash para leer archivos, modificar código y ejecutar pruebas.

## ¿Qué es una observation?
Una observación es el resultado que recibe el agente después de utilizar una herramienta. Esta información le permite conocer qué ocurrió y decidir cuál será su siguiente acción. Es decir, es la información que el agente obtiene del entorno después de una acción/tool call, y esa información alimenta la siguiente decisión del Agent Loop.

## ¿Qué es el Agent Loop? 
El Agent Loop es el ciclo mediante el cual un agente observa una situación, utiliza una herramienta para realizar una acción, recibe el resultado y decide cuál será su siguiente acción. Este proceso puede repetirse hasta alcanzar el objetivo.

## ¿Qué operaciones corresponden a read, write, edit y bash?

- **Read:** permite leer y consultar el contenido de archivos.


- **Write:** permite crear archivos nuevos o escribir contenido en ellos.


- **Edit:** permite modificar partes específicas de archivos existentes.


- **Bash:** permite ejecutar comandos en la terminal, como pytest, para interactuar con el sistema y comprobar resultados.

## ¿Dónde intervino el agente?
El agente intervino directamente en el repositorio. Inspeccionó los archivos utilizando Read, ejecutó las pruebas mediante Bash, identificó el error, modificó calculator.py mediante Edit y finalmente volvió a ejecutar las pruebas para comprobar la solución.

## ¿Dónde intervino el humano?
El humano intervino principalmente al proporcionar las instrucciones y requisitos de la tarea, por ejemplo, indicando que no se modificaran las pruebas, que se ejecutaran antes y después de realizar el cambio y que se hiciera la modificación mínima necesaria. Además, el humano intervino al aceptar algunas de las acciones propuestas por el agente para permitir su ejecución, como la ejecución de comandos y la modificación del archivo. Finalmente, el humano revisó y evaluó las acciones realizadas y los resultados obtenidos por el agente.

## ¿Qué capacidad se perdería sin ejecución de comandos?
Sin la ejecución de comandos, el agente perdería la capacidad de comprobar directamente si sus hipótesis y cambios funcionan en el entorno real. Podría analizar el código y proponer que el error está en divide(), pero no podría ejecutar pytest para confirmar que la prueba falla antes del cambio y que las cuatro pruebas pasan después.

Por lo tanto, sin ejecución de comandos el agente tendría que basarse principalmente en el análisis del código, mientras que con herramientas puede actuar, observar los resultados y verificar sus decisiones.