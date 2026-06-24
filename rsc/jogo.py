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

        # Dicionário de mapas cadastrados
        self.gerenciador_mapas = {
            (0, 0): "../res/Layout_Examples/fundo_central_bloqueado.png",  # Centro (bloqueado no começo)
            (1, 0): "../res/Layout_Examples/fundo_loop.png",               # Direita
            (-1, 0): "../res/Layout_Examples/fundo_memory_leak.png",            # Esquerda
            (0, 1): "../res/Layout_Examples/fundo_trojan.png",       # Baixo
            (0, -1): "../res/Layout_Examples/fundo_python.png"             # Cima
        }

        # Mapas especiais para o centro desbloqueado e topo liberado depois disso
        self.caminho_mapa_central_bloqueado = "../res/Layout_Examples/fundo_central_bloqueado.png"
        self.caminho_mapa_central_desbloqueado = "../res/Layout_Examples/fundo_central_desbloqueado.png"
        self.mapa_central_desbloqueado = False

        #posições iniciais
        self.pos_npc_x, self.pos_npc_y = 600, 400
        self.pos_jogador_x, self.pos_jogador_y = 400, 300
        self.pos_colet_x, self.pos_colet_y = -1000, -1000

        # Máquina de Estados
        self.estado_atual = 'MENU'
        self.venceu_fase = False
        self.mostrando_dialogo = False # Novo estado para interação

        # Inicializa o mapa atual
        self.mapa = None
        self.inimigos_necessarios = 3
        self.inimigos_por_mapa = {
            (-1, 0): {'x': 200, 'y': 300, 'tipo': 'memory_leak'},
            (1, 0): {'x': 800, 'y': 300, 'tipo': 'loop_infinito'},
            (0, 1): {'x': 500, 'y': 500, 'tipo': 'trojan'}
        }

        self.carregar_mapa_atual()
        self.inicializar_elementos_jogo()

    def carregar_mapa_atual(self):
        """ Carrega o arquivo TMX baseado nas coordenadas atuais do mundo """
        caminho_tmx = self.obter_caminho_mapa_atual()
        if caminho_tmx:
            self.mapa = Mapa(caminho_tmx)
            self.redefinir_inimigos_do_mapa()
        else:
            print(f"ERRO: Mapa na posição ({self.mapa_x}, {self.mapa_y}) não encontrado!")

    def obter_caminho_mapa_atual(self):
        """Escolhe o mapa correto do centro de acordo com o progresso do jogador."""
        if (self.mapa_x, self.mapa_y) == (0, 0) and self.mapa_central_desbloqueado:
            return self.caminho_mapa_central_desbloqueado
        return self.gerenciador_mapas.get((self.mapa_x, self.mapa_y))

    def pode_acessar_mapa(self, x, y):
        """Impede o topo de ser liberado antes do centro desbloquear."""
        if (x, y) == (0, -1):
            return self.mapa_central_desbloqueado
        return (x, y) in self.gerenciador_mapas

    def redefinir_inimigos_do_mapa(self):
        """Cria os inimigos apenas nos mapas que precisam deles."""
        self.inimigos = []
        posicao = (self.mapa_x, self.mapa_y)
        if posicao in self.inimigos_por_mapa:
            dados = self.inimigos_por_mapa[posicao]
            self.inimigos.append(
                Inimigo(
                    dados['x'],
                    dados['y'],
                    self.interface,
                    tipo=dados['tipo']
                )
            )

    def inicializar_elementos_jogo(self):
        self.jogador = Jogador(self.pos_jogador_x, self.pos_jogador_y, self.interface)
        self.npc = Npc(self.pos_npc_x, self.pos_npc_y)
        self.venceu_fase = False
        self.mostrando_dialogo = False
        self.inimigos_derrotados = 0
        self.mapa_central_desbloqueado = False
        self.coletavel = Coletavel(self.pos_colet_x, self.pos_colet_y, 'coletavel', None)

        # Inventário do jogador (set de cores: 'amarelo','roxo','azul')
        self.inventario = set()

        self.coletaveis_coletados = {(-1, 0): "escondido",
                                    (1, 0): "escondido",
                                    (0, 1): "escondido"}

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
            # Verifica se o novo mapa pode ser acessado
            if self.pode_acessar_mapa(novo_mapa_x, novo_mapa_y):
                self.mapa_x, self.mapa_y = novo_mapa_x, novo_mapa_y
                self.jogador.x, self.jogador.y = nova_pos_x, nova_pos_y
                
                # Sincroniza a hitbox IMEDIATAMENTE antes de carregar o mapa
                self.jogador.hitbox.centerx = int(self.jogador.x)
                self.jogador.hitbox.centery = int(self.jogador.y)
                
                self.carregar_mapa_atual()

                if self.mapa_x == -1 and self.mapa_y == 0:
                    # Mapa da esquerda -> coletável azul
                    self.coletavel.rect.center = (300, 300)
                    try:
                        self.coletavel.atualizar_imagem('coletavel_azul.png')
                    except Exception:
                        pass

                elif self.mapa_x == 0 and self.mapa_y == 1:
                    # Mapa de baixo -> coletável roxo
                    self.coletavel.rect.center = (600, 600)
                    try:
                        self.coletavel.atualizar_imagem('coletavel_roxo.png')
                    except Exception:
                        pass
                
                elif self.mapa_x == 1 and self.mapa_y == 0:
                    # Mapa da direita -> coletável amarelo
                    self.coletavel.rect.center = (900, 300)
                    try:
                        self.coletavel.atualizar_imagem('coletavel_amarelo.png')
                    except Exception:
                        pass

                self.coletavel.hitbox.center = self.coletavel.rect.center

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

    def atualizar_combate(self):
        """Atualiza inimigos e verifica se o jogador derrotou os três chefes."""
        for inimigo in self.inimigos[:]:
            if inimigo.vida <= 0:
                self.inimigos.remove(inimigo)
                self.inimigos_derrotados += 1

                # Faz o coletável aparecer apenas qaundo o inimigo morre
                posicao_atual = (self.mapa_x, self.mapa_y)
                if posicao_atual in self.coletaveis_coletados:
                    self.coletaveis_coletados[posicao_atual] = "no_chao"

                if self.inimigos_derrotados >= self.inimigos_necessarios:
                    self.mapa_central_desbloqueado = True
                continue

            inimigo.update(self.jogador)

        if self.jogador.atacando:
            area_ataque = self.jogador.criar_hitbox_ataque()
            for inimigo in self.inimigos:
                if area_ataque.colliderect(inimigo.hitbox):
                    inimigo.receber_dano(25)
                    break

    def adicionar_item_inventario(self, posicao):
        """Adiciona o item correto ao inventário com base na posição do mapa.
        Posições mapeadas:
            (1,0) -> amarelo (direita)
            (0,1) -> roxo (baixo)
            (-1,0) -> azul (esquerda)
        """
        mapa_para_cor = {
            (1, 0): 'amarelo',
            (0, 1): 'roxo',
            (-1, 0): 'azul'
        }
        cor = mapa_para_cor.get(posicao)
        if not cor:
            return
        if cor in self.inventario:
            return
        self.inventario.add(cor)

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
                    self.atualizar_combate()
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
                posicao_atual = (self.mapa_x, self.mapa_y)
                if self.coletaveis_coletados.get(posicao_atual) == "no_chao":
                    if self.jogador.hitbox.colliderect(self.coletavel.hitbox):
                        self.coletaveis_coletados[posicao_atual] = "coletado"
                        # Atualiza inventário conforme o mapa em que o item foi coletado
                        self.adicionar_item_inventario(posicao_atual)

                # DESENHO
                self.tela.fill(self.COR_GRAMA)
                if self.mapa:
                    self.mapa.desenhar(self.tela)

                # Y-SORT
                sprites_para_desenhar = [self.jogador]
                if self.mapa_x == 0 and self.mapa_y == 0:
                    sprites_para_desenhar.append(self.npc)

                if self.coletaveis_coletados.get(posicao_atual) == "no_chao":
                    sprites_para_desenhar.append(self.coletavel)

                sprites_para_desenhar.extend(self.inimigos)
                
                sprites_para_desenhar.sort(key=lambda sprite: sprite.hitbox.centery)

                for sprite in sprites_para_desenhar:
                    self.tela.blit(sprite.image, sprite.rect)

                self.interface.desenhar_hud_jogo(self.tela, self.jogador.vida, self.inventario)

                # DESENHAR DIÁLOGO SE ATIVO
                if self.mostrando_dialogo:
                    self.interface.desenhar_caixa_dialogo(
                        self.tela, 
                        "Rogerin", 
                        f'''Olá Rogerin, me chamo PHP véi, você foi sugado para o universo tecnológico dentro dos computadores do GRAD 5. Preciso da sua ajuda para derrotar o python e recuperar meus poderes como linguagem mais popular.
                         Mas, para isso, você precisa enfrentar cada um dos inimigos que estão ao nosso redor: à esquerda está o trojan, à direita
                          está o loop infinito e em baixo está o memory leak. Cada um vai lhe dar um item para derrotar o python que está atualmente acima de nós. Conto com sua ajuda! '''
                    )

            pygame.display.update()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()
