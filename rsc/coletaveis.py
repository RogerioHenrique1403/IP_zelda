import pygame
import os

class Coletavel(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo, nome_arquivo=None):
        super().__init__()
        self.tipo = tipo
        self.x = x
        self.y = y

        diretorio_rsc = os.path.dirname(os.path.abspath(__file__))
        diretorio_raiz = os.path.dirname(diretorio_rsc)
        self.pasta_coletaveis = os.path.join(diretorio_raiz, 'res', 'Coletaveis')

        # carrega a imagem inicial (pode ser None)
        self._carregar_imagem(nome_arquivo)

        # define rect e hitbox com a posição passada
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.copy()

    def _carregar_imagem(self, nome_arquivo):
        caminho_imagem = None
        if nome_arquivo:
            possivel = os.path.join(self.pasta_coletaveis, nome_arquivo)
            if os.path.exists(possivel):
                caminho_imagem = possivel

        if caminho_imagem is None:
            try:
                for f in os.listdir(self.pasta_coletaveis):
                    if f.lower().endswith('.png'):
                        caminho_imagem = os.path.join(self.pasta_coletaveis, f)
                        break
            except FileNotFoundError:
                caminho_imagem = None

        if caminho_imagem and os.path.exists(caminho_imagem):
            try:
                imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
                self.image = pygame.transform.scale(imagem_original, (32, 32))
            except Exception:
                surf = pygame.Surface((32, 32), pygame.SRCALPHA)
                surf.fill((255, 0, 255, 255))
                self.image = surf
        else:
            surf = pygame.Surface((32, 32), pygame.SRCALPHA)
            surf.fill((255, 0, 255, 255))  # magenta visível para depuração
            self.image = surf

    def atualizar_imagem(self, nome_arquivo):
        """Atualiza a sprite do coletável em tempo de execução, preservando o centro atual."""
        old_center = None
        if hasattr(self, 'rect') and self.rect:
            old_center = self.rect.center

        self._carregar_imagem(nome_arquivo)

        if old_center:
            self.rect = self.image.get_rect(center=old_center)
            self.hitbox = self.rect.copy()
        else:
            # se não tinha rect, usa posição inicial
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
            self.hitbox = self.rect.copy()

#classe do npc
class Npc(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        diretorio_rsc = os.path.dirname(os.path.abspath(__file__))
        diretorio_raiz = os.path.dirname(diretorio_rsc)
        caminho_imagem = os.path.join(diretorio_raiz, 'res', 'npc', 'npc.png')
        
        imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
        
        #Criação do npc
        self.image = pygame.transform.scale(imagem_original, (120, 120))
        
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.copy()

class Coracao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Cria um quadrado de 16x16 pixels
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 20, 147)) # Cor Rosa Choque (Deep Pink)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.copy()