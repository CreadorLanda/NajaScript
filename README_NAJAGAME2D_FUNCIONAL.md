# NajaGame2D - Guia de Implementação Funcional

Este guia explica como usar a biblioteca NajaGame2D para criar jogos 2D funcionais em NajaScript que podem ser executados em navegadores web.

## Índice

1. [Visão Geral](#visão-geral)
2. [Requisitos](#requisitos)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Integração com HTML5](#integração-com-html5)
5. [Recursos Principais](#recursos-principais)
6. [Guia de Início Rápido](#guia-de-início-rápido)
7. [Exemplos Avançados](#exemplos-avançados)
8. [Solução de Problemas](#solução-de-problemas)

## Visão Geral

O NajaGame2D é uma biblioteca para desenvolvimento de jogos 2D utilizando NajaScript e o Canvas HTML5. A biblioteca permite:

- Renderização de sprites e animações
- Sistema de física básica com colisões
- Gerenciamento de entrada (teclado e mouse)
- Sistema de áudio para efeitos sonoros e música
- Efeitos de partículas
- Sistema de cenas para organizar seu jogo

## Requisitos

Para implementar um jogo com NajaGame2D, você precisará:

1. **Servidor web** - para servir os arquivos do jogo
2. **Navegador moderno** - com suporte a Canvas HTML5 e ES6
3. **Compilador/interpretador NajaScript** - para executar códigos NajaScript no navegador
4. **Arquivos de recursos** - sprites, sons, etc.

## Estrutura do Projeto

Um projeto típico de NajaGame2D deve ter a seguinte estrutura:

```
seu-projeto/
├── index.html              # Página HTML principal
├── NajaGame2D.naja         # Biblioteca do motor de jogos
├── MeuJogo.naja            # Seu código de jogo
├── assets/                 # Pasta de recursos
│   ├── sprites/            # Imagens do jogo
│   ├── audio/              # Sons e músicas
│   └── fonts/              # Fontes personalizadas (opcional)
└── README.md               # Documentação do seu jogo
```

## Integração com HTML5

Para executar o jogo no navegador, você precisa de um arquivo HTML que carregue o NajaScript e seus arquivos:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meu Jogo NajaScript</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #f0f0f0;
        }
    </style>
</head>
<body>
    <!-- O canvas será criado pelo NajaGame2D -->
    
    <!-- Carregamento do interpretador NajaScript -->
    <script src="najascript-interpreter.js"></script>
    
    <!-- Carregamento dos scripts do jogo -->
    <script>
        NajaScript.loadAndRun([
            "NajaGame2D.naja",
            "MeuJogo.naja"
        ]);
    </script>
</body>
</html>
```

## Recursos Principais

### Sistema de Renderização

O NajaGame2D utiliza o Canvas HTML5 para renderizar gráficos 2D, oferecendo:

- Renderização de sprites simples
- Suporte a sprite sheets para animações
- Transformações (rotação, escala)
- Efeitos de partículas
- Desenho de texto e formas básicas

Exemplo de uso:

```naja
# Criando um sprite animado
dict spritePersonagem = criarSprite("assets/personagem.png", 192, 256);
configurarSpriteSheet(spritePersonagem, 8, 3, 0.1);  # 8 frames, 3 por linha, 100ms por frame

# Criando um objeto de jogo
dict jogador = criarObjeto("jogador", 100, 100, spritePersonagem);
```

### Sistema de Física

Implementa física básica para jogos de plataforma:

- Movimento baseado em velocidade
- Gravidade
- Detecção de colisão AABB (caixas delimitadoras alinhadas aos eixos)
- Detecção de colisão circular (mais precisa para objetos circulares)

Exemplo de aplicação de física:

```naja
# Aplicando gravidade
aplicarGravidade(objeto, GRAVIDADE, delta_tempo);

# Verificando colisão entre objetos
if (verificarColisao(objeto1, objeto2)) {
    # Resposta à colisão
}
```

### Sistema de Entrada

Captura eventos de teclado e mouse:

- Detecção de teclas pressionadas
- Posição e cliques do mouse

Exemplo de uso:

```naja
# Verificando teclas pressionadas
if (teclaEstaPressionada(game, "ArrowRight") || teclaEstaPressionada(game, "d")) {
    objeto.velocidade_x = VELOCIDADE_JOGADOR;
}

# Verificando cliques do mouse
if (mouseEstaSendoClicado(game)) {
    dict posicao = obterPosicaoMouse(game);
    # Usar posicao.x e posicao.y
}
```

### Sistema de Áudio

Gerencia a reprodução de efeitos sonoros e música:

- Reprodução de sons pontuais
- Música de fundo com controle de volume
- Loop automático de músicas

Exemplo de uso:

```naja
# Tocando um efeito sonoro
tocarSom("assets/som_pulo.wav");

# Tocando música de fundo em loop
tocarMusicaFundo("assets/musica_jogo.mp3", true);

# Ajustando volume
ajustarVolumeMusicaFundo(0.5);  # 50% do volume
```

### Sistema de Partículas

Cria efeitos visuais com partículas:

- Explosões
- Faíscas
- Poeira
- Outros efeitos de partículas

Exemplo de uso:

```naja
# Criando um sistema de partículas douradas (para coleta de moedas)
dict particulas = criarSistemaParticulas(x, y, "255, 215, 0", 15, 0.8);
adicionarObjetoACena(cena, particulas);
```

## Guia de Início Rápido

Siga estes passos para criar seu primeiro jogo:

1. **Configure seu projeto com a estrutura recomendada**

2. **Importe a biblioteca NajaGame2D:**
   ```naja
   import "NajaGame2D.naja";
   ```

3. **Inicialize o jogo:**
   ```naja
   # Inicializa a página HTML
   inicializarPagina();
   
   # Cria o objeto de jogo
   dict jogo = initGame(800, 600, "Meu Primeiro Jogo");
   ```

4. **Carregue recursos:**
   ```naja
   dict spritePersonagem = criarSprite("assets/personagem.png", 64, 64);
   dict spritePlataforma = criarSprite("assets/plataforma.png", 128, 32);
   ```

5. **Crie objetos do jogo:**
   ```naja
   dict jogador = criarObjeto("jogador", 100, 100, spritePersonagem);
   dict plataforma = criarObjeto("plataforma", 300, 400, spritePlataforma);
   ```

6. **Defina a lógica de atualização:**
   ```naja
   fun atualizarJogo(dict game, float delta) {
       # Lógica de movimento, colisão, etc.
   }
   ```

7. **Defina a renderização:**
   ```naja
   fun renderizarJogo(dict game) {
       # Renderização dos objetos
   }
   ```

8. **Crie e configure cenas:**
   ```naja
   dict cena = criarCena("principal", atualizarJogo, renderizarJogo);
   adicionarObjetoACena(cena, jogador);
   adicionarObjetoACena(cena, plataforma);
   adicionarCena(jogo, cena);
   ```

9. **Inicie o jogo:**
   ```naja
   trocarCena(jogo, "principal");
   startGame(jogo);
   ```

## Exemplos Avançados

### Sistema de Física Personalizado

```naja
# Implementando um sistema de física personalizado com resistência do ar
fun aplicarFisicaPersonalizada(dict objeto, float delta_tempo) {
    # Aplica gravidade
    objeto.velocidade_y = objeto.velocidade_y + (GRAVIDADE * delta_tempo);
    
    # Aplica resistência do ar
    float resistencia = 0.98;
    objeto.velocidade_x = objeto.velocidade_x * resistencia;
    
    # Atualiza posição
    objeto.x = objeto.x + (objeto.velocidade_x * delta_tempo);
    objeto.y = objeto.y + (objeto.velocidade_y * delta_tempo);
}
```

### Animações Condicionais

```naja
# Alterando animações com base no estado do jogador
fun atualizarAnimacaoJogador(dict jogador) {
    if (!jogador.no_chao) {
        # Animação de pulo
        jogador.sprite.frame_atual = 5;
        jogador.sprite.animacao_ativa = false;
    } else if (jogador.velocidade_x != 0) {
        # Animação de corrida
        jogador.sprite.animacao_ativa = true;
        jogador.sprite.total_frames = 4;
        jogador.sprite.intervalo_frame = 0.1;
    } else {
        # Animação parado
        jogador.sprite.animacao_ativa = true;
        jogador.sprite.total_frames = 2;
        jogador.sprite.intervalo_frame = 0.5;
    }
}
```

### Sistema de Parallax (Fundo com Múltiplas Camadas)

```naja
# Criando efeito de parallax com múltiplas camadas
fun renderizarFundoParallax(dict game, float delta) {
    # Camada mais distante (se move mais lentamente)
    dict camada1 = {
        sprite: game.sprites.get("fundo_ceu"),
        x: (game.camera_x * 0.1) % 800,
        y: 0,
        visivel: true,
        centro_x: 0,
        centro_y: 0,
        rotacao: 0,
        escala_x: 1,
        escala_y: 1,
        largura: 800,
        altura: 600
    };
    
    # Camada intermediária
    dict camada2 = {
        sprite: game.sprites.get("fundo_montanhas"),
        x: (game.camera_x * 0.3) % 800,
        y: 100,
        visivel: true,
        centro_x: 0,
        centro_y: 0,
        rotacao: 0,
        escala_x: 1,
        escala_y: 1,
        largura: 800,
        altura: 300
    };
    
    # Camada mais próxima (se move mais rapidamente)
    dict camada3 = {
        sprite: game.sprites.get("fundo_arvores"),
        x: (game.camera_x * 0.7) % 800,
        y: 300,
        visivel: true,
        centro_x: 0,
        centro_y: 0,
        rotacao: 0,
        escala_x: 1,
        escala_y: 1,
        largura: 800,
        altura: 200
    };
    
    # Renderiza as camadas
    renderizarObjeto(game, camada1);
    renderizarObjeto(game, camada2);
    renderizarObjeto(game, camada3);
}
```

## Solução de Problemas

### Arquivos não carregam

- Verifique se os caminhos para os arquivos estão corretos
- Use DevTools do navegador para verificar erros de rede
- Certifique-se de que está executando via servidor web (não abrindo o arquivo diretamente)

### Problemas de Performance

- Reduza o número de objetos sendo renderizados
- Use `objeto.visivel = false` para objetos fora da tela
- Otimize as funções de atualização e colisão
- Use sprite sheets menores ou comprimidas

### Problemas de Colisão

- Use o debug visual para ver as caixas de colisão
- Verifique se os tamanhos dos objetos estão corretos
- Para objetos circulares, use `verificarColisaoCircular` em vez de `verificarColisao`

### Código de debug visual

```naja
# Função para desenhar caixas de colisão (debug)
fun desenharColisores(dict game) {
    forin (objeto in game.cenas.get(game.cena_atual).objetos) {
        if (objeto.colisor) {
            desenharRetangulo(
                objeto.x, objeto.y,
                objeto.largura, objeto.altura,
                "rgba(255, 0, 0, 0.5)",
                false
            );
        }
    }
}
```

---

## Recursos Adicionais

- **Documentação Completa da API**: Consulte o arquivo `README_NAJAGAME2D.md`
- **Exemplo Completo**: Veja o arquivo `ExemploJogoReal.naja`
- **Fórum de Suporte**: [forum.najascript.org](https://forum.najascript.org)
- **Repositório de Exemplos**: [github.com/najascript/najagame2d-examples](https://github.com/najascript/najagame2d-examples)

---

Desenvolvido para NajaScript - Torne suas ideias de jogos realidade! 