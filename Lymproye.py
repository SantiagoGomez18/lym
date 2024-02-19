verificador = True

instrucciones = ['defvar', '=', 'move', 'skip', 'turn', 'move-dir', 'runs-dir', 'move-face', 
        'Dim', 'myXpos', 'myYpose', 'myChips', 'myBallons', 'baloonsHere', 'ChipsHere', 'Spaces', 'null',
        'if', 'while', 'repeat', 'not', 'facing?', 'blocked?', 'can-put?', 'can', 'not', 'J', 'Go', ':',
        '(', ')', 'defun', 'loop', 'can-move', 'can-pick', 'iszero?' ]

posiciones = [':north', ':south', ':east', ':west', ':front', ':back', ':right', ':left']

condiciones = ['facing?', 'blocked?', 'can-put?', 'can-pick?', 'can-move?', 'iszero?', 'not']

def parser(filetxt, instrucciones):
    verificador = True
    prueba = filetxt
    contador_defi = 0
    prueba = prueba.replace('\n', ' ').replace('\t', ' ')
    
    if prueba[len(prueba)- 1] == ' ':
         prueba = prueba[0:len(prueba)- 1]
         
    prueba = prueba.replace(')', ' )').replace('(', '( ')
    tokens = [i.lower() for i in prueba.split(' ')]
    parentesis = (tokens.count('(') + tokens.count(')'))
        
    if parentesis % 2 != 0 or tokens.count('(') != tokens.count(')'):
        verificador = False
        
    variables = {}
    variables = anadir_variable(tokens, variables)
    variables = actualizar_variable(tokens, variables)

    funciones = {}
    funciones = anadir_funcion(tokens, funciones)
    
    i = 0  #iterador
    posicion = 0 #indice
    
     #Elimina el carascter vacio de la lista de tokens para poder realizar un mero estudio
    while '' in tokens:
        tokens.remove('')
    contador_defvar = tokens.count('defvar')
    
    while posicion < len(tokens) and verificador == True:
        if i == 0:
            avance, verificador, contador = comandos(tokens[posicion], tokens, instrucciones, posicion, variables, funciones)
            posicion += avance
            contador_defi += contador
            
    
    if contador_defvar != contador_defi:
        verificador = False

    if verificador == True:
        respuesta = 'Sirve :D'
    elif verificador == False:
        respuesta = 'No sirve :c' 

    return print(respuesta)


def comandos(token: str, tokens: list, instrucciones: list, posicionAct: int, variables: dict, funciones: dict):
    verificador = True
    avance = 1
    contador_def = 0
    
    
    
    if token == '(':
        #Dervaf hechos

        if tokens[posicionAct + 1] in ['defvar', '='] and tokens[posicionAct + 2] in variables.keys() and \
            tokens[posicionAct + 3] in variables.values() or tokens[posicionAct + 3] in variables.keys() and tokens[posicionAct + 4] == ')':
            nuevoBloque = tokens[posicionAct: posicionAct + 5]

            if nuevoBloque[4] != ')':
                verificador = False
            else: 
                if (nuevoBloque[1] == 'defvar' or nuevoBloque[1] == '='):
                    avance = nuevoBloque.index(')') + 1
                contador_def += 1
            for i in range(len(nuevoBloque)):
                if i == 2 and not nuevoBloque[i].isalpha():
                    verificador = False
                elif i == 3:
                    if nuevoBloque[i] not in variables.keys() and nuevoBloque[i] != 'myxpos' and \
                        nuevoBloque[i] != 'myypos' and not nuevoBloque[i].isdigit():
                        verificador = False 
        
        #Bloque de condicionales, not y loops                
        elif(tokens[posicionAct + 1] in ['if', 'loop', 'not']):
            if tokens[posicionAct + 2] != '(':
                verificador = False
                
            elif tokens[posicionAct + 2] == '(':
                contar_parentesis_der = 0
                contar_parentesis_izq = 2
                i = 3
                while contar_parentesis_der != contar_parentesis_izq:
                    if tokens[posicionAct + i] == '(':
                        contar_parentesis_izq += 1
                    elif tokens[posicionAct + i] == ')':
                        contar_parentesis_der += 1
                    i+=1
                nuevoBloque = tokens[posicionAct: posicionAct + i]
                j = 1
                for i in range(len(nuevoBloque)):
                    if j < len(nuevoBloque):
                        if nuevoBloque[i]  == '(' and nuevoBloque[j] == ')':
                            verificador = False
                    #Valida que haya algo dentro de la condicion
                    j+=1
                    if nuevoBloque[i] not in instrucciones and nuevoBloque[i] not in posiciones\
                        and nuevoBloque[i] not in variables.keys() and nuevoBloque[i] not in funciones.keys():
                        verificador = False
                    #Valida que dentro de la condicion halla un comando o una variable creada
                    if nuevoBloque[i]  == 'if':
                        if nuevoBloque[i + 2] == ['loop', 'repeat']:
                            verificador = False 
                    #Valida que no haya un loop o repeat dentro de un if
                        if nuevoBloque[i + 2] in ['facing?', 'can-move', 'move-dir', 'move-face']:
                            if nuevoBloque[i + 3] not in posiciones:
                                verificador = False
                    #Valida que si hay un comando de movimiento, haya una posicion
                        if nuevoBloque[i + 2] in ['move', 'move-dir', 'move-face']:
                            if nuevoBloque[i + 3] not in variables.keys():
                                verificador = False
                    #Valida que si hay un comando de movimiento, haya una variable creada
                    if nuevoBloque[i] == 'not':
                        if nuevoBloque[i + 2] not in condiciones:
                            verificador = False
                        if nuevoBloque[i + 2] in ['facing?', 'can-move', 'move-dir', 'move-face']:
                            if nuevoBloque[i + 3] not in posiciones:
                                verificador = False
                    
                    

                

                



                        
    return avance, verificador, contador_def
  
  
  
  
  
  
  
  
  
  
  
    
def anadir_variable(tokens, variables):
    for i in range(len(tokens)):
        if tokens[i] == 'defvar':
            if tokens[i + 1] not in variables:
                variables[tokens[i + 1]] = tokens[i + 2]
                if tokens[i + 2] == '':
                    variables[tokens[i + 1]] = tokens[i + 3]
                    if tokens[i + 3] == '':
                        variables[tokens[i + 1]] = tokens[i + 4]
                        if tokens[i + 4] == '':
                            variables[tokens[i + 1]] = tokens[i + 5]
                            if tokens[i + 5] == '':
                                variables[tokens[i + 1]] = tokens[i + 6]    
    return variables

def actualizar_variable(tokens, variables):
    for i in range(len(tokens)):
        if tokens[i] == '=':
            if tokens[i + 1] in variables:
                variables[tokens[i + 1]] = tokens[i + 2]
                if tokens[i + 2] == '':
                    variables[tokens[i + 1]] = tokens[i + 3]
                    if tokens[i + 3] == '':
                        variables[tokens[i + 1]] = tokens[i + 4]
                        if tokens[i + 4] == '':
                            variables[tokens[i + 1]] = tokens[i + 5]
                            if tokens[i + 5] == '':
                                variables[tokens[i + 1]] = tokens[i + 6]
    return variables


def anadir_funcion(tokens, funciones):
    for i in range(len(tokens)):
        if tokens[i] == 'defun':
            if tokens[i + 1] not in funciones:
                funciones[tokens[i + 1]] = 0
    return funciones
    
prueba = '''
(defvar s 5)
(defvar a 2)
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

(defun recursion (p q r) 
	(defvar start myYpos)
	(move-dir start :back)
	(run-dirs :front :front :right :right)
	(move-face c :east)
	(if (blocked?) (if (isZero? b) (recursion a b c) (null)) (recursion c d start))
)
'''
parser(prueba, instrucciones)