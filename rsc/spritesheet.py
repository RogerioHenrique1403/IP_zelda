import pygame

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def pegar_imagem(self, frame, linha, largura, altura, escala):
        img = pygame.Surface((largura, altura), pygame.SRCALPHA)

        # Desenha o recorte na superfície transparente
        img.blit(self.sheet, (0, 0), ((frame * largura), (linha * altura), largura, altura))

        # Aumenta o tamanho (escala)
        img = pygame.transform.scale(img, (largura * escala, altura * escala))

        return img
