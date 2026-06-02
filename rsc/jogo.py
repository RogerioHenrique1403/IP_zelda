import pygame
import sys
from jogador import Jogador
from interface import Interface
from inimigos import Inimigo
from mapa import Mapa


class Jogo:
    def __init__(self, tela, interface):
        self.tela = tela
        self.interface = interface
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.COR_GRAMA = (34, 139, 34)
        # --- CARREGAR O MAPA ---
        self.mapa = Mapa("../res/Layout_Examples/Mapa_teste.tmx")

        #criar jogador
        largura, altura = self.tela.get_size()
        # Passamos a interface para o jogador (para ele ter acesso se precisar)
        self.jogador = Jogador(largura // 2, altura // 2, self.interface)

        #GRUPOS DE SPRITES
        self.inimigos = pygame.sprite.Group()

        self.criar_inimigos()

    def criar_inimigos(self):
        # Cria os inimigos
        inimigo1 = Inimigo(100, 100, self.interface, tipo='slime')
        inimigo2 = Inimigo(700, 150, self.interface, tipo='slime')
        inimigo3 = Inimigo(400, 100, self.interface, tipo='morcego')
        inimigo4 = Inimigo(200, 400, self.interface, tipo='slime')

        # Adiciona todos ao grupo de uma vez
        self.inimigos.add(inimigo1, inimigo2, inimigo3, inimigo4)

    def logica_de_ataque(self):
        # Só verifica se o jogador estiver atacando
        if self.jogador.atacando:

            # 1. Pega a hitbox da espada (área de dano)
            area_espada = self.jogador.criar_hitbox_ataque()

            # --- DEBUG VISUAL (Opcional) ---
            # Se quiser ver onde o golpe está pegando, descomente a linha abaixo:
            # pygame.draw.rect(self.tela, (255, 0, 255), area_espada)

            # 2. Verifica colisão com o GRUPO de inimigos
            hit_list = []
            for inimigo in self.inimigos:
                # Usamos .hitbox para ser mais preciso que o .rect
                if area_espada.colliderect(inimigo.hitbox):
                    hit_list.append(inimigo)

            # 3. Aplica o dano
            for inimigo in hit_list:
                # O método receber_dano cuida da invencibilidade
                inimigo.receber_dano(20)

    def run(self):
        rodando = True
        while rodando:
            # 1. EVENTOS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                    pygame.quit()
                    sys.exit()

            # 2. UPDATE (Atualizações de Lógica)
            self.jogador.update()

            # Passamos o jogador para o update do inimigo (caso ele precise perseguir)
            # Se o seu inimigo.update não aceita argumentos, mude para: self.inimigos.update()
            self.inimigos.update(self.jogador)

            self.logica_de_ataque()

            # Verifica Game Over
            if self.jogador.vida <= 0:
                print("GAME OVER")
                # Aqui você pode colocar um return ou reiniciar o jogo

            # 3. DESENHO
            self.tela.fill(self.COR_GRAMA)
            self.mapa.desenhar(self.tela)

            # --- Y-SORT (Ordenação por Profundidade) ---
            # Isso faz com que sprites mais "embaixo" na tela desenhem por cima dos que estão "atrás"
            # 1. Pega todos os sprites do grupo de inimigos e coloca numa lista junto com o jogador
            sprites_para_desenhar = self.inimigos.sprites() + [self.jogador]

            # 2. Ordena a lista baseado no Y da hitbox
            sprites_para_desenhar.sort(
                key=lambda sprite: sprite.hitbox.centery)

            # 3. Desenha na ordem correta
            for sprite in sprites_para_desenhar:
                # Desenhamos o sprite.image na posição do sprite.rect
                # Mas aplicamos um pequeno ajuste: Desenhamos deslocado para centralizar na hitbox
                # Se sua imagem e rect já estão alinhados, apenas:
                self.tela.blit(sprite.image, sprite.rect)

                # Debug Hitbox (Opcional - descomente para ver as caixas de colisão)
                # pygame.draw.rect(self.tela, (255, 0, 0), sprite.hitbox, 1)

            # --- HUD (Interface) ---
            # A interface é desenhada por último para ficar em cima de tudo
            self.interface.desenhar(self.tela, self.jogador.vida)

            pygame.display.update()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()
