import pygame
import os
from personagem import Personagem
from spritesheet import SpriteSheet

class Inimigo(Personagem):
    def __init__(self, x, y, interface, tipo='slime'):
        if tipo == 'morcego':
            vida = 30
            velocidade = 2.5
            img_arquivo = 'BatAnim.png'
            frames_idle = 4
            frames_run = 4
            self.hitbox_rect = (32, 20)
        else:  # Slime
            vida = 50
            velocidade = 2
            img_arquivo = 'SlimeAnim.png'
            frames_idle = 4
            frames_run = 4
            self.hitbox_rect = (40, 25)

        super().__init__(x, y, velocidade=velocidade, vida=vida, vida_max=vida)

        self.tipo = tipo
        self.raio_visao = 300
        self.dano = 10
        self.alcance_ataque = 20
        self.cooldown_ataque = 1000
        self.ultimo_ataque = 0

        #sistema de dano e de stun
        self.invencivel = False
        self.cooldown_hit = 400   
        self.stunado = False      
        self.tempo_stun = 0
        self.duracao_stun = 500   

        #carregar sprites
        tamanho_sprite = 32
        escala = 2

        try:
            diretorio_script = os.path.dirname(os.path.abspath(__file__))
            caminho = os.path.join(diretorio_script, '..', 'res', 'Enemies', img_arquivo)

            if not os.path.exists(caminho):
                raise FileNotFoundError

            img_sheet = pygame.image.load(caminho).convert_alpha()
            img_sheet.set_colorkey((0, 0, 0))  

            sheet = SpriteSheet(img_sheet)
            self.sprites = {'parado': [], 'andando': []}

            for i in range(frames_idle):
                self.sprites['parado'].append(sheet.pegar_imagem(i, 0, tamanho_sprite, tamanho_sprite, escala))

            for i in range(frames_run):
                self.sprites['andando'].append(sheet.pegar_imagem(i, 1, tamanho_sprite, tamanho_sprite, escala))

            self.sprites['atacando'] = self.sprites['andando']
            self.image = self.sprites['parado'][0]

        except Exception:
            #caso ele não encontre a imagem
            self.image = pygame.Surface((32, 32))
            if tipo == 'morcego':
                self.image.fill((105, 105, 105)) # Cinza para o morcego
            else:
                self.image.fill((0, 0, 255)) # Azul para o slime
                
            self.sprites = {'parado': [self.image], 'andando': [self.image], 'atacando': [self.image]}

        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(x, y, *self.hitbox_rect)
        self.hitbox.center = self.rect.center
        self.virado_esquerda = False

    def update(self, jogador):
        self.cooldowns()

        if self.stunado:
            return

        alvo_rect = getattr(jogador, 'hitbox', jogador.rect)
        dx = alvo_rect.centerx - self.hitbox.centerx
        dy = alvo_rect.centery - self.hitbox.centery
        distancia = (dx**2 + dy**2)**0.5

        if distancia < self.raio_visao:
            if distancia > self.alcance_ataque:
                if distancia > 0:  
                    self.x += (dx / distancia) * self.velocidade
                    self.y += (dy / distancia) * self.velocidade
                self.estado = 'andando'
            else:
                self.estado = 'atacando'
                self.atacar(jogador)

            self.virado_esquerda = dx < 0
        else:
            self.estado = 'parado'

        self.hitbox.centerx = int(self.x)
        self.hitbox.centery = int(self.y)
        self.rect.center = self.hitbox.center  

        self.animar()
        if self.virado_esquerda:
            self.image = pygame.transform.flip(self.image, True, False)

    def animar(self):
            if self.estado in self.sprites and self.sprites[self.estado]:
                animacao = self.sprites[self.estado]
                
                # Usamos um valor fixo local para os inimigos não dependerem da classe mãe
                velocidade_animacao_inimigo = 0.15 
                self.index_animacao += velocidade_animacao_inimigo
                
                if self.index_animacao >= len(animacao):
                    self.index_animacao = 0
                self.image = animacao[int(self.index_animacao)]

    def atacar(self, jogador):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_ataque > self.cooldown_ataque:
            jogador.vida -= self.dano
            self.ultimo_ataque = agora

    def receber_dano(self, quantidade):
        if not self.invencivel:
            self.vida -= quantidade
            self.stunado = True
            self.invencivel = True

            agora = pygame.time.get_ticks()
            self.tempo_stun = agora
            self.tempo_invencivel = agora

            # Knockback reativo
            self.x += 20 if self.virado_esquerda else -20

            if self.vida <= 0:
                self.kill()

    def cooldowns(self):
        agora = pygame.time.get_ticks()
        if self.stunado and agora - self.tempo_stun >= self.duracao_stun:
            self.stunado = False
        if self.invencivel and agora - self.tempo_invencivel >= self.cooldown_hit:
            self.invencivel = False
