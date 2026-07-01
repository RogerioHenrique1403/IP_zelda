# The Python's Trial

**Disciplina:** Introdução a Programação - UFPE  
**Semestre:**  2026.1

"Bem-vindo ao *The Python's Trial*, o pesadelo real de todo estudante de TI!

Um erro crítico corrompeu o sistema acadêmico, e a última linha de defesa é você: o Calouro de IP. Armado apenas com sua capa de estudante e uma espada de "debug" corpo a corpo, você precisará limpar o código na marra.
Sob a orientação do lendário e enferrujado C-Véio, um compilador das antigas, sua missão é provar seu valor derrotando os três maiores traumas de qualquer programador iniciante: escape do ácido do Memory Leak, quebre o ciclo mortal do Loop Infinito e desmascare a traição do Trojan.
Somente ao dominar a memória, a lógica e a segurança do sistema, você terá acesso ao confronto final contra o chefão supremo: a temível hidra de cabos conhecida como Python.

Empunhe sua espada, rebata os SyntaxErrors e lute para dar orgulho ao seu mentor. O semestre já começou."

## 👥 Membros da Equipe
* **Rafaela Lins**: [Seu GitHub e/ou LinkedIn]
* **Rogério Henrique**: [GitHub e/ou LinkedIn]
* **Lucas Mateus**: [GitHub e/ou LinkedIn]
* **Lucas Ryan**: [GitHub e/ou LinkedIn]

---

## 🏗️ Arquitetura do Projeto

O projeto foi estruturado seguindo o paradigma de Orientação a Objetos (POO), com uma separação clara entre a lógica de programação e os recursos visuais. O repositório está dividido em dois diretórios principais: `res/` (recursos gráficos) e `rsc/` (scripts em Python).

### 📁 Estrutura de Diretórios

**1. Diretório `rsc/` (Código-Fonte)**
Contém toda a lógica do jogo, com responsabilidades modulares bem definidas:
* `main.py`: Ponto de entrada do programa. Inicializa o Pygame e dá o gatilho inicial na execução.
* `jogo.py`: Gerenciador principal do game loop, coordenando atualizações de tela, eventos e estados do jogo.
* `configuracoes.py`: Arquivo central para constantes globais (tamanho de tela, FPS, cores, caminhos de diretórios).
* `personagem.py`: Classe mãe (superclasse) que dita a física, vida e base de movimentação das entidades vivas.
* `jogador.py` e `inimigos.py`: Classes filhas que herdam de `Personagem`, checagem de inputs, ataques e lógicas específicas.
* `mapa.py`: Responsável por carregar o layout dos níveis, gerenciar colisões com o cenário e renderizar o chão/paredes.
* `interface.py`: Controla a camada de UI, desenhando a HUD, menus, barras de vida e textos na tela.
* `coletaveis.py`: Gerencia a lógica de itens que o jogador pode interagir ou pegar pelo mapa.
* `spritesheet.py`: Classe utilitária focada exclusivamente em fatiar e processar arquivos de imagem complexos.

**2. Diretório `res/` (Assets / Recursos Visuals)**
Armazena todos os arquivos de mídia, devidamente categorizados para facilitar a manutenção:
* `Player/` e `Inimigos sprite/`: Sprites animados e folhas de textura das entidades.
* `ui/` e `sprites inventario/`: Elementos da interface de usuário, cursores e ícones de itens.
* `Layout_Examples/`: Modelos e arquivos auxiliares para a montagem dos mapas.
* `Objects/`, `Itens/`, `npc/` e `Coletaveis/`: Gráficos estáticos e interativos espalhados pelo mundo do jogo.

## 📸 Galeria do Projeto

Aqui estão algumas capturas de tela demonstrando o sistema em funcionamento:

---

## 🛠️ Ferramentas, Bibliotecas e Frameworks

* **Python 3.11:** Linguagem principal escolhida por sua curva de aprendizado ágil e adequação aos requisitos acadêmicos da disciplina.
* **Pygame:** Biblioteca utilizada para a renderização gráfica 2D, manipulação de inputs do teclado, detecção de colisões (hitboxes) e controle da taxa de quadros (FPS), justificada pela sua robustez para prototipagem rápida de jogos independentes.
* **Git e GitHub:** Utilizados para o versionamento de código e colaboração em equipe, garantindo a integridade do projeto através do fluxo de branches e merges.
* **VS Code:** IDE adotada pela facilidade de integração com o GitHub e suporte a extensões de produtividade.

---

## 📊 Divisão de Trabalho

| Membro da Equipe | Responsabilidades Principais |
| :--- | :--- |
| **[Seu Nome]** | Implementação da lógica de Inimigos (refatoração de classes, correção de bugs de animação de sprites), sistema de herança e mecânica do boss final. |
| **[Colega 1]** | [Ex: Criação do mapa, sistema de interface e HUD] |
| **[Colega 2]** | [Ex: Lógica do jogador, controles de ataque e colisão] |

---

## 📚 Conceitos da Disciplina Utilizados

Durante o desenvolvimento, aplicamos diversos conceitos abordados em aula:

* **Programação Orientada a Objetos (Herança e Polimorfismo):** Utilizado intensamente nas classes de entidades. A classe base `Personagem` concentra a lógica de vida e movimentação, enquanto `Jogador` e `Inimigo` herdam essas características e implementam seus próprios comportamentos de `update` e `animar`.
* **Lógica de Colisão e Hitboxes:** Implementação matemática para calcular a distância entre o centro do jogador e os inimigos (`dx` e `dy`), permitindo o raio de visão e os ataques.
* **[Adicione outro conceito 1]:** [Onde foi usado, ex: Padrões de Projeto / Lógica de Estados (Máquina de Estados para animações)].
* **[Adicione outro conceito 2]:** [Onde foi usado].

---

## ⚠️ Desafios, Erros e Lições Aprendidas

### Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?
Ex: O maior erro ocorreu na manipulação e fatiamento das *sprite sheets* dos inimigos (ex: a animação corria rápido demais parecendo um "rolo de filme"). O erro aconteceu porque tentamos aplicar uma divisão matemática padrão de frames para imagens que possuíam quantidades diferentes de desenhos (algumas tinham 5 frames, outras 2). Lidamos com isso refatorando a classe de carregamento para aceitar quantidades dinâmicas de fatiamento e mesclando o uso de tiras com o carregamento de imagens individuais (no caso do Trojan).

### Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?
[Descreva aqui um desafio. Ex: O maior desafio foi gerenciar as transições de estado do jogo de forma limpa, como a mudança de comportamento de "disfarçado" para "revelado" do inimigo Trojan, sem que a animação travasse. Lidamos com isso separando o controle de tempo (ticks) da troca de eixos (X e Y), resetando a animação apenas quando o estado real do personagem era alterado.]

### Quais as lições aprendidas durante o projeto?
* A importância de manter uma estrutura de pastas de assets padronizada e nomeada de forma clara.
* Compreensão profunda do game loop e como a atualização visual precisa estar desvinculada da lógica física para não causar travamentos.
* A necessidade de comunicação constante no Git para evitar conflitos ao trabalhar no mesmo repositório.
