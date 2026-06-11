import pygame

class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade, vida, vida_max):
        super().__init__()
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.vida = vida
        self.vida_max = vida_max
        
        # Atributos de estado e animação compartilhados
        self.index_animacao = 0
        self.tempo_animacao = 0
        self.estado = 'parado'
        self.sprites = {}
        
        # Superfície padrão para evitar que o PyGame quebre antes do carregamento das imagens
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.copy()

    def animar(self):
        # Cada classe filha (Jogador/Inimigo) implementará ou estenderá sua própria lógica de chaves de animação
        pass
