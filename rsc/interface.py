import pygame
import os
from configuracoes import Configuracao


class Interface:
    def __init__(self):
        self.config = Configuracao()
        self.tela = pygame.display.set_mode(
            (self.config.largura, self.config.altura))
        pygame.display.set_caption("the python's trial")

        # Inicializa as fontes do PyGame
        pygame.font.init()

        caminho_fonte = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'res', 'Fonts', 'upheaval' ,'upheavtt.ttf')
        
        if os.path.exists(caminho_fonte):
            self.fonte_placar = pygame.font.Font(caminho_fonte, 20)
            self.fonte_titulo = pygame.font.Font(caminho_fonte, 48)
            self.fonte_botoes = pygame.font.Font(caminho_fonte, 24) # <--- Esta muda a fonte do botão COMEÇAR e FIM DE JOGO
        else:
            # Caso não ache o arquivo, mantém o comportamento atual
            self.fonte_placar = pygame.font.SysFont('Arial', 24, bold=True)
            self.fonte_titulo = pygame.font.SysFont('Arial', 60, bold=True)
            self.fonte_botoes = pygame.font.SysFont('Arial', 32, bold=True)
        
        self.carregar_imagens_vida()

        # Carrega imagem de fundo do menu (fundo_menu) se existir
        self.fundo_menu = None
        self.carregar_fundo_menu()

        # Carrega imagens de fim de jogo (vitória e derrota)
        self.fundo_win = None
        self.fundo_game_over = None
        self.carregar_fundos_fim_de_jogo()


        # Carrega sprites do inventário
        self.inventario_imgs = {}
        self.carregar_inventario_sprites()

    def criar_tela(self):
        pygame.display.set_caption("the python's trial")
        return pygame.display.set_mode((self.largura_tela, self.altura_tela))

    def carregar_imagens_vida(self):
        self.imagens_vida = {}
        valores_vida = [20, 40, 60, 80, 100]
        diretorio_script = os.path.dirname(os.path.abspath(__file__))

        caminhos_possiveis = [
            os.path.join(diretorio_script, '..', 'res', 'ui'),
            os.path.join(diretorio_script, 'res', 'ui'),
            os.path.join('res', 'ui')
        ]

        caminho_final = None
        for caminho in caminhos_possiveis:
            if os.path.exists(caminho):
                caminho_final = caminho
                print(f"--- SUCESSO: Pasta de imagens encontrada em: {caminho}")
                break

        if caminho_final:
            for val in valores_vida:
                nome_arquivo = f'vida_{val}.png'
                caminho_img = os.path.join(caminho_final, nome_arquivo)
                try:
                    img = pygame.image.load(caminho_img).convert_alpha()
                    escala = 0.8
                    img = pygame.transform.scale(
                        img, (img.get_width() * escala, img.get_height() * escala))
                    self.imagens_vida[val] = img
                except Exception as e:
                    print(f"ERRO ao carregar {nome_arquivo}: {e}")
        else:
            print("--- ERRO FATAL: Não encontrei a pasta 'res/ui' em lugar nenhum!")

    def carregar_fundo_menu(self):
        diretorio_script = os.path.dirname(os.path.abspath(__file__))
        caminhos_possiveis = [
            os.path.join(diretorio_script, '..', 'res', 'Layout_Examples'),
            os.path.join(diretorio_script, '..', 'res', 'ui'),
            os.path.join(diretorio_script, 'res', 'ui'),
            os.path.join('res', 'Layout_Examples'),
            os.path.join('res', 'ui')
        ]

        caminho_final = None
        for caminho in caminhos_possiveis:
            if os.path.exists(caminho):
                # procura por arquivos que comecem com 'fundo_menu'
                for f in os.listdir(caminho):
                    if f.lower().startswith('fundo_menu') and f.lower().endswith(('.png', '.jpg', '.jpeg')):
                        caminho_final = os.path.join(caminho, f)
                        break
            if caminho_final:
                break

        if caminho_final and os.path.exists(caminho_final):
            try:
                self.fundo_menu = pygame.image.load(caminho_final).convert()
            except Exception as e:
                print(f"ERRO ao carregar fundo_menu: {e}")
        else:
            self.fundo_menu = None

    def carregar_fundos_fim_de_jogo(self):
       
        diretorio_script = os.path.dirname(os.path.abspath(__file__))
        pasta_imagens = os.path.join(diretorio_script, '..', 'res', 'Layout_Examples')

        if not os.path.exists(pasta_imagens):
            print(f"--- AVISO: Pasta {pasta_imagens} não encontrada. Fundos de fim de jogo serão pretos.")
            return

        # Carregar imagem de vitória (fundo_win.png)
        caminho_win = os.path.join(pasta_imagens, 'fundo_win.png')
        if os.path.exists(caminho_win):
            try:
                self.fundo_win = pygame.image.load(caminho_win).convert()
                # Opcional: redimensionar para o tamanho da tela
                self.fundo_win = pygame.transform.scale(self.fundo_win, (self.config.largura, self.config.altura))
            except Exception as e:
                print(f"ERRO ao carregar fundo_win.png: {e}")

        # Carregar imagem de derrota (fundo_game_over.png)
        caminho_loss = os.path.join(pasta_imagens, 'fundo_game_over.png')
        if os.path.exists(caminho_loss):
            try:
                self.fundo_game_over = pygame.image.load(caminho_loss).convert()
                # Opcional: redimensionar para o tamanho da tela
                self.fundo_game_over = pygame.transform.scale(self.fundo_game_over, (self.config.largura, self.config.altura))
            except Exception as e:
                print(f"ERRO ao carregar fundo_game_over.png: {e}")

    def carregar_inventario_sprites(self):
        diretorio_script = os.path.dirname(os.path.abspath(__file__))
        caminhos_possiveis = [
            os.path.join(diretorio_script, '..', 'res', 'sprites inventario'),
            os.path.join(diretorio_script, '..', 'res', 'sprites_inventario'),
            os.path.join(diretorio_script, 'res', 'sprites inventario'),
            os.path.join('res', 'sprites inventario')
        ]

        pasta_final = None
        for caminho in caminhos_possiveis:
            if os.path.exists(caminho):
                pasta_final = caminho
                break

        if pasta_final:
            try:
                for f in os.listdir(pasta_final):
                    if f.lower().endswith(('.png', '.jpg', '.jpeg')) and f.lower().startswith('inventario'):
                        try:
                            img = pygame.image.load(os.path.join(pasta_final, f)).convert_alpha()
                            self.inventario_imgs[f] = img
                        except Exception as e:
                            print(f"ERRO ao carregar inventário {f}: {e}")
            except Exception as e:
                print(f"ERRO acessando pasta de inventário: {e}")
        else:
            print("--- Aviso: pasta de sprites de inventario não encontrada. Usarei placeholders.")

    def desenhar_hud_jogo(self, tela, vida_atual, inventario_jogador):
        """ Desenha a vida e o placar de coletáveis durante a gameplay """
        # BARRA DE VIDA
        if vida_atual > 80:
            chave = 100
        elif vida_atual > 60:
            chave = 80
        elif vida_atual > 40:
            chave = 60
        elif vida_atual > 20:
            chave = 40
        else:
            chave = 20

        pos_x, pos_y = 10, 10
        if chave in self.imagens_vida:
            tela.blit(self.imagens_vida[chave], (pos_x, pos_y))
        else:
            pygame.draw.rect(tela, (255, 0, 0), (pos_x, pos_y, 100, 30))

        # 2. Desenha inventário no canto inferior direito
        try:
            self.desenhar_inventario(tela, inventario_jogador)
        except Exception as e:
            # Não quebrar o jogo por falha no inventário
            print(f"ERRO desenhando inventario: {e}")

    def desenhar_caixa_dialogo(self, tela, nome, mensagem):
        """ Desenha uma caixa de diálogo que ajusta o tamanho conforme o texto """
        largura_caixa = self.config.largura - 100
        largura_maxima_texto = largura_caixa - 40 # Margem interna
        espacamento_y = 30
        
        # Lógica de Quebra de Linha (Word Wrap) antecipada para calcular altura
        palavras = mensagem.replace('\n', ' ').split(' ')
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            if not palavra: continue
            test_line = linha_atual + palavra + " "
            if self.fonte_placar.size(test_line)[0] < largura_maxima_texto:
                linha_atual = test_line
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + " "
        linhas.append(linha_atual)

        # Calcular Altura Dinâmica
        # (Topo + Nome + Linhas de Texto + Rodapé + Margem)
        altura_caixa = 60 + (len(linhas) * espacamento_y) + 40
        x = 50
        y = self.config.altura - altura_caixa - 30

        # Desenhar Fundo da caixa
        rect_caixa = pygame.Rect(x, y, largura_caixa, altura_caixa)
        pygame.draw.rect(tela, (0, 0, 0), rect_caixa)
        pygame.draw.rect(tela, (255, 255, 255), rect_caixa, 3) 

        # Desenhar Nome do Personagem
        surf_nome = self.fonte_placar.render(f"[{nome}]", True, (255, 215, 0))
        tela.blit(surf_nome, (x + 20, y + 15))

        # Desenhar cada linha de texto
        pos_y_texto = y + 55
        for linha in linhas:
            surf_msg = self.fonte_placar.render(linha.strip(), True, (255, 255, 255))
            tela.blit(surf_msg, (x + 20, pos_y_texto))
            pos_y_texto += espacamento_y

        # Instrução de rodapé
        surf_inst = self.fonte_placar.render("ENTER para fechar", True, (150, 150, 150))
        tela.blit(surf_inst, (x + largura_caixa - 220, y + altura_caixa - 35))


    def desenhar_menu(self, tela, eventos=[]):
        """ Desenha a tela inicial de Menu e retorna True se clicar em Começar """
        # Desenha fundo do menu
        if self.fundo_menu:
            try:
                # Nota: A imagem já deve estar redimensionada se você fez isso no carregar_fundo_menu
                # Se não, mantenha a linha abaixo.
                img = pygame.transform.scale(self.fundo_menu, (self.config.largura, self.config.altura))
                tela.blit(img, (0, 0))
            except Exception:
                tela.fill((20, 40, 20))
        else:
            tela.fill((20, 40, 20)) # Fundo verde escuro

        # Botão Começar 
        largura_btn, altura_btn = 295, 110
        x_btn = (self.config.largura // 2) - (largura_btn // 2)
        y_btn = int(self.config.altura * 0.70)
        rect_botao = pygame.Rect(x_btn, y_btn, largura_btn, altura_btn)

        # Detecta clique e hover do mouse
        pos_mouse = pygame.mouse.get_pos()
        clique_mouse = False
        for event in eventos:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clique_mouse = True

        cor_botao = (0, 0, 0)  # fundo preto
        if rect_botao.collidepoint(pos_mouse):
            cor_botao = (50, 50, 50)  # ligeiro destaque no hover
            if clique_mouse:  # Clique com botão esquerdo
                return "JOGANDO"

        pygame.draw.rect(tela, cor_botao, rect_botao, border_radius=10)
        pygame.draw.rect(tela,(0, 0, 0,), rect_botao, 2, border_radius=10)  # Borda preta

        texto_btn = self.fonte_botoes.render("COMEÇAR", True, (255, 255, 255))
        rect_texto_btn = texto_btn.get_rect(center=rect_botao.center)
        tela.blit(texto_btn, rect_texto_btn)

        return "MENU"

    def desenhar_inventario(self, tela, inventario_set):
        """Desenha a sprite do inventário no canto inferior direito com base nos itens coletados.
        inventario_set é um set() contendo strings: 'amarelo', 'roxo', 'azul'
        """
        # Normaliza e monta nome do arquivo esperado
        itens = sorted(list(inventario_set)) if inventario_set else []
        if len(itens) == 0:
            nome = 'inventario_vazio.png'
        elif len(itens) == 3:
            nome = 'inventario_completo.png'
        else:
            nome = 'inventario_' + '_'.join(itens) + '.png'

        img = None
        # Tenta obter imagem carregada
        if nome in self.inventario_imgs:
            img = self.inventario_imgs[nome]
        else:
            # fallback: inventario_vazio
            img = self.inventario_imgs.get('inventario_vazio.png')

        if img:
            margem = 20
            largura = img.get_width()
            altura = img.get_height()
            x = self.config.largura - largura - margem
            y = self.config.altura - altura - margem
            tela.blit(img, (x, y))
        else:
            # fallback simples: caixa preta no canto
            margem = 10
            largura = 96
            altura = 96
            x = self.config.largura - largura - margem
            y = self.config.altura - altura - margem
            pygame.draw.rect(tela, (0, 0, 0), (x, y, largura, altura))

    def desenhar_fim_de_jogo(self, tela, venceu=False, eventos=[]):
        """ Desenha a tela de Vitória ou Derrota e gerencia os cliques nos botões """
        
        # 1. Desenha a imagem de fundo correspondente
        fundo_a_desenhar = None
        if venceu:
            fundo_a_desenhar = self.fundo_win
        else:
            fundo_a_desenhar = self.fundo_game_over

        if fundo_a_desenhar:
            try:
                tela.blit(fundo_a_desenhar, (0, 0))
            except Exception:
                tela.fill((10, 10, 10)) 
        else:
            tela.fill((10, 10, 10)) 

        # 3. Configurações de clique do mouse
        pos_mouse = pygame.mouse.get_pos()
        clique_mouse = False
        for event in eventos:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clique_mouse = True

        # JOGAR DE NOVO 
        largura_btn_novo, altura_btn_novo = 205, 150  # Maior para preencher bem o monitor central
        x_btn_novo = (self.config.largura // 2) - (largura_btn_novo // 2)
        y_btn_novo = 300  # Posição centralizada verticalmente no monitor do meio
        rect_btn_novo = pygame.Rect(x_btn_novo, y_btn_novo, largura_btn_novo, altura_btn_novo)
        
        cor_btn_novo = (0,0,0)  # Cor escura para camuflar no monitor apagado
        if rect_btn_novo.collidepoint(pos_mouse):
            cor_btn_novo = (55, 55, 55)
            if clique_mouse:
                return "REINICIAR"

        # --- BOTÃO 2: VOLTAR AO MENU 
        largura_btn_menu, altura_btn_menu = 300, 120  # Bem largo para abranger ambos os monitores inferiores
        x_btn_menu = (self.config.largura // 2) - (largura_btn_menu // 2)
        y_btn_menu = 500  # Alinhado na altura dos monitores de baixo
        rect_btn_menu = pygame.Rect(x_btn_menu, y_btn_menu, largura_btn_menu, altura_btn_menu)
        
        cor_btn_menu = (0,0,0)  # Cor preta padrão
        if rect_btn_menu.collidepoint(pos_mouse):
            cor_btn_menu = (55, 55, 55)
            if clique_mouse:
                return "VOLTAR_MENU"

        # Desenhar Botão Jogar de Novo
        pygame.draw.rect(tela, cor_btn_novo, rect_btn_novo, border_radius=6)
        pygame.draw.rect(tela, (0,0,0), rect_btn_novo, 1, border_radius=6) # Borda sutil
        txt_novo = self.fonte_botoes.render("JOGAR DE NOVO", True, (255, 255, 255))
        tela.blit(txt_novo, txt_novo.get_rect(center=rect_btn_novo.center))

        # Desenhar Botão Voltar ao Menu
        pygame.draw.rect(tela, cor_btn_menu, rect_btn_menu, border_radius=6)
        pygame.draw.rect(tela, (0,0,0), rect_btn_menu, 1, border_radius=6)
        txt_menu = self.fonte_botoes.render("VOLTAR AO MENU", True, (255, 255, 255))
        tela.blit(txt_menu, txt_menu.get_rect(center=rect_btn_menu.center))

        return "FIM_DE_JOGO"