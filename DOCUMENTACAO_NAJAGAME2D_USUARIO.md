# NajaGame2D - Motor de Jogos 2D para NajaScript

O NajaGame2D é um motor de jogos 2D simples e poderoso para criar jogos diretamente em NajaScript. Inspirado pelos princípios de simplicidade de motores como Godot, ele permite que você desenvolva jogos com poucos comandos e conceitos intuitivos.

## Instalação

Para usar o NajaGame2D, basta importar a biblioteca em seu projeto:

```naja
import "NajaGame2D";
```

## Conceitos Básicos

### Nós e Cenas

Assim como em motores modernos, no NajaGame2D tudo é um objeto de jogo (ou "nó"), que podem ser organizados em cenas:

- **Objetos de Jogo**: Elementos que aparecem no jogo, como personagens, plataformas, inimigos, etc.
- **Cenas**: Conjuntos de objetos que formam um nível, menu ou qualquer outra tela do jogo.

### Ciclo de Vida de um Jogo

1. **Inicialização**: Configure a janela e carregue recursos
2. **Loop Principal**: Atualize e renderize o jogo continuamente
3. **Finalização**: Limpe recursos quando o jogo terminar

## Primeiros Passos

### Criando um Jogo

```naja
# Inicializa o jogo com largura, altura e título
dict jogo = initGame(800, 600, "Meu Primeiro Jogo");

# Cria uma cena principal
dict cena_principal = criarCena("principal", atualizarJogo, renderizarJogo);
adicionarCena(jogo, cena_principal);

# Inicia o loop do jogo
startGame(jogo);

# Função de atualização - chamada a cada quadro
fun atualizarJogo(dict jogo, float delta_tempo) {
    # Lógica do jogo aqui
}

# Função de renderização - chamada após a atualização
fun renderizarJogo(dict jogo) {
    # Renderização aqui
}
```

### Sprites e Objetos

```naja
# Carrega e cria um sprite
dict sprite_jogador = criarSprite("imagens/jogador.png", 64, 64);

# Cria um objeto de jogo com esse sprite
dict jogador = criarObjeto("jogador", 100, 100, sprite_jogador);

# Adiciona o objeto à cena
adicionarObjetoACena(cena_principal, jogador);
```

### Animações

```naja
# Configura uma sprite sheet para animação (6 frames, 3 por linha)
configurarSpriteSheet(sprite_jogador, 6, 3, 0.1);
```

## Principais Recursos

### Entrada de Usuário

```naja
# Verifica se uma tecla está pressionada
if (teclaEstaPressionada(jogo, "direita")) {
    jogador.velocidade_x = 200;
} else if (teclaEstaPressionada(jogo, "esquerda")) {
    jogador.velocidade_x = -200;
} else {
    jogador.velocidade_x = 0;
}

# Obtém posição do mouse
dict posicao_mouse = obterPosicaoMouse(jogo);
```

### Física e Movimento

```naja
# Atualiza a posição do objeto com base em sua velocidade
atualizarObjeto(jogador, delta_tempo);

# Aplica gravidade
aplicarGravidade(jogador, 980, delta_tempo);  # 980 pixels/s²
```

### Colisões

```naja
# Verifica colisão entre dois objetos
if (verificarColisao(jogador, inimigo)) {
    # Código para lidar com a colisão
}

# Verifica colisões com todos os objetos da cena
list colisoes = verificarTodasColisoes(cena_atual, jogador);
```

### Áudio

```naja
# Toca um efeito sonoro
tocarSom("sons/pulo.wav");

# Toca música de fundo (em loop)
tocarMusicaFundo("musicas/tema.mp3", true);
```

### Efeitos Visuais

```naja
# Cria um sistema de partículas (posição x, y, cor RGB, quantidade, vida máxima)
dict particulas = criarSistemaParticulas(jogador.x, jogador.y, "255,255,0", 20, 1.5);

# Atualiza e renderiza as partículas
atualizarParticulas(particulas, delta_tempo);
renderizarParticulas(particulas);
```

## Exemplo Completo: Jogo de Plataforma

```naja
# Variáveis globais
dict jogador;
dict plataformas = list();
float gravidade = 980;
float forca_pulo = -400;

# Função de inicialização
fun iniciarJogo() {
    # Inicializa o jogo
    dict jogo = initGame(800, 600, "Jogo de Plataforma");
    
    # Carrega sprites
    dict sprite_jogador = criarSprite("imagens/jogador.png", 64, 64);
    dict sprite_plataforma = criarSprite("imagens/plataforma.png", 128, 32);
    
    # Configura animação do jogador
    configurarSpriteSheet(sprite_jogador, 6, 3, 0.1);
    
    # Cria o jogador
    jogador = criarObjeto("jogador", 100, 100, sprite_jogador);
    jogador.no_chao = false;
    
    # Cria plataformas
    criarPlataformas(sprite_plataforma);
    
    # Cria e configura a cena
    dict cena_principal = criarCena("principal", atualizarJogo, renderizarJogo);
    
    # Adiciona objetos à cena
    adicionarObjetoACena(cena_principal, jogador);
    forin (plataforma in plataformas) {
        adicionarObjetoACena(cena_principal, plataforma);
    }
    
    # Adiciona cena ao jogo
    adicionarCena(jogo, cena_principal);
    
    # Inicia o jogo
    startGame(jogo);
    
    return jogo;
}

# Cria plataformas
fun criarPlataformas(dict sprite) {
    # Plataforma base
    dict plataforma1 = criarObjeto("plataforma1", 100, 500, sprite);
    plataformas.add(plataforma1);
    
    dict plataforma2 = criarObjeto("plataforma2", 300, 450, sprite);
    plataformas.add(plataforma2);
    
    dict plataforma3 = criarObjeto("plataforma3", 500, 400, sprite);
    plataformas.add(plataforma3);
}

# Função de atualização
fun atualizarJogo(dict jogo, float delta_tempo) {
    # Processa entrada
    processarEntrada(jogo);
    
    # Aplica física
    aplicarGravidade(jogador, gravidade, delta_tempo);
    atualizarObjeto(jogador, delta_tempo);
    
    # Verifica colisões com plataformas
    jogador.no_chao = false;
    forin (plataforma in plataformas) {
        if (verificarColisao(jogador, plataforma)) {
            if (jogador.velocidade_y > 0 && jogador.y + jogador.altura < plataforma.y + 20) {
                jogador.y = plataforma.y - jogador.altura;
                jogador.velocidade_y = 0;
                jogador.no_chao = true;
            }
        }
    }
}

# Processa entrada do usuário
fun processarEntrada(dict jogo) {
    # Movimento horizontal
    if (teclaEstaPressionada(jogo, "direita")) {
        jogador.velocidade_x = 200;
        jogador.escala_x = 1;  # Não inverte o sprite
    } else if (teclaEstaPressionada(jogo, "esquerda")) {
        jogador.velocidade_x = -200;
        jogador.escala_x = -1;  # Inverte o sprite horizontalmente
    } else {
        jogador.velocidade_x = 0;
    }
    
    # Pulo
    if (teclaEstaPressionada(jogo, "espaco") && jogador.no_chao) {
        jogador.velocidade_y = forca_pulo;
        tocarSom("sons/pulo.wav");
    }
}

# Função de renderização
fun renderizarJogo(dict jogo) {
    # Renderiza todos os objetos da cena atual
    dict cena = jogo.cenas.get(jogo.cena_atual);
    forin (objeto in cena.objetos) {
        renderizarObjeto(jogo, objeto);
    }
}

# Inicia o jogo
dict jogo = iniciarJogo();
```

## Componentes e Comportamentos

Para criar comportamentos reutilizáveis, você pode organizar seu código em componentes:

```naja
# Componente de movimento
fun componenteMovimento(dict objeto, dict jogo, float delta_tempo, float velocidade) {
    if (teclaEstaPressionada(jogo, "direita")) {
        objeto.velocidade_x = velocidade;
    } else if (teclaEstaPressionada(jogo, "esquerda")) {
        objeto.velocidade_x = -velocidade;
    } else {
        objeto.velocidade_x = 0;
    }
    
    atualizarObjeto(objeto, delta_tempo);
}
```

## Dicas Avançadas

### Gerenciamento de Estados

```naja
# Máquina de estados simples
dict estados = {
    PARADO: 0,
    CORRENDO: 1,
    PULANDO: 2,
    CAINDO: 3
};

dict jogador = {
    estado_atual: estados.PARADO,
    # Outras propriedades...
};

fun atualizarEstadoJogador(dict jogador) {
    if (jogador.velocidade_y < 0) {
        jogador.estado_atual = estados.PULANDO;
    } else if (jogador.velocidade_y > 0) {
        jogador.estado_atual = estados.CAINDO;
    } else if (jogador.velocidade_x != 0) {
        jogador.estado_atual = estados.CORRENDO;
    } else {
        jogador.estado_atual = estados.PARADO;
    }
}
```

### Paralaxe e Efeitos de Câmera

```naja
fun aplicarEfeitoParalaxe(dict camada, float fator) {
    camada.x = -(jogador.x * fator);
}
```

## Conclusão

O NajaGame2D foi projetado para ser intuitivo e fácil de usar, permitindo que você crie jogos rapidamente sem precisar se preocupar com detalhes de implementação complexos. Esta documentação cobre os conceitos básicos, mas há muito mais que você pode fazer!

Para mais exemplos, consulte os jogos de exemplo incluídos com a biblioteca.

Bom desenvolvimento de jogos! 