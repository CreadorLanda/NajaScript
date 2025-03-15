# NajaGame2D: Documentação para Desenvolvedores

Este documento explica como a biblioteca NajaGame2D é implementada internamente utilizando Pygame. Esta informação é destinada apenas aos desenvolvedores da biblioteca, não aos usuários finais.

## Visão Geral

NajaGame2D é uma biblioteca que fornece uma API simples e intuitiva para desenvolvimento de jogos 2D em NajaScript, inspirada pela abordagem do Godot Engine. Internamente, utilizamos o Pygame como motor de renderização, mas isso é completamente transparente para o usuário final.

## Arquitetura

A arquitetura do NajaGame2D é composta por três camadas:

1. **API NajaScript**: Funções simples e intuitivas expostas ao usuário
2. **Camada de Tradução**: Converte chamadas de API em operações do Pygame
3. **Motor Pygame**: Executa as operações de baixo nível

```
+-------------------------+
|    Código do Usuário    |
+-------------------------+
           |
           | (chamadas de API)
           v
+-------------------------+
|    API do NajaGame2D    |
+-------------------------+
           |
           | (camada de tradução)
           v
+-------------------------+
|       Motor Pygame      |
+-------------------------+
           |
           | (SDL e OpenGL)
           v
+-------------------------+
|     Sistema Operac.     |
+-------------------------+
```

## Implementação

### 1. Funções Nativas do Interpretador

As funções com prefixo `__` (como `__criarJanela`, `__desenharImagem`, etc.) são implementadas nativamente no interpretador NajaScript e repassam as chamadas ao Pygame.

Exemplo de implementação de `__criarJanela`:

```python
def implement_criarJanela(args):
    """Implementação nativa de __criarJanela usando Pygame"""
    largura = args[0]
    altura = args[1]
    titulo = args[2]
    
    # Inicializa o Pygame se necessário
    if not pygame.get_init():
        pygame.init()
        pygame.mixer.init()
    
    # Cria a janela
    window = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption(titulo)
    
    # Armazena a referência da janela
    GAME_DATA["window"] = window
    
    # Retorna um objeto representando a janela
    return {"id": "window"}
```

### 2. Mapeamento de Recursos

Os recursos do jogo (imagens, sons, etc.) são mapeados entre o NajaScript e o Pygame:

| Recurso NajaScript | Recurso Pygame |
|--------------------|----------------|
| `Sprite`           | `pygame.Surface` e metadados |
| `Som`              | `pygame.mixer.Sound` |
| `Música`           | `pygame.mixer.music` |

### 3. Loop Principal do Jogo

O loop principal do jogo é implementado no Pygame, mas controlado pelo NajaScript através da função `__iniciarLoopJogo`:

```python
def implement_iniciarLoopJogo(args):
    """Implementação nativa de __iniciarLoopJogo usando Pygame"""
    callback_loop = args[0]  # Função de callback NajaScript
    game_obj = args[1]       # Objeto de jogo NajaScript
    tick_rate = args[2]      # Taxa de atualização desejada
    
    # Configura o clock do Pygame
    clock = pygame.time.Clock()
    
    # Define uma função para o loop do Pygame
    def game_loop():
        # Processa eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # Processa outros eventos...
        
        # Chama o callback NajaScript
        result = callback_loop(game_obj)
        
        # Controla a taxa de frames
        clock.tick(tick_rate)
        
        return result
    
    # Inicia o loop
    running = True
    while running:
        running = game_loop()
    
    # Finaliza o Pygame
    pygame.quit()
```

### 4. Manipulação de Eventos

Os eventos do Pygame são capturados e traduzidos para o modelo de eventos do NajaScript:

```python
def handle_pygame_events():
    """Processa eventos do Pygame e repassa para os callbacks NajaScript"""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            CALLBACKS["key_press"](key_name)
        elif event.type == pygame.KEYUP:
            key_name = pygame.key.name(event.key)
            CALLBACKS["key_release"](key_name)
        elif event.type == pygame.MOUSEMOTION:
            CALLBACKS["mouse_move"](event.pos[0], event.pos[1])
        # ... outros eventos
```

### 5. Renderização

As chamadas de renderização do NajaScript são traduzidas para as equivalentes do Pygame:

```python
def implement_desenharImagem(args):
    """Implementação nativa de __desenharImagem usando Pygame"""
    imagem_id = args[0]["id"]  # ID da imagem no cache
    x = args[1]
    y = args[2]
    largura = args[3]
    altura = args[4]
    rotacao = args[5]
    escala_x = args[6]
    escala_y = args[7]
    
    # Obtém a imagem do cache
    original_surface = RESOURCE_CACHE.get(imagem_id)
    if not original_surface:
        return
    
    # Aplica escala
    if escala_x != 1.0 or escala_y != 1.0:
        scaled_w = int(largura * escala_x)
        scaled_h = int(altura * escala_y)
        scaled_surface = pygame.transform.scale(original_surface, (scaled_w, scaled_h))
    else:
        scaled_surface = original_surface
    
    # Aplica rotação
    if rotacao != 0:
        rotated_surface = pygame.transform.rotate(scaled_surface, -rotacao)  # Pygame usa sentido horário
        # Ajusta posição para rotação em torno do centro
        rect = rotated_surface.get_rect(center=scaled_surface.get_rect(topleft=(x, y)).center)
        GAME_DATA["window"].blit(rotated_surface, rect.topleft)
    else:
        GAME_DATA["window"].blit(scaled_surface, (x, y))
```

## Integrando com o Interpretador NajaScript

Para integrar o NajaGame2D ao interpretador NajaScript, as funções nativas são registradas no ambiente de execução:

```python
def register_najagame2d_functions(interpreter):
    """Registra as funções nativas do NajaGame2D no interpretador NajaScript"""
    # Funções de janela e renderização
    interpreter.register_native_function("__criarJanela", implement_criarJanela)
    interpreter.register_native_function("__atualizarTela", implement_atualizarTela)
    interpreter.register_native_function("__limparTela", implement_limparTela)
    
    # Funções de tempo
    interpreter.register_native_function("__obterTempoAtual", implement_obterTempoAtual)
    
    # Funções de eventos
    interpreter.register_native_function("__configurarEventosTeclado", implement_configurarEventosTeclado)
    interpreter.register_native_function("__configurarEventosMouse", implement_configurarEventosMouse)
    interpreter.register_native_function("__iniciarLoopJogo", implement_iniciarLoopJogo)
    
    # Funções de recursos
    interpreter.register_native_function("__carregarImagem", implement_carregarImagem)
    interpreter.register_native_function("__carregarAudio", implement_carregarAudio)
    interpreter.register_native_function("__obterLarguraImagem", implement_obterLarguraImagem)
    # ... outras funções
```

## Variáveis Globais no Backend

O backend Pygame mantém um estado global para gerenciar recursos e dados:

```python
# Estado global do jogo
GAME_DATA = {
    "window": None,          # Janela do Pygame
    "clock": None,           # Clock do Pygame
    "current_time": 0,       # Tempo atual
    "keys": {},              # Estado das teclas
    "mouse_pos": (0, 0),     # Posição do mouse
    "mouse_pressed": False,  # Estado do clique
}

# Cache de recursos
RESOURCE_CACHE = {}  # Mapeia IDs para recursos do Pygame

# Callbacks para eventos
CALLBACKS = {
    "key_press": None,
    "key_release": None,
    "mouse_move": None,
    "mouse_click": None,
    "mouse_release": None,
}
```

## Desafios e Considerações

### 1. Sincronização de Estado

Manter consistência entre o estado do Pygame e o estado representado no NajaScript é um desafio. Utilizamos uma abordagem onde o estado "oficial" é mantido no NajaScript, e o Pygame apenas renderiza esse estado.

### 2. Gerenciamento de Memória

O Pygame aloca recursos na memória que precisam ser adequadamente gerenciados. Implementamos um sistema de cache que mantém rastreamento de recursos e os libera quando não são mais necessários.

### 3. Performance

Para jogos maiores, pode ser necessário implementar otimizações como culling de objetos fora da tela, batching de sprites, etc.

## Personalização e Extensão

Para adicionar novas funcionalidades ao NajaGame2D:

1. Adicione a função na API NajaScript (NajaGame2D_Nativo.naja)
2. Implemente a função correspondente no backend Pygame
3. Registre a função no interpretador NajaScript

## Conclusão

Esta implementação fornece uma camada de abstração sobre o Pygame que permite aos usuários do NajaScript criar jogos sem se preocuparem com os detalhes internos. A API inspirada no Godot proporciona uma experiência familiar e intuitiva, enquanto o Pygame oferece um motor robusto e bem testado sob o capô. 