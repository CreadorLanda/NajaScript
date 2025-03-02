# NajaScript

NajaScript é uma linguagem de programação interpretada baseada em Python e JavaScript. Esta implementação contém um interpretador básico para a linguagem.

## ✨ Características da Linguagem

### ⚡ Tipos de Dados

- `int` - Números inteiros
- `float` - Números de ponto flutuante
- `string` - Cadeias de caracteres
- `bool` - Valores booleanos (`true`/`false`)
- `dict` - Dicionários que permitem qualquer tipo de dado
- `vecto` - Vetores imutáveis
- `list` - Listas mutáveis
- `null` - Valor nulo
- `void` - Tipo para funções sem retorno
- `flux` - Variáveis reativas que são reavaliadas automaticamente
- `any` - Tipo dinâmico que pode representar qualquer valor

### 🔧 Operadores

- **Aritméticos:** `+`, `-`, `*`, `/`, `%`, `**` (potência)
- **Comparativos:** `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Lógicos:** `&&`, `||`, `!`
- **Ternário:** `cond ? valor_se_verdadeiro : valor_se_falso`

### 🌐 Estruturas de Controle

- Condicionais: `if`, `elif`, `else`, `switch`, `case`, `default`
- Laços: `while`, `do-while`, `for`, `forin`
- Controle de fluxo: `break`, `continue`

### 🌐 Funções

- Definição com `fun`
- Funções com tipo de retorno
- Funções recursivas
- Funções de ordem superior

### 📝 Funções Nativas

- `print()`, `println()`
- `input()`
- `type()`
- `add()`, `remove()`, `removeLast()`, `replace()`
- `get()`, `length()`
- `min()`, `max()`
- `sort()`, `isEmpty()`, `count()`
- `onChange()`: Registra callback para mudanças em variáveis
- `printChange()`: Exibe mudanças em variáveis no console

## 💪 Recursos Especiais

### Flux: Variáveis Reativas

As variáveis `flux` armazenam expressões, não valores, e são reavaliadas automaticamente sempre que as variáveis das quais dependem são alteradas.

```javascript
int a = 10;
int b = 5;
flux x = a + b;

println(x);  // 15

// Quando 'a' muda, 'x' é automaticamente recalculado
a = 20;
println(x);  // 25
```

### ⚡ Sistema de Eventos `onChange`

Permite monitorar mudanças em variáveis através de callbacks:

```javascript
onChange("contador", printChange);
contador = 5;  // "Variável 'contador' mudou: 0 -> 5"
```

Callbacks personalizados:

```javascript
fun apenasAumentos(string nome_var, any valor_antigo, any valor_novo) {
    if (valor_novo > valor_antigo) {
        println("AUMENTO em " + nome_var + ": " + valor_antigo + " -> " + valor_novo);
    }
}

onChange("temperatura", apenasAumentos);
```

## 🔧 Como Usar

### ⚡ Requisitos

- Python 3.6 ou superior

### 📂 Execução

Para executar um programa NajaScript:

```bash
python najascript.py arquivo.naja
```

## 📚 Exemplos

### Exemplo Básico

```javascript
int x = 10;
int y = 5;
println("Soma: " + (x + y));
println("Subtração: " + (x - y));
println("Multiplicação: " + (x * y));
println("Divisão: " + (x / y));

if (x > y) {
    println("x é maior que y");
} else {
    println("y é maior ou igual a x");
}

int contador = 0;
while (contador < 5) {
    println("Contador: " + contador);
    contador = contador + 1;
}

fun saudacao(string nome) {
    return "Olá, " + nome + "!";
}
println(saudacao("Mundo"));
```

### Exemplo com Flux e `onChange`

```javascript
int contador = 0;
string mensagem = "Inicial";
flux resultado = "Contador: " + contador + ", Mensagem: " + mensagem;

onChange("contador", printChange);
println("Inicial: " + resultado);

contador = 5;
println("Final: " + resultado);
```

## 🤖 Implementação

O interpretador consiste em:

- **Lexer**: Converte o código-fonte em tokens
- **Parser**: Analisa os tokens e gera uma AST (Abstract Syntax Tree)
- **Interpreter**: Percorre a AST e executa o código

## 🚫 Limitações

- Sem suporte para classes e objetos
- Funções de ordem superior limitadas
- Mensagens de erro podem ser aprimoradas
- Não otimizado para alto desempenho

## 💚 Licença

Este projeto é de código aberto. Modificações e distribuições são permitidas, desde que o nome do autor original seja mantido.

## ✍️ Autor

Este projeto foi desenvolvido por Alexandre Landa.

