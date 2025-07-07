# NajaScript Package Manager - Guia Completo

O NajaScript Package Manager é um sistema moderno de gerenciamento de pacotes que usa o GitHub como registry central para distribuir módulos e bibliotecas da linguagem NajaScript.

## 🚀 Características

- ✅ **Registry GitHub**: Usa [https://github.com/NajaScript/Naja](https://github.com/NajaScript/Naja) como repositório central
- ✅ **Fácil de usar**: Interface de linha de comando intuitiva
- ✅ **Versionamento**: Suporte completo a versionamento semântico
- ✅ **Templates automáticos**: Cria templates quando pacotes não estão disponíveis
- ✅ **Cross-platform**: Funciona no Windows, Linux e macOS
- ✅ **Configuração flexível**: Sistema de configuração personalizável

## 📦 Instalação

O package manager já vem incluído com o NajaScript. Para usá-lo:

### Windows:
```bash
naja_pkg.bat <comando>
```

### Linux/macOS:
```bash
python naja_pkg <comando>
```

## 🎯 Comandos Principais

### 1. Inicializar um Projeto

```bash
# Criar novo projeto
python naja_pkg init meu-projeto

# Criar projeto no diretório atual
python naja_pkg init
```

Isso cria:
- `naja_packages.json` - Arquivo de configuração do projeto
- `main.naja` - Arquivo principal do projeto
- `.gitignore` - Ignorar arquivos desnecessários

### 2. Instalar Pacotes

```bash
# Instalar última versão
python naja_pkg install nome-do-pacote

# Instalar versão específica
python naja_pkg install nome-do-pacote --version 1.2.0

# Instalar como dependência de desenvolvimento
python naja_pkg install nome-do-pacote --dev

# Instalar todas as dependências do projeto
python naja_pkg install
```

### 3. Listar Pacotes

```bash
# Ver todos os pacotes instalados
python naja_pkg list
```

Saída exemplo:
```
📦 Pacotes Instalados
========================================

📋 Dependências:
  ✅ exemplo-basico@1.0.0
  ✅ math-utils@2.1.0

🔧 Dependências de Desenvolvimento:
  ✅ test-framework@1.0.0
```

### 4. Pesquisar Pacotes

```bash
# Pesquisar por nome ou descrição
python naja_pkg search utilitarios
python naja_pkg search math
python naja_pkg search game
```

### 5. Desinstalar Pacotes

```bash
# Remover pacote
python naja_pkg uninstall nome-do-pacote
```

### 6. Atualizar Pacotes

```bash
# Atualizar todos os pacotes para última versão
python naja_pkg update
```

### 7. Publicar Pacotes

```bash
# Publicar pacote atual
python naja_pkg publish

# Publicar pacote de outro diretório
python naja_pkg publish /caminho/para/pacote
```

## 📁 Estrutura de Projeto

### naja_packages.json
```json
{
  "name": "meu-projeto",
  "version": "1.0.0",
  "description": "Meu projeto NajaScript",
  "main": "main.naja",
  "scripts": {
    "start": "najascript main.naja"
  },
  "keywords": ["najascript"],
  "author": "Seu Nome",
  "license": "MIT",
  "dependencies": {
    "exemplo-basico": "1.0.0"
  },
  "devDependencies": {
    "test-framework": "1.0.0"
  }
}
```

### Estrutura de Diretórios
```
meu-projeto/
├── naja_packages.json    # Configuração do projeto
├── main.naja            # Arquivo principal
├── .gitignore           # Arquivos a ignorar
├── naja_modules/        # Pacotes instalados
│   └── exemplo-basico/
│       ├── index.naja
│       └── package.json
└── .naja_cache/         # Cache do sistema
```

## 🔧 Configuração

### Arquivo .naja_config
```json
{
  "registry": {
    "url": "https://github.com/NajaScript/Naja",
    "api": "https://api.github.com/repos/NajaScript/Naja",
    "raw": "https://raw.githubusercontent.com/NajaScript/Naja"
  },
  "cache_dir": ".naja_cache",
  "user": {
    "name": "Seu Nome",
    "email": "seu@email.com",
    "github_token": "seu_token_github"
  }
}
```

## 📚 Usando Pacotes no Código

### Importar e Usar

```naja
// Importar o pacote
import "exemplo-basico";

fun main() {
    // Usar funções do pacote
    string saudacao = exemploBasico.saudar("Mundo");
    println(saudacao);
    
    int resultado = exemploBasico.calcular(5, 3);
    println("Resultado: " + resultado);
    
    dicionario info = exemploBasico.info();
    println("Pacote: " + info.obter("nome"));
}

main();
```

## 🏗️ Criando Seus Próprios Pacotes

### 1. Estrutura Mínima

```
meu-pacote/
├── package.json         # Metadados do pacote
├── index.naja          # Código principal
└── README.md           # Documentação
```

### 2. package.json do Pacote

```json
{
  "name": "meu-pacote",
  "version": "1.0.0",
  "description": "Descrição do meu pacote",
  "main": "index.naja",
  "keywords": ["najascript", "utility"],
  "author": "Seu Nome",
  "license": "MIT",
  "dependencies": {},
  "najascript": {
    "min_version": "1.0.0"
  }
}
```

### 3. index.naja do Pacote

```naja
// Meu Pacote Personalizado
classe MeuPacote {
    funcao construtor() {
        println("MeuPacote carregado!");
    }
    
    funcao funcaoUtil(string input) {
        return "Processado: " + input;
    }
    
    funcao info() {
        dicionario info = {};
        info.add("nome", "meu-pacote");
        info.add("versao", "1.0.0");
        info.add("autor", "Seu Nome");
        return info;
    }
}

// Exportar instância
var meuPacote = MeuPacote();
```

## 🌐 Publicando no GitHub Registry

### 1. Fork do Repositório
1. Visite [https://github.com/NajaScript/Naja](https://github.com/NajaScript/Naja)
2. Clique em "Fork"
3. Clone seu fork localmente

### 2. Adicionar Seu Pacote
```bash
# Estrutura no repositório
packages/
└── seu-pacote/
    └── 1.0.0/
        ├── index.naja
        ├── package.json
        └── README.md
```

### 3. Atualizar registry/index.json
```json
{
  "packages": {
    "seu-pacote": {
      "name": "seu-pacote",
      "description": "Descrição do seu pacote",
      "author": "Seu Nome",
      "license": "MIT",
      "keywords": ["najascript"],
      "versions": ["1.0.0"],
      "latest": "1.0.0"
    }
  }
}
```

### 4. Criar Pull Request
1. Commit suas mudanças
2. Push para seu fork
3. Criar Pull Request para o repositório principal

## 🔍 Exemplos Práticos

### Projeto de Jogo Simples

```bash
# Criar projeto
python naja_pkg init meu-jogo

# Instalar NajaGame
python naja_pkg install najagame

# Código do jogo
```

```naja
import "najagame";

fun main() {
    NajaGame.initGame(800, 600, "Meu Jogo");
    
    while (NajaGame.isGameRunning()) {
        NajaGame.handleEvents();
        NajaGame.clearScreen(0, 100, 200);
        
        // Lógica do jogo aqui
        
        NajaGame.updateDisplay();
    }
    
    NajaGame.quitGame();
}

main();
```

### Aplicação Web

```bash
# Instalar módulos web
python naja_pkg install http-server
python naja_pkg install json-utils
```

```naja
import "http-server";
import "json-utils";

fun main() {
    httpServer.start(8080);
    println("Servidor rodando em http://localhost:8080");
}

main();
```

## 🛠️ Resolução de Problemas

### Pacote não encontrado
```
❌ Pacote 'exemplo' não encontrado no registry.
✅ Criando template básico...
```
- O sistema automaticamente cria um template para desenvolvimento local
- Você pode implementar as funcionalidades no arquivo gerado

### Erro de conexão
```
❌ Erro ao buscar índice de pacotes
```
- Verifique sua conexão com a internet
- O registry pode estar temporariamente indisponível
- Pacotes já instalados continuam funcionando

### Conflitos de versão
- Use `python naja_pkg list` para ver versões instaladas
- Use `python naja_pkg install pacote --version X.Y.Z` para versão específica

## 📋 Referência Rápida

| Comando | Descrição |
|---------|-----------|
| `init [nome]` | Criar novo projeto |
| `install [pacote]` | Instalar pacote |
| `install` | Instalar dependências |
| `uninstall pacote` | Remover pacote |
| `list` | Listar pacotes |
| `search termo` | Pesquisar pacotes |
| `update` | Atualizar todos |
| `publish [path]` | Publicar pacote |

## 🤝 Contribuindo

1. Fork o repositório [NajaScript/Naja](https://github.com/NajaScript/Naja)
2. Crie um pacote seguindo as convenções
3. Teste localmente
4. Submeta Pull Request
5. Aguarde revisão da comunidade

## 📞 Suporte

- 🐛 **Bugs**: Abra uma issue no [GitHub](https://github.com/NajaScript/Naja/issues)
- 💬 **Discussões**: Use as [Discussions](https://github.com/NajaScript/Naja/discussions)
- 📚 **Documentação**: Veja a [Wiki](https://github.com/NajaScript/Naja/wiki)

---

**© 2025 NajaScript Community**

Feito com ❤️ para a comunidade NajaScript 