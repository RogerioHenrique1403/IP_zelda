import pygame
import pytmx
import os

class Mapa:
    def __init__(self, arquivo_tmx):
        # Resolve o caminho do arquivo de forma segura
        diretorio_rsc = os.path.dirname(os.path.abspath(__file__))
        caminho_completo = os.path.normpath(os.path.join(diretorio_rsc, arquivo_tmx))
        
        try:
            # Carrega os dados do arquivo TMX
            self.tmx_data = pytmx.util_pygame.load_pygame(caminho_completo)
            self.largura = self.tmx_data.width * self.tmx_data.tilewidth
            self.altura = self.tmx_data.height * self.tmx_data.tileheight
        except Exception as e:
            print(f"ERRO ao carregar o mapa {arquivo_tmx}: {e}")
            self.tmx_data = None

    def desenhar(self, tela):
        """ Desenha todas as camadas do mapa na tela """
        if not self.tmx_data:
            return

        for camada in self.tmx_data.visible_layers:
            # Apenas desenha se for uma camada de Tiles
            if isinstance(camada, pytmx.TiledTileLayer):
                for x, y, gid in camada:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tela.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))
            #se você tiver camadas de objetos ou imagens, adicionamos a logica aqui
