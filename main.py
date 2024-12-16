import sys
import tkinter as tk
from tkinter import filedialog
from GLUD_reader import LeArquivoGLUD
from AFDCreator import makeAF
from conversions import nfaε_to_nfa, nfa_to_dfa
from models import DFA


def read_file(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        return file.read().split(',')


def recognize_word(M: DFA, w: str) -> bool:
    state = M.q0
    for c in w:
        state = M.δ[state].get(c)
        if state is None:
            return False
    return state in M.F


def prompt_file(prompt, filetypes):
    if input(prompt).lower() != 's':
        sys.exit("Programa encerrado.")
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        filetypes=filetypes, title="Selecione um arquivo")
    if not file_path:
        sys.exit("Nenhum arquivo selecionado.")
    return file_path


if __name__ == "__main__":
    grammar_file_path = prompt_file(
        prompt="Deseja iniciar a leitura de uma GLUD? "
        "(s para iniciar, qualquer outro input para fechar o programa): ",
        filetypes=[("Arquivos de texto", "*.txt"),
                   ("Todos os arquivos", "*.*")]
    )

    words_file_path = prompt_file(
        prompt="Deseja iniciar a leitura de um arquivo de palavras? "
        "(s para iniciar, qualquer outro input para fechar o programa): ",
        filetypes=[("Arquivos de texto", ["*.txt", "*.csv"]),
                   ("Todos os arquivos", "*.*")]
    )

    G = LeArquivoGLUD(grammar_file_path)
    M = nfa_to_dfa(nfaε_to_nfa(makeAF(G)))

    words = read_file(words_file_path)
    aceita = [w for w in words if recognize_word(M, w)]
    rejeita = [w for w in words if w not in aceita]

    print(f"\nW = {{{','.join(words)}}}")
    print("\nW ∩ ACEITA(M):", *aceita, sep="\n")
    print("\nW ∩ REJEITA(M):", *rejeita, sep="\n")
