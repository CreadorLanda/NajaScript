# NajaGame - Documentação

NajaGame é uma biblioteca de jogos para a linguagem NajaScript, permitindo criar jogos 2D de forma simples e intuitiva.

## Instalação

Para usar o NajaGame, você precisa ter o NajaScript instalado e a biblioteca pygame. O NajaGame já vem incluído no pacote padrão do NajaScript.

## Sintaxe Básica

### Inicialização do Jogo

```naja
import "NajaGame";

// Inicializa o jogo com dimensões e título
initGame(800, 600, "My Game");
```

### Cores

As cores podem ser definidas de duas formas:

1. Usando valores RGB individuais:
```naja
// Define cores usando valores RGB
greenColor = [0, 128, 0];
blueColor = [0, 0, 255];
blackColor = [0, 0, 0];
whiteColor = [255, 255, 255];
```

2. Usando listas de cores:
```naja
// Define cores usando listas
greenColor = [0, 128, 0];
blueColor = [0, 0, 255];
blackColor = [0, 0, 0];
whiteColor = [255, 255, 255];
```

### Carregando Recursos

```naja
// Carrega uma imagem
image = loadImage("path/to/image.png");

// Define a imagem como ícone da janela
setIcon(image);
```

### Funções de Desenho

#### Retângulos
```naja
// Desenha um retângulo preenchido
drawRect(x, y, width, height, color);

// Desenha um retângulo vazio
drawRectEmpty(x, y, width, height, color);
```

#### Círculos
```naja
// Desenha um círculo preenchido
drawCircle(x, y, radius, color);

// Desenha um círculo vazio
drawCircleEmpty(x, y, radius, color);
```

#### Linhas
```naja
// Desenha uma linha
drawLine(x1, y1, x2, y2, color);
```

#### Texto
```naja
// Desenha texto
drawText(text, x, y, color);
```

### Controle de Tela

```naja
// Limpa a tela com uma cor
clearScreen(color);

// Atualiza a tela
updateScreen();
```

### Entrada do Usuário

```naja
// Verifica se uma tecla está pressionada
isKeyPressed(key);

// Teclas disponíveis:
// "ESCAPE" - Tecla ESC
// "SPACE" - Barra de espaço
// "UP" - Seta para cima
// "DOWN" - Seta para baixo
// "LEFT" - Seta para esquerda
// "RIGHT" - Seta para direita
```

### Loop Principal do Jogo

```naja
while (true) {
    // Limpa a tela
    clearScreen(blueColor);
    
    // Verifica entrada do usuário
    if (isKeyPressed("ESCAPE")) {
        exit();
    }
    
    // Desenha elementos do jogo
    drawRect(100, 100, 50, 50, greenColor);
    
    // Atualiza a tela
    updateScreen();
}
```

## Versão em Português (NajaPt)

Para usar NajaGame com sintaxe em português, é necessário importar a biblioteca "NajaPt":

```naja
importar "NajaPt";
importar "NajaGame";

// Agora você pode usar os comandos em português
iniciarJogo(800, 600, "Meu Jogo");
```

Com o NajaPt, todas as funções e palavras-chave podem ser escritas em português:

```naja
enquanto (verdadeiro) {
    limparTela(corAzul);
    
    se (teclaPressionada("ESCAPE")) {
        sair();
    }
    
    desenharRetangulo(100, 100, 50, 50, corVerde);
    
    atualizarTela();
}
```

## Exemplos

### Exemplo Simples - Quadrado Móvel

```naja
import "NajaGame";

// Inicializa o jogo
initGame(800, 600, "Moving Square");

// Define cores
blueColor = [135, 206, 235];
greenColor = [0, 128, 0];

// Posição inicial do quadrado
x = 100;
y = 100;

// Loop principal
while (true) {
    // Limpa a tela
    clearScreen(blueColor);
    
    // Verifica entrada do usuário
    if (isKeyPressed("ESCAPE")) {
        exit();
    }
    
    // Move o quadrado com as setas
    if (isKeyPressed("UP")) {
        y = y - 5;
    }
    if (isKeyPressed("DOWN")) {
        y = y + 5;
    }
    if (isKeyPressed("LEFT")) {
        x = x - 5;
    }
    if (isKeyPressed("RIGHT")) {
        x = x + 5;
    }
    
    // Desenha o quadrado
    drawRect(x, y, 50, 50, greenColor);
    
    // Atualiza a tela
    updateScreen();
}
```

### Exemplo - Flappy Bird Simplificado

```naja
import "NajaGame";

// Inicializa o jogo
initGame(800, 600, "Flappy Bird");

// Define cores
blueColor = [135, 206, 235];
greenColor = [0, 128, 0];
blackColor = [0, 0, 0];
whiteColor = [255, 255, 255];

// Carrega imagem do pássaro
bird = loadImage("Flappy_Bird_assets/images/bird.png");
setIcon(bird);

// Configurações do pássaro
birdX = 150;
birdY = 300;
gravity = 0.5;
jumpForce = -10;
velocityY = 0;

// Configurações dos canos
pipeWidth = 70;
pipeHeight = 400;
pipeX = 800;
pipeY = 200;
gap = 150;

// Loop principal
while (true) {
    // Limpa a tela
    clearScreen(blueColor);
    
    // Verifica entrada do usuário
    if (isKeyPressed("ESCAPE")) {
        exit();
    }
    
    // Pulo do pássaro
    if (isKeyPressed("SPACE") || isKeyPressed("UP")) {
        velocityY = jumpForce;
    }
    
    // Atualiza posição do pássaro
    velocityY = velocityY + gravity;
    birdY = birdY + velocityY;
    
    // Move os canos
    pipeX = pipeX - 2;
    if (pipeX < -pipeWidth) {
        pipeX = 800;
        pipeY = 200 + (random() * 200);
    }
    
    // Desenha os canos
    drawRect(pipeX, 0, pipeWidth, pipeY, greenColor);
    drawRect(pipeX, pipeY + gap, pipeWidth, 600, greenColor);
    
    // Desenha o pássaro
    drawImage(bird, birdX, birdY, 50, 35);
    
    // Atualiza a tela
    updateScreen();
}
```

## Dicas e Boas Práticas

1. **Organização do Código**
   - Mantenha as configurações iniciais no início do arquivo
   - Agrupe variáveis relacionadas
   - Use comentários para documentar partes importantes do código

2. **Performance**
   - Evite criar objetos dentro do loop principal
   - Reutilize objetos e variáveis quando possível
   - Limpe a tela apenas uma vez por frame

3. **Controles**
   - Use constantes para valores que não mudam
   - Implemente controles suaves para melhor experiência do usuário
   - Adicione feedback visual para ações do usuário

4. **Colisões**
   - Implemente detecção de colisão simples usando retângulos
   - Use variáveis booleanas para controlar estados do jogo
   - Adicione efeitos visuais para colisões

## Limitações Conhecidas

1. O NajaGame é uma biblioteca 2D simples e não suporta:
   - Sprites animados
   - Efeitos de partículas
   - Física complexa
   - Som

2. A performance pode ser afetada por:
   - Muitos objetos na tela
   - Operações complexas no loop principal
   - Uso excessivo de funções de desenho

## Suporte

Para mais informações e exemplos, consulte a documentação oficial do NajaScript ou entre em contato com a comunidade de desenvolvedores. 