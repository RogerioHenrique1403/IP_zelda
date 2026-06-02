import pygame
import os
from pytmx.util_pygame import load_pygame


class Mapa:
    def __init__(self, nome_arquivo):
        self.mapa_dados = None
        self.superficie = None
        self.cor_fundo_padrao = (34, 139, 34)  # Verde grama

        self.carregar_mapa(nome_arquivo)

    def carregar_mapa(self, nome_arquivo):
        """ Carrega o arquivo .tmx e já gera a imagem otimizada do mapa """
        try:
            # Garante que o Python ache o arquivo independente de onde o jogo for aberto
            diretorio_script = os.path.dirname(os.path.abspath(__file__))
            caminho_mapa = os.path.join(diretorio_script, nome_arquivo)

            self.mapa_dados = load_pygame(caminho_mapa)
            self.superficie = self.criar_superficie()
            print(f"--- SUCESSO: Mapa '{nome_arquivo}' carregado! ---")

        except Exception as e:
            print(f"ERRO AO CARREGAR O MAPA '{nome_arquivo}': {e}")

    def criar_superficie(self):
        """ Desenha todos os blocos do Tiled em uma única imagem grande (Otimização) """
        if not self.mapa_dados:
            return None

        # Calcula o tamanho total do mapa em pixels
        largura_mapa = self.mapa_dados.width * self.mapa_dados.tilewidth
        altura_mapa = self.mapa_dados.height * self.mapa_dados.tileheight

        # Cria uma superfície (quadro) do tamanho exato do mapa
        # pygame.SRCALPHA permite que o mapa tenha transparência, se necessário
        superficie = pygame.Surface(
            (largura_mapa, altura_mapa), pygame.SRCALPHA)
        superficie.fill(self.cor_fundo_padrao)

        # Passa por todas as camadas criadas lá no Tiled
        for layer in self.mapa_dados.visible_layers:
            # Verifica se a camada é uma camada de blocos (Tiles)
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    # Multiplica a posição X e Y pelo tamanho do bloco (ex: 16x16)
                    pos_x = x * self.mapa_dados.tilewidth
                    pos_y = y * self.mapa_dados.tileheight
                    # "Carimba" o bloco na superfície gigante
                    superficie.blit(surf, (pos_x, pos_y))

        return superficie

    def desenhar(self, tela, pos_x=0, pos_y=0):
        """ Desenha o mapa inteiro na tela do jogo """
        if self.superficie:
            # Desenha a imagem gerada na posição pedida
            tela.blit(self.superficie, (pos_x, pos_y))
        else:
            # Se deu erro ao carregar, desenha só um fundo verde para o jogo não quebrar
            tela.fill(self.cor_fundo_padrao)
