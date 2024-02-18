verificador = True

instrucciones = ["defvar", "=", "move", "skip", "turn", "move-dir", "runs-dir", "move-face", 
        "Dim", "myXpos", "myYpose", "myChips", "myBallons", "baloonsHere", "ChipsHere", "Spaces", "null",
        "if", "while", "repeat", "not", "facing?" "blocked?", "can-put?", "can", "not", "J", "Go", ":",
        "(", ")", "defun", 'loop']

posiciones = ["north", "south", "east", "west", "front", "back", "right", "left"]

def parser(filetxt, instruccioens):
    verificador = True
    prueba = filetxt
    prueba = prueba.replace("\n", " ").replace("\t", " ")
    
    if prueba[len(prueba)- 1] == " ":
         prueba = prueba[0:len(prueba)- 1]
         
    prueba = prueba.replace(")", " )").replace("(", "( ")
    tokens = [i.lower() for i in prueba.split(" ")]
    parentesis = (tokens.count("(") + tokens.count(")"))
        
    if parentesis % 2 != 0 or tokens.count("(") != tokens.count(")"):
        verificador = False
        
    variables = {}
    variables = anadir_variable(tokens, variables)
    
    funciones = {}
    funciones = anadir_funcion(tokens, funciones)
    
    i = 0  #iterador
    posicion = 0 #indice
    
     #Elimina el carascter vacio de la lista de tokens para poder realizar un mero estudio
    tokens = [token for token in tokens if token != ""]
    
    while posicion < len(tokens) and verificador == True:
        if i == 0:
            avance, verificador = comandos(tokens[posicion], tokens, instrucciones, posicion, variables, funciones)

            posicion += avance
        
    
    if verificador == True:
        respuesta = "Sirve :D"
    elif verificador == False:
        respuesta = "No sirve :c"
    
    return respuesta




def comandos(token: str, tokens: list, instrucciones: list, posicionAct: int, variables: dict, funciones: dict):
    verificador = True
    avance = 1

    if token == "(":
        if tokens[posicionAct + 1] == "defvar" and tokens[posicionAct + 2] in variables and \
            tokens[posicionAct + 3] in variables and tokens[posicionAct + 4] == ")":
            pass
    return avance, verificador
  
    
def anadir_variable(tokens, variables):
    for i in range(len(tokens)):
        if tokens[i] == "defvar":
            if tokens[i + 1] not in variables:
                variables[tokens[i + 1]] = 0
    return variables

def anadir_funcion(tokens, funciones):
    for i in range(len(tokens)):
        if tokens[i] == "defun":
            if tokens[i + 1] not in funciones:
                funciones[tokens[i + 1]] = 0
    return funciones
    
prueba = """
(defvar a  3)
(defvar b a)
(defvar c myXpos)
(defvar d 0)
(= d 7)

(if (facing? :north) (turn :right) (null))

(loop (not (not (not (blocked?)))) (skip a))

(repeat b (
	(face :south)
	(move c)
	(put :chips 1)
))

(defun recursion (x y z)          
	(defvar start myYpos)
	(move-dir start :back)
	(run-dirs :front :front :right :right)
	(move-face z :east)
	(if (blocked?) (if (isZero? y) (recursion z y x) (null)) (recursion x d start))
)
"""
parser(prueba, instrucciones)