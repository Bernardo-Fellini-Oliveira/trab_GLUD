from AFDCreator import makeAF

def afRecognizer(afD: tuple, word: str):
    funcProgram = afD[2] #recebe a função programa
    estado =  afD[3] #começa no estado inicial
    finalStatev = afD[4] #recebe o estado final
    
    aceita = False #inicia em false para tratar de movimentos indefinidos
    for i in word: # para cada símbolo da fita de entrada, procura um movimento correspondente
        try:
            if i in list(funcProgram[estado].keys()): #se o estado atual reconhece o símbolo atual, move para o próximo estado
                proxEstado = funcProgram[estado][i]
                estado = proxEstado
        except Exception: #caso não haja movimento para o símbolo atual (qualquer que seja), rejeita a entrada retornando False
            return aceita
            
    if estado ==  finalStatev: #se ao final da fita, o estado final foi encontrado, aceita a palavra, caso contrário rejeita
        aceita = True
    else: 
        aceita = False

    return aceita
    








afD = (['a', 'b'], ['Aa', 'Bb', 'C', 'qf'], {'Aa': {'a': 'Bb', 'b': 'C'}, 'Bb': {'a': 'Bb', 'b': 'C'}, 'C': {'a':"", 'b': 'qf'}, 'qf': {'a': "", 'b': ""}}, 'Aa', 'qf')
aceita = afRecognizer(afD, "aaaaaaaaabb")
print(aceita)
