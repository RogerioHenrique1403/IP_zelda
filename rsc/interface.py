import pygame
import os
from configuracoes import Configuracao


class Interface:
    def __init__(self):
        # 1. Carrega as configurações
        self.config = Configuracao()

        # Salvamos em self.tela para podermos acessar depois
        self.tela = pygame.display.set_mode(
            (self.config.largura, self.config.altura))
        pygame.display.set_caption("Zelda Clone")

        # 3. AGORA pode carregar as imagens (pois a tela já existe!)
        self.carregar_imagens_vida()

    def criar_tela(self):
        pygame.display.set_caption("Pixel Quest RPG")
        return pygame.display.set_mode((self.largura_tela, self.altura_tela))

    def carregar_imagens_vida(self):
        self.imagens_vida = {}
        valores_vida = [20, 40, 60, 80, 100]

        # 1. Pega onde o script está
        diretorio_script = os.path.dirname(os.path.abspath(__file__))

        # 2. Define as possíveis localizações da pasta 'ui'
        caminhos_possiveis = [
            # Tenta voltar uma pasta (padrão rsc/..)
            os.path.join(diretorio_script, '..', 'res', 'ui'),
            # Tenta na mesma pasta (padrão raiz)
            os.path.join(diretorio_script, 'res', 'ui'),
            # Tenta relativo à execução
            os.path.join('res', 'ui')
        ]

        caminho_final = None

        # 3. Testa qual caminho existe de verdade
        for caminho in caminhos_possiveis:
            if os.path.exists(caminho):
                caminho_final = caminho
                print(
                    f"--- SUCESSO: Pasta de imagens encontrada em: {caminho}")
                break

        # 4. Se achou a pasta, carrega as imagens
        if caminho_final:
            for val in valores_vida:
                nome_arquivo = f'vida_{val}.png'
                caminho_img = os.path.join(caminho_final, nome_arquivo)

                try:
                    img = pygame.image.load(caminho_img).convert_alpha()
                    # Aumenta o tamanho (escala)
                    escala = 0.8
                    img = pygame.transform.scale(
                        img, (img.get_width() * escala, img.get_height() * escala))
                    self.imagens_vida[val] = img
                except Exception as e:
                    print(f"ERRO ao carregar {nome_arquivo}: {e}")
        else:
            print("--- ERRO FATAL: Não encontrei a pasta 'res/ui' em lugar nenhum!")
            print(f"Tentamos procurar em: {caminhos_possiveis}")

    def desenhar(self, tela, vida_atual):
        # 1. Lógica de Seleção da Imagem (Mantendo a sua lógica, que está boa)
        if vida_atual > 80:
            chave = 100
        elif vida_atual > 60:
            chave = 80
        elif vida_atual > 40:
            chave = 60
        elif vida_atual > 20:
            chave = 40
        else:
            chave = 20  # Vida crítica ou 0

        # 2. DEFININDO A POSIÇÃO (Canto Superior Esquerdo)
        # X = Distância da esquerda
        # Y = Distância do topo
        pos_x = 10
        pos_y = 10

        # 3. Desenha a imagem
        if chave in self.imagens_vida:
            # Desenha a imagem na posição (20, 20)
            tela.blit(self.imagens_vida[chave], (pos_x, pos_y))
        else:
            # PLANO B: Quadrado vermelho (Debug)
            # Desenha no mesmo lugar (20, 20)
            pygame.draw.rect(tela, (255, 0, 0), (pos_x, pos_y, 100, 30))
            print(f"ALERTA: Imagem da vida {chave} não encontrada!")
