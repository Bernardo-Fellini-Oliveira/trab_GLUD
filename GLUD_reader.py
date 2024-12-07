import tkinter as tk
from tkinter import filedialog

def EncontraNesimaLinhaNaoVazia(arq : str, n : int):
    for linha in arq:
        if linha.strip():
            n -= 1
        if n == 0:
            linha_nao_vazia = linha
            break
    
    return linha_nao_vazia

def EncontraNesimaOcorrenciaDeSubstringNaString(string : str, substring : str, n : int):
    inicio = string.find(substring)
    while inicio >=0 and n > 1:
        inicio = string.find(substring, inicio+len(substring))
        n -= 1
    return inicio

# usa a biblioteca tkinter para abrir a janela paraseleção de arquivo
iniciar = input("Deseja iniciar a leitura de uma GLUD? (s para iniciar, qualquer outro input para fechar o programa)")
if iniciar == 's':
    root = tk.Tk()
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt"),("Todos os arquivos", "*.*")],title="Selecione um arquivo")
    root.withdraw()
    root.quit()
    if file_path:
        continuar_execucao = True
    else:
        continuar_execucao = False
        print("nenhum arquivo selecionado, fechando programa")
else:
    continuar_execucao = False
    print("fechando programa")

while(continuar_execucao):

    # arq é uma lista de strings com todas as linha do arquivo aberto
    try:
        with open(file_path, "r", encoding="utf8") as file:
            arq = file.readlines()

    except FileNotFoundError:
        print("Falha na abertura do arquivo (arquivo não encontrado)")

    else:
        # primeira linha deve ser do tipo : "<G>=({<V1>,...,<Vn>}, {<t0>,...,<tn>}, P, <Ini>)""
        primeira_linha = EncontraNesimaLinhaNaoVazia(arq, 1).strip()

        # ainda não coloquei tratamento de erros sintáticos nessa parte pq vai ser um porre :P
        conteudos_linha = primeira_linha.split("=")
        nome_GLUD = conteudos_linha[0]
        conjuntos_da_GLUD = conteudos_linha[1]
        variaveis = conjuntos_da_GLUD[conjuntos_da_GLUD.find('{')+1 : conjuntos_da_GLUD.find('}')].split(',')
        terminais = conjuntos_da_GLUD[EncontraNesimaOcorrenciaDeSubstringNaString(conjuntos_da_GLUD, '{', 2)+1 : EncontraNesimaOcorrenciaDeSubstringNaString(conjuntos_da_GLUD, '}', 2)].split(',')
        simbolo_producao = conjuntos_da_GLUD[EncontraNesimaOcorrenciaDeSubstringNaString(conjuntos_da_GLUD, '}', 2)+3]
        simbolo_inicial = conjuntos_da_GLUD[conjuntos_da_GLUD.find(')')-1]

        if simbolo_producao != 'P':
            print("Erro: símbolo de produções deve ser o caractere 'P'")
            continuar_execucao = False
            break

        if simbolo_inicial not in variaveis:
            print("Erro: símbolo inicial não faz parte do conjunto de variáveis")
            continuar_execucao = False
            break

        # segunda linha deve ser "P = {"
        if EncontraNesimaLinhaNaoVazia(arq, 2).strip() != "P = {":
            print("Erro: segunda linha não é exatamente \"P = {\"")
            continuar_execucao = False
            break

        sintaxe_de_fim_correta = False
        producoes = []

        for linhanum, linha in enumerate(arq):
            if linha.strip() == primeira_linha or linha.strip() == "P = {" or not linha.strip():
                continue
            if linha[:-1] == '}':
                sintaxe_de_fim_correta = True
                continue
            if sintaxe_de_fim_correta:
                print("Erro: arquivo da GLUD possui conteúdo após caractere terminador das produções ('}')")
                continuar_execucao = False
                break
            # adicionar teste de erro para ver se a sintaxe da linha é do tipo < V > −> < t >< W > (também parece ser um porre)
            producoes.append(linha[:-1])
        
        if not continuar_execucao:
            break
        
        continuar_execucao = False

# pedir para selecionar o arquivo da GLUD ou sair
# verificar se é válido
# construir AFD
# pedir para selecionar o arquivo de palavras ou uma nova GLUD ou sair
# rodar no AFD e apresentar quais palavras pertencem à linguagem e repetir o pedido