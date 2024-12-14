def onlyTermOrVar(prod, v): #função que verifica se dada uma produção, ela é constituída apenas de variáveis ou terminais
    if prod in v:
        return True
    return False



def prodToTransition(prodVal, prodAtual, v,t, estado):
    if prodVal == " ": #se a produção for vazia, o estado atual faz um movimento vazio para qf
        estado["ε"].append("qf")
    elif(onlyTermOrVar(prodVal, t)): #se prodval conter apenas um terminal, então é um movimento do estado atual para o estado final
        estado[prodVal].append("qf")
    elif(onlyTermOrVar(prodVal, v)): #se prodval conter apenas uma variável, então é um movimento vazio do estado atual para o prox estado
        estado["ε"].append(prodVal)
    else:
        for i in v: #encontra qual variável está na produção
            if i in prodVal:
                aux = prodVal.replace(i, "") #ao encontrar, remove a variável da produção para obter o terminal
                estado[aux].append(i)  #monta o reconhecimento do terminal com a variável removida



def makeStates(v,p, t):
    q = dict() #inicializa um dicionário vazio
    for i in v: # para cada variável, cria um estado. Inicialmente nenhum estado possui  transição
        q[i] ={}
        for j in t:
            q[i][j] = []
        q[i]["ε"] = []
    

    for prod in p: #para cada produção do conjunto de produções , transforma em uma transição
        for k in range (len(p[prod])):
            prodVal = (p[prod][k])
            estado  = q[prod]
            prodToTransition(prodVal, prod, v, t, estado)
    return q
                 


    


def makeAF(glud): # glud = (V, T, P, S)
    v = glud[0] #recebe as variáveis
    v.append("qf") #adiciona uma variável qf para a transição variavel -> estados
    t = glud[1] #recebe os terminais
    p = glud[2] #recebe o conjunto de produções
    s = glud[3] # recebe o símbolo inicial
    q = makeStates(v, p, t) #monta a função programa do autômato
    
    # M = (Σ, Q, δ, q0, F)
    automato = (t, v, q, s, "qf") #Σ = T, Q = V ∪ {qf } (para qf 6∈ V ), F = {qf },  q0 = S
    return automato



MinhaG=(["A","B","C"], ["a","b"], {'A': ["aB", "bC"], 'B': ["aB", "bC"], "C": ["bC", " "]}, "A")
a = makeAF(MinhaG)
print(a)