# Funcionamento do NajaGame2D: Do Início ao Fim

## 1. Visão Geral da Arquitetura

O NajaGame2D é uma biblioteca de desenvolvimento de jogos 2D para NajaScript que utiliza o Pygame como motor de renderização. A biblioteca atua como uma camada intermediária que traduz comandos de alto nível em NajaScript para operações de mais baixo nível no Pygame, permitindo aos desenvolvedores criar jogos sem precisar lidar diretamente com as complexidades do Pygame.

## 2. Inicialização do Motor

### Carregamento da Biblioteca
```naja
import "NajaGame2D_Pygame.naja";
```

O processo começa importando a biblioteca NajaGame2D, que configura o ambiente básico e define todas as funções necessárias para desenvolvimento de jogos.

### Inicialização do Pygame
Durante a importação, o código Python embutido é executado para inicializar o Pygame:

```python
pygame.init()
pygame.mixer.init()
```

Isso prepara os subsistemas do Pygame, incluindo renderização, áudio e entrada.

### Criação do Jogo
```naja
dict jogo = initGame(800, 600, "Meu Jogo NajaScript");
```

A função `initGame()` realiza várias tarefas cruciais:
- Cria uma janela do Pygame com as dimensões especificadas
- Define o título da janela
- Inicializa estruturas de dados para gerenciar cenas, sprites e eventos
- Retorna um dicionário que contém o estado do jogo

## 3. Carregamento de Recursos

### Imagens e Sprites
```naja
dict spriteJogador = criarSprite("assets/jogador.png", 64, 64);
```

O carregamento de imagens ocorre através da função `criarSprite()`, que:
- Carrega a imagem do arquivo usando `pygame.image.load()`
- Redimensiona a imagem conforme necessário com `pygame.transform.scale()`
- Configura propriedades como dimensões e estado de animação
- Armazena a imagem em um dicionário para uso posterior

### Configuração de Sprite Sheets
```naja
configurarSpriteSheet(spriteJogador, 8, 4, 0.1);
```

Para animações, a função `configurarSpriteSheet()`:
- Divide a imagem em quadros individuais com base nos parâmetros fornecidos
- Cria superfícies separadas para cada quadro
- Configura propriedades como tempo entre quadros e número total de quadros

### Áudio
```naja
tocarSom("assets/som_pulo.wav");
tocarMusicaFundo("assets/musica_jogo.mp3", true);
```

O carregamento e reprodução de áudio são gerenciados através de:
- `pygame.mixer.Sound()` para efeitos sonoros curtos
- `pygame.mixer.music` para música de fundo mais longa

## 4. Estrutura do Jogo

### Criação de Cenas
```naja
dict cenaPrincipal = criarCena("principal", atualizarJogo, renderizarJogo);
```

As cenas são unidades organizacionais que contêm:
- Uma função de atualização que executa a lógica do jogo
- Uma função de renderização que desenha os elementos visuais
- Uma lista de objetos pertencentes à cena

### Objetos de Jogo
```naja
dict jogador = criarObjeto("jogador", 100, 100, spriteJogador);
adicionarObjetoACena(cenaPrincipal, jogador);
```

Os objetos do jogo são criados com:
- Um nome para identificação
- Posição inicial (coordenadas x, y)
- Um sprite associado
- Propriedades como velocidade, colisor, etc.

### Adição de Cenas ao Jogo
```naja
adicionarCena(jogo, cenaPrincipal);
trocarCena(jogo, "principal");
```

Múltiplas cenas podem ser adicionadas ao jogo (menu principal, níveis, game over, etc.) e a troca entre elas é gerenciada pelo sistema.

## 5. Loop Principal do Jogo

### Iniciando o Loop
```naja
startGame(jogo);
```

A função `startGame()` inicializa o loop principal em uma thread separada:

```python
def main_loop():
    while _najagame_data['rodando']:
        # Processamento de eventos
        # Atualização da lógica
        # Renderização
        # Controle de taxa de quadros
```

O loop é executado em uma thread separada para que o código NajaScript possa continuar executando outras operações enquanto o jogo está rodando.

### Processamento de Eventos
Durante cada quadro, o sistema:
- Coleta todos os eventos do Pygame com `pygame.event.get()`
- Processa eventos de teclado, mouse e da janela
- Atualiza estruturas de dados internas para refletir o estado atual dos inputs

### Cálculo do Delta Tempo
```python
agora = time()
delta_tempo = agora - ultima_atualizacao
ultima_atualizacao = agora
```

O delta tempo (tempo entre quadros) é calculado para garantir que o jogo funcione na mesma velocidade independentemente da taxa de quadros.

## 6. Ciclo de Atualização e Renderização

### Atualização da Lógica
```naja
fun atualizarJogo(dict game, float delta) {
    # Atualização de objetos
    forin (objeto in game.cenas.get(game.cena_atual).objetos) {
        atualizarObjeto(objeto, delta);
        # Lógica específica do jogo
    }
}
```

A lógica do jogo é executada na função de atualização da cena atual:
- Movimentação de objetos
- Verificação de colisões
- Resposta a entradas do usuário
- Aplicação de física (gravidade, etc.)

### Detecção de Colisões
```naja
if (verificarColisao(jogador, inimigo)) {
    # Resposta à colisão
}
```

O sistema oferece múltiplos métodos de detecção de colisão:
- `verificarColisao()` para colisões baseadas em retângulos (AABB)
- `verificarColisaoCircular()` para colisões mais precisas baseadas em círculos

### Renderização
```naja
fun renderizarJogo(dict game) {
    # Desenha o fundo
    # Renderiza objetos
    forin (objeto in game.cenas.get(game.cena_atual).objetos) {
        renderizarObjeto(game, objeto);
    }
    # Desenha interface
}
```

A renderização ocorre após a atualização lógica e inclui:
- Limpeza da tela com `screen.fill((0,0,0))`
- Renderização de sprites de cada objeto
- Desenho de texto e formas geométricas
- Aplicação de transformações (rotação, escala, etc.)
- Atualização da tela com `pygame.display.flip()`

## 7. Sistemas Especiais

### Sistema de Partículas
```naja
dict particulas = criarSistemaParticulas(x, y, "255, 215, 0", 15, 0.8);
adicionarObjetoACena(cena, particulas);
```

O sistema de partículas:
- Cria múltiplas partículas com propriedades aleatórias
- Atualiza posição e vida de cada partícula
- Remove partículas quando sua vida chega a zero
- Renderiza partículas com opacidade baseada em sua vida restante

### Sistema de Áudio
O áudio é gerenciado através de duas principais funções:
- `tocarSom()` para efeitos sonoros curtos
- `tocarMusicaFundo()` para música contínua de fundo

Funções adicionais permitem:
- Ajustar volume
- Pausar/retomar música
- Verificar se um som está tocando

## 8. Finalização do Jogo

### Parada Manual
```naja
stopGame(jogo);
```

O jogo pode ser parado manualmente com a função `stopGame()`, que:
- Define a flag de execução como falsa
- Finaliza o loop principal
- Encerra o Pygame com `pygame.quit()`

### Fechamento da Janela
Se o usuário fechar a janela do jogo, um evento `pygame.QUIT` é gerado e capturado pelo loop principal, levando ao mesmo processo de finalização.

## 9. Ponte entre NajaScript e Pygame

A comunicação entre NajaScript e Pygame é mediada pela função `__python()`:

```naja
__python("
    # Código Python que acessa diretamente o Pygame
");
```

Esta função precisa ser implementada no interpretador NajaScript para:
- Executar código Python embutido em strings
- Permitir que dados sejam passados entre os dois ambientes
- Capturar e relatar erros adequadamente

## 10. Considerações de Desempenho

Para manter um bom desempenho, o sistema:
- Limita a taxa de quadros com `clock.tick(60)`
- Usa caching de recursos para evitar recarregamento
- Implementa verificações de visibilidade para evitar renderizar objetos fora da tela
- Otimiza a detecção de colisão conforme necessário

Este framework proporciona uma base robusta para desenvolvimento de jogos 2D em NajaScript, abstraindo as complexidades do Pygame enquanto mantém todo o seu poder e flexibilidade.

## 11. Guia de Uso Rápido

### Inicialização Básica
```naja
import "NajaGame2D_Pygame.naja";

# Inicializa o jogo
dict jogo = initGame(800, 600, "Meu Primeiro Jogo");

# Carrega recursos
dict spriteJogador = criarSprite("assets/jogador.png", 64, 64);
dict spritePlataforma = criarSprite("assets/plataforma.png", 128, 32);

# Cria objetos
dict jogador = criarObjeto("jogador", 100, 100, spriteJogador);
dict plataforma = criarObjeto("plataforma", 300, 400, spritePlataforma);

# Define a função de atualização
fun atualizarJogo(dict game, float delta) {
    # Lógica de movimento, colisão, etc.
    forin (objeto in game.cenas.get(game.cena_atual).objetos) {
        atualizarObjeto(objeto, delta);
        
        if (objeto.nome == "jogador") {
            # Controles do jogador
            if (teclaEstaPressionada(game, "ArrowRight")) {
                objeto.velocidade_x = 200;
            } elif (teclaEstaPressionada(game, "ArrowLeft")) {
                objeto.velocidade_x = -200;
            } else {
                objeto.velocidade_x = 0;
            }
            
            # Aplicar gravidade
            aplicarGravidade(objeto, 980, delta);
            
            # Verificar colisões
            forin (outro in game.cenas.get(game.cena_atual).objetos) {
                if (outro.nome == "plataforma" && verificarColisao(objeto, outro)) {
                    if (objeto.velocidade_y > 0) {
                        objeto.y = outro.y - objeto.altura;
                        objeto.velocidade_y = 0;
                    }
                }
            }
        }
    }
}

# Define a função de renderização
fun renderizarJogo(dict game) {
    # Renderiza todos os objetos
    forin (objeto in game.cenas.get(game.cena_atual).objetos) {
        renderizarObjeto(game, objeto);
    }
}

# Cria e configura a cena
dict cena = criarCena("principal", atualizarJogo, renderizarJogo);
adicionarObjetoACena(cena, jogador);
adicionarObjetoACena(cena, plataforma);
adicionarCena(jogo, cena);

# Inicia o jogo
trocarCena(jogo, "principal");
startGame(jogo);
```

### Requisitos para Execução

Para executar jogos desenvolvidos com o NajaGame2D, você precisará:

1. Um interpretador NajaScript com suporte à função `__python()`
2. Python 3.6+ instalado com as seguintes bibliotecas:
   - Pygame (versão 2.0.0+)
   - Numpy (opcional, para operações matemáticas avançadas)

## 12. API Completa

Consulte a documentação completa da API para detalhes sobre todas as funções disponíveis no NajaGame2D. Algumas das funções principais incluem:

### Inicialização
- `initGame(largura, altura, titulo)` - Inicializa o jogo
- `startGame(jogo)` - Inicia o loop principal
- `stopGame(jogo)` - Para o jogo

### Gerenciamento de Cenas
- `criarCena(nome, atualizar, renderizar)` - Cria uma nova cena
- `adicionarCena(jogo, cena)` - Adiciona uma cena ao jogo
- `trocarCena(jogo, nome)` - Troca para uma cena específica

### Recursos e Objetos
- `criarSprite(caminho, largura, altura)` - Cria um sprite
- `configurarSpriteSheet(sprite, total_frames, frames_por_linha, intervalo_frame)` - Configura uma sprite sheet
- `criarObjeto(nome, x, y, sprite)` - Cria um objeto de jogo
- `adicionarObjetoACena(cena, objeto)` - Adiciona um objeto a uma cena

### Renderização
- `renderizarObjeto(game, objeto)` - Renderiza um objeto
- `desenharTexto(texto, x, y, cor, fonte)` - Desenha texto na tela
- `desenharRetangulo(x, y, largura, altura, cor, preenchido)` - Desenha um retângulo
- `desenharCirculo(x, y, raio, cor, preenchido)` - Desenha um círculo

### Física e Colisões
- `atualizarObjeto(objeto, delta_tempo)` - Atualiza a física de um objeto
- `verificarColisao(objeto1, objeto2)` - Verifica colisão entre dois objetos
- `verificarColisaoCircular(objeto1, objeto2)` - Verifica colisão circular
- `aplicarGravidade(objeto, gravidade, delta_tempo)` - Aplica gravidade a um objeto

### Entrada do Usuário
- `teclaEstaPressionada(game, tecla)` - Verifica se uma tecla está pressionada
- `obterPosicaoMouse(game)` - Obtém a posição do mouse
- `mouseEstaSendoClicado(game)` - Verifica se o mouse está sendo clicado

### Áudio
- `tocarSom(caminho_som)` - Toca um som
- `tocarMusicaFundo(caminho_musica, repetir)` - Toca uma música de fundo
- `pausarMusicaFundo()` - Pausa a música de fundo
- `ajustarVolumeMusicaFundo(volume)` - Ajusta o volume da música de fundo

### Efeitos Especiais
- `criarSistemaParticulas(x, y, cor, quantidade, vida_max)` - Cria um sistema de partículas
- `atualizarParticulas(sistema, delta_tempo)` - Atualiza um sistema de partículas
- `renderizarParticulas(sistema)` - Renderiza um sistema de partículas 