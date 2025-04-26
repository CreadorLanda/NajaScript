# NajaScript Module Repository System

O Sistema de Repositórios de Módulos NajaScript permite o compartilhamento e reuso de código através de um repositório centralizado de pacotes.

## Componentes

O sistema consiste em quatro partes principais:

1. **Gerenciador de Pacotes** (`naja_package_manager.py`) - Gerencia pacotes instalados localmente
2. **Gerenciador de Repositórios** (`naja_repository_manager.py`) - Conecta-se a repositórios locais e remotos
3. **Criador de Repositórios** (`create_repository.py`) - Cria e gerencia repositórios de módulos
4. **Publicador Remoto** (`naja_remote.py`) - Publica pacotes diretamente no repositório central

## Instalação

Todos os scripts necessários já estão incluídos na instalação do NajaScript. Para atualizar ou reinstalar:

```
git clone https://github.com/seu-usuario/najascript-repo.git
cd najascript-repo
python setup.py install
```

## Comandos Básicos

### Adicionar Pacotes

O comando `naja_add` busca pacotes nos repositórios configurados:

```
python naja_add.py MathUtils
python naja_add.py --version 1.2.0 GraphicsLib
python naja_add.py --dev TestingKit
```

### Pesquisar Pacotes

```
python naja_add.py --search math
```

### Configurar Repositórios

```
python naja_repository_manager.py set-local /caminho/para/repositorio/local
python naja_repository_manager.py set-remote https://github.com/CreadorLanda/naja-packages.git
python naja_repository_manager.py use-remote --enable
```

### Publicar Pacotes no Repositório Central

```
python naja_remote.py MathUtils
python naja_remote.py Pygame --version 1.1.0 --description "Integração com a biblioteca Pygame"
```

Ou usando o atalho no Windows:

```
naja_remote MathUtils
```

O comando `naja_remote` automaticamente:
1. Clona o repositório remoto em uma área temporária
2. Adiciona seu pacote com a estrutura correta
3. Atualiza o índice do repositório
4. Faz commit e push das alterações para o repositório remoto

### Criar um Repositório Local

```
python create_repository.py init
python create_repository.py add MathUtils 1.0.0 ./naja_modules/MathUtils --description "Biblioteca de funções matemáticas"
python create_repository.py list
```

## Estrutura de Diretórios

```
meu_projeto/
├── main.naja
├── naja_packages.json    # Configuração de pacotes
├── .naja_config          # Configuração de repositórios
└── naja_modules/         # Pacotes instalados
    └── MathUtils/
        └── index.naja

naja_repository/          # Repositório local
├── index.json            # Índice de pacotes
└── modules/              # Pacotes no repositório
    └── MathUtils/
        └── 1.0.0/
            └── index.naja
```

## Repositório Remoto Central

O sistema agora está integrado com o repositório remoto central em:

```
https://github.com/CreadorLanda/naja-packages.git
```

Este repositório serve como a fonte oficial de pacotes para a comunidade NajaScript.

## Criando Seu Próprio Módulo

1. Crie uma pasta com o nome do seu módulo em `naja_modules/NomeDoModulo`
2. Adicione um arquivo `index.naja` que exporte funções e variáveis
3. Use `naja_remote` para publicar no repositório central:
   ```
   naja_remote NomeDoModulo --description "Descrição do seu módulo"
   ```

Exemplo de módulo:

```naja
// Arquivo: MeuModulo/index.naja

export fun minhaFuncao(parametro) {
    // Implementação
    return resultado;
}

export var MINHA_CONSTANTE = 42;
```

## Usando Módulos em Seu Código

```naja
import "MathUtils";

fun main() {
    println(MathUtils.add(5, 3));
}

main();
```

## Autenticação para Publicação

Para publicar pacotes no repositório central, você precisa:

1. Ter permissões de escrita no repositório GitHub
2. Ter suas credenciais do Git configuradas na máquina local
3. Se necessário, executar `git config --global user.name "Seu Nome"` e `git config --global user.email "seu@email.com"` antes de usar `naja_remote`

## Melhorias Futuras

- Suporte a versionamento semântico
- Resolução de dependências
- Interface web para explorar pacotes
- Autenticação com token para publicação
- Verificação de integridade e segurança 