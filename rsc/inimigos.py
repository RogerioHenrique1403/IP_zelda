import os
import pygame
from personagem import Personagem

class Inimigo(Personagem):
    def __init__(self, x, y, interface, tipo='loop'):
        self.tipo = tipo
        self.hitbox_rect = (48, 48)

        if tipo == 'python':
            vida = 150
            velocidade = 2.0
            dano = 25
            raio_visao = 300
            alcance_ataque = 35
            cooldown_ataque = 800
        elif tipo == 'trojan':
            vida = 70
            velocidade = 0.0 # começa parado
            dano = 10
            raio_visao = 220
            alcance_ataque = 30
            cooldown_ataque = 1000
        elif tipo == 'leak':
            vida = 60
            velocidade = 1.8
            dano = 10
            raio_visao = 260
            alcance_ataque = 24
            cooldown_ataque = 1000
        else: # loop
            vida = 70
            velocidade = 2.0
            dano = 10
            raio_visao = 280
            alcance_ataque = 25
            cooldown_ataque = 1000

        super().__init__(x, y, velocidade=velocidade, vida=vida, vida_max=vida)

        self.raio_visao = raio_visao
        self.dano = dano
        self.alcance_ataque = alcance_ataque
        self.cooldown_ataque = cooldown_ataque
        self.ultimo_ataque = 0

        self.invencivel = False
        self.cooldown_hit = 400
        self.stunado = False
        self.tempo_stun = 0
        self.duracao_stun = 500
        self.morto_completamente = False

        self.transformado = False
        self.direcao = 'baixo'
        self.sprites = {}

        self._carregar_sprites()

        if self.sprites.get('parado_baixo'):
            self.image = self.sprites['parado_baixo'][0]
        else:
            self.image = pygame.Surface((96, 96), pygame.SRCALPHA)
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(x, y, *self.hitbox_rect)
        self.hitbox.center = self.rect.center

    def _carregar_sprites(self):
        try:
            diretorio_script = os.path.dirname(os.path.abspath(__file__))
            caminho_pasta = os.path.join(diretorio_script, '..', 'res', 'Inimigos sprite', 'Python sprite')

            if self.tipo == 'trojan':
                self._carregar_sprites_trojan(caminho_pasta)
            elif self.tipo == 'python':
                self._carregar_sprites_python(caminho_pasta)
            elif self.tipo == 'leak':
                self._carregar_sprites_leak(caminho_pasta)
            else:
                self._carregar_sprites_loop(caminho_pasta)

        except Exception as exc:
            print(f'ERRO AO CARREGAR SPRITES DO INIMIGO {self.tipo.upper()}: {exc}')
            self._montar_placeholder()

    def _carregar_sprites_loop(self, caminho_pasta):
        #usando exatamente 5 frames para a caminhada
        frames_caminhada = 5 
        
        andando_baixo = self.carregar_tira(os.path.join(caminho_pasta, 'loop-walkingdown.png'), frames_caminhada)
        andando_cima = self.carregar_tira(os.path.join(caminho_pasta, 'loop-walking-up.png'), frames_caminhada)
        andando_direita = self.carregar_tira(os.path.join(caminho_pasta, 'loop-walking.png'), frames_caminhada)
        andando_esquerda = [pygame.transform.flip(img, True, False) for img in andando_direita]

        # Mantendo 4 frames para idle e morte
        idle = self.carregar_tira(os.path.join(caminho_pasta, 'loop-idle.png'), 4) 
        morte = self.carregar_tira(os.path.join(caminho_pasta, 'loop-morte.png'), 4)

        self.sprites['andando_baixo'] = andando_baixo
        self.sprites['andando_cima'] = andando_cima
        self.sprites['andando_direita'] = andando_direita
        self.sprites['andando_esquerda'] = andando_esquerda
        
        self.sprites['parado_baixo'] = idle
        self.sprites['parado_cima'] = idle
        self.sprites['parado_direita'] = idle
        self.sprites['parado_esquerda'] = idle
        
        self.sprites['atacando_baixo'] = andando_baixo
        self.sprites['atacando_cima'] = andando_cima
        self.sprites['atacando_direita'] = andando_direita
        self.sprites['atacando_esquerda'] = andando_esquerda
        
        self.sprites['morrendo'] = morte

    def _carregar_sprites_leak(self, caminho_pasta):
        andando_direita = self.carregar_tira(os.path.join(caminho_pasta, 'leak-walking.png'), 4)
        andando_esquerda = [pygame.transform.flip(img, True, False) for img in andando_direita]
        andando_cima = self.carregar_tira(os.path.join(caminho_pasta, 'leak-walking-up.png'), 4)
        
        # Fatiar o idle em 5 frames 
        idle = self.carregar_tira(os.path.join(caminho_pasta, 'leak-idle.png'), 5)
        
        # Se ele não achar o andar para baixo ele usa os 5 frames do idle
        caminho_baixo = os.path.join(caminho_pasta, 'leak-walkingdown.png')
        if os.path.exists(caminho_baixo):
            andando_baixo = self.carregar_tira(caminho_baixo, 4)
        else:
            andando_baixo = idle

        morte = self._carregar_fallback(os.path.join(caminho_pasta, 'leak-death.png'), os.path.join(caminho_pasta, 'leak-death-2.png'), 4)

        self.sprites['andando_baixo'] = andando_baixo
        self.sprites['andando_cima'] = andando_cima
        self.sprites['andando_direita'] = andando_direita
        self.sprites['andando_esquerda'] = andando_esquerda
        
        self.sprites['parado_baixo'] = idle
        self.sprites['parado_cima'] = idle
        self.sprites['parado_direita'] = idle
        self.sprites['parado_esquerda'] = idle
        
        self.sprites['atacando_baixo'] = andando_baixo
        self.sprites['atacando_cima'] = andando_cima
        self.sprites['atacando_direita'] = andando_direita
        self.sprites['atacando_esquerda'] = andando_esquerda
        
        self.sprites['morrendo'] = morte

    def _carregar_sprites_trojan(self, caminho_pasta):
        transformacao = self.carregar_imagens_individuais([
            'TROJAN_TRANSFORMAÇÃO-removebg-preview.png',
            'TROJAN_TRANSFORMAÇÃO-removebg-preview1.png',
            'TROJAN_TRANSFORMAÇÃO-removebg-preview2.png',
            'TROJAN_TRANSFORMAÇÃO-removebg-preview3.png'
        ], caminho_pasta)
        
        # Ajustado para fatiar a tira de movimento para baixo em 4 frames
        andando_baixo = self.carregar_tira(os.path.join(caminho_pasta, 'TROJAN_ANDANDO_PARA_BAIXO-removebg-preview.png'), 4)
        
        # Mantendo 2 frames (arquivos individuais) para cima
        andando_cima = self.carregar_imagens_individuais([
            'TROJAN_ANDANDO_PARA_CIMA-removebg-preview.png'
        ], caminho_pasta)
        
        # Mantendo 2 frames (arquivos individuais) para a direita para equilibrar
        andando_direita = self.carregar_imagens_individuais([
            'TROJAN_MOVIMENTAÇÃO-removebg-preview.png'
        ], caminho_pasta)
        
        andando_esquerda = [pygame.transform.flip(img, True, False) for img in andando_direita]
        
        morte = self.carregar_imagens_individuais([
            'TROJAN_DERROTADO-removebg-preview2.png'
        ], caminho_pasta)

        self.sprites['transformando'] = transformacao
        self.sprites['parado_baixo'] = transformacao
        self.sprites['parado_cima'] = transformacao
        self.sprites['parado_direita'] = transformacao
        self.sprites['parado_esquerda'] = transformacao
        
        self.sprites['andando_baixo'] = andando_baixo
        self.sprites['andando_cima'] = andando_cima
        self.sprites['andando_direita'] = andando_direita
        self.sprites['andando_esquerda'] = andando_esquerda
        
        self.sprites['atacando_baixo'] = andando_baixo
        self.sprites['atacando_cima'] = andando_cima
        self.sprites['atacando_direita'] = andando_direita
        self.sprites['atacando_esquerda'] = andando_esquerda
        
        self.sprites['morrendo'] = morte

    def _montar_placeholder(self):
        self.image = pygame.Surface((96, 96), pygame.SRCALPHA)
        self.image.fill((255, 0, 0))
        self.sprites = {chave: [self.image] for chave in [
            'parado_baixo', 'parado_cima', 'parado_direita', 'parado_esquerda',
            'andando_baixo', 'andando_cima', 'andando_direita', 'andando_esquerda',
            'atacando_baixo', 'atacando_cima', 'atacando_direita', 'atacando_esquerda',
            'morrendo', 'transformando'
        ]}

    def carregar_tira(self, caminho_completo, quantidade_frames, target_size=(96, 96)):
        if not os.path.exists(caminho_completo):
            raise FileNotFoundError(f'Arquivo não encontrado: {caminho_completo}')

        sheet = pygame.image.load(caminho_completo).convert_alpha()
        w, h = sheet.get_size()

        for x in range(w):
            for y in range(h):
                r, g, b, _ = sheet.get_at((x, y))
                is_light = (210 <= r <= 245) and (210 <= g <= 245) and (210 <= b <= 245)
                is_medium = (135 <= r <= 175) and (135 <= g <= 175) and (135 <= b <= 175)
                if is_light or is_medium:
                    sheet.set_at((x, y), (0, 0, 0, 0))

        if quantidade_frames <= 1:
            return [pygame.transform.scale(sheet, target_size)]

        largura_frame = w // quantidade_frames
        altura_frame = h

        imagens = []
        for i in range(quantidade_frames):
            x_ini = i * largura_frame
            corte = sheet.subsurface((x_ini, 0, largura_frame, altura_frame))
            imagens.append(pygame.transform.scale(corte, target_size))

        return imagens

    def carregar_imagens_individuais(self, nomes_arquivos, caminho_pasta, target_size=(96, 96)):
        imagens = []
        for nome in nomes_arquivos:
            caminho_completo = os.path.join(caminho_pasta, nome)
            if not os.path.exists(caminho_completo):
                continue
                
            sheet = pygame.image.load(caminho_completo).convert_alpha()
            w, h = sheet.get_size()
            
            # Remove o fundo das imagens individuais
            for x in range(w):
                for y in range(h):
                    r, g, b, _ = sheet.get_at((x, y))
                    is_light = (210 <= r <= 245) and (210 <= g <= 245) and (210 <= b <= 245)
                    is_medium = (135 <= r <= 175) and (135 <= g <= 175) and (135 <= b <= 175)
                    if is_light or is_medium:
                        sheet.set_at((x, y), (0, 0, 0, 0))
                        
            imagens.append(pygame.transform.scale(sheet, target_size))
            
        if not imagens:
            return [pygame.Surface(target_size, pygame.SRCALPHA)]
        return imagens
    
    def _carregar_fallback(self, caminho_principal, caminho_fallback, quantidade_frames):
        if os.path.exists(caminho_principal):
            return self.carregar_tira(caminho_principal, quantidade_frames)
        if os.path.exists(caminho_fallback):
            return self.carregar_tira(caminho_fallback, quantidade_frames)
        raise FileNotFoundError('Nenhum arquivo de fallback encontrado')

    def update(self, jogador):
        self.cooldowns()

        if self.estado == 'morrendo':
            self.animar()
            return

        if self.stunado:
            return

        estado_anterior = self.estado

        if self.tipo == 'trojan' and not self.transformado:
            self.estado = 'transformando'
            self.animar()
            return

        alvo_rect = getattr(jogador, 'hitbox', jogador.rect)
        dx = alvo_rect.centerx - self.hitbox.centerx
        dy = alvo_rect.centery - self.hitbox.centery
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia < self.raio_visao:
            if distancia > self.alcance_ataque:
                if distancia > 0:
                    self.x += (dx / distancia) * self.velocidade
                    self.y += (dy / distancia) * self.velocidade
                self.estado = 'andando'
            else:
                self.estado = 'atacando'
                self.atacar(jogador)

            if abs(dx) > abs(dy):
                self.direcao = 'direita' if dx > 0 else 'esquerda'
            else:
                self.direcao = 'baixo' if dy > 0 else 'cima'
        else:
            self.estado = 'parado'

        # Resetamos a animação apenas se o estado mudar (ex: de parado para andando)
        if self.estado != estado_anterior:
            self.index_animacao = 0
            self.tempo_animacao = pygame.time.get_ticks()

        self.hitbox.centerx = int(self.x)
        self.hitbox.centery = int(self.y)
        self.rect.center = self.hitbox.center

        self.animar()

    def animar(self):
        if self.estado == 'morrendo':
            chave = 'morrendo'
        elif self.tipo == 'trojan' and not self.transformado and self.estado == 'transformando':
            chave = 'transformando'
        else:
            chave = f'{self.estado}_{self.direcao}'

        if chave in self.sprites and self.sprites[chave]:
            animacao = self.sprites[chave]
            agora = pygame.time.get_ticks()

            if self.estado == 'morrendo':
                atraso = 120
            elif self.estado == 'transformando':
                atraso = 90
            else:
                atraso = 90

            if agora - self.tempo_animacao >= atraso:
                self.tempo_animacao = agora
                self.index_animacao += 1

                if self.index_animacao >= len(animacao):
                    if self.estado == 'morrendo':
                        self.index_animacao = len(animacao) - 1
                        self.morto_completamente = True
                    elif self.estado == 'transformando':
                        # Para o Trojan não piscar, ele fica no último frame do brinquedo até ser atacado
                        self.index_animacao = len(animacao) - 1 
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
        if self.estado == 'morrendo' or self.invencivel:
            return

        self.vida -= quantidade
        self.stunado = True
        self.invencivel = True

        agora = pygame.time.get_ticks()
        self.tempo_stun = agora
        self.tempo_invencivel = agora

        if self.tipo == 'trojan' and not self.transformado:
            self.transformado = True
            self.velocidade = 1.8
            self.vida_max = 120
            self.vida = self.vida_max
            
            self._carregar_sprites_trojan(os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '..', 'res', 'Inimigos sprite', 'Python sprite'
            ))
            
            if 'andando_baixo' in self.sprites and self.sprites['andando_baixo']:
                self.sprites['parado_baixo'] = [self.sprites['andando_baixo'][0]]
                self.sprites['parado_cima'] = [self.sprites['andando_cima'][0]]
                self.sprites['parado_direita'] = [self.sprites['andando_direita'][0]]
                self.sprites['parado_esquerda'] = [self.sprites['andando_esquerda'][0]]

            self.estado = 'parado'
            self.index_animacao = 0

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