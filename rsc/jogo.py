import pygame
import sys
import random
from jogador import Jogador
from interface import Interface
from inimigos import Inimigo
from mapa import Mapa
from coletaveis import Npc
from coletaveis import Coletavel


class Jogo:
    def __init__(self, tela, interface):
        self.tela = tela
        self.interface = interface
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.COR_GRAMA = (34, 139, 34)

        
        # Coordenadas do mundo
        self.mapa_x = 0
        self.mapa_y = 0

        # Dicionário de mapas cadastrados (Tupla (x,y): Caminho do arquivo .tmx)
        self.gerenciador_mapas = {
            (0, 0): "../res/Layout_Examples/Mapa_teste.tmx", # Centro
            (1, 0): "../res/Layout_Examples/Mapa_teste.tmx", # Direita
            (-1, 0): "../res/Layout_Examples/Mapa_teste.tmx", # Esquerda
            (0, 1): "../res/Layout_Examples/Mapa_teste.tmx", # Baixo
            (0, -1): "../res/Layout_Examples/Mapa_teste.tmx" # Cima
        }

        # --- POSIÇÕES INICIAIS ---
        self.pos_npc_x, self.pos_npc_y = 600, 400
        self.pos_jogador_x, self.pos_jogador_y = 400, 300
        self.pos_colet_x, self.pos_colet_y = 0, 0

        # Máquina de Estados
        self.estado_atual = 'MENU'
        self.venceu_fase = False
        self.mostrando_dialogo = False # Novo estado para interação

        # Inicializa o mapa atual
        self.mapa = None
        self.carregar_mapa_atual()
        self.inicializar_elementos_jogo()

    def carregar_mapa_atual(self):
        """ Carrega o arquivo TMX baseado nas coordenadas atuais do mundo """
        caminho_tmx = self.gerenciador_mapas.get((self.mapa_x, self.mapa_y))
        if caminho_tmx:
            self.mapa = Mapa(caminho_tmx)
        else:
            print(f"ERRO: Mapa na posição ({self.mapa_x}, {self.mapa_y}) não encontrado!")

    def inicializar_elementos_jogo(self):
        self.jogador = Jogador(self.pos_jogador_x, self.pos_jogador_y, self.interface)
        self.npc = Npc(self.pos_npc_x, self.pos_npc_y)
        self.venceu_fase = False
        self.mostrando_dialogo = False
        self.coletavel = Coletavel(self.pos_colet_x, self.pos_colet_y, 'coletavel', 'SwordIcon.png')

    def tratar_transicao_de_tela(self):
        """ 
        Verifica se o jogador saiu dos limites da tela e gerencia a transição
        entre mapas ou bloqueio de borda.
        """
        largura_tela, altura_tela = self.tela.get_size()
        # Aumentamos a margem para garantir que a hitbox inteira entre no novo mapa
        margem_seguranca = 50 
        mudou_mapa = False

        # Variáveis temporárias para as novas coordenadas
        novo_mapa_x, novo_mapa_y = self.mapa_x, self.mapa_y
        nova_pos_x, nova_pos_y = self.jogador.x, self.jogador.y

        # SAÍDA PELA DIREITA
        if self.jogador.hitbox.right > largura_tela:
            novo_mapa_x += 1
            # Posiciona o lado esquerdo da hitbox após a margem
            nova_pos_x = margem_seguranca 
            mudou_mapa = True
        
        # SAÍDA PELA ESQUERDA
        elif self.jogador.hitbox.left < 0:
            novo_mapa_x -= 1
            nova_pos_x = largura_tela - margem_seguranca
            mudou_mapa = True

        # SAÍDA POR BAIXO
        elif self.jogador.hitbox.bottom > altura_tela:
            novo_mapa_y += 1
            nova_pos_y = margem_seguranca
            mudou_mapa = True

        # SAÍDA POR CIMA
        elif self.jogador.hitbox.top < 0:
            novo_mapa_y -= 1
            nova_pos_y = altura_tela - margem_seguranca
            mudou_mapa = True

        if mudou_mapa:
            # Verifica se existe um mapa cadastrado nas novas coordenadas
            if (novo_mapa_x, novo_mapa_y) in self.gerenciador_mapas:
                self.mapa_x, self.mapa_y = novo_mapa_x, novo_mapa_y
                self.jogador.x, self.jogador.y = nova_pos_x, nova_pos_y
                
                # Sincroniza a hitbox IMEDIATAMENTE antes de carregar o mapa
                self.jogador.hitbox.centerx = int(self.jogador.x)
                self.jogador.hitbox.centery = int(self.jogador.y)
                
                self.carregar_mapa_atual()

                if self.mapa_x == -1 and self.mapa_y == 0:
                    self.coletavel.rect.center = (300,300)

                elif self.mapa_x == 0 and self.mapa_y == 1:
                    self.coletavel.rect.center = (600, 600)
                
                elif self.mapa_x == 1 and self.mapa_y == 0:
                    self.coletavel.rect.center = (900, 300)   

                print(f"Mudando para Mapa: ({self.mapa_x}, {self.mapa_y})")
            else:
                # BLOQUEIO DE BORDA: Se não houver mapa, impede a passagem (parede sólida)
                if self.jogador.hitbox.right > largura_tela: 
                    self.jogador.x = largura_tela - (self.jogador.hitbox.width // 2)
                elif self.jogador.hitbox.left < 0: 
                    self.jogador.x = self.jogador.hitbox.width // 2
                elif self.jogador.hitbox.bottom > altura_tela: 
                    self.jogador.y = altura_tela - (self.jogador.hitbox.height // 2)
                elif self.jogador.hitbox.top < 0: 
                    self.jogador.y = self.jogador.hitbox.height // 2
                
                # Sincroniza a hitbox após o bloqueio
                self.jogador.hitbox.centerx = int(self.jogador.x)
                self.jogador.hitbox.centery = int(self.jogador.y)

    def interacao_npc(self):
        """ Verifica se o jogador está perto o suficiente para interagir """
        if self.mapa_x == 0 and self.mapa_y == 0:
            area_interacao = self.npc.hitbox.inflate(50, 50)
            return self.jogador.hitbox.colliderect(area_interacao)
        return False

    def interacao_coletavel(self):
        """ Cria os coletáveis nos mapas esquerdo, baixo e direito """

        # Esquerda
        if self.mapa_x == -1 and self.mapa_y == 0:
            area_coletavel = self.coletavel.hitbox
            return self.jogador.hitbox.colliderect(area_coletavel)
    
        # Baixo
        if self.mapa_x == 0 and self.mapa_y == 1:
            area_coletavel = self.coletavel.hitbox
            return self.jogador.hitbox.colliderect(area_coletavel)
    
        # Direita
        if self.mapa_x == 1 and self.mapa_y == 0:
            area_coletavel = self.coletavel.hitbox
            return self.jogador.hitbox.colliderect(area_coletavel)
        return False

    def run(self):
        rodando = True
        while rodando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                    pygame.quit()
                    sys.exit()
                
                # Gerenciamento de Interação com ENTER
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.mostrando_dialogo:
                            # Se já está aberto, fecha
                            self.mostrando_dialogo = False
                        elif self.interacao_npc():
                            # Se está perto do NPC e fechado, abre
                            self.mostrando_dialogo = True

            if self.estado_atual == 'MENU':
                self.estado_atual = self.interface.desenhar_menu(self.tela)

            elif self.estado_atual == 'FIM_DE_JOGO':
                comando = self.interface.desenhar_fim_de_jogo(
                    self.tela, venceu=self.venceu_fase)
                if comando == "REINICIAR":
                    self.mapa_x, self.mapa_y = 0, 0 # Reseta coordenadas ao reiniciar
                    self.carregar_mapa_atual()
                    self.inicializar_elementos_jogo()
                    self.estado_atual = 'JOGANDO'
                elif comando == "VOLTAR_MENU":
                    self.estado_atual = 'MENU'

            elif self.estado_atual == 'JOGANDO':
                # Salva posição para colisão com NPC
                pos_anterior_x, pos_anterior_y = self.jogador.x, self.jogador.y
                
                # Só move se não estiver em diálogo
                if not self.mostrando_dialogo:
                    self.jogador.update()
                    # 1. TRATAR TRANSIÇÃO DE TELA
                    self.tratar_transicao_de_tela()

                # 2. COLISÃO COM NPC (Só se o NPC estiver no mapa (0,0))
                if self.mapa_x == 0 and self.mapa_y == 0:
                    if self.jogador.hitbox.colliderect(self.npc.hitbox):
                        self.jogador.x, self.jogador.y = pos_anterior_x, pos_anterior_y
                        self.jogador.hitbox.centerx, self.jogador.hitbox.centery = int(self.jogador.x), int(self.jogador.y)

                # 3. INTERAÇÃO (ENTER)
                self.interacao_npc()

                # 4. ITERAÇÃO COM OS COLETÁVEIS

                # Esquerdo
                if self.mapa_x == -1 and self.mapa_y == 0:
                    if self.jogador.hitbox.colliderect(self.coletavel.hitbox):
                        self.jogador.x, self.jogador.y = pos_anterior_x, pos_anterior_y
                        self.jogador.hitbox.centerx, self.jogador.hitbox.centery = int(self.jogador.x), int(self.jogador.y)
                 # Baixo
                if self.mapa_x == 0 and self.mapa_y == 1:
                    if self.jogador.hitbox.colliderect(self.coletavel.hitbox):
                        self.jogador.x, self.jogador.y = pos_anterior_x, pos_anterior_y
                        self.jogador.hitbox.centerx, self.jogador.hitbox.centery = int(self.jogador.x), int(self.jogador.y)

                 # Direito
                if self.mapa_x == 1 and self.mapa_y == 0:
                    if self.jogador.hitbox.colliderect(self.coletavel.hitbox):
                        self.jogador.x, self.jogador.y = pos_anterior_x, pos_anterior_y
                        self.jogador.hitbox.centerx, self.jogador.hitbox.centery = int(self.jogador.x), int(self.jogador.y)

                # DESENHO
                self.tela.fill(self.COR_GRAMA)
                if self.mapa:
                    self.mapa.desenhar(self.tela)

                # Y-SORT
                sprites_para_desenhar = [self.jogador]
                if self.mapa_x == 0 and self.mapa_y == 0:
                    sprites_para_desenhar.append(self.npc)

                if self.mapa_x == -1 and self.mapa_y == 0:
                    sprites_para_desenhar.append(self.coletavel)

                if self.mapa_x == 0 and self.mapa_y == 1:
                    sprites_para_desenhar.append(self.coletavel)

                if self.mapa_x == 1 and self.mapa_y == 0:
                    sprites_para_desenhar.append(self.coletavel)
                
                sprites_para_desenhar.sort(key=lambda sprite: sprite.hitbox.centery)

                for sprite in sprites_para_desenhar:
                    self.tela.blit(sprite.image, sprite.rect)

                self.interface.desenhar_hud_jogo(self.tela, self.jogador.vida, {})

                # DESENHAR DIÁLOGO SE ATIVO
                if self.mostrando_dialogo:
                    self.interface.desenhar_caixa_dialogo(
                        self.tela, 
                        "Rogerin", 
                        f'''Olá Rogerin,me chamo PHP véi, você foi sugado para o universo tecnologico que existe
                        nos computadores do GRAD 5 e preciso da sua ajuda para derrotar o python para eu poder recuperar meus poderes
                         mas, pra isso você precisa enfrentar cada um dos bosses que estão em cada uma das direções. Na esquerda está o trojan, na direita
                          está o loop infinito e em baixo está o memory leak e cada um vai lhe dar um item para derrotar o python que está acima de nós. Conto com sua ajuda '''
                    )

            pygame.display.update()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()
