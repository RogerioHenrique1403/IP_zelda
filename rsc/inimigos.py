import os
import pygame
from personagem import Personagem

class Inimigo(Personagem):
    def __init__(self, x, y, interface, tipo='loop'):
        self.tipo = tipo

        if tipo == 'python':
            self.hitbox_rect = (120, 120)
            vida = 400
            velocidade = 2.0
            dano = 25
            raio_visao = 350
            alcance_ataque = 65
            cooldown_ataque = 800
        elif tipo == 'trojan':
            self.hitbox_rect = (64, 64)
            vida = 70
            velocidade = 0.0 # começa parado
            dano = 10
            raio_visao = 220
            alcance_ataque = 40
            cooldown_ataque = 1000
        elif tipo == 'leak':
            self.hitbox_rect = (64, 64)
            vida = 60
            velocidade = 1.8
            dano = 10
            raio_visao = 260
            alcance_ataque = 32
            cooldown_ataque = 1000
        else: # loop
            self.hitbox_rect = (64, 64)
            vida = 70
            velocidade = 2.0
            dano = 10
            raio_visao = 280
            alcance_ataque = 35
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

        # Python boss variaveis de ataque
        if self.tipo == 'python':
            self.tempo_ultimo_ataque_especial = pygame.time.get_ticks()
            self.ataque_especial_ativo = False
            self.tempo_inicio_especial = 0
            self.meteoros = []
            self.proximo_spawn_meteoro = 0

        self._carregar_sprites()

        if self.sprites.get('parado_baixo'):
            self.image = self.sprites['parado_baixo'][0]
        else:
            self.image = pygame.Surface((192, 192) if tipo == 'python' else (128, 128), pygame.SRCALPHA)
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

        andando_baixo = self.carregar_tira(os.path.join(caminho_pasta, 'loop-walkingdown.png'), frames_caminhada, ref_h=115)
        andando_cima = self.carregar_tira(os.path.join(caminho_pasta, 'loop-walking-up.png'), frames_caminhada, ref_h=115)
        andando_direita = self.carregar_tira(os.path.join(caminho_pasta, 'loop-walking.png'), frames_caminhada, ref_h=115)
        andando_esquerda = [pygame.transform.flip(img, True, False) for img in andando_direita]

        # Mantendo 4 frames para idle e morte
        idle = self.carregar_tira(os.path.join(caminho_pasta, 'loop-idle.png'), 4, ref_h=115) 
        morte = self.carregar_tira(os.path.join(caminho_pasta, 'loop-morte.png'), 4, ref_h=115)

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
        andando_direita = self.carregar_tira(os.path.join(caminho_pasta, 'leak-walking.png'), 4, ref_h=132)
        andando_esquerda = [pygame.transform.flip(img, True, False) for img in andando_direita]
        andando_cima = self.carregar_tira(os.path.join(caminho_pasta, 'leak-walking-up.png'), 4, ref_h=132)
        
        # Fatiar o idle em 5 frames 
        idle = self.carregar_tira(os.path.join(caminho_pasta, 'leak-idle.png'), 5, ref_h=132)
        
        # Se ele não achar o andar para baixo ele usa os 5 frames do idle
        caminho_baixo = os.path.join(caminho_pasta, 'leak-walkingdown.png')
        if os.path.exists(caminho_baixo):
            andando_baixo = self.carregar_tira(caminho_baixo, 4, ref_h=132)
        else:
            andando_baixo = idle
            
        morte = self._carregar_fallback(os.path.join(caminho_pasta, 'leak-death.png'), os.path.join(caminho_pasta, 'leak-death-2.png'), 4, ref_h=132)

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

    def _carregar_sprites_python(self, caminho_pasta):
        # Python boss na verdade possui 4 frames em suas spritesheets
        andando_baixo = self.carregar_tira(os.path.join(caminho_pasta, 'python_walking_down.png'), 4, target_size=(192, 192), ref_h=339)
        andando_direita = self.carregar_tira(os.path.join(caminho_pasta, 'python_walking_right.png'), 4, target_size=(192, 192), ref_h=339)
        andando_cima = self.carregar_tira(os.path.join(caminho_pasta, 'python_walking_up.png'), 4, target_size=(192, 192), ref_h=339)
        andando_esquerda = [pygame.transform.flip(img, True, False) for img in andando_direita]

        idle = andando_baixo[:]

        # Morte também possui 4 frames
        morte = self.carregar_tira(os.path.join(caminho_pasta, 'python_death.png'), 4, target_size=(192, 192), ref_h=339)

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
        transformacao = self.carregar_tira(os.path.join(caminho_pasta, 'TROJAN_TRANSFORMAÇÃO-removebg-preview.png'), 4, ref_h=192)
        
        andando_baixo = self.carregar_tira(os.path.join(caminho_pasta, 'TROJAN_ANDANDO_PARA_BAIXO-removebg-preview.png'), 4, ref_h=192)
        # andando_cima tem 2 frames no preview2
        andando_cima = self.carregar_tira(os.path.join(caminho_pasta, 'TROJAN_ANDANDO_PARA_CIMA-removebg-preview2.png'), 2, ref_h=192)
        # andando_direita tem 2 frames no preview
        andando_direita = self.carregar_tira(os.path.join(caminho_pasta, 'TROJAN_MOVIMENTAÇÃO-removebg-preview.png'), 2, ref_h=192)
        andando_esquerda = [pygame.transform.flip(img, True, False) for img in andando_direita]
        
        # morte tem 2 frames no preview
        morte = self.carregar_tira(os.path.join(caminho_pasta, 'TROJAN_DERROTADO-removebg-preview.png'), 2, ref_h=192)

        self.sprites['transformando'] = transformacao
        self.sprites['morrendo'] = morte
        
        if not self.transformado:
            # Antes de ser atacado, ele fica parado no disfarce (frame 0 da transformação)
            self.sprites['parado_baixo'] = [transformacao[0]]
            self.sprites['parado_cima'] = [transformacao[0]]
            self.sprites['parado_direita'] = [transformacao[0]]
            self.sprites['parado_esquerda'] = [transformacao[0]]
            
            self.sprites['andando_baixo'] = [transformacao[0]]
            self.sprites['andando_cima'] = [transformacao[0]]
            self.sprites['andando_direita'] = [transformacao[0]]
            self.sprites['andando_esquerda'] = [transformacao[0]]
        else:
            # Após se transformar, ele usa as sprites normais de movimento
            self.sprites['parado_baixo'] = [andando_baixo[0]]
            self.sprites['parado_cima'] = [andando_cima[0]]
            self.sprites['parado_direita'] = [andando_direita[0]]
            self.sprites['parado_esquerda'] = [andando_esquerda[0]]
            
            self.sprites['andando_baixo'] = andando_baixo
            self.sprites['andando_cima'] = andando_cima
            self.sprites['andando_direita'] = andando_direita
            self.sprites['andando_esquerda'] = andando_esquerda
            
        self.sprites['atacando_baixo'] = self.sprites['andando_baixo']
        self.sprites['atacando_cima'] = self.sprites['andando_cima']
        self.sprites['atacando_direita'] = self.sprites['andando_direita']
        self.sprites['atacando_esquerda'] = self.sprites['andando_esquerda']

    def _montar_placeholder(self):
        size = (192, 192) if self.tipo == 'python' else (128, 128)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill((255, 0, 0))
        self.sprites = {chave: [self.image] for chave in [
            'parado_baixo', 'parado_cima', 'parado_direita', 'parado_esquerda',
            'andando_baixo', 'andando_cima', 'andando_direita', 'andando_esquerda',
            'atacando_baixo', 'atacando_cima', 'atacando_direita', 'atacando_esquerda',
            'morrendo', 'transformando'
        ]}

    def _obter_limites_x(self, surface):
        w, h = surface.get_size()
        x_min = w
        x_max = 0
        for x in range(w):
            for y in range(h):
                _, _, _, a = surface.get_at((x, y))
                if a > 0:
                    if x < x_min:
                        x_min = x
                    if x > x_max:
                        x_max = x
        if x_min > x_max:
            return 0, w
        return x_min, x_max + 1

    def carregar_tira(self, caminho_completo, quantidade_frames, target_size=(128, 128), ref_h=None):
        if not os.path.exists(caminho_completo):
            raise FileNotFoundError(f'Arquivo não encontrado: {caminho_completo}')

        sheet = pygame.image.load(caminho_completo).convert_alpha()
        w, h = sheet.get_size()

        # Remove o fundo
        for x in range(w):
            for y in range(h):
                r, g, b, _ = sheet.get_at((x, y))
                is_light = (210 <= r <= 245) and (210 <= g <= 245) and (210 <= b <= 245)
                is_medium = (135 <= r <= 175) and (135 <= g <= 175) and (135 <= b <= 175)
                if is_light or is_medium:
                    sheet.set_at((x, y), (0, 0, 0, 0))

        # Determina a escala proporcional para manter a proporção da arte original
        if ref_h is not None:
            scale = target_size[1] / ref_h
        else:
            scale = target_size[1] / h

        largura_frame = w // quantidade_frames
        altura_frame = h

        scaled_w = int(largura_frame * scale)
        scaled_h = int(altura_frame * scale)

        imagens = []
        for i in range(quantidade_frames):
            x_ini = i * largura_frame
            corte = sheet.subsurface((x_ini, 0, largura_frame, altura_frame))
            
            # Redimensiona proporcionalmente para manter a proporção da arte original
            corte_escalado = pygame.transform.scale(corte, (scaled_w, scaled_h))
            
            # Auto-centraliza o conteúdo do frame escalado horizontalmente
            x_min_esc, x_max_esc = self._obter_limites_x(corte_escalado)
            content_w_esc = x_max_esc - x_min_esc
            
            final_frame = pygame.Surface(target_size, pygame.SRCALPHA)
            
            if content_w_esc > 0:
                shift_x = int((target_size[0] / 2) - (x_min_esc + content_w_esc / 2))
            else:
                shift_x = int((target_size[0] - scaled_w) / 2)
            
            # Alinha no chão (borda inferior da tela/canvas de 96x96)
            shift_y = target_size[1] - scaled_h
            
            final_frame.blit(corte_escalado, (shift_x, shift_y))
            imagens.append(final_frame)

        return imagens

    def carregar_imagens_individuais(self, nomes_arquivos, caminho_pasta, target_size=(128, 128), ref_h=None):
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
            
            if ref_h is not None:
                scale = target_size[1] / ref_h
            else:
                scale = target_size[1] / h
                
            scaled_w = int(w * scale)
            scaled_h = int(h * scale)
            
            scaled_img = pygame.transform.scale(sheet, (scaled_w, scaled_h))
            
            # Auto-centraliza horizontalmente
            x_min, x_max = self._obter_limites_x(scaled_img)
            content_w = x_max - x_min
            
            final_frame = pygame.Surface(target_size, pygame.SRCALPHA)
            if content_w > 0:
                shift_x = int((target_size[0] / 2) - (x_min + content_w / 2))
            else:
                shift_x = int((target_size[0] - scaled_w) / 2)
            
            # Alinha no chão (borda inferior)
            shift_y = target_size[1] - scaled_h
            final_frame.blit(scaled_img, (shift_x, shift_y))
            imagens.append(final_frame)
            
        if not imagens:
            return [pygame.Surface(target_size, pygame.SRCALPHA)]
        return imagens

    def _carregar_fallback(self, caminho_principal, caminho_fallback, quantidade_frames, ref_h=None):
        if os.path.exists(caminho_principal):
            return self.carregar_tira(caminho_principal, quantidade_frames, ref_h=ref_h)
        if os.path.exists(caminho_fallback):
            return self.carregar_tira(caminho_fallback, quantidade_frames, ref_h=ref_h)
        raise FileNotFoundError('Nenhum arquivo de fallback encontrado')

    def update(self, jogador):
        self.cooldowns()

        if self.estado == 'morrendo':
            if self.tipo == 'python' and hasattr(self, 'meteoros'):
                self.meteoros.clear()
            self.animar()
            return

        if self.stunado:
            return

        agora = pygame.time.get_ticks()

        # Lógica de ataque especial para o Python boss
        if self.tipo == 'python':
            if not hasattr(self, 'tempo_ultimo_ataque_especial'):
                self.tempo_ultimo_ataque_especial = agora
                self.ataque_especial_ativo = False
                self.tempo_inicio_especial = 0
                self.meteoros = []
                self.proximo_spawn_meteoro = 0

            # Atualiza sempre os meteoros existentes
            for met in self.meteoros[:]:
                met.update(jogador)
                if met.destruido:
                    self.meteoros.remove(met)

            if self.ataque_especial_ativo:
                if agora - self.tempo_inicio_especial >= 4000:
                    self.ataque_especial_ativo = False
                    self.tempo_ultimo_ataque_especial = agora
                else:
                    self.estado = 'parado'
                    self.velocidade = 0.0

                    if agora >= self.proximo_spawn_meteoro:
                        import random
                        target_rect = getattr(jogador, 'hitbox', jogador.rect)
                        px = target_rect.centerx + random.randint(-180, 180)
                        py = target_rect.centery + random.randint(-180, 180)
                        px = max(60, min(1140, px))
                        py = max(60, min(660, py))
                        
                        self.meteoros.append(MeteoroCodigo(px, py))
                        self.proximo_spawn_meteoro = agora + 500

                self.animar()

                self.hitbox.centerx = int(self.x)
                self.hitbox.centery = int(self.y)
                self.rect.center = self.hitbox.center
                return
            else:
                self.velocidade = 2.0
                alvo_rect = getattr(jogador, 'hitbox', jogador.rect)
                dx = alvo_rect.centerx - self.hitbox.centerx
                dy = alvo_rect.centery - self.hitbox.centery
                distancia = (dx ** 2 + dy ** 2) ** 0.5
                if distancia < self.raio_visao and agora - self.tempo_ultimo_ataque_especial >= 8000:
                    self.ataque_especial_ativo = True
                    self.tempo_inicio_especial = agora
                    self.proximo_spawn_meteoro = agora
                    self.meteoros = []
                    self.estado = 'parado'
                    self.velocidade = 0.0
                    self.animar()
                    return

        estado_anterior = self.estado

        if self.tipo == 'trojan' and not self.transformado:
            if self.estado == 'transformando':
                self.animar()
            else:
                self.estado = 'parado'
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
                        # A animação de transformação terminou!
                        self.transformado = True
                        self.velocidade = 1.8
                        self.vida_max = 120
                        self.vida = self.vida_max
                        
                        # Recarrega as sprites para o Trojan em sua forma final ativa
                        self._carregar_sprites_trojan(os.path.join(
                            os.path.dirname(os.path.abspath(__file__)),
                            '..', 'res', 'Inimigos sprite', 'Python sprite'
                        ))
                        
                        self.estado = 'parado'
                        self.index_animacao = 0
                    else:
                        self.index_animacao = 0

            if self.index_animacao < len(animacao):
                self.image = animacao[int(self.index_animacao)]

    def atacar(self, jogador):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_ataque > self.cooldown_ataque:
            if hasattr(jogador, 'receber_dano'):
                jogador.receber_dano(self.dano, self.hitbox.centerx, self.hitbox.centery)
            else:
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
            # Começa a animação de transformação e impede novos danos durante o processo
            self.estado = 'transformando'
            self.index_animacao = 0
            self.tempo_animacao = agora
            self.stunado = False # não fica stunado enquanto se transforma
            self.invencivel = True # fica invencível durante a transformação para não morrer no meio
            self.tempo_invencivel = agora + 1000 # 1 segundo de invencibilidade
            return

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

    def desenhar_zonas_vermelhas(self, tela):
        if self.tipo == 'python' and hasattr(self, 'meteoros'):
            for met in self.meteoros:
                met.desenhar_zona(tela)

    def desenhar_meteoros_e_explosoes(self, tela):
        if self.tipo == 'python' and hasattr(self, 'meteoros'):
            for met in self.meteoros:
                met.desenhar_meteoro(tela)


class MeteoroCodigo:
    def __init__(self, x_alvo, y_alvo):
        self.x_alvo = x_alvo
        self.y_alvo = y_alvo
        self.x = x_alvo
        self.y = -100  
        
        self.tempo_spawn = pygame.time.get_ticks()
        self.tempo_aviso = 1200  
        self.caindo = False
        self.explodindo = False
        self.tempo_explosao = 0
        self.destruido = False
        
        self.velocidade = 22  
        self.raio_dano = 55  
        self.dano = 15
        
        #Código que podem cair
        codigos = [
            "SyntaxError: invalid syntax",
            "IndexError: list index out of range",
            "ZeroDivisionError: division by zero",
            "KeyError: 'python'",
            "RecursionError: maximum depth exceeded",
            "NameError: name 'boss' is not defined",
            "TypeError: unsupported operand type(s)",
            "SystemExit",
            "KeyboardInterrupt",
            "AttributeError: 'NoneType' has no attribute",
            "import os; os.system('rm -rf /')",
            "while True: print('ERROR')"
        ]
        import random
        self.texto = random.choice(codigos)
        self.cor = (57, 255, 20) if random.random() > 0.4 else (255, 50, 50)
        
        self.fonte = pygame.font.SysFont('Courier New', 16, bold=True)

    def update(self, jogador):
        agora = pygame.time.get_ticks()
        
        if not self.caindo and not self.explodindo:
            if agora - self.tempo_spawn >= self.tempo_aviso:
                self.caindo = True
                
        elif self.caindo:
            self.y += self.velocidade
            if self.y >= self.y_alvo:
                self.y = self.y_alvo
                self.caindo = False
                self.explodindo = True
                self.tempo_explosao = agora
                
                #checagem de colisão
                alvo_rect = getattr(jogador, 'hitbox', jogador.rect)
                dx = alvo_rect.centerx - self.x_alvo
                dy = alvo_rect.centery - self.y_alvo
                dist = (dx**2 + dy**2)**0.5
                if dist <= self.raio_dano:
                    jogador.receber_dano(self.dano, self.x_alvo, self.y_alvo)
                    
        elif self.explodindo:
            if agora - self.tempo_explosao >= 400:  
                self.destruido = True

    def desenhar_zona(self, tela):
        agora = pygame.time.get_ticks()
        if not self.explodindo:
            tempo_decorrido = agora - self.tempo_spawn
            import math
            pulso = abs(math.sin(tempo_decorrido * 0.01))
            raio_atual = int(self.raio_dano * (0.85 + 0.15 * pulso))
            
            superficie_alfa = pygame.Surface((raio_atual * 2, raio_atual * 2), pygame.SRCALPHA)
            pygame.draw.circle(superficie_alfa, (255, 0, 0, 70), (raio_atual, raio_atual), raio_atual)
            pygame.draw.circle(superficie_alfa, (255, 0, 0, 200), (raio_atual, raio_atual), raio_atual, 2)
            
            tela.blit(superficie_alfa, (self.x_alvo - raio_atual, self.y_alvo - raio_atual))
            
            pygame.draw.line(tela, (255, 0, 0), (self.x_alvo - 10, self.y_alvo), (self.x_alvo + 10, self.y_alvo), 2)
            pygame.draw.line(tela, (255, 0, 0), (self.x_alvo, self.y_alvo - 10), (self.x_alvo, self.y_alvo + 10), 2)

    def desenhar_meteoro(self, tela):
        agora = pygame.time.get_ticks()
        if self.caindo:
            surf_texto = self.fonte.render(self.texto, True, self.cor)
            rect_texto = surf_texto.get_rect(center=(int(self.x), int(self.y)))
    
            surf_sombra = self.fonte.render(self.texto, True, (0, 0, 0))
            tela.blit(surf_sombra, (rect_texto.x + 1, rect_texto.y + 1))
            tela.blit(surf_texto, rect_texto)
            
            pygame.draw.line(tela, (self.cor[0], self.cor[1], self.cor[2], 100), 
                             (self.x_alvo, 0), (self.x_alvo, int(self.y)), 1)
                             
        elif self.explodindo:
            tempo_decorrido = agora - self.tempo_explosao
            progresso = min(1.0, tempo_decorrido / 400.0)
            
            partes = self.texto.split()
            for idx, parte in enumerate(partes):
                import math
                angulo = (idx / len(partes)) * 2 * math.pi
                dist = progresso * 40
                px = self.x_alvo + math.cos(angulo) * dist
                py = self.y_alvo + math.sin(angulo) * dist
                
                alfa = int((1.0 - progresso) * 255)
                surf_p = self.fonte.render(parte, True, self.cor)
                surf_final = surf_p.copy()
                surf_final.fill((255, 255, 255, alfa), special_flags=pygame.BLEND_RGBA_MULT)
                
                rect_p = surf_final.get_rect(center=(int(px), int(py)))
                tela.blit(surf_final, rect_p)