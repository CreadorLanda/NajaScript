# NajaGame2D - Framework para Jogos 2D em NajaScript

NajaGame2D é uma biblioteca simples e poderosa para desenvolvimento de jogos 2D usando a linguagem NajaScript. Esta biblioteca facilita a criação de jogos com elementos como sprites, animações, física básica, detecção de colisões e gerenciamento de cenas.

## Índice

1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Estrutura Básica](#estrutura-básica)
4. [Principais Componentes](#principais-componentes)
5. [Ciclo de Vida do Jogo](#ciclo-de-vida-do-jogo)
6. [Exemplos](#exemplos)
7. [API Completa](#api-completa)

## Visão Geral

NajaGame2D é uma biblioteca para desenvolvimento de jogos 2D que aproveita os recursos da linguagem NajaScript, como:

- Tipagem estática para código mais robusto
- Variáveis reativas (flux) para UI dinâmica
- Sistema de eventos para monitorar mudanças
- Estrutura de dados como listas e dicionários para gerenciar objetos do jogo

A biblioteca implementa um design baseado em cenas e objetos, com um loop de jogo que gerencia a física, entrada do usuário e renderização.

## Instalação

Para usar a biblioteca em seu projeto:

```naja
# Importe a biblioteca no seu arquivo .naja
import "NajaGame2D.naja";
```

## Estrutura Básica

Um jogo típico usando NajaGame2D segue esta estrutura:

1. **Inicialização**: Configure o ambiente de jogo
2. **Carregamento de recursos**: Carregue sprites, sons e outros recursos
3. **Criação de objetos**: Defina personagens, plataformas, etc.
4. **Configuração de cenas**: Organize objetos em cenas (níveis, menus)
5. **Lógica do jogo**: Implemente as regras e comportamentos
6. **Loop principal**: Execute o jogo

Exemplo mínimo:

```naja
# Cria o jogo
dict meuJogo = initGame(800, 600, "Meu Jogo");

# Cria recursos
dict sprite = criarSprite("imagem.png", 64, 64);
dict personagem = criarObjeto("jogador", 100, 100, sprite);

# Cria uma cena
fun atualizar(dict game, float delta) {
    # Lógica do jogo
}

fun renderizar(dict game) {
    # Renderização
}

dict cena = criarCena("principal", atualizar, renderizar);
adicionarObjetoACena(cena, personagem);
adicionarCena(meuJogo, cena);

# Inicia o jogo
trocarCena(meuJogo, "principal");
startGame(meuJogo);
```

## Principais Componentes

### Gerenciador de Jogo

O componente principal é o objeto de jogo, que contém:

- Configurações de tela (largura, altura)
- Gerenciamento de cenas
- Controle de entrada (teclado, mouse)
- Loop principal

### Cenas

As cenas representam diferentes partes do jogo (níveis, menus, etc) e contêm:

- Conjunto de objetos de jogo
- Função de atualização (lógica)
- Função de renderização (visual)

### Objetos

Cada entidade no jogo é um objeto que possui:

- Posição (x, y)
- Sprite (aparência visual)
- Velocidade (para movimento)
- Propriedades específicas

### Sistema de Física

Implementação básica de física para jogos:

- Gravidade
- Detecção de colisão AABB (Axis-Aligned Bounding Box)
- Resposta à colisão

### Sistema de Entrada

Gerencia entradas do usuário:

- Teclado (teclas pressionadas)
- Mouse (posição, cliques)

### Sistema de Áudio

Controla efeitos sonoros e música:

- Sons pontuais
- Música de fundo
- Controle de volume e repetição

## Ciclo de Vida do Jogo

1. **Inicialização**: `initGame()` configura os sistemas
2. **Loop principal**: Executa continuamente:
   - Cálculo de delta tempo (diferença entre frames)
   - Atualização da lógica do jogo
   - Verificação de entrada do usuário
   - Detecção de colisões
   - Renderização de objetos
   - Repetição do loop

## Exemplos

### Jogo de Plataforma

Veja o arquivo `JogoExemplo.naja` para um exemplo completo de um jogo de plataforma 2D que implementa:

- Personagem controlado pelo jogador
- Plataformas para pular
- Colecionáveis (moedas)
- Inimigos móveis
- Sistema de pontuação
- Tela de game over

### Animações

Exemplo simples de animação de sprite:

```naja
dict sprite = criarSprite("personagem.png", 64, 64);
sprite.total_frames = 4;  # Sprite sheet com 4 frames

# Na função de atualização
fun atualizarAnimacao(dict objeto, float delta) {
    objeto.sprite.frame_atual = (objeto.sprite.frame_atual + 1) % objeto.sprite.total_frames;
}
```

## API Completa

### Núcleo do Jogo

```naja
dict initGame(int largura, int altura, string titulo)
void startGame(dict game)
void stopGame(dict game)
void loopPrincipal(dict game)
```

### Gerenciamento de Cenas

```naja
dict criarCena(string nome, fun atualizar, fun renderizar)
void adicionarCena(dict game, dict cena)
void trocarCena(dict game, string nome_cena)
```

### Sprites e Objetos

```naja
dict criarSprite(string caminho, int largura, int altura)
void carregarSprite(dict game, string nome, dict sprite)
dict criarObjeto(string nome, int x, int y, dict sprite)
void adicionarObjetoACena(dict cena, dict objeto)
void renderizarObjeto(dict game, dict objeto)
void atualizarObjeto(dict objeto, float delta_tempo)
```

### Sistema de Colisões

```naja
bool verificarColisao(dict objeto1, dict objeto2)
list verificarTodasColisoes(dict cena, dict objeto)
```

### Input

```naja
bool teclaEstaPressionada(dict game, string tecla)
dict obterPosicaoMouse(dict game)
bool mouseEstaSendoClicado(dict game)
```

### Áudio

```naja
void tocarSom(string caminho_som)
void tocarMusicaFundo(string caminho_musica, bool repetir)
```

## Aproveite os Recursos Especiais do NajaScript

A biblioteca NajaGame2D está otimizada para aproveitar os recursos especiais do NajaScript:

### Reatividade com Flux

Use variáveis flux para criar elementos de UI reativos:

```naja
int pontos = 0;
flux texto_pontuacao = "Pontos: " + pontos;

# Quando os pontos mudarem, o texto atualiza automaticamente
pontos = pontos + 10;
```

### Sistema de Eventos

Use o sistema onChange para reagir a mudanças:

```naja
# Monitore a pontuação para conquistas
onChange("pontos", verificarConquistas);

fun verificarConquistas(string nome_var, any valor_antigo, any valor_novo) {
    if (valor_novo >= 100 && valor_antigo < 100) {
        println("Conquista desbloqueada: 100 pontos!");
    }
}
```

## Dicas de Desempenho

1. **Minimize a criação de objetos** dentro do loop principal
2. **Use verificação de visibilidade** para renderizar apenas objetos visíveis
3. **Implemente particionamento espacial** para grandes quantidades de objetos
4. **Recicle objetos** em vez de criar/destruir frequentemente

---

Desenvolvido para NajaScript - Uma linguagem de programação reativa e tipada 
