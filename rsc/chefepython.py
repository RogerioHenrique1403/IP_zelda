import os
import pygame
import random
from inimigos import Inimigo

class PythonBoss(Inimigo): # Herda tudo de Inimigo
    def __init__(self, x, y, interface):
        super().__init__(x, y, interface, tipo='python')

        self.vida = 300
        self.cooldown_ataque = 0
        self.projeteis = pygame.sprite.Group()

    def ataque_projetil(self, jogador):
        novo_tiro = Projetil(self.hitbox.centerx, self.hitbox.centery, jogador)
        self.projeteis.add(novo_tiro)

    def ataque_cruz(self, jogador):
        """ Ataque 2: Trava uma cruz de aviso na posição atual do jogador """
        alvo_x = jogador.hitbox.centerx
        alvo_y = jogador.hitbox.centery
        
        # Cria as duas linhas (Horizontal e Vertical) centralizadas no herói
        linha_h = AtaqueCruz(alvo_x, alvo_y, 'H')
        linha_v = AtaqueCruz(alvo_x, alvo_y, 'V')
        
        # Adiciona ambas no grupo para o jogo desenhar e testar colisão automaticamente
        self.projeteis.add(linha_h)
        self.projeteis.add(linha_v)

    def update(self, jogador):
        super().update(jogador)
        self.projeteis.update()

        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1

        else:
            if self.hitbox.inflate(300, 300).colliderect(jogador.hitbox):
                ataque_escolhido = random.choice([self.ataque_projetil, self.ataque_cruz])
                ataque_escolhido(jogador)
                self.cooldown_ataque = 180

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, jogador):
        super().__init__()

        diretorio_rsc = os.path.dirname(os.path.abspath(__file__))
        diretorio_raiz = os.path.dirname(diretorio_rsc)
        caminho_imagem = os.path.join(diretorio_raiz, 'res', 'ataques', 'projetil.png')
        
        imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
        self.image = pygame.transform.scale(imagem_original, (25, 25))

        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.copy()
        
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.velocidade = 7 
        self.tempo_projetil = 180 # 3 segundos para sumir caso não acerte nada

        vetor_pos_inicial = pygame.math.Vector2(x, y)
        vetor_alvo = pygame.math.Vector2(jogador.hitbox.center)
        
        self.direcao = vetor_alvo - vetor_pos_inicial
        
        if self.direcao.length() > 0:
            self.direcao = self.direcao.normalize()
        else:
            self.direcao = pygame.math.Vector2(1, 0)

    def update(self):
        self.pos_x += self.direcao.x * self.velocidade
        self.pos_y += self.direcao.y * self.velocidade
        
        # Sincroniza as posições do Pygame
        self.hitbox.centerx = int(self.pos_x)
        self.hitbox.centery = int(self.pos_y)
        self.rect.center = self.hitbox.center

        # Destrói o projétil após 3 segundos para poupar memória do computador
        self.tempo_projetil -= 1
        if self.tempo_projetil <= 0:
            self.kill()

class AtaqueCruz(pygame.sprite.Sprite):
    def __init__(self, x, y, orientacao):
        super().__init__()
        self.orientacao = orientacao
        self.tempo_projetil = 90  # 1.5 segundos de duração total

        diretorio_rsc = os.path.dirname(os.path.abspath(__file__))
        diretorio_raiz = os.path.dirname(diretorio_rsc)
        self.caminho_sprite = os.path.join(diretorio_raiz, 'res', 'ataques', 'ataque_cruz.png')

        # Descobre o tamanho da tela atual do jogo para expandir a linha até as bordas
        tela = pygame.display.get_surface()
        self.largura_tela = tela.get_width()
        self.altura_tela = tela.get_height()

        # --- FASE 1: AVISO (Linha fina amarela) ---
        if self.orientacao == 'H':
            self.image = pygame.Surface((self.largura_tela, 20))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=(self.largura_tela // 2, y))
        else:
            self.image = pygame.Surface((20, self.altura_tela))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=(x, self.altura_tela // 2))

        self.hitbox = pygame.Rect(0, 0, 0, 0)

    def _gerar_linha_repetida(self, espessura):
        """Preenche a linha mantendo a proporção correta do sprite (sem esticar)"""
        sprite_original = pygame.image.load(self.caminho_sprite).convert_alpha()
        
        if self.orientacao == 'H':
            # Descobre quanto a imagem precisa encolher para caber na espessura (altura)
            proporcao = espessura / sprite_original.get_height()
            nova_largura = int(sprite_original.get_width() * proporcao)
            
            # Garante que a largura não vire zero caso a imagem seja bizarramente pequena
            if nova_largura <= 0: nova_largura = espessura 

            # Redimensiona mantendo o desenho perfeito
            sprite_redimensionado = pygame.transform.scale(sprite_original, (nova_largura, espessura))
            
            superficie_final = pygame.Surface((self.largura_tela, espessura), pygame.SRCALPHA)
            
            for pos_x in range(0, self.largura_tela, nova_largura):
                superficie_final.blit(sprite_redimensionado, (pos_x, 0))
        else:
            # Para a linha em pé, rotacionamos primeiro
            sprite_rotacionado = pygame.transform.rotate(sprite_original, 90)
            
            # Descobre quanto encolher na largura para bater com a espessura da linha vertical
            proporcao = espessura / sprite_rotacionado.get_width()
            nova_altura = int(sprite_rotacionado.get_height() * proporcao)
            
            if nova_altura <= 0: nova_altura = espessura

            # Redimensiona mantendo o desenho perfeito
            sprite_redimensionado = pygame.transform.scale(sprite_rotacionado, (espessura, nova_altura))
            
            superficie_final = pygame.Surface((espessura, self.altura_tela), pygame.SRCALPHA)
        
            for pos_y in range(0, self.altura_tela, nova_altura):
                superficie_final.blit(sprite_redimensionado, (0, pos_y))
        
        return superficie_final

    def update(self):
        self.tempo_projetil -= 1

        # --- FASE 2: EXPLOSÃO (Faltando 30 frames / 0.5 segundos para o ataque acabar) ---
        if self.tempo_projetil == 30:
            self.image = self._gerar_linha_repetida(espessura=50)

            if self.orientacao == 'H':
                self.rect = self.image.get_rect(center=(self.largura_tela // 2, self.rect.centery))
            else:
                self.rect = self.image.get_rect(center=(self.rect.centerx, self.altura_tela // 2))

            self.hitbox = self.rect.copy()

        # Remove a linha do jogo assim que o tempo expirar
        if self.tempo_projetil <= 0:
            self.kill()