# Sintaxe Completa do NajaScript

NajaScript é uma linguagem de programação moderna que combina características de Python e JavaScript, com adições como sistema reativo e tipagem estática.

## Índice
1. [Tipos de Dados](#tipos-de-dados)
2. [Variáveis e Constantes](#variáveis-e-constantes)
3. [Operadores](#operadores)
4. [Estruturas de Controle](#estruturas-de-controle)
5. [Funções](#funções)
6. [Funções Nativas](#funções-nativas)
7. [Sistema de Eventos](#sistema-de-eventos)
8. [Comentários](#comentários)
9. [Características Especiais](#características-especiais)
10. [Boas Práticas](#boas-práticas)

## Tipos de Dados

### Tipos Básicos
```naja
# Números inteiros
int numero = 42;

# Números decimais
float decimal = 3.14;

# Texto
string texto = "Olá mundo";

# Booleanos
bool flag = true;  # ou false

# Tipo dinâmico
any qualquer = "aceita qualquer tipo";

# Valor nulo
null valor_nulo;
```

### Tipos Compostos
```naja
# Lista mutável
list numeros = list(1, 2, 3);

# Vetor imutável
vecto vetor = vecto(1, 2, 3);

# Dicionário
dict pessoa = {nome: "João", idade: 25};
```

## Variáveis e Constantes

### Variáveis Normais
```naja
int idade = 25;
string nome = "João";
float altura = 1.75;
```

### Constantes
```naja
const int MAX_VALOR = 100;
const string VERSAO = "1.0.0";
const float PI = 3.14159;
```

### Variáveis Reativas (Flux)
```naja
int a = 10;
int b = 5;
flux resultado = a + b;  # Atualiza automaticamente quando a ou b mudam
```

## Operadores

### Operadores Aritméticos
```naja
int soma = a + b;
int subtracao = a - b;
int multiplicacao = a * b;
int divisao = a / b;
int modulo = a % b;
int potencia = a ** b;
```

### Operadores de Comparação
```naja
bool igual = a == b;
bool diferente = a != b;
bool maior = a > b;
bool menor = a < b;
bool maior_igual = a >= b;
bool menor_igual = a <= b;
```

### Operadores Lógicos
```naja
bool e = condicao1 && condicao2;
bool ou = condicao1 || condicao2;
bool nao = !condicao;
```

### Operador Ternário
```naja
string status = idade >= 18 ? "Adulto" : "Menor";
```

## Estruturas de Controle

### Condicionais
```naja
# If-elif-else
if (condicao) {
    println("Condição verdadeira");
} elif (outra_condicao) {
    println("Outra condição verdadeira");
} else {
    println("Nenhuma condição verdadeira");
}

# Switch-case
switch (valor) {
    case 1:
        println("Um");
        break
    case 2:
        println("Dois");
        break
    default:
        println("Outro número");
}
```

### Loops
```naja
# While
while (condicao) {
    # código
}

# Do-While
do {
    # código
} while (condicao);

# For tradicional
for (int i = 0; i < 10; i = i + 1) {
    # código
}

# For-in (iteração em coleções)
forin (item in lista) {
    # código
}
```

### Controle de Fluxo
```naja
break;      # Sai do loop atual
continue;   # Pula para próxima iteração
```

## Funções

### Função Básica
```naja
fun soma(int a, int b) {
    return a + b;
}
```

### Função Sem Retorno (void)
```naja
fun saudacao(string nome) {
    println("Olá, " + nome);
}
```

### Função com Tipo Dinâmico
```naja
fun mostrarInfo(any valor) {
    println("Tipo: " + type(valor));
    println("Valor: " + valor);
}
```

## Funções Nativas

### Entrada e Saída
```naja
print("Sem quebra de linha");
println("Com quebra de linha");
string entrada = input("Digite algo: ");
```

### Manipulação de Listas
```naja
lista.add(valor);              # Adiciona elemento
lista.remove(indice);          # Remove por índice
lista.removeLast();            # Remove último elemento
lista.replace(indice, valor);  # Substitui elemento
valor = lista.get(indice);     # Obtém elemento
tamanho = lista.length();      # Tamanho da lista
```

### Utilitários
```naja
tipo = type(valor);            # Tipo da variável
min_valor = min(lista);        # Valor mínimo
max_valor = max(lista);        # Valor máximo
lista_ordenada = lista.sort(); # Ordenação
esta_vazio = lista.isEmpty();  # Verifica se vazio
contagem = lista.count(item);  # Conta ocorrências
```

## Sistema de Eventos

### Monitoramento Básico
```naja
onChange("variavel", printChange);
```

### Callback Personalizado
```naja
fun monitorarMudancas(string nome_var, any valor_antigo, any valor_novo) {
    println("Variável '" + nome_var + "' mudou:");
    println("  De: " + valor_antigo);
    println("  Para: " + valor_novo);
}

onChange("contador", monitorarMudancas);
```

## Comentários
```naja
# Comentário de linha única
```

## Características Especiais

1. **Tipagem Estática**
   - Todas as variáveis precisam ter tipo declarado
   - Maior segurança e detecção de erros em tempo de compilação

2. **Sistema Reativo**
   - Variáveis `flux` atualizam automaticamente
   - Ideal para interfaces reativas e processamento em tempo real

3. **Imutabilidade Opcional**
   - Suporte a constantes com `const`
   - Vetores imutáveis com `vecto`

4. **Funções de Primeira Classe**
   - Funções podem ser passadas como argumentos
   - Suporte a callbacks e eventos

5. **Escopo em Bloco**
   - Variáveis limitadas ao seu bloco de declaração
   - Melhor organização e prevenção de conflitos

## Boas Práticas

1. **Pontuação**
   - Use ponto e vírgula (`;`) ao final das instruções
   - Delimite blocos com chaves (`{}`)

2. **Estilo de Código**
   - Indente o código adequadamente
   - Use nomes descritivos para variáveis e funções
   - Adicione comentários quando necessário

3. **Organização**
   - Agrupe código relacionado
   - Mantenha funções pequenas e focadas
   - Evite repetição de código

4. **Tipos**
   - Use tipos específicos em vez de `any` quando possível
   - Aproveite o sistema de tipos para prevenir erros

5. **Reatividade**
   - Use `flux` com moderação
   - Monitore apenas variáveis que realmente precisam ser observadas

## Exemplos Práticos

### Calculadora Simples
```naja
fun calculadora(float a, float b, string operacao) {
    switch (operacao) {
        case "+":
            return a + b;
        case "-":
            return a - b;
        case "*":
            return a * b;
        case "/":
            if (b == 0) {
                return null;
            }
            return a / b;
        default:
            return null;
    }
}

# Uso
float resultado = calculadora(10, 5, "+");
println("10 + 5 = " + resultado);
```

### Sistema Reativo
```naja
int temperatura = 20;
flux mensagem = temperatura < 20 ? "Frio" : 
                temperatura > 25 ? "Quente" : 
                "Agradável";

fun monitorarTemperatura(string nome, any antigo, any novo) {
    println("Temperatura mudou de " + antigo + "°C para " + novo + "°C");
    println("Sensação: " + mensagem);
}

onChange("temperatura", monitorarTemperatura);
```

### Manipulação de Lista
```naja
list numeros = list(1, 2, 3, 4, 5);
int soma = 0;

forin (numero in numeros) {
    soma = soma + numero;
}

println("Soma: " + soma);
println("Média: " + (soma / numeros.length()));
``` 