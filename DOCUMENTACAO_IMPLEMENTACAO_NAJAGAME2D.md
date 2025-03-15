# Implementação Nativa do NajaGame2D no Interpretador NajaScript

Este documento detalha como implementar o NajaGame2D diretamente no interpretador NajaScript, sem depender de bibliotecas externas como Pygame. Essa abordagem permite uma integração mais profunda e eficiente.

## Visão Geral da Implementação

O NajaGame2D nativo é implementado por meio de funções especiais no interpretador NajaScript que fornecem acesso a recursos de baixo nível para gráficos, entrada e áudio. Em vez de utilizar Pygame ou outra biblioteca externa, o interpretador implementa diretamente essas funcionalidades usando APIs do sistema operacional ou outras bibliotecas nativas.

## Funções Nativas a Implementar

Para que o NajaGame2D funcione, o interpretador NajaScript precisa implementar as seguintes funções nativas:

### Janela e Renderização

```naja
# Cria uma janela e retorna uma referência a ela
fun __criarJanela(int largura, int altura, string titulo) { return null; }

# Atualiza o conteúdo da tela
fun __atualizarTela() {}

# Limpa a tela com a cor especificada
fun __limparTela(string cor) {}
```

### Tempo

```naja
# Retorna o tempo atual em milissegundos
fun __obterTempoAtual() { return 0; }
```

### Manipulação de Eventos

```naja
# Configura callbacks para eventos de teclado
fun __configurarEventosTeclado(fun callback_pressionar, fun callback_soltar) {}

# Configura callbacks para eventos de mouse
fun __configurarEventosMouse(fun callback_movimento, fun callback_clique, fun callback_soltar) {}

# Inicia o loop principal do jogo
fun __iniciarLoopJogo(fun callback_loop, dict game, int tick_rate) {}
```

### Manipulação de Recursos

```naja
# Carrega uma imagem do disco
fun __carregarImagem(string caminho) { return null; }

# Carrega um arquivo de áudio do disco
fun __carregarAudio(string caminho) { return null; }

# Obtém a largura de uma imagem
fun __obterLarguraImagem(any imagem) { return 0; }

# Obtém a altura de uma imagem
fun __obterAlturaImagem(any imagem) { return 0; }

# Redimensiona uma imagem
fun __redimensionarImagem(any imagem, int largura, int altura) { return null; }

# Recorta uma parte de uma imagem
fun __recortarImagem(any imagem, int x, int y, int largura, int altura) { return null; }
```

### Desenho

```naja
# Desenha uma imagem na tela
fun __desenharImagem(any imagem, int x, int y, int largura, int altura, float rotacao, float escala_x, float escala_y) {}

# Desenha texto na tela
fun __desenharTexto(string texto, int x, int y, string cor, string fonte) {}

# Desenha um retângulo na tela
fun __desenharRetangulo(int x, int y, int largura, int altura, string cor, bool preenchido) {}

# Desenha um círculo na tela
fun __desenharCirculo(int x, int y, int raio, string cor, bool preenchido) {}
```

### Áudio

```naja
# Toca um som
fun __tocarSom(any som) {}

# Toca uma música de fundo
fun __tocarMusica(any musica, bool repetir) {}

# Pausa a música de fundo
fun __pausarMusica() {}

# Ajusta o volume da música de fundo
fun __ajustarVolumeMusica(float volume) {}
```

## Implementação no Interpretador

### Opções de Implementação

Existem várias opções para implementar essas funções nativas no interpretador NajaScript:

1. **SDL2**: Uma biblioteca multiplataforma que fornece acesso a áudio, teclado, mouse, joystick e gráficos.
2. **SFML**: Uma biblioteca orientada a objetos para desenvolvimento de jogos e aplicações multimídia.
3. **Bibliotecas específicas da plataforma**: 
   - Windows: DirectX ou GDI+
   - Linux: X11 ou Wayland
   - macOS: Cocoa ou Metal

### Exemplo de Implementação com SDL2

Aqui está um exemplo de como implementar as funções nativas usando SDL2 em C/C++:

```cpp
// Estrutura para armazenar os dados do SDL
struct SDLData {
    SDL_Window* window;
    SDL_Renderer* renderer;
    std::map<std::string, SDL_Texture*> textures;
    std::map<std::string, Mix_Chunk*> sounds;
    Mix_Music* currentMusic;
};

// Variável global para armazenar os dados do SDL
SDLData sdlData;

// Implementação de __criarJanela
Value najascript_createWindow(const std::vector<Value>& args) {
    int width = args[0].asInt();
    int height = args[1].asInt();
    std::string title = args[2].asString();
    
    // Inicializa o SDL
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO) < 0) {
        std::cerr << "Erro ao inicializar SDL: " << SDL_GetError() << std::endl;
        return Value::null();
    }
    
    // Inicializa SDL_mixer para áudio
    if (Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 2048) < 0) {
        std::cerr << "Erro ao inicializar SDL_mixer: " << Mix_GetError() << std::endl;
    }
    
    // Cria a janela
    sdlData.window = SDL_CreateWindow(
        title.c_str(),
        SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
        width, height,
        SDL_WINDOW_SHOWN
    );
    
    if (!sdlData.window) {
        std::cerr << "Erro ao criar janela: " << SDL_GetError() << std::endl;
        return Value::null();
    }
    
    // Cria o renderer
    sdlData.renderer = SDL_CreateRenderer(sdlData.window, -1, SDL_RENDERER_ACCELERATED);
    if (!sdlData.renderer) {
        std::cerr << "Erro ao criar renderer: " << SDL_GetError() << std::endl;
        SDL_DestroyWindow(sdlData.window);
        return Value::null();
    }
    
    // Retorna uma referência à janela (pode ser um objeto com detalhes adicionais)
    return Value::makeObject("window");
}

// Implementação de __atualizarTela
Value najascript_updateScreen(const std::vector<Value>& args) {
    SDL_RenderPresent(sdlData.renderer);
    return Value::null();
}

// Implementação de __limparTela
Value najascript_clearScreen(const std::vector<Value>& args) {
    std::string colorStr = args[0].asString();
    SDL_Color color = parseColor(colorStr); // Função auxiliar para converter string de cor para SDL_Color
    
    SDL_SetRenderDrawColor(sdlData.renderer, color.r, color.g, color.b, color.a);
    SDL_RenderClear(sdlData.renderer);
    
    return Value::null();
}

// Implementação de __carregarImagem
Value najascript_loadImage(const std::vector<Value>& args) {
    std::string path = args[0].asString();
    
    // Verifica se a imagem já está carregada
    if (sdlData.textures.find(path) != sdlData.textures.end()) {
        return Value::makeObject(path); // Retorna referência à textura existente
    }
    
    // Carrega a imagem
    SDL_Surface* surface = IMG_Load(path.c_str());
    if (!surface) {
        std::cerr << "Erro ao carregar imagem " << path << ": " << IMG_GetError() << std::endl;
        return Value::null();
    }
    
    // Cria textura a partir da superfície
    SDL_Texture* texture = SDL_CreateTextureFromSurface(sdlData.renderer, surface);
    SDL_FreeSurface(surface);
    
    if (!texture) {
        std::cerr << "Erro ao criar textura: " << SDL_GetError() << std::endl;
        return Value::null();
    }
    
    // Armazena a textura no mapa
    sdlData.textures[path] = texture;
    
    // Retorna uma referência à textura
    return Value::makeObject(path);
}

// Implementação de __desenharImagem
Value najascript_drawImage(const std::vector<Value>& args) {
    std::string texturePath = args[0].asObject()->id;
    int x = args[1].asInt();
    int y = args[2].asInt();
    int width = args[3].asInt();
    int height = args[4].asInt();
    float rotation = args[5].asFloat();
    float scaleX = args[6].asFloat();
    float scaleY = args[7].asFloat();
    
    // Verifica se a textura existe
    if (sdlData.textures.find(texturePath) == sdlData.textures.end()) {
        std::cerr << "Textura não encontrada: " << texturePath << std::endl;
        return Value::null();
    }
    
    SDL_Texture* texture = sdlData.textures[texturePath];
    
    // Configura o retângulo de destino
    SDL_Rect dstRect = {x, y, width, height};
    
    // Aplica escala se necessário
    if (scaleX != 1.0f || scaleY != 1.0f) {
        dstRect.w = static_cast<int>(width * scaleX);
        dstRect.h = static_cast<int>(height * scaleY);
    }
    
    // Desenha a textura
    SDL_RenderCopyEx(
        sdlData.renderer,
        texture,
        NULL, // Origem (NULL = toda a textura)
        &dstRect,
        rotation, // Ângulo em graus
        NULL, // Ponto de rotação (NULL = centro da textura)
        SDL_FLIP_NONE // Não inverte a textura
    );
    
    return Value::null();
}
```

### Integrando no Interpretador NajaScript

Para integrar essas funções no interpretador, você precisará:

1. **Registrar as funções nativas**: Adicione as funções ao ambiente global do interpretador.
2. **Gerenciar o ciclo de vida dos recursos**: Implemente limpeza adequada para evitar vazamentos de memória.
3. **Lidar com exceções e erros**: Implemente tratamento de erros robusto para fornecer feedback útil.

Exemplo de como registrar as funções nativas no interpretador:

```cpp
void registerNajaGameFunctions(Interpreter& interpreter) {
    interpreter.registerNativeFunction("__criarJanela", najascript_createWindow);
    interpreter.registerNativeFunction("__atualizarTela", najascript_updateScreen);
    interpreter.registerNativeFunction("__limparTela", najascript_clearScreen);
    interpreter.registerNativeFunction("__obterTempoAtual", najascript_getCurrentTime);
    interpreter.registerNativeFunction("__carregarImagem", najascript_loadImage);
    // ... registre as demais funções
}
```

## Recursos do Sistema Operacional

A implementação deve lidar corretamente com recursos do sistema operacional:

1. **Janelas e Contextos Gráficos**: Crie e gerencie janelas e contextos de renderização.
2. **Eventos**: Capture eventos do sistema operacional (teclado, mouse, janela) e repasse-os para o código NajaScript.
3. **Áudio**: Gerencie a reprodução de som e música, incluindo mixagem e streaming.
4. **Temporização**: Implemente um sistema de temporização preciso para o loop do jogo.
5. **Recursos**: Carregue e gerencie recursos como imagens e arquivos de áudio.

## Considerações de Performance

Para garantir um bom desempenho, considere:

1. **Uso de GPU**: Utilize aceleração de hardware quando disponível.
2. **Gerenciamento de Memória**: Implemente um sistema eficiente de cache e liberação de recursos não utilizados.
3. **Otimização de Renderização**: Use batching e outras técnicas para minimizar chamadas de desenho.
4. **Multithreading**: Considere usar threads separadas para renderização, física e áudio.

## Arquitetura Final

A arquitetura final consiste em:

1. **Interpretador NajaScript**: Executa o código NajaScript.
2. **Funções Nativas**: Fornecem acesso a recursos do sistema.
3. **Camada de Abstração**: Implementa as funções nativas usando bibliotecas como SDL ou APIs do sistema.
4. **Sistema Operacional**: Provê acesso a hardware e recursos.

### Fluxo de Execução

1. O código NajaScript chama uma função da biblioteca NajaGame2D.
2. A biblioteca chama uma função nativa do interpretador.
3. A função nativa interage com a biblioteca gráfica (SDL, etc.).
4. A biblioteca gráfica usa APIs do sistema operacional para renderizar, reproduzir áudio, etc.
5. Os eventos do sistema operacional são capturados e passados de volta para o código NajaScript através de callbacks.

## Conclusão

Implementar o NajaGame2D nativamente no interpretador NajaScript resulta em um sistema mais eficiente e integrado, sem dependências externas como Pygame. Esta abordagem requer mais trabalho inicial, mas oferece maior controle e desempenho, permitindo que os desenvolvedores criem jogos 2D diretamente em NajaScript.

Ao seguir estas diretrizes, você poderá criar uma implementação robusta e eficiente do NajaGame2D que aproveitará ao máximo as capacidades do sistema subjacente. 