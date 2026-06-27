import pygame
import os
from personagem import Personagem

class Jogador(Personagem):
    def __init__(self, x, y, interface):
        # Chama o construtor da classe mãe (Personagem)
        super().__init__(x, y, velocidade=4, vida=100, vida_max=100)

        self.escala = 3
        self.direcao = 'baixo'  # Guarda para onde o personagem está olhando

        # Controle de Animação
        self.velocidade_animacao = 9  # Quanto maior, mais lenta a animação
        self.velocidade_ataque = 4    # Ataque deve ser mais rápido

        # Controle de Ataque
        self.atacando = False
        self.pode_atacar = True
        self.cooldown_ataque = 500  # milissegundos
        self.ultimo_ataque = 0

        # Invencibilidade e Dano
        self.invencivel = False
        self.tempo_invencivel = 0
        self.cooldown_invencivel = 1000 # 1 segundo

        # Morte
        self.tempo_morte = 0
        self.morte_completa = False

        self.carregar_todas_imagens()

        # Configuração geométrica do jogador e da hitbox de colisão dos pés
        if 'parado_baixo' in self.sprites and self.sprites['parado_baixo']:
            self.image = self.sprites['parado_baixo'][0]
        else:
            self.image = pygame.Surface((32, 32))
            self.image.fill((0, 255, 0)) # Placeholder visual verde

        self.rect = self.image.get_rect()
        # A hitbox agora é baseada em self.x e self.y como centro
        self.hitbox = pygame.Rect(0, 0, 40, 20)
        self.hitbox.center = (int(self.x), int(self.y))

    def carregar_todas_imagens(self):
        try:
            diretorio_script = os.path.dirname(os.path.abspath(__file__))
            pasta_player = os.path.abspath(os.path.join(diretorio_script, '..', 'res', 'Player'))

            if not os.path.exists(pasta_player):
                print("AVISO: A pasta de assets do jogador não foi encontrada. Usando placeholders.")
                return

            pasta_run = os.path.join(pasta_player, 'Run')
            self.sprites['andando_baixo'] = self.carregar_tira(os.path.join(pasta_run, 'RunDown.png'), 6)
            self.sprites['andando_cima'] = self.carregar_tira(os.path.join(pasta_run, 'RunUp.png'), 6)
            self.sprites['andando_direita'] = self.carregar_tira(os.path.join(pasta_run, 'RunRight.png'), 6)
            self.sprites['andando_esquerda'] = self.carregar_tira(os.path.join(pasta_run, 'RunLeft.png'), 6)

            pasta_ataque = os.path.join(pasta_player, 'Attack')
            self.sprites['atacando_baixo'] = self.carregar_tira(os.path.join(pasta_ataque, 'AttackDown.png'), 6)
            self.sprites['atacando_cima'] = self.carregar_tira(os.path.join(pasta_ataque, 'AttackUp.png'), 6)
            self.sprites['atacando_direita'] = self.carregar_tira(os.path.join(pasta_ataque, 'AttackRight.png'), 6)
            self.sprites['atacando_esquerda'] = self.carregar_tira(os.path.join(pasta_ataque, 'AttackLeft.png'), 6)

            # Define os estados parados baseados no primeiro frame de movimento
            self.sprites['parado_baixo'] = [self.sprites['andando_baixo'][0]]
            self.sprites['parado_cima'] = [self.sprites['andando_cima'][0]]
            self.sprites['parado_direita'] = [self.sprites['andando_direita'][0]]
            self.sprites['parado_esquerda'] = [self.sprites['andando_esquerda'][0]]

        except Exception as e:
            print(f"ERRO PLAYER AO CARREGAR IMAGENS: {e}")
            self.sprites = {}

    def carregar_tira(self, caminho_completo, quantidade_frames):
        imagens = []
        if not os.path.exists(caminho_completo):
            surf = pygame.Surface((32, 32))
            surf.fill((255, 0, 255))
            return [surf] * quantidade_frames

        sheet = pygame.image.load(caminho_completo).convert_alpha()
        largura_frame = sheet.get_width() // quantidade_frames
        altura_frame = sheet.get_height()

        for i in range(quantidade_frames):
            corte = sheet.subsurface((i * largura_frame, 0, largura_frame, altura_frame))
            largura_nova = int(largura_frame * self.escala)
            altura_nova = int(altura_frame * self.escala)
            img_escalada = pygame.transform.scale(corte, (largura_nova, altura_nova))
            imagens.append(img_escalada)

        return imagens

    def entrada_teclado(self):
        if self.atacando:
            return

        keys = pygame.key.get_pressed()
        movendo = False
        estado_anterior = self.estado

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.velocidade
            self.direcao = 'cima'
            movendo = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.velocidade
            self.direcao = 'baixo'
            movendo = True
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.velocidade
            self.direcao = 'esquerda'
            movendo = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.velocidade
            self.direcao = 'direita'
            movendo = True

        if keys[pygame.K_SPACE] and self.pode_atacar:
            self.atacando = True
            self.pode_atacar = False
            self.ultimo_ataque = pygame.time.get_ticks()
            self.index_animacao = 0
            self.tempo_animacao = 0 # Reset importante para não pular frames
            self.estado = 'atacando'
            return

        if movendo:
            self.estado = 'andando'
        else:
            self.estado = 'parado'
        
        # Reset de timer se mudou o estado (ex: de parado para andando)
        if self.estado != estado_anterior:
            self.index_animacao = 0
            self.tempo_animacao = 0

    def cooldowns(self):
        agora = pygame.time.get_ticks()
        if not self.pode_atacar:
            if agora - self.ultimo_ataque >= self.cooldown_ataque:
                self.pode_atacar = True
        if self.invencivel:
            if agora - self.tempo_invencivel >= self.cooldown_invencivel:
                self.invencivel = False

    def animar(self):
        chave = f"{self.estado}_{self.direcao}"
        if chave in self.sprites and self.sprites[chave]:
            animacao_atual = self.sprites[chave]
            velocidade = self.velocidade_ataque if self.estado == 'atacando' else self.velocidade_animacao

            self.tempo_animacao += 1
            if self.tempo_animacao >= velocidade:
                self.tempo_animacao = 0
                self.index_animacao += 1

                if self.index_animacao >= len(animacao_atual):
                    if self.estado == 'atacando':
                        self.atacando = False
                        self.estado = 'parado'
                        self.index_animacao = 0
                    else:
                        self.index_animacao = 0

            if self.index_animacao < len(animacao_atual):
                self.image = animacao_atual[self.index_animacao]
                
                # Efeito de piscar caso esteja invencível
                if self.invencivel:
                    agora = pygame.time.get_ticks()
                    if (agora // 100) % 2 == 0:
                        # Substitui temporariamente por uma superfície invisível neste frame
                        self.image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                
                # Posiciona a imagem baseada na hitbox atualizada
                self.rect = self.image.get_rect(center=self.hitbox.center)
                self.rect.bottom = self.hitbox.bottom

    def update(self):
        self.cooldowns()
        
        if self.estado == 'morrendo':
            agora = pygame.time.get_ticks()
            if agora - self.tempo_morte >= 1500: # 1.5 segundos de animação de morte
                self.morte_completa = True
            self.animar_morte()
            return
            
        self.entrada_teclado()
        
        # Atualiza a hitbox ANTES de animar para garantir que o rect siga a posição correta
        self.hitbox.centerx = int(self.x)
        self.hitbox.centery = int(self.y)
        
        self.animar()

    def receber_dano(self, quantidade, fonte_x, fonte_y):
        if self.invencivel or self.estado == 'morrendo':
            return

        self.vida -= quantidade
        self.invencivel = True
        self.tempo_invencivel = pygame.time.get_ticks()

        if self.vida <= 0:
            self.vida = 0
            self.estado = 'morrendo'
            self.tempo_morte = pygame.time.get_ticks()
            self.index_animacao = 0
        else:
            # Knockback: empurra o jogador para longe da fonte do dano
            dx = self.x - fonte_x
            dy = self.y - fonte_y
            dist = (dx**2 + dy**2)**0.5
            if dist > 0:
                self.x += (dx / dist) * 35
                self.y += (dy / dist) * 35

    def animar_morte(self):
        agora = pygame.time.get_ticks()
        pct = min(1.0, (agora - self.tempo_morte) / 1500.0)
        
        # Rotaciona o sprite em até 90 graus (caindo para o lado)
        angulo = pct * 90
        chave_base = f"parado_{self.direcao}"
        if chave_base in self.sprites and self.sprites[chave_base]:
            img_base = self.sprites[chave_base][0]
        else:
            img_base = self.image
            
        img_rotacionada = pygame.transform.rotate(img_base, angulo)
        
        # Aplica efeito de fade out (redução de opacidade)
        alpha = int((1.0 - pct) * 255)
        img_final = img_rotacionada.copy()
        img_final.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
        
        self.image = img_final
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def criar_hitbox_ataque(self):
        area_ataque = self.hitbox.copy()
        alcance = 50 # Aumentado um pouco para ser mais generoso
        largura_espada = 50

        if self.direcao == 'direita':
            area_ataque.left = self.hitbox.right
            area_ataque.width = alcance
            area_ataque.height = largura_espada
            area_ataque.centery = self.hitbox.centery
        elif self.direcao == 'esquerda':
            area_ataque.right = self.hitbox.left
            area_ataque.width = alcance
            area_ataque.height = largura_espada
            area_ataque.centery = self.hitbox.centery
        elif self.direcao == 'baixo':
            area_ataque.top = self.hitbox.bottom
            area_ataque.height = alcance
            area_ataque.width = largura_espada
            area_ataque.centerx = self.hitbox.centerx
        elif self.direcao == 'cima':
            area_ataque.bottom = self.hitbox.top
            area_ataque.height = alcance
            area_ataque.width = largura_espada
            area_ataque.centerx = self.hitbox.centerx

        return area_ataque
