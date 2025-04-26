# NajaScript - Extensão VSCode

Esta extensão oferece suporte à linguagem NajaScript no Visual Studio Code, com destaque especial para o português.

## Características

### Suporte Completo para Português

NajaScript é uma linguagem que suporta sintaxe tanto em inglês quanto em português, permitindo escrever código em português nativo:

```naja
// Exemplo de código NajaScript em português
funcao principal() {
    inteiro contador = 0;
    enquanto (contador < 10) {
        escreverln("Contador: " + contador);
        contador += 1;
    }
    
    se (contador > 5) {
        escreverln("Valor final: " + contador);
    } senao {
        escreverln("Valor baixo");
    }
}
```

### Palavras-chave em Português

Esta extensão oferece coloração para palavras-chave em português:

- **Declarações**: `classe`, `funcao`, `construtor`, `interface`
- **Controle de Fluxo**: `se`, `senao`, `enquanto`, `para`, `paracada`, `tentar`, `pegar`, `finalmente`
- **Tipos**: `inteiro`, `decimal`, `texto`, `booleano`, `vazio`, `lista`, `mapa`
- **Modificadores**: `publico`, `privado`, `protegido`, `estatico`
- **Operadores**: `e`, `ou`, `nao`
- **Valores**: `verdadeiro`, `falso`, `nulo`

### Tema de Cores NajaScript Dark

A extensão inclui um tema dark específico para NajaScript com as seguintes cores:

| Elemento | Exemplo | Cor |
|----------|---------|-----|
| Variáveis | `let nome` | Azul claro (#9CDCFE) |
| Constantes | `const PI = 3.14` | Azul escuro (#569CD6) |
| Funções | `funcao ola() {}` | Amarelo claro (#DCDCAA) |
| Parâmetros | `funcao(a, b)` | Azul claro (#9CDCFE) |
| Classes | `classe Animal {}` | Verde água (#4EC9B0) |
| Métodos | `andar() {}` | Amarelo claro (#DCDCAA) |
| Palavra-chave este | `este.nome` | Rosa claro (#C586C0) |
| Palavra-chave super | `super()` | Rosa claro (#C586C0) |
| Palavra-chave novo | `novo Pessoa()` | Azul claro (#569CD6) |
| Tipos | `: texto`, `: Pessoa` | Verde água (#4EC9B0) |
| Strings | `"texto"` | Laranja (#CE9178) |
| Números | `123` | Verde pálido (#B5CEA8) |
| Booleanos | `verdadeiro`, `falso` | Azul claro (#569CD6) |
| Null | `nulo` | Rosa claro (#C586C0) |
| Palavras-chave | `se`, `para`, `retornar` | Azul claro (#569CD6) |
| Comentários | `// comentário` | Verde musgo (#6A9955) |
| Operadores | `+`, `-`, `*`, `=` | Branco (#D4D4D4) |
| Pontuação | `()`, `{}`, `;` | Branco (#D4D4D4) |

## Instalação

1. Baixe o arquivo .vsix
2. Abra o VS Code
3. Vá para a aba Extensões
4. Clique nos três pontos (...) no topo da aba Extensões
5. Selecione "Instalar do VSIX..."
6. Selecione o arquivo .vsix baixado

## Uso

Após a instalação, arquivos .naja serão automaticamente reconhecidos. Para selecionar o tema:

1. Pressione Ctrl+K Ctrl+T (ou Cmd+K Cmd+T no Mac)
2. Selecione "NajaScript Dark" na lista

## Licença

Esta extensão está licenciada sob a [licença MIT](LICENSE.md). 