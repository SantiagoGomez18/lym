verificador = True

instrucciones = ['defvar', '=', 'move', 'skip', 'turn', 'move-dir', 'runs-dir', 'move-face', 
        'dim', 'myxpos', 'myypose', 'mychips', 'myballoons', 'balloonshere', 'chipsHere', 'spaces', 'null',
        'if', 'while', 'repeat', 'not', 'facing?', 'blocked?', 'can-put?', 'can', 'not', 'J', 'Go', ':',
        '(', ')', 'defun', 'loop', 'can-move', 'can-pick', 'iszero?', 'put', 'pick' ]

posiciones = [':north', ':south', ':east', ':west']

dirs = [':front', ':back', ':left', ':right', ':down']

turn = [':right', ':left', ':around']

condiciones = ['facing?', 'blocked?', 'can-put?', 'can-pick?', 'can-move?', 'iszero?', 'not']

put_pick = [':chips', ':balloons']

constantes = ['mychips', 'dim','myballoons', 'myxpos', 'myypos', 'balloonshere', 'chipsHere', 'spaces']



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
        print('error parentesis impares')
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
            avance, verificador, contador= comandos(tokens[posicion], tokens, instrucciones, posicion, variables, funciones)
            posicion += avance
            contador_defi += contador
    if contador_defvar != contador_defi:
        print('error en contador de dervaf')
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
            tokens[posicionAct + 3] in variables.values() or (tokens[posicionAct + 3] in variables.keys() and tokens[posicionAct + 4] == ')'):
            nuevoBloque = tokens[posicionAct: posicionAct + 5]

            if nuevoBloque[4] != ')':
                print('error en dervaf mas elementos de los esperados')
                verificador = False
            else: 
                if (nuevoBloque[1] == 'defvar' or nuevoBloque[1] == '='):
                    avance = nuevoBloque.index(')') + 1
                    for i in range(len(nuevoBloque)):
                        if i == 2 and not nuevoBloque[i].isalpha() and nuevoBloque[i]:

                            print('error en defvar no es letra')
                            verificador = False
                        elif i == 3:
                            if nuevoBloque[i] not in variables.keys() and nuevoBloque[i] != 'myxpos' and \
                                nuevoBloque[i] != 'myypos' and not nuevoBloque[i].isdigit() and nuevoBloque[i] != 'dim' and\
                                nuevoBloque[i] != 'mychips' and nuevoBloque[i] != 'myballons' and nuevoBloque[i] != 'baloonshere' and\
                                nuevoBloque[i] != 'chipshere' and nuevoBloque[i] != 'spaces':
                                print('error en defvar algo no cuadra')
                                verificador = False 
                    contador_def += 1

        #Bloque de condicionales, not y loops                
        elif(tokens[posicionAct + 1] in ['if', 'loop', 'not']):
            if tokens[posicionAct + 2] != '(':
                print('hay algo en medio de un if, loop o not')
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
                for i in range(len(nuevoBloque)):
                    if nuevoBloque[i] == 'if': 

                        parentesis_der = nuevoBloque.count(')')
                        parentesis_izq = nuevoBloque.count('(')
                        suma = parentesis_der + parentesis_izq

                        if suma % 2 != 0 or suma < 6:
                            print('error en if parametros internos')
                            verificador = False
                
                if 'skip' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('skip') + 1] not in variables.keys():
                        print('error en skip dentro if')
                        verificador = False
                if 'move' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('move') + 1] not in variables.keys() and (not nuevoBloque[nuevoBloque.index('move') + 1].isdigit()):
                        print('error en move dentro if')
                        verificador = False
                if 'turn' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('turn') + 1] not in turn:
                        print('error en turn dentro if')
                        verificador = False
                if 'move-face' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('move-face') + 1] not in variables.keys() or nuevoBloque[nuevoBloque.index('move-face') + 2] not in posiciones:
                        print('error en move-face dentro if')
                        verificador = False
                if 'face' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('face') + 1] not in posiciones:
                        print('error en face dentro if')
                        verificador = False
                if 'facing?' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('facing?') + 1] not in posiciones:
                        print('error en facing? dentro if')
                        verificador = False
                if 'can-move' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('can-move') + 1] not in posiciones:
                        print('error en can-move dentro if')
                        verificador = False
                if 'can-put' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('can-put') + 1] not in put_pick:
                        print('error en can-put dentro if')
                        verificador = False
                    if nuevoBloque[nuevoBloque.index('can-put') + 2] not in variables.keys() and not nuevoBloque[nuevoBloque.index('can-put') + 2].isdigit():
                        print('error en can-put2 dentro if')
                        verificador = False
                if 'can-pick' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('can-pick') + 1] not in put_pick:
                        print('error can pick dentro if')
                        verificador = False
                    if nuevoBloque[nuevoBloque.index('can-pick') + 2] not in variables.keys() and not nuevoBloque[nuevoBloque.index('can-pick') + 2].isdigit():
                        print('error en can-pick2 dentro if')
                        verificador = False
                        
                if 'iszero?' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('iszero?') + 1] not in variables.keys() and not nuevoBloque[nuevoBloque.index('iszero?') + 1].isdigit()\
                        and nuevoBloque[nuevoBloque.index('iszero?') + 1] not in constantes:
                        print('error iszero dentro if')
                        verificador = False
                
                j = 1
                for i in range(len(nuevoBloque)):
                    if j < len(nuevoBloque):
                        if nuevoBloque[i]  == '(' and nuevoBloque[j] == ')':
                            print('error if vacio')
                            verificador = False
                    j+=1
                    #Valida que haya algo dentro de la condicion

                    if nuevoBloque[i] not in instrucciones and nuevoBloque[i] not in posiciones\
                        and nuevoBloque[i] not in variables.keys() and nuevoBloque[i] not in funciones.keys()\
                        and nuevoBloque[i] not in turn and nuevoBloque[i] not in condiciones and nuevoBloque[i] not in put_pick\
                        and nuevoBloque[i] not in dirs and nuevoBloque[i] not in variables.values() and nuevoBloque not in funciones.values():

                        print('dentro if variable o comando no creado')
                        verificador = False
                    #Valida que dentro de la condicion halla un comando o una variable creada
                    
                    if nuevoBloque[i]  == 'if':
                        if nuevoBloque[i + 2] == ['loop', 'repeat']:
                            print('loop o repeat en un if')
                            verificador = False 
                    #Valida que no haya un loop o repeat dentro de un if
                    
                        if nuevoBloque[i + 2] in ['facing?', 'can-move', 'move-face']:
                            if nuevoBloque[i + 3] not in posiciones:
                                print('error de argumentos dentro de un facing?, can-move, move-face')
                                verificador = False
                    #Valida que si hay un comando de movimiento, haya una posicion
                    
                        if nuevoBloque[i + 2] in ['move','skip']:
                            if nuevoBloque[i + 3] not in variables.keys():
                                print('variable no creada dentro de una condicion skip o move')
                                verificador = False
                    #Valida que si hay un comando de movimiento, haya una variable creada
                    
                        if nuevoBloque[i + 2] == 'turn':
                            if nuevoBloque[i + 3] not in turn:
                                print('error en la posicion asignada a un turn')
                                verificador = False
                    #Valida que si hay un comando de movimiento, haya una posicion
                    
                        if nuevoBloque[i + 2] == 'face':
                            if nuevoBloque[i + 3] not in posiciones:
                                print('error en una posicion despues de un face')
                                verificador = False
                    #Valida que si hay un comando de movimiento, haya una posicion
                       
                    #Hacen falta las que usan el .digit()
                    
                    
                    if nuevoBloque[i] == 'not':
                        if nuevoBloque[i + 2] not in condiciones:
                            print('error en que no hay una condicion despues de un not')
                            verificador = False
                            
                    if nuevoBloque[i] == 'loop':
                        if nuevoBloque[i + 2] not in condiciones:
                            print('error no hay condicion despues de un loop')
                            verificador = False
                            
                            
        #bloques de defun
                    
        elif tokens[posicionAct + 1] in ['defun']:
            if tokens[posicionAct + 2] not in funciones.keys():
                print('error en que una funcion no esta creada despues de un defun pero se intenta llamar')
                verificador = False

            if tokens[posicionAct + 3] != '(':
                print('error hay un elemento en medio de una funcion su nombre y el parentesis')
                verificador = False
            
            if tokens[posicionAct + 3] == '(':
                contar_parentesis_der = 0
                contar_parentesis_izq = 2
                i = 4
                while contar_parentesis_der != contar_parentesis_izq:
                    if tokens[posicionAct + i] == '(':
                        contar_parentesis_izq += 1
                    elif tokens[posicionAct + i] == ')':
                        contar_parentesis_der += 1
                    i+=1
                nuevoBloque = tokens[posicionAct: posicionAct + i]
                #Valida que haya algo dentro de la condicion
            if nuevoBloque[3] == '(':
                bloque2 = nuevoBloque[3: nuevoBloque.index(')')]
                variables = anadir_variablesxfuncion(bloque2, variables)

                
        #Bloques libres
        elif tokens[posicionAct + 1] in funciones.keys():
            indice_cierre = tokens.index(')', posicionAct)
            nuevoBloque = tokens[posicionAct + 2: indice_cierre]
            variables = actualizar_None(nuevoBloque, variables)
        
        elif (tokens[posicionAct + 1] in ['move', 'skip']):
            nuevoBloque = tokens[posicionAct : posicionAct + 4]           
            if nuevoBloque[3] != ')':
                print('el bloque tiene elementos de mas en bloques libres')
                verificador = False
            if nuevoBloque[2] not in variables.keys() and not nuevoBloque[2].isdigit():
                print('el valor dado a un skip o move no esta creado, variables libres')
                verificador = False 
                
        elif (tokens[posicionAct + 1] in ['turn']):
            nuevoBloque = tokens[posicionAct : posicionAct + 4]
            if nuevoBloque[3] != ')':
                print('mas elementos de los esperados en un turn, bloque libre')
                verificador = False
            if nuevoBloque[2] not in turn:
                print('no hay posicion esperada para turn en bloques libres')
                verificador = False
                
        elif (tokens[posicionAct + 1] in ['face']): 
            nuevoBloque = tokens[posicionAct : posicionAct + 4]
            if nuevoBloque[3] != ')':
                print('error mas elementos de los esperados para un face bloque libre')
                verificador = False
            if nuevoBloque[2] not in posiciones:
                print('elemento no esperado para un face bloque libre')
                verificador = False
                
        elif tokens[posicionAct + 1] in ['move-dir']:
            nuevoBloque = tokens[posicionAct: posicionAct + 5]
            if nuevoBloque[4] != ')':
                print('error en move-dir mas elementos de los esperados en bloque libre')
                verificador = False
            if (nuevoBloque[2] not in variables.keys() and not nuevoBloque[2].isdigit()) or nuevoBloque[3] not in dirs :
                print('error en move-dir elemento no esperado en bloque libre')
                verificador = False
                
        elif tokens[posicionAct + 1] in ['put', 'picks']:
            nuevoBloque = tokens[posicionAct: posicionAct + 5]
            if nuevoBloque[4] != ')':
                print('mas elementos de los esperados para put o pick, bloque libre')
                verificador = False
            if nuevoBloque[2] not in put_pick:
                print('elemento no esta en put_pick bloque libre')
                verificador = False
            if nuevoBloque[3] not in variables.keys() and not nuevoBloque[3].isdigit():
                print('valor no esperado en put bloque libre')
                verificador = False
                
        elif tokens[posicionAct + 1] == 'move-face':
            nuevoBloque = tokens[posicionAct: posicionAct + 5]
            if nuevoBloque[4] != ')':
                print('mas posiciones de las esperadas move-face ')
                verificador = False
            if nuevoBloque[2] not in variables.keys() and not nuevoBloque[2].isdigit() or nuevoBloque[3] not in posiciones:
                print('valor no esperado move-face en bloque libre')
                verificador = False
                
        elif tokens[posicionAct + 1] == 'run-dirs':
            indice_cierre = tokens.index(')', posicionAct)
            nuevoBloque = tokens[posicionAct: indice_cierre + 1]    
            
            for i in range(2, len(nuevoBloque)-1):
                if nuevoBloque[i] not in dirs:
                    print('valor no esperado en la lista run-dirs')
                    verificador = False
                    
            #bloques de repeat
        elif tokens[posicionAct + 1] == 'repeat':
            if tokens[posicionAct + 3] == '(':
                contar_parentesis_der = 0
                contar_parentesis_izq = 2   
                i = 4
                while contar_parentesis_der != contar_parentesis_izq:
                    if tokens[posicionAct + i] == '(':
                        contar_parentesis_izq += 1
                    elif tokens[posicionAct + i] == ')':
                        contar_parentesis_der += 1
                    i+=1
                nuevoBloque = tokens[posicionAct: posicionAct + i]
                parentesis_der = nuevoBloque.count(')')
                parentesis_izq = nuevoBloque.count('(')
                suma = parentesis_der + parentesis_izq
                if suma % 2 != 0 or suma < 6:
                    print('no hay suficientes parametros para la funcion')
                    verificador = False
                if nuevoBloque[2] not in variables.keys() and not nuevoBloque[2].isdigit() and nuevoBloque[2] not in constantes:
                    print('relacion invalida para un repeat')
                    verificador = False
                if nuevoBloque[3] != '(':
                    print('hay algo entre el repeat su instruccion y el parentesis')
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

def anadir_variablesxfuncion(tokens, variables):
    for i in range(len(tokens)):
        if tokens[i] == '(' or tokens[i]  in variables.keys():
            if i < len(tokens)-1:
                if tokens[i + 1] not in variables:
                    variables[tokens[i + 1]] = None
                elif tokens[i + 2] not in variables:
                    variables[tokens[i + 2]] = None
                elif tokens[i + 3] not in variables:
                    variables[tokens[i + 3]] = None
                elif tokens[i + 4] not in variables:
                    variables[tokens[i + 4]] = None
                elif tokens[i + 5] not in variables:
                    variables[tokens[i + 5]] = None
                elif tokens[i + 6] not in variables:
                    variables[tokens[i + 6]] = None
                elif tokens[i + 7] not in variables:
                    variables[tokens[i + 7]] = None
                elif tokens[i + 8] not in variables:
                    variables[tokens[i + 8]] = None
            
    return variables

def actualizar_variable(tokens, variables):

    for i in range(len(tokens)):
        if tokens[i] == '=':
            if tokens[i + 1] in variables:
                variables[tokens[i + 1]] = tokens[i + 2]
    return variables

def actualizar_None(tokens, variables):
    llaves_none = [llave for llave, valor in variables.items() if valor is None]  # Obtener las llaves con valor None
    for i, llave in enumerate(llaves_none):
        if i < len(tokens) and tokens[i].isdigit():  # Verificar que hay elementos en la lista tokens
            variables[llave] = tokens[i]  # Asignar el valor correspondiente de tokens al None actual
    return variables

def anadir_funcion(tokens, funciones):
    for i in range(len(tokens)):
        if tokens[i] == 'defun':
            if tokens[i + 1] not in funciones:
                funciones[tokens[i + 1]] = 0
    return funciones
    
    
prueba = '''

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
'''



prueba2 =  '''(defvar rotate 3)

(if (can-move? :north) (move-dir 1 :front) (null))

(
(if (not (blocked?)) (move 1) (null))
(turn :left)
)

(defvar one 1)

(defun foo (c p)
	(put :chips c)
	(put :balloons p)
	(move rotate))
(foo 1 3)

(defun goend ()
	(if (not (blocked?))
	((move one)
		(goend))
	(null)))

(defun fill ()
	(repeat Spaces (if (not (isZero? myChips)) (put :chips 1) ))
)

(defun pickAllB ()
	(pick :balloons balloonsHere)
)

(run-dirs :left :front :left :down :right)'''
parser(prueba, instrucciones)