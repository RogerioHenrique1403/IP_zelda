import pygame
import os

class Coletavel(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo, nome_arquivo):
        super().__init__()
        self.tipo = tipo
        
        diretorio_rsc = os.path.dirname(os.path.abspath(__file__))
        diretorio_raiz = os.path.dirname(diretorio_rsc)
        caminho_imagem = os.path.join(diretorio_raiz, 'res', 'items', nome_arquivo)
        
        
        imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
        self.image = pygame.transform.scale(imagem_original, (32, 32))
            
        self.rect = self.image.get_rect(topleft=(x, y))
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