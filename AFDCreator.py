from models import RRG, NFAε


def onlyTermOrVar(prod, v): #função que verifica se dada uma produção, ela é constituída apenas de variáveis ou terminais
    if prod in v:
        return True
    return False



def prodToTransition(prodVal, prodAtual, v,t, estado):
    if prodVal == "": #se a produção for vazia, o estado atual faz um movimento vazio para qf
        estado["ε"].add("qf")
    elif(onlyTermOrVar(prodVal, t)): #se prodval conter apenas um terminal, então é um movimento do estado atual para o estado final
        estado[prodVal].add("qf")
    elif(onlyTermOrVar(prodVal, v)): #se prodval conter apenas uma variável, então é um movimento vazio do estado atual para o prox estado
        estado["ε"].add(prodVal)
    else:
        for i in v: #encontra qual variável está na produção
            if i in prodVal:
                aux = prodVal.replace(i, "") #ao encontrar, remove a variável da produção para obter o terminal
                estado[aux].add(i)  #monta o reconhecimento do terminal com a variável removida



def makeStates(v,p, t):
    q = dict() #inicializa um dicionário vazio
    for i in v: # para cada variável, cria um estado. Inicialmente nenhum estado possui  transição
        q[i] ={}
        for j in t:
            q[i][j] = set()
        q[i]["ε"] = set()
    

    for prod in p: #para cada produção do conjunto de produções , transforma em uma transição
        for prodVal in p[prod]:
            estado  = q[prod]
            prodToTransition(prodVal, prod, v, t, estado)
    return q
                 


    


def makeAF(glud: RRG) -> NFAε: # glud = (V, T, P, S)
    v = glud.N #recebe as variáveis
    v.add("qf") #adiciona uma variável qf para a transição variavel -> estados
    t = glud.Σ #recebe os terminais
    p = glud.P #recebe o conjunto de produções
    s = glud.S # recebe o símbolo inicial
    q = makeStates(v, p, t) #monta a função programa do autômato
    
    # M = (Σ, Q, δ, q0, F)
    automato = NFAε(v, t, q, s, {"qf"}) #Σ = T, Q = V ∪ {qf } (para qf 6∈ V ), F = {qf },  q0 = S
    return automato
