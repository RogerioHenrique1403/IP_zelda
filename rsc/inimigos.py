import pygame
import os
from personagem import Personagem

class Inimigo(Personagem):
    def __init__(self, x, y, interface, tipo='python'):
        vida = 80
        velocidade = 2.0
        self.hitbox_rect = (48, 48)

        super().__init__(x, y, velocidade=velocidade, vida=vida, vida_max=vida)

        self.tipo = tipo
        self.raio_visao = 300
        self.dano = 10
        self.alcance_ataque = 25
        self.cooldown_ataque = 1000
        self.ultimo_ataque = 0

        # Sistema de dano e de stun
        self.invencivel = False
        self.cooldown_hit = 400   
        self.stunado = False      
        self.tempo_stun = 0
        self.duracao_stun = 500   
        self.morto_completamente = False

        self.direcao = 'baixo'
        self.sprites = {}

        # Carregar sprites
        try:
            diretorio_script = os.path.dirname(os.path.abspath(__file__))
            caminho_pasta = os.path.join(diretorio_script, '..', 'res', 'Inimigos sprite', 'Python sprite')

            # Cada tira de caminhada tem 4 frames
            andando_baixo = self.carregar_tira(os.path.join(caminho_pasta, 'python_walking_down.png'), 4)
            andando_cima = self.carregar_tira(os.path.join(caminho_pasta, 'python_walking_up.png'), 4)
            andando_direita = self.carregar_tira(os.path.join(caminho_pasta, 'python_walking_right.png'), 4)
            
            # Direção esquerda é a direção direita espelhada horizontalmente
            andando_esquerda = [pygame.transform.flip(img, True, False) for img in andando_direita]

            self.sprites['andando_baixo'] = andando_baixo
            self.sprites['andando_cima'] = andando_cima
            self.sprites['andando_direita'] = andando_direita
            self.sprites['andando_esquerda'] = andando_esquerda

            # Parado usa o primeiro frame de andar correspondente
            self.sprites['parado_baixo'] = [andando_baixo[0]]
            self.sprites['parado_cima'] = [andando_cima[0]]
            self.sprites['parado_direita'] = [andando_direita[0]]
            self.sprites['parado_esquerda'] = [andando_esquerda[0]]

            # Atacando usa os mesmos frames de andar
            self.sprites['atacando_baixo'] = andando_baixo
            self.sprites['atacando_cima'] = andando_cima
            self.sprites['atacando_direita'] = andando_direita
            self.sprites['atacando_esquerda'] = andando_esquerda

            # Tira de morte (4 frames)
            self.sprites['morrendo'] = self.carregar_tira(os.path.join(caminho_pasta, 'python_death.png'), 4)

            self.image = self.sprites['parado_baixo'][0]

        except Exception as e:
            print(f"ERRO AO CARREGAR SPRITES DO INIMIGO PYTHON: {e}")
            # Placeholder visual caso falhe o carregamento
            self.image = pygame.Surface((96, 96), pygame.SRCALPHA)
            self.image.fill((255, 0, 0))
            self.sprites = {
                'parado_baixo': [self.image],
                'parado_cima': [self.image],
                'parado_direita': [self.image],
                'parado_esquerda': [self.image],
                'andando_baixo': [self.image],
                'andando_cima': [self.image],
                'andando_direita': [self.image],
                'andando_esquerda': [self.image],
                'atacando_baixo': [self.image],
                'atacando_cima': [self.image],
                'atacando_direita': [self.image],
                'atacando_esquerda': [self.image],
                'morrendo': [self.image]
            }

        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(x, y, *self.hitbox_rect)
        self.hitbox.center = self.rect.center

    def carregar_tira(self, caminho_completo, quantidade_frames, target_size=(96, 96)):
        if not os.path.exists(caminho_completo):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_completo}")

        sheet = pygame.image.load(caminho_completo).convert_alpha()
        w, h = sheet.get_size()

        # Remove background (Cluster A: light gray, Cluster B: medium gray)
        for x in range(w):
            for y in range(h):
                r, g, b, a = sheet.get_at((x, y))
                is_light = (210 <= r <= 245) and (210 <= g <= 245) and (210 <= b <= 245)
                is_medium = (135 <= r <= 175) and (135 <= g <= 175) and (135 <= b <= 175)
                if is_light or is_medium:
                    sheet.set_at((x, y), (0, 0, 0, 0))

        largura_frame = w // quantidade_frames
        altura_frame = h

        imagens = []
        for i in range(quantidade_frames):
            corte = sheet.subsurface((i * largura_frame, 0, largura_frame, altura_frame))
            img_escalada = pygame.transform.scale(corte, target_size)
            imagens.append(img_escalada)

        return imagens

    def update(self, jogador):
        self.cooldowns()

        if self.estado == 'morrendo':
            self.animar()
            return

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

            # Determina a direção com base no vetor de movimento
            if abs(dx) > abs(dy):
                self.direcao = 'direita' if dx > 0 else 'esquerda'
            else:
                self.direcao = 'baixo' if dy > 0 else 'cima'
        else:
            self.estado = 'parado'

        self.hitbox.centerx = int(self.x)
        self.hitbox.centery = int(self.y)
        self.rect.center = self.hitbox.center  

        self.animar()

    def animar(self):
        chave = f"{self.estado}_{self.direcao}"
        if self.estado == 'morrendo':
            chave = 'morrendo'

        if chave in self.sprites and self.sprites[chave]:
            animacao = self.sprites[chave]
            
            # Usamos um valor fixo local para os inimigos não dependerem da classe mãe
            velocidade_animacao_inimigo = 0.15 
            self.index_animacao += velocidade_animacao_inimigo
            
            if self.index_animacao >= len(animacao):
                if self.estado == 'morrendo':
                    self.index_animacao = len(animacao) - 1
                    self.morto_completamente = True
                else:
                    self.index_animacao = 0

            if self.index_animacao < len(animacao):
                self.image = animacao[int(self.index_animacao)]

    def atacar(self, jogador):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_ataque > self.cooldown_ataque:
            jogador.vida -= self.dano
            self.ultimo_ataque = agora

    def receber_dano(self, quantidade):
        if not self.invencivel and self.estado != 'morrendo':
            self.vida -= quantidade
            self.stunado = True
            self.invencivel = True

            agora = pygame.time.get_ticks()
            self.tempo_stun = agora
            self.tempo_invencivel = agora

            # Knockback reativo apenas se estiver vivo
            if self.vida > 0:
                self.x += 20 if self.direcao == 'esquerda' else -20
            else:
                self.estado = 'morrendo'
                self.index_animacao = 0

    def cooldowns(self):
        agora = pygame.time.get_ticks()
        if self.stunado and agora - self.tempo_stun >= self.duracao_stun:
            self.stunado = False
        if self.invencivel and agora - self.tempo_invencivel >= self.cooldown_hit:
            self.invencivel = False
