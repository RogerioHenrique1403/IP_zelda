import pygame
import sys
from jogo import Jogo
from interface import Interface


def main():
    pygame.init()

    # 1. Ao criar a Interface, ela já cria a tela e carrega as imagens sozinhas
    interface = Interface()

    # 2. Pegamos a tela que a interface criou para passar pro Jogo
    tela_do_jogo = interface.tela

    # 3. Passamos tudo para o Jogo
    jogo = Jogo(tela_do_jogo, interface)

    jogo.run()


if __name__ == '__main__':
    main()
