verificador = True

instrucciones = ['defvar', '=', 'move', 'skip', 'turn', 'move-dir', 'runs-dir', 'move-face', 
        'dim', 'myxpos', 'myypose', 'mychips', 'myballoons', 'balloonshere', 'chipsHere', 'spaces', 'null',
        'if', 'while', 'repeat', 'not', 'facing?', 'blocked?', 'can-put?', 'can', 'not', 'J', 'Go', ':',
        '(', ')', 'defun', 'loop', 'can-move', 'can-pick', 'iszero?' ]

posiciones = [':north', ':south', ':east', ':west']

dirs = [':front', ':back', ':left', ':right']

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
        print('error parentesis')
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
        print('error en defvar 0')
        verificador = False
    print(contador_defvar, contador_defi)
    print(funciones.keys())

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
                print('error en defvar 6')
                verificador = False
            else: 
                if (nuevoBloque[1] == 'defvar' or nuevoBloque[1] == '='):
                    avance = nuevoBloque.index(')') + 1
                    for i in range(len(nuevoBloque)):
                        if i == 2 and not nuevoBloque[i].isalpha() and nuevoBloque[i]:
                            print(nuevoBloque[i])
                            print(nuevoBloque)
                            print('error en defvar 1')
                            verificador = False
                        elif i == 3:
                            if nuevoBloque[i] not in variables.keys() and nuevoBloque[i] != 'myxpos' and \
                                nuevoBloque[i] != 'myypos' and not nuevoBloque[i].isdigit() and nuevoBloque[i] != 'dim' and\
                                nuevoBloque[i] != 'mychips' and nuevoBloque[i] != 'myballons' and nuevoBloque[i] != 'baloonshere' and\
                                nuevoBloque[i] != 'chipshere' and nuevoBloque[i] != 'spaces':
                                print('error en defvar 4')
                                verificador = False 
                    contador_def += 1
            
        
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
                
        
                if 'skip' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('skip') + 1] not in variables.keys():
                        verificador = False
                if 'move' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('move') + 1] not in variables.keys():
                        verificador = False
                if 'turn' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('turn') + 1] not in turn:
                        verificador = False
                if 'move-face' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('move-face') + 1] not in variables.keys() or nuevoBloque[nuevoBloque.index('move-face') + 2] not in posiciones:
                        verificador = False
                if 'face' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('face') + 1] not in posiciones:
                        verificador = False
                if 'facing?' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('facing?') + 1] not in posiciones:
                        verificador = False
                if 'can-move' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('can-move') + 1] not in posiciones:
                        verificador = False
                if 'can-put' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('can-put') + 1] not in put_pick:
                        verificador = False
                    if nuevoBloque[nuevoBloque.index('can-put') + 2] not in variables.keys() and not nuevoBloque[nuevoBloque.index('can-put') + 2].isdigit():
                        verificador = False
                if 'can-pick' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('can-pick') + 1] not in put_pick:
                        verificador = False
                    if nuevoBloque[nuevoBloque.index('can-pick') + 2] not in variables.keys() and not nuevoBloque[nuevoBloque.index('can-pick') + 2].isdigit():
                        verificador = False
                        
                if 'iszero?' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('iszero?') + 1] not in variables.keys() and not nuevoBloque[nuevoBloque.index('iszero?') + 1].isdigit()\
                        and nuevoBloque[nuevoBloque.index('iszero?') + 1] not in constantes:
                        print(nuevoBloque[nuevoBloque.index('iszero?') + 1])
                        verificador = False
                        
                if 'put' in nuevoBloque:
                    if nuevoBloque[nuevoBloque.index('put') + 1] not in put_pick:
                        print('toy aca')
                        verificador = False
                    if nuevoBloque[nuevoBloque.index('put') + 2] not in variables.keys() and not nuevoBloque[nuevoBloque.index('put') + 2].isdigit():
                        print('toy aca2')
                        verificador = False
                        
                #put, pick, move-dir, run-dirs
                        
                #Hace falta mopve-dir, iszero, can-put, can-pick, put, pickk, run-dirs esto pq no se usar el .digit()
                
                j = 1
                for i in range(len(nuevoBloque)):
                    if j < len(nuevoBloque):
                        if nuevoBloque[i]  == '(' and nuevoBloque[j] == ')':
                            verificador = False
                    j+=1
                    #Valida que haya algo dentro de la condicion
                    
                    
                    
                    if nuevoBloque[i] not in instrucciones and nuevoBloque[i] not in posiciones\
                        and nuevoBloque[i] not in variables.keys() and nuevoBloque[i] not in funciones.keys()\
                        and nuevoBloque[i] not in turn and nuevoBloque[i] not in condiciones and nuevoBloque[i] not in put_pick:
                        verificador = False
                    #Valida que dentro de la condicion halla un comando o una variable creada
                    
                    
                    
                    if nuevoBloque[i]  == 'if':
                        if nuevoBloque[i + 2] == ['loop', 'repeat']:
                            verificador = False 
                    #Valida que no haya un loop o repeat dentro de un if
                    
                        if nuevoBloque[i + 2] in ['facing?', 'can-move', 'move-face']:
                            if nuevoBloque[i + 3] not in posiciones:
                                verificador = False
                    #Valida que si hay un comando de movimiento, haya una posicion
                    
                        if nuevoBloque[i + 2] in ['move','skip']:
                            if nuevoBloque[i + 3] not in variables.keys():
                                verificador = False
                    #Valida que si hay un comando de movimiento, haya una variable creada
                    
                        if nuevoBloque[i + 2] == 'turn':
                            if nuevoBloque[i + 3] not in turn:
                                verificador = False
                    #Valida que si hay un comando de movimiento, haya una posicion
                    
                        if nuevoBloque[i + 2] == 'face':
                            if nuevoBloque[i + 3] not in posiciones:
                                verificador = False
                    #Valida que si hay un comando de movimiento, haya una posicion
                       
                    #Hacen falta las que usan el .digit()
                    
                    
                    if nuevoBloque[i] == 'not':
                        if nuevoBloque[i + 2] not in condiciones:
                            verificador = False
                            
                    if nuevoBloque[i] == 'loop':
                        if nuevoBloque[i + 2] not in condiciones:
                            verificador = False
                            
        #Bloques libres, no he creado los bloques pero estan las condiciones
        elif (tokens[posicionAct + 1] in ['move', 'skip']):
            nuevoBloque = tokens[posicionAct : posicionAct + 4]           
            if nuevoBloque[3] != ')':
                verificador = False
            if nuevoBloque[2] not in variables.keys():
                verificador = False 
                
        elif (tokens[posicionAct + 1] in ['turn']):
            nuevoBloque = tokens[posicionAct : posicionAct + 4]
            if nuevoBloque[3] != ')':
                verificador = False
            if nuevoBloque[2] not in turn:
                verificador = False
                
        elif (tokens[posicionAct + 1] in ['face']): 
            nuevoBloque = tokens[posicionAct : posicionAct + 4]
            if nuevoBloque[3] != ')':
                verificador = False
            if nuevoBloque[2] not in posiciones:
                verificador = False
                
        elif tokens[posicionAct + 1] in ['move-dir']:
            nuevoBloque = tokens[posicionAct: posicionAct + 5]
            if nuevoBloque[4] != ')':
                print('error en move-dir')
                verificador = False
            if (nuevoBloque[2] not in variables.keys() and not nuevoBloque[2].isdigit()) or nuevoBloque[3] not in dirs :
                print('error en move-dir')
                verificador = False
                
        elif tokens[posicionAct + 1] in ['put', 'picks']:
            nuevoBloque = tokens[posicionAct: posicionAct + 5]
            if nuevoBloque[4] != ')':
                verificador = False
            if nuevoBloque[2] not in put_pick:
                verificador = False
            if nuevoBloque[3] not in variables.keys() and not nuevoBloque[3].isdigit():
                verificador = False
                
        elif tokens[posicionAct + 1] == 'move-face':
            nuevoBloque = tokens[posicionAct: posicionAct + 5]
            if nuevoBloque[4] != ')':
                verificador = False
            if nuevoBloque[2] not in variables.keys() and not nuevoBloque[2].isdigit() or nuevoBloque[3] not in posiciones:
                verificador = False

        #falta solo el run-dirs 
        
        #Bloque de funciones
        elif tokens[posicionAct + 1] in ['defun']:
            if tokens[posicionAct + 2] not in funciones.keys():
                verificador = False

            if tokens[posicionAct + 3] != '(':
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
                print(nuevoBloque)

            j = 1
            for i in range(len(nuevoBloque)):
                if j < len(nuevoBloque):
                    if nuevoBloque[i]  == '(' and nuevoBloque[j] == ')':
                        verificador = False
                j+=1
                #Valida que haya algo dentro de la condicion
                

                

                    
                    
                        
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
(defvar x 2)
(defvar a 2)
(defvar b a)
(defvar c myXpos)
(defvar d 0)
(= d 7)

(if (facing? :north) (turn :right) (put :chips 1))

(move a)

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
	(if (blocked?) (if (isZero? mychips) (recursion a b c) (null)) (recursion c d start))
)
'''
parser(prueba, instrucciones)