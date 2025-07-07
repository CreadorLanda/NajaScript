# NajaScript Package Registry

Registry oficial de pacotes para a linguagem de programação NajaScript.

## Estrutura

- `registry/` - Índice de pacotes e metadados
- `packages/` - Código fonte dos pacotes
- `docs/` - Documentação
- `examples/` - Exemplos de uso

## Como Usar

### Instalar um Pacote

```bash
naja_pkg install nome-do-pacote
```

### Listar Pacotes

```bash
naja_pkg list
```

### Pesquisar Pacotes

```bash
naja_pkg search termo
```

## Estrutura de Pacotes

Cada pacote deve seguir esta estrutura:

```
packages/
└── nome-do-pacote/
    └── versao/
        ├── index.naja      # Código principal
        ├── package.json    # Metadados
        └── README.md       # Documentação
```

## Contribuindo

1. Fork este repositório
2. Crie seu pacote seguindo a estrutura acima
3. Atualize o `registry/index.json`
4. Faça um Pull Request

## Pacotes Disponíveis

Veja `registry/index.json` para a lista completa de pacotes.
