import pygame
import os
from personagem import Personagem


class Jogador(Personagem):
    def __init__(self, x, y, interface):
        super().__init__(x, y, velocidade=4, vida=100, vida_max=100)

        self.escala = 3
        self.sprites = {}
        self.direcao = 'baixo'  # Guarda para onde o personagem está olhando
        self.estado = 'parado'  # parado, andando, atacando

        # Controle de Animação
        self.tempo_animacao = 0
        self.velocidade_animacao = 9  # Quanto maior, mais lenta a animação
        self.velocidade_ataque = 4    # Ataque deve ser mais rápido
        self.index_animacao = 0

        # Controle de Ataque
        self.atacando = False
        self.pode_atacar = True
        self.cooldown_ataque = 500  # milissegundos
        self.ultimo_ataque = 0

        self.carregar_todas_imagens()

        # Define imagem inicial e retângulos
        if 'parado_baixo' in self.sprites:
            self.image = self.sprites['parado_baixo'][0]
        else:
            self.image = pygame.Surface((32, 32))
            self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(x, y, 40, 20)
        # Centraliza a hitbox na base do personagem
        self.hitbox.midbottom = self.rect.midbottom

    def carregar_todas_imagens(self):
        try:
            # --- TRUQUE DO CAMINHO ABSOLUTO ---
            diretorio_script = os.path.dirname(os.path.abspath(__file__))
            # Sobe uma pasta (..) e entra em res/Player
            pasta_player = os.path.abspath(os.path.join(
                diretorio_script, '..', 'res', 'Player'))

            if not os.path.exists(pasta_player):
                print("ERRO CRÍTICO: A pasta do jogador não existe!")

            # --- 1. CARREGANDO ANDAR (Run) ---
            # Caminho: res/Player/Run
            pasta_run = os.path.join(pasta_player, 'Run')
            self.sprites['andando_baixo'] = self.carregar_tira(
                os.path.join(pasta_run, 'RunDown.png'), 6)
            self.sprites['andando_cima'] = self.carregar_tira(
                os.path.join(pasta_run, 'RunUp.png'), 6)
            self.sprites['andando_direita'] = self.carregar_tira(
                os.path.join(pasta_run, 'RunRight.png'), 6)
            self.sprites['andando_esquerda'] = self.carregar_tira(
                os.path.join(pasta_run, 'RunLeft.png'), 6)

            # --- 2. CARREGANDO ATAQUE (Attack) ---
            # AQUI ESTÁ A CORREÇÃO:
            # Antes estava: pasta_ataque = pasta_player
            # Agora apontamos para a subpasta 'Attack':
            pasta_ataque = os.path.join(pasta_player, 'Attack')

            print(f"Carregando ataques de: {pasta_ataque}")

            # Carrega os arquivos
            self.sprites['atacando_baixo'] = self.carregar_tira(
                os.path.join(pasta_ataque, 'AttackDown.png'), 6)
            self.sprites['atacando_cima'] = self.carregar_tira(
                os.path.join(pasta_ataque, 'AttackUp.png'), 6)
            self.sprites['atacando_direita'] = self.carregar_tira(
                os.path.join(pasta_ataque, 'AttackRight.png'), 6)
            self.sprites['atacando_esquerda'] = self.carregar_tira(
                os.path.join(pasta_ataque, 'AttackLeft.png'), 6)

            # --- 3. PARADO (Idle) ---
            self.sprites['parado_baixo'] = [self.sprites['andando_baixo'][0]]
            self.sprites['parado_cima'] = [self.sprites['andando_cima'][0]]
            self.sprites['parado_direita'] = [
                self.sprites['andando_direita'][0]]
            self.sprites['parado_esquerda'] = [
                self.sprites['andando_esquerda'][0]]

        except Exception as e:
            print(f"ERRO PLAYER AO CARREGAR IMAGENS: {e}")
            self.sprites = {}

    def carregar_tira(self, caminho_completo, quantidade_frames):
        """ Corta uma imagem comprida em vários pedaços """
        imagens = []

        if not os.path.exists(caminho_completo):
            print(f"ATENÇÃO: Arquivo não encontrado: {caminho_completo}")
            # Retorna uma lista com um quadrado rosa para debug
            surf = pygame.Surface((32, 32))
            surf.fill((255, 0, 255))
            return [surf] * quantidade_frames

        sheet = pygame.image.load(caminho_completo).convert_alpha()

        # Calcula a largura de UM quadro
        largura_frame = sheet.get_width() // quantidade_frames
        altura_frame = sheet.get_height()

        for i in range(quantidade_frames):
            # Recorta o pedaço (subsurface)
            corte = sheet.subsurface(
                (i * largura_frame, 0, largura_frame, altura_frame))

            # Aumenta o tamanho (Escala)
            largura_nova = int(largura_frame * self.escala)
            altura_nova = int(altura_frame * self.escala)
            img_escalada = pygame.transform.scale(
                corte, (largura_nova, altura_nova))

            imagens.append(img_escalada)

        return imagens

    def entrada_teclado(self):
        # Se estiver atacando, NÃO recebe input de movimento
        if self.atacando:
            return

        keys = pygame.key.get_pressed()
        movendo = False

        # --- Movimentação ---
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

        # --- Ataque ---
        if keys[pygame.K_SPACE] and self.pode_atacar:
            self.atacando = True
            self.pode_atacar = False
            self.ultimo_ataque = pygame.time.get_ticks()
            self.index_animacao = 0  # Reinicia animação para o golpe sair do começo
            self.estado = 'atacando'
            # print("Atacando!") # Debug
            return  # Sai da função para não sobrescrever o estado com 'andando'

        # Atualiza estado de movimento se não estiver atacando
        if movendo:
            self.estado = 'andando'
        else:
            self.estado = 'parado'

    def cooldowns(self):
        if not self.pode_atacar:
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_ataque >= self.cooldown_ataque:
                self.pode_atacar = True

    def animar(self):
        # Define qual lista de sprites usar
        chave = f"{self.estado}_{self.direcao}"

        if chave in self.sprites:
            animacao_atual = self.sprites[chave]

            # Define a velocidade (ataque é mais rápido)
            if self.estado == 'atacando':
                velocidade = self.velocidade_ataque
            else:
                velocidade = self.velocidade_animacao

            self.tempo_animacao += 1

            if self.tempo_animacao >= velocidade:
                self.tempo_animacao = 0
                self.index_animacao += 1

                # --- Lógica de Fim da Animação ---
                if self.index_animacao >= len(animacao_atual):
                    if self.estado == 'atacando':
                        # Se acabou a animação de ataque, para de atacar
                        self.atacando = False
                        self.estado = 'parado'
                        self.index_animacao = 0
                    else:
                        # Loop normal (andar/parado)
                        self.index_animacao = 0

            # Segurança para não estourar lista
            if self.index_animacao < len(animacao_atual):
                self.image = animacao_atual[self.index_animacao]

                # Ajusta o retangulo para a imagem não "pular" se o tamanho mudar
                # Mantém o centro da hitbox alinhado
                self.rect = self.image.get_rect(center=self.hitbox.center)
                # Sobe um pouco o rect visual em relação à hitbox (pés no chão)
                self.rect.bottom = self.hitbox.bottom

    def update(self):
        self.cooldowns()
        self.entrada_teclado()
        self.animar()

        # Atualiza posição da hitbox baseada no X e Y
        self.hitbox.centerx = int(self.x)
        self.hitbox.centery = int(self.y)

    def criar_hitbox_ataque(self):
        """ Cria um retângulo na frente do jogador para detectar colisão """
        # Começa copiando o retângulo do jogador
        area_ataque = self.hitbox.copy()

        # Define o tamanho do alcance (ex: 20 pixels para frente)
        alcance = 30
        largura_espada = 30

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
