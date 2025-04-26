# NajaScript Package Manager

O NajaScript Package Manager permite que você instale, gerencie e use pacotes externos em seus projetos NajaScript, semelhante ao funcionamento do npm ou yarn para JavaScript.

## Instalação

O gerenciador de pacotes está incluído na instalação do NajaScript. As principais ferramentas são:

- `naja_package_manager.py` - Funcionalidade principal do gerenciador de pacotes
- `naja_add.py` - Script auxiliar para adicionar pacotes rapidamente
- `naja_add.bat` - Wrapper em batch para Windows

## Comandos Básicos

### Adicionar Pacotes

```
naja_add <nome_pacote> [versão] [--dev/-d]
```

Exemplo:
```
naja_add MathUtils 1.0.0
naja_add TestingLibrary --dev
```

### Usar o Gerenciador de Pacotes Diretamente

Para operações mais avançadas, você pode usar o script do gerenciador de pacotes diretamente:

```
python naja_package_manager.py add <nome_pacote> [--version VERSÃO] [--dev]
python naja_package_manager.py remove <nome_pacote> [--dev]
python naja_package_manager.py list
python naja_package_manager.py install
```

## Estrutura do Projeto

Quando você adiciona pacotes, eles são armazenados no diretório `naja_modules` na raiz do seu projeto:

```
meu_projeto/
├── main.naja
├── naja_packages.json    # Arquivo de configuração de pacotes
└── naja_modules/         # Pacotes instalados
    ├── MathUtils/
    │   └── index.naja
    └── OutroPacote/
        └── index.naja
```

## Usando Pacotes no Seu Código

Para usar um pacote no seu código, importe-o usando a declaração de importação padrão:

```
import "MathUtils";

fun main() {
    println(MathUtils.info());  // Imprime informações do pacote
    println("5 + 3 = " + MathUtils.add(5, 3));
    // Use outras funções do pacote
}

main();
```

## Formato do Pacote

Cada pacote deve ter um arquivo `index.naja` que exporta funções e variáveis:

```
// Exemplo de arquivo de pacote: naja_modules/MathUtils/index.naja

export fun add(int a, int b) {
    return a + b;
}

export fun subtract(int a, int b) {
    return a - b;
}

export fun info() {
    return "MathUtils package v1.0.0";
}
```

## Criando Seus Próprios Pacotes

Para criar um pacote que outros possam usar, crie um diretório com o nome do seu pacote e adicione um arquivo `index.naja` que exporte suas funções e variáveis.

## Melhorias Futuras

- Registro remoto de pacotes para download
- Resolução de versão e gerenciamento de dependências
- Funcionalidade de publicação de pacotes 