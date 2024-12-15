import tkinter as tk
from tkinter import filedialog

import regex as re

def ExisteUmMesmoElementoNos2Conjuntos(conjunto1 : list, conjunto2 : list):
    for elemento in conjunto2:
        if elemento in conjunto1:
            return True
    return False

def VerificaSeLadoEsquerdoEInvalido(lado_esquerdo : str, variaveis : list):
    if lado_esquerdo not in variaveis:
        return True
    else:
        return False

def VerificaSeLadoDireitoEInvalido(lado_direito : str, tamanho_maximo_de_terminal : int, tamanho_maximo_de_variavel : int, chars_ignorados : int, terminais : list, variaveis : list):

    lado_direito = lado_direito[:chars_ignorados]

    if len(lado_direito) > tamanho_maximo_de_terminal + tamanho_maximo_de_variavel:
        print("Erro: lado direito da produção é maior do que o maior terminal e a maior variável concatenadas")
        return True

    lado_invalido = True

    if not lado_direito.strip():
        lado_invalido = False
    elif lado_direito.strip() in terminais:
        lado_invalido = False
    else:
        for i in range(tamanho_maximo_de_terminal, -1, -1):
            if lado_direito[0:i] in terminais and lado_direito[i:].strip() in variaveis:
                lado_invalido = False
                break
    
    if lado_invalido:
        print("Erro: lado direito da produção não é da forma tV, V ou vazio")
        
    return lado_invalido
        
# usa a biblioteca tkinter para abrir a janela para seleção de arquivo
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

    # arq é uma lista de strings com todas as linhas do arquivo aberto
    try:
        with open(file_path, "r", encoding="utf8") as file:
            arq = file.readlines()

    except FileNotFoundError:
        print("Falha na abertura do arquivo (arquivo não encontrado)")

    else:
        # primeira linha deve ser do tipo : "<G>=({<V1>,...,<Vn>}, {<t0>,...,<tn>}, P, <Ini>)""
        primeira_linha = arq[0].strip()

        if primeira_linha.find('=') == -1:
            print("Erro: primeira linha não possui caractere '=' separando o nome da GLUD de seus conjuntos. Certifique-se de que ela não esteja vazia")
            continuar_execucao = False
            break

        if primeira_linha[0 : primeira_linha.find('=')] == "" or primeira_linha[primeira_linha.find('=')+1 :] == "":
            print("Erro: o nome ou os conjuntos da GLUD ou ambos estão vazios")
            continuar_execucao = False
            break

        conteudos_linha = primeira_linha.split("=", 1)
        nome_GLUD = conteudos_linha[0]

        if nome_GLUD.find(' ') != -1 or nome_GLUD.find('  ') != -1:
            print("Erro: não deve haver espaços em branco entre os caracteres do nome da GLUD")
            continuar_execucao = False
            break

        conjuntos_da_GLUD = conteudos_linha[1]

        if len(conjuntos_da_GLUD) < 15:
            print("Erro: tamanho dos conjuntos da GLUD é menor do que o mínimo necessário para ser um formato válido")
            continuar_execucao = False
            break

        if conjuntos_da_GLUD[0] != '(' or conjuntos_da_GLUD[-1] != ')':
            print("Erro: os conjuntos da GLUD devem estar cercados por parênteses")
            continuar_execucao = False
            break

        if conjuntos_da_GLUD.find("}, {") == -1 or conjuntos_da_GLUD.find("}, P, ") == -1:
            print("Erro: sinalizador de fechamento do conjunto de terminais ou de variáveis inexistente")
            continuar_execucao = False
            break

        if conjuntos_da_GLUD[1] != '{':
            print("Erro: caractere indefinido entre o inicio dos conjuntos da GLUD e o conjunto de variáveis")
            continuar_execucao = False
            break

        if conjuntos_da_GLUD[2 : conjuntos_da_GLUD.find("}, {")].find(' ') != -1 or conjuntos_da_GLUD[2 : conjuntos_da_GLUD.find("}, {")].find('   ') != -1:
            print("Erro: não deve haver espaços em branco entre os elementos ou entre os caracteres de um mesmo elemento ou entre um elemento e um separador dentro do conjunto de variáveis")
            continuar_execucao = False
            break

        if conjuntos_da_GLUD[2 : conjuntos_da_GLUD.find("}, {")].find("{,") != -1 or conjuntos_da_GLUD[2 : conjuntos_da_GLUD.find("}, {")].find(",,") != -1 or conjuntos_da_GLUD[2 : conjuntos_da_GLUD.find("}, {")+1].find(",}") != -1:
            print("Erro: não deve haver variáveis representadas por um símbolo vazio na gramática (atenção, o caractere ',' não pode ser usado como símbolo de variável pois é o separador dos elementos)")
            continuar_execucao = False
            break

        variaveis = conjuntos_da_GLUD[2 : conjuntos_da_GLUD.find("}, {")].split(',')
        variavel_max_len = max(len(variavel) for variavel in variaveis)

        if '' in variaveis:
            print("Erro: deve existir ao menos 1 símbolo de variável")
            continuar_execucao = False
            break

        if conjuntos_da_GLUD[conjuntos_da_GLUD.find("}, ")+3] != '{':
            print("Erro: caractere indefinido entre o conjunto de variáveis e o conjunto de terminais")
            continuar_execucao = False
            break

        if conjuntos_da_GLUD[conjuntos_da_GLUD.find("}, {")+4 : conjuntos_da_GLUD.find("}, P, ")].find(' ') != -1 or conjuntos_da_GLUD[conjuntos_da_GLUD.find("}, {")+4 : conjuntos_da_GLUD.find("}, P, ")].find('   ') != -1:
            print("Erro: não deve haver espaços em branco entre os elementos ou entre os caracteres de um mesmo elemento ou entre um elemento e um separador dentro do conjunto de terminais")
            continuar_execucao = False
            break

        if conjuntos_da_GLUD[conjuntos_da_GLUD.find("}, {")+3 : conjuntos_da_GLUD.find("}, P, ")].find("{,") != -1 or conjuntos_da_GLUD[conjuntos_da_GLUD.find("}, {")+4 : conjuntos_da_GLUD.find("}, P, ")].find(",,") != -1 or conjuntos_da_GLUD[conjuntos_da_GLUD.find("}, {")+4 : conjuntos_da_GLUD.find("}, P, ")+1].find(",}") != -1:
            print("Erro: não deve haver terminais não vazios representados por um símbolo vazio na gramática (atenção, o caractere ',' não pode ser usado como símbolo de terminal pois é o separador dos elementos)")
            continuar_execucao = False
            break

        terminais = conjuntos_da_GLUD[conjuntos_da_GLUD.find("}, {")+4 : conjuntos_da_GLUD.find("}, P, ")].split(',')
        terminal_max_len = max(len(terminal) for terminal in terminais)

        if(ExisteUmMesmoElementoNos2Conjuntos(variaveis, terminais)):
            print("Erro: o conjunto de terminais e o connjunto de variáveis não podem compartilhar elementos")
            continuar_execucao = False
            break

        if conjuntos_da_GLUD.find("}, P, ")+6 != len(conjuntos_da_GLUD)-2:
            print("Erro: há caractere(s) não definido(s) após a definição do símbolo inicial")
            continuar_execucao = False
            break

        if '' in terminais:
            print("Atenção: nenhum símbolo terminal definido. A linguagem poderá gerar apenas a palavra vazia")

        simbolo_producao = conjuntos_da_GLUD[conjuntos_da_GLUD.find("}, P, ")+3]
        simbolo_inicial = conjuntos_da_GLUD[conjuntos_da_GLUD.find("}, P, ")+6]

        # tratamento de errros relacionados ao símbolo de produções e ao símbolo inicial
        if simbolo_producao != 'P':
            print("Erro: símbolo de produções deve ser o caractere 'P'")
            continuar_execucao = False
            break

        if simbolo_producao in variaveis:
            print("Erro: símbolo de produções não pode fazer parte do conjunto de variáveis")
            continuar_execucao = False
            break

        if simbolo_producao in terminais:
            print("Erro: símbolo de produções não pode fazer parte do conjunto de terminais")
            continuar_execucao = False
            break

        if simbolo_inicial not in variaveis:
            print("Erro: símbolo inicial não faz parte do conjunto de variáveis")
            continuar_execucao = False
            break

        if simbolo_inicial in terminais:
            print("Erro: símbolo inicial não pode fazer parte do conjunto de terminais")
            continuar_execucao = False
            break

        if simbolo_inicial == ' ' or simbolo_inicial == '  ':
            print("Erro: símbolo inicial não pode ser um espaço. Certifique-se de que ele não seja vazio")
            continuar_execucao = False
            break   

        # segunda linha deve ser "P = {"
        if arq[1].strip() != "P = {":
            print("Erro: segunda linha não é exatamente \"P = {\"")
            continuar_execucao = False
            break

        sintaxe_de_fim_correta = False
        ultima_linha_significativa = False
        producoes = []
        qtd_de_caracteres_finais_ignorados = -2

        #tratamento das produções
        for linhanum, linha in enumerate(arq, 1):
            # se for a primeira ou a segunda linha, pula pois não é para ser uma produção
            if linhanum == 1 or linhanum == 2:
                continue
            # se a última linha possuir apenas o caractere '}', significa que devemos ter chegado ao fim das produções
            if ultima_linha_significativa and linha[0] == '}':
                if len(linha) <= 2:
                    ultima_linha_significativa = False
                    sintaxe_de_fim_correta = True
                    continue
                else:
                    print("Erro: forma incorreta do fim das produções")
                    continuar_execucao = False
                    break
            # se o arquivo possui linhas não vazias depois de chegarmos ao fim das produções, então o arquivo não está no formato especificado
            if sintaxe_de_fim_correta:
                if linha.strip():
                    print("Erro: arquivo da GLUD possui conteúdo após caractere terminador das produções ('}')")
                    continuar_execucao = False
                    break
                else:
                    continue

            # verifica se chegamos na última produção (não possui vírgula a separando de outras produções), para de ignorar os últimos 2 caracteres (,\n) e passa a igorar somente o último (\n)
            if  linha[-2] != ',':
                qtd_de_caracteres_finais_ignorados = -1
                ultima_linha_significativa = True

            # Verifica se a linha é da forma sintaticamente correta
            if re.fullmatch(".+ -> .*\n?", linha) is None:
                print("Erro: Alguma produção dada não é da forma correta")
                continuar_execucao = False
                break

            # verifica se o lado esquerdo da produção é uma variável
            if VerificaSeLadoEsquerdoEInvalido(linha[0:linha.find(" -> ")],variaveis):
                print("Erro: Lado esquerdo de alguma produção é inválido")
                continuar_execucao = False
                break

            # verifica se o lado esquerdo da produção é um vazio, um terminal, ou um terminal e uma variável
            if VerificaSeLadoDireitoEInvalido(linha[linha.find(" -> ")+4:], terminal_max_len, variavel_max_len, qtd_de_caracteres_finais_ignorados, terminais, variaveis):
                continuar_execucao = False
                break

            producoes.append(linha[:qtd_de_caracteres_finais_ignorados])

        if not sintaxe_de_fim_correta:
            print("Erro: conjunto de produções não tem caractere terminador '}'")
            continuar_execucao = False
            break
        
        if not continuar_execucao:
            break

        print(variaveis)
        print(terminais)
        print(producoes)
        print(simbolo_inicial)
        
        continuar_execucao = False

# pedir para selecionar o arquivo da GLUD ou sair
# verificar se é válido
# construir AFD
# pedir para selecionar o arquivo de palavras ou uma nova GLUD ou sair
# rodar no AFD e apresentar quais palavras pertencem à linguagem e repetir o pedido