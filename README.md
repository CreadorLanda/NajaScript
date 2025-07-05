# NajaScript 🐍

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

Uma linguagem de programação educacional moderna e intuitiva, com suporte nativo ao português e recursos avançados para desenvolvimento de jogos 2D.

![NajaScript Logo](assets/NajaScript_logo.png)

## ✨ Características

- **Sintaxe Simples**: Fácil de aprender e usar
- **Suporte ao Português**: Programe usando palavras-chave em português
- **Tipagem Estática**: Tipos definidos para maior segurança
- **Orientação a Objetos**: Classes, herança, interfaces e encapsulamento
- **Sistema Reativo**: Variáveis `flux` que atualizam automaticamente
- **Engine de Jogos**: NajaGame2D integrado para desenvolvimento de jogos
- **Async/Await**: Programação assíncrona nativa
- **Sistema de Módulos**: Importação e exportação de código
- **Editor Integrado**: IDE completo com sintaxe destacada

## 🚀 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação via Git

```bash
git clone https://github.com/seu-usuario/najascript.git
cd najascript/NajaScript
pip install -r requirements.txt
```

### Uso

```bash
# Executar um arquivo NajaScript
python najascript.py exemplo.naja

# Executar em português
python najascript.py --pt exemplo.naja

# Abrir o editor
python naja_editor.py

# Modo debug
python najascript.py --debug exemplo.naja
```

## 📖 Exemplos

### Exemplo Básico

```naja
// Olá Mundo em NajaScript
fun main() {
    println("Olá, mundo!");
    
    int numero = 42;
    string texto = "NajaScript";
    
    println("Número: " + numero);
    println("Texto: " + texto);
}

main();
```

### Exemplo em Português

```naja
// Importa suporte ao português
importar "NajaPt";

funcao principal() {
    inteiro idade = 25;
    texto nome = "Maria";
    
    se (idade >= 18) {
        escreverln("Você é maior de idade");
    } senao {
        escreverln("Você é menor de idade");
    }
    
    lista numeros = [1, 2, 3, 4, 5];
    paracada (inteiro num em numeros) {
        escreverln("Número: " + num);
    }
}

principal();
```

### Exemplo de Jogo Simples

```naja
import "NajaGame";

// Inicializar jogo
initGame(800, 600, "Meu Jogo");

// Cores
list corVerde = [0, 128, 0];
list corAzul = [135, 206, 235];

// Posição do jogador
int x = 100, y = 100;

// Loop principal
while (true) {
    clearScreen(corAzul);
    
    // Controles
    if (isKeyPressed("UP")) y = y - 5;
    if (isKeyPressed("DOWN")) y = y + 5;
    if (isKeyPressed("LEFT")) x = x - 5;
    if (isKeyPressed("RIGHT")) x = x + 5;
    
    // Desenhar jogador
    drawRect(x, y, 50, 50, corVerde);
    
    updateWindow();
}
```

### Orientação a Objetos

```naja
class Pessoa {
    private string nome;
    private int idade;
    
    constructor(string nome, int idade) {
        this.nome = nome;
        this.idade = idade;
    }
    
    public void saudacao() {
        println("Olá, sou " + this.nome + " e tenho " + this.idade + " anos");
    }
}

// Uso
Pessoa pessoa = new Pessoa("João", 30);
pessoa.saudacao();
```

## 📚 Documentação

- [Sintaxe Completa](SINTAXE_NAJASCRIPT.md)
- [Documentação em Português](DOCUMENTACAO_NAJASCRIPT_PT.md)
- [NajaGame2D - Engine de Jogos](DOCUMENTACAO_NAJAGAME2D.md)
- [Sistema de Módulos](DOCUMENTACAO_CLASSES.md)
- [Guia de Desenvolvedor](NAJAGAME2D_PARA_DESENVOLVEDORES.md)

## 🎮 NajaGame2D

Engine de jogos 2D integrada baseada em Pygame:

```naja
import "NajaGame";

initGame(800, 600, "Meu Jogo");

// Carregar recursos
int sprite = loadImage("player.png");
setIcon("icon.png");

// Loop do jogo
while (true) {
    clearScreen([0, 0, 0]);
    
    // Sua lógica de jogo aqui
    drawImage(sprite, 100, 100);
    
    updateWindow();
}
```

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
NajaScript/
├── interpreter.py      # Interpretador principal
├── lexer.py           # Analisador léxico
├── parser_naja.py     # Analisador sintático
├── ast_nodes.py       # Nós da AST
├── environment.py     # Ambiente de execução
├── naja_editor.py     # Editor/IDE
├── modules/           # Módulos integrados
│   ├── NajaGame.naja  # Engine de jogos
│   └── NajaPt.naja    # Suporte ao português
├── exemplos/          # Exemplos de código
└── docs/             # Documentação
```

### Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 🔧 Ferramentas

- **Editor Integrado**: IDE completo com autocompletar e sintaxe destacada
- **REPL**: Console interativo para testes rápidos
- **Package Manager**: Sistema de gerenciamento de pacotes
- **Compilador JIT**: Compilação Just-In-Time com LLVM
- **Extensão VSCode**: Suporte completo no Visual Studio Code

## 📦 Funcionalidades Avançadas

### Sistema Reativo

```naja
int a = 10;
int b = 5;
flux resultado = a + b;  // Atualiza automaticamente

// Quando a ou b mudam, resultado é recalculado
a = 20;  // resultado agora é 25
```

### Async/Await

```naja
async fun buscarDados() {
    var resposta = await fetch("https://api.exemplo.com/dados");
    return resposta.json();
}

async fun main() {
    var dados = await buscarDados();
    println(dados);
}
```

### Generics

```naja
class Caixa<T> {
    private T conteudo;
    
    constructor(T valor) {
        this.conteudo = valor;
    }
    
    public T getConteudo() {
        return this.conteudo;
    }
}

Caixa<int> caixaNumero = new Caixa<int>(42);
Caixa<string> caixaTexto = new Caixa<string>("Olá");
```

## 🎯 Casos de Uso

- **Educação**: Ensino de programação em português
- **Jogos 2D**: Desenvolvimento rápido de jogos
- **Prototipagem**: Criação rápida de protótipos
- **Aprendizado**: Primeira linguagem de programação

## 🏆 Reconhecimentos

- Inspirado em linguagens como Python, JavaScript e TypeScript
- Engine de jogos baseada em Pygame
- Suporte da comunidade open source

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/najascript/issues)
- **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/najascript/discussions)
- **Wiki**: [GitHub Wiki](https://github.com/seu-usuario/najascript/wiki)

## 📈 Roadmap

- [ ] Melhorias na performance do interpretador
- [ ] Mais módulos integrados
- [ ] Suporte a mais plataformas
- [ ] Documentação expandida
- [ ] Tutoriais em vídeo
- [ ] Comunidade Discord

---

**Feito com ❤️ pela comunidade NajaScript**

