import pygame


class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade, vida, vida_max):
        super().__init__()
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.vida = vida
        self.vida_max = vida_max
        self.index_animacao = 0
        self.velocidade_animacao = 0.14
        self.estado = 'parado'
        self.sprites = {}

    def animar(self):
        if self.estado in self.sprites:
            animacao = self.sprites[self.estado]
            if not animacao:
                return

            self.index_animacao += self.velocidade_animacao
            if self.index_animacao >= len(animacao):
                self.index_animacao = 0

            self.image = animacao[int(self.index_animacao)]
            centro = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = centro
