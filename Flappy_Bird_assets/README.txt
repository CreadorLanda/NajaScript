Assets do Flappy Bird para NajaScript
===================================

Esta pasta contém os recursos (assets) necessários para criar uma versão do jogo Flappy Bird usando NajaScript.

Estrutura de diretórios:
------------------------

- /images/ - Contém as imagens do jogo (pássaro, canos, fundo, etc.)
- /sounds/ - Contém os efeitos sonoros do jogo
- /UI/ - Contém elementos da interface do usuário (números, tela de game over, etc.)

Sobre os arquivos:
-----------------

IMAGENS:
- bird.png - O pássaro protagonista do jogo
- background.png - Imagem de fundo do céu
- pipe-green.png - Cano verde (obstáculo)
- base.png - Chão do jogo

SONS:
- wing.wav - Som de bater asas (quando o jogador pula)
- point.wav - Som de marcar ponto (quando passa por um cano)
- hit.wav - Som de colisão (quando bate em um obstáculo)
- die.wav - Som de fim de jogo

UI:
- message.png - Tela inicial do jogo
- gameover.png - Mensagem de fim de jogo
- 0.png até 9.png - Números para mostrar a pontuação

Como usar:
---------

Para carregar uma imagem no seu jogo NajaScript:

```
int imagemPassaro = loadImage("Flappy_Bird_assets/images/bird.png");
```

Para desenhar a imagem:

```
drawImage(imagemPassaro, posX, posY, largura, altura);
```

Você pode ver um exemplo completo no arquivo exemplos/flappy_assets_teste.naja.

Créditos:
--------
Estes assets são baseados nos recursos originais do Flappy Bird, disponibilizados para uso educacional.

Fonte: https://github.com/samuelcust/flappy-bird-assets 