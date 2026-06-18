import os
import pygame
import pytmx


class Mapa:
    def __init__(self, arquivo):
        # Resolve o caminho do arquivo de forma segura
        diretorio_rsc = os.path.dirname(os.path.abspath(__file__))
        caminho_completo = os.path.normpath(os.path.join(diretorio_rsc, arquivo))

        self.tmx_data = None
        self.imagem = None

        try:
            if arquivo.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".webp")):
                self.imagem = pygame.image.load(caminho_completo).convert()
                self.largura = self.imagem.get_width()
                self.altura = self.imagem.get_height()
            else:
                self.tmx_data = pytmx.util_pygame.load_pygame(caminho_completo)
                self.largura = self.tmx_data.width * self.tmx_data.tilewidth
                self.altura = self.tmx_data.height * self.tmx_data.tileheight
        except Exception as e:
            print(f"ERRO ao carregar o mapa {arquivo}: {e}")
            self.tmx_data = None
            self.imagem = None

    def desenhar(self, tela):
        """Desenha o mapa na tela, seja ele TMX ou imagem de fundo."""
        if self.imagem:
            tela.blit(self.imagem, (0, 0))
            return

        if not self.tmx_data:
            return

        for camada in self.tmx_data.visible_layers:
            if isinstance(camada, pytmx.TiledTileLayer):
                for x, y, gid in camada:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tela.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))
