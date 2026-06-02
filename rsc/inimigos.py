import pygame
import os
from personagem import Personagem
from spritesheet import SpriteSheet

class Inimigo(Personagem):
    def __init__(self, x, y, interface, tipo='slime'):
        if tipo == 'morcego':
            vida = 30
            velocidade = 3
            img_arquivo = 'BatAnim.png'
            frames_idle = 4
            frames_run = 4
            self.hitbox_rect = (32, 20)  # Largura, Altura da hitbox
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

        # --- SISTEMA DE DANO E STUN ---
        self.invencivel = False
        self.cooldown_hit = 400   # Tempo invencível após levar hit
        self.stunado = False      # Estado de atordoamento
        self.tempo_stun = 0
        self.duracao_stun = 500   # 500ms parado

        # --- CARREGAMENTO DE SPRITES ---
        tamanho_sprite = 32
        escala = 2

        try:
            # Garante o caminho correto independente do SO
            diretorio_script = os.path.dirname(os.path.abspath(__file__))
            # Caminho: .../res/Enemies/SlimeAnim.png
            caminho = os.path.join(
                diretorio_script, '..', 'res', 'Enemies', img_arquivo)

            img_sheet = pygame.image.load(caminho).convert_alpha()
            img_sheet.set_colorkey((0, 0, 0))  # Remove fundo preto

            sheet = SpriteSheet(img_sheet)
            self.sprites = {}

            # Linha 0 = Parado
            self.sprites['parado'] = []
            for i in range(frames_idle):
                self.sprites['parado'].append(sheet.pegar_imagem(
                    i, 0, tamanho_sprite, tamanho_sprite, escala))

            # Linha 1 = Andando
            self.sprites['andando'] = []
            for i in range(frames_run):
                self.sprites['andando'].append(sheet.pegar_imagem(
                    i, 1, tamanho_sprite, tamanho_sprite, escala))

            # Reutiliza andando para atacar por enquanto
            self.sprites['atacando'] = self.sprites['andando']

            self.image = self.sprites['parado'][0]

        except Exception as e:
            print(f"ERRO INIMIGO ({tipo}): {e}")
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 0, 0))
            self.sprites = {'parado': [self.image], 'andando': [
                self.image], 'atacando': [self.image]}

        # --- HITBOX ---
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(x, y, *self.hitbox_rect)
        self.hitbox.center = self.rect.center
        self.virado_esquerda = False

    def update(self, jogador):
        # 1. Gerencia temporizadores (Invencibilidade e Stun)
        self.cooldowns()

        # 2. SE ESTIVER STUNADO, NÃO FAZ NADA!
        if self.stunado:
            return

        # 3. COMPORTAMENTO NORMAL (Perseguir e Atacar)
        alvo_rect = getattr(jogador, 'hitbox', jogador.rect)

        dx = alvo_rect.centerx - self.hitbox.centerx
        dy = alvo_rect.centery - self.hitbox.centery
        distancia = (dx**2 + dy**2)**0.5

        if distancia < self.raio_visao:
            if distancia > self.alcance_ataque:
                # Move na direção do jogador
                if distancia > 0:  # Evita divisão por zero
                    self.x += (dx / distancia) * self.velocidade
                    self.y += (dy / distancia) * self.velocidade

                self.estado = 'andando'
            else:
                self.estado = 'atacando'
                self.atacar(jogador)

            # Define o lado que está olhando
            if dx < 0:
                self.virado_esquerda = True
            else:
                self.virado_esquerda = False
        else:
            self.estado = 'parado'

        # Atualiza posições
        self.hitbox.centerx = int(self.x)
        self.hitbox.centery = int(self.y)
        self.rect.center = self.hitbox.center  # O sprite segue a hitbox

        # Animação e Espelhamento
        self.animar()
        if self.virado_esquerda:
            self.image = pygame.transform.flip(self.image, True, False)

    def atacar(self, jogador):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_ataque > self.cooldown_ataque:
            # Verifica se o jogador tem o método receber_dano, se não, tira vida direto
            if hasattr(jogador, 'receber_dano'):
                jogador.receber_dano(self.dano)
            else:
                jogador.vida -= self.dano

            self.ultimo_ataque = agora

    def receber_dano(self, quantidade):
        if not self.invencivel:
            self.vida -= quantidade

            # --- ATIVA O STUN E INVENCIBILIDADE ---
            self.stunado = True
            self.invencivel = True

            agora = pygame.time.get_ticks()
            self.tempo_stun = agora
            self.tempo_invencivel = agora

            # Knockback (Empurrãozinho para trás)
            if self.virado_esquerda:
                self.x += 20
            else:
                self.x -= 20

            if self.vida <= 0:
                self.kill()

    def cooldowns(self):
        agora = pygame.time.get_ticks()

        # Gerencia o fim do STUN
        if self.stunado:
            if agora - self.tempo_stun >= self.duracao_stun:
                self.stunado = False
                # print("Inimigo recuperado do stun!")

        # Gerencia o fim da invencibilidade
        if self.invencivel:
            if agora - self.tempo_invencivel >= self.cooldown_hit:
                self.invencivel = False
