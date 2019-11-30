# -*- coding: utf-8 -*-

""" EXECUTAR UTILIZANDO PYTHON 3 """

from math import inf as infinity
from random import choice
import platform
from os import system


class vitoriasCPU(object):
    qtd = 0

    def processo(self):
        self.qtd = 1


class vitoriasPessoa(object):
    qtd = 0

    def processo(self):
        self.qtd = 1


Pessoa = -1
CPU = +1
Tabuleiro = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def definir_valor(estado):
    """
      Função responsável por avaliar a heurítica do estado.
      variavel estado: o estado do atual Tabuleiro
      se o computador verificarVencedor retorna +1 / se a Pessoa verificarVencedor retorna -1; 0 empate
    """
    if verificaVencedor(estado, CPU):
        pontos = +1
    elif verificaVencedor(estado, Pessoa):
        pontos = -1
    else:
        pontos = 0

    return pontos


def verificaVencedor(estado, jogador):
    """
    Função responsável por verificar se algum jogador venceu. Possibilidades:
      Três linhas, colunas ou diagonais [X X X] ou [O O O]
      estado: o estado do atual Tabuleiro
      jogador: a Pessoa ou um computador
      retorna True se o jogador verificarVencedor
    """
    estadosVitoriosos = [
        [estado[0][0], estado[0][1], estado[0][2]],
        [estado[1][0], estado[1][1], estado[1][2]],
        [estado[2][0], estado[2][1], estado[2][2]],
        [estado[0][0], estado[1][0], estado[2][0]],
        [estado[0][1], estado[1][1], estado[2][1]],
        [estado[0][2], estado[1][2], estado[2][2]],
        [estado[0][0], estado[1][1], estado[2][2]],
        [estado[2][0], estado[1][1], estado[0][2]],
    ]
    if [jogador, jogador, jogador] in estadosVitoriosos:
        return True
    else:
        return False


def fimdeJogo(estado):
    """
    Esta função testa se o Pessoa ou o computador venceu, ou seja fim de jogo
    """
    return verificaVencedor(estado, Pessoa) or verificaVencedor(estado, CPU)


def camposVazios(estado):
    """
      Recebe como parametro o estado atual
      Cada campo vazio será adicionado à lista de campos
    """
    campos = []

    for x, linha in enumerate(estado):
        for y, campo in enumerate(linha):
            if campo == 0:
                campos.append([x, y])

    return campos


def movimentacaoValida(x, y):
    """
      Funcao responsavel por validar jogada, só é valido se o campo for vazio
    """
    if [x, y] in camposVazios(Tabuleiro):
        return True
    else:
        return False


def definirMovimento(x, y, jogador):
    """
    Funcao responsavel por movimentar / jogar, recebendo como paramentro as coordenadas das jogadas
    """
    if movimentacaoValida(x, y):
        Tabuleiro[x][y] = jogador
        return True
    else:
        return False


def minimax(estado, profundidade_arvore, jogador):
    """
    Funcao minimax, responsavel por escolher o melhor movimento / jogada possivel
    """
    if jogador == CPU:
        melhorPossivel = [-1, -1, -infinity]
    else:
        melhorPossivel = [-1, -1, +infinity]

    if profundidade_arvore == 0 or fimdeJogo(estado):
        pontos = definir_valor(estado)
        return [-1, -1, pontos]

    for campo in camposVazios(estado):
        x, y = campo[0], campo[1]
        estado[x][y] = jogador
        pontos = minimax(estado, profundidade_arvore - 1, -jogador)
        estado[x][y] = 0
        pontos[0], pontos[1] = x, y

        if jogador == CPU:
            if pontos[2] > melhorPossivel[2]:
                melhorPossivel = pontos
        else:
            if pontos[2] < melhorPossivel[2]:
                melhorPossivel = pontos

    return melhorPossivel


def limparConsole():
    sistemaOperacional = platform.system().lower()
    if 'windows' in sistemaOperacional:
        system('cls')
    else:
        system('clear')


def imprimirTabuleiro(estado, escolhaCPU, escolhaPessoa):
    """ Funcao responsavel por imprimir o tabuleiro no console """
    legenda = {
        -1: escolhaPessoa,
        +1: escolhaCPU,
        0: ' '
    }
    tracos = '---------------'

    print('\n' + tracos)
    for linha in estado:
        for campo in linha:
            simbolo = legenda[campo]
            print(f"| {simbolo} |", end='')
        print('\n' + tracos)


def jogadadoComputador(escolhaCPU, escolhaPessoa):
    """ Funcao responsavel por realizar a jogada do computador, se a profundidade for menor que 9 , é escolhida uma coordenada aleatoria """
    profundidade_arvore = len(camposVazios(Tabuleiro))
    if profundidade_arvore == 0 or fimdeJogo(Tabuleiro):
        return

    limparConsole()
    print(f'Vez da CPU [{escolhaCPU}]')
    imprimirTabuleiro(Tabuleiro, escolhaCPU, escolhaPessoa)

    if profundidade_arvore == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        movimento = minimax(Tabuleiro, profundidade_arvore, CPU)
        x, y = movimento[0], movimento[1]

    definirMovimento(x, y, CPU)


def jogadadaPessoa(escolhaCPU, escolhaPessoa):
    """ Jogada da pessoa, sendo possivel somente jogar em uma posicao valida, ou seja, vazia """
    profundidade_arvore = len(camposVazios(Tabuleiro))
    if profundidade_arvore == 0 or fimdeJogo(Tabuleiro):
        return

    # Movimentacoes validas
    movimento = -1
    movimentos = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    limparConsole()
    print(f'Sua vez [{escolhaPessoa}]')
    imprimirTabuleiro(Tabuleiro, escolhaCPU, escolhaPessoa)

    while movimento < 1 or movimento > 9:
        try:
            movimento = int(
                input('Escolha de acordo com as posicoes do numpad, de 1 a 9:  '))
            xydoMovimento = movimentos[movimento]
            movimentoValido = definirMovimento(
                xydoMovimento[0], xydoMovimento[1], Pessoa)

            if not movimentoValido:
                print('Não foi possivel movimentar para o local desejado')
                movimento = -1
        except (EOFError, KeyboardInterrupt):
            print('erro')
            exit()
        except (KeyError, ValueError):
            print('erro')


def main():
    """ Funcao main, resposnsavel por estruturar o jogo """
    limparConsole()
    escolhaPessoa = ''  # X ou O
    escolhaCPU = ''  # X ou O
    comeca = '' 

    while escolhaPessoa != 'O' and escolhaPessoa != 'X':
        try:
            print('')
            escolhaPessoa = input('Você deseja ser X ou O: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('erro')
            exit()
        except (KeyError, ValueError):
            print('erro')

    # Define qual será a opcao do computador
    if escolhaPessoa == 'X':
        escolhaCPU = 'O'
    else:
        escolhaCPU = 'X'

    limparConsole()
    while comeca != 'Y' and comeca != 'N':
        try:
            comeca = input('Voce deseja começar? [y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('erro')
            exit()
        except (KeyError, ValueError):
            print('erro')

    # Loop de funcoes do jogo
    while len(camposVazios(Tabuleiro)) > 0 and not fimdeJogo(Tabuleiro):
        if comeca == 'N':
            jogadadoComputador(escolhaCPU, escolhaPessoa)
            comeca = ''

        jogadadaPessoa(escolhaCPU, escolhaPessoa)
        jogadadoComputador(escolhaCPU, escolhaPessoa)

    if verificaVencedor(Tabuleiro, Pessoa):
        limparConsole()
        print(f'Sua vez [{escolhaPessoa}]')
        imprimirTabuleiro(Tabuleiro, escolhaCPU, escolhaPessoa)
        vitoriasPessoa.qtd += 1
        print('Você Venceuu!!!')
    elif verificaVencedor(Tabuleiro, CPU):
        limparConsole()
        print(f'Vez da CPU [{escolhaCPU}]')
        imprimirTabuleiro(Tabuleiro, escolhaCPU, escolhaPessoa)
        vitoriasCPU.qtd += 1
        print('Você Perdeuu!')
    else:
        limparConsole()
        imprimirTabuleiro(Tabuleiro, escolhaCPU, escolhaPessoa)
        print('Empatou!')
    print('Placar: Pessoa ' + str(vitoriasPessoa.qtd) +
          ' x ' + str(vitoriasCPU.qtd) + ' CPU')


def continuarJogando():
    jogar = input('Deseja continuar? [y/n]').upper()
    while jogar != 'Y' and jogar != 'N':
        jogar = input('Digite um valor valido? [y/n]').upper()
    return jogar


main()
jogar = continuarJogando()

while jogar == 'Y':
    Tabuleiro = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    main()
    jogar = continuarJogando()
