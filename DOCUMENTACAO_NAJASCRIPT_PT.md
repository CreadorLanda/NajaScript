# Documentação NajaScript - Suporte a Português

## Introdução

O NajaScript agora oferece suporte nativo para programação em português através do módulo NajaPt. Esta documentação explica como utilizar a linguagem NajaScript com sintaxe em português, facilitando o aprendizado para falantes de português.

## Configuração

Para utilizar o NajaScript em português, você tem duas opções:

1. **Importar o módulo NajaPt**: Adicione a linha `importar "NajaPt";` no início do seu código.
2. **Usar a flag --pt**: Execute o interpretador NajaScript com a flag `--pt` para habilitar automaticamente o suporte a português para todo o código.

```bash
python najascript.py --pt meu_script.naja
```

## Palavras-chave em Português

O módulo NajaPt traduz as seguintes palavras-chave:

### Estruturas de Controle
| Português | NajaScript |
|-----------|------------|
| se        | if         |
| senao     | else       |
| para      | for        |
| enquanto  | while      |
| paracada  | forin      |
| parar     | break      |
| continuar | continue   |

### Declarações
| Português   | NajaScript |
|-------------|------------|
| funcao      | fun        |
| retornar    | return     |
| importar    | import     |
| verdadeiro  | true       |
| falso       | false      |
| nulo        | null       |
| em          | in         |

### Operadores Lógicos
| Português   | NajaScript |
|-------------|------------|
| e           | &&         |
| ou          | \|\|       |
| nao         | !          |

### Tipos de Dados
| Português   | NajaScript |
|-------------|------------|
| inteiro     | int        |
| decimal     | float      |
| texto       | string     |
| booleano    | bool       |
| lista       | list       |
| dicionario  | dict       |
| qualquer    | any        |

### Funções Nativas
| Português            | NajaScript  |
|----------------------|-------------|
| escrever             | print       |
| escreverln           | println     |
| comprimento          | length      |
| converter_para_texto | toString    |
| converter_para_inteiro | toInt     |
| converter_para_decimal | toFloat   |

### Métodos
| Português     | NajaScript |
|---------------|------------|
| adicionar     | add        |
| remover       | remove     |
| obter         | get        |
| adicionarUltimo | add      |
| removerUltimo | removeLast |
| substituir    | replace    |

## Exemplo de Código

### Usando Importação Explícita

```
// Habilita suporte a português
importar "NajaPt";

// Função principal
funcao principal() {
    inteiro idade = 25;
    texto nome = "Maria";
    
    escreverln("Olá, " + nome + "!");
    
    se (idade >= 18) {
        escreverln("Você é maior de idade.");
    } senao {
        escreverln("Você é menor de idade.");
    }
    
    // Loop com 'para'
    para (inteiro i = 0; i < 5; i = i + 1) {
        escreverln("Iteração: " + i);
    }
    
    // Array e iteração com 'paracada'
    lista numeros = [1, 2, 3, 4, 5];
    
    paracada (inteiro num em numeros) {
        escreverln("Número: " + num);
    }
    
    // Usando operadores lógicos
    booleano temIdade = idade > 20;
    booleano temNome = nome != "";
    
    se (temIdade e temNome) {
        escreverln("Condições atendidas!");
    }
    
    se (temIdade ou idade < 15) {
        escreverln("Pelo menos uma condição atendida!");
    }
    
    se (nao temIdade) {
        escreverln("Condição negada!");
    }
}

// Chamada da função principal
principal();
```

## Limitações Atuais

- Os operadores lógicos em português (`e`, `ou`, `nao`) requerem espaços entre eles e os operandos para serem reconhecidos corretamente.
- Todos os operadores aritméticos (+, -, *, /, %) permanecem em sua forma original.
- A implementação atual não modifica mensagens de erro, que continuarão em inglês.

## Considerações Técnicas

O módulo NajaPt implementa um pré-processador que traduz o código em português para o formato NajaScript padrão antes da análise léxica e sintática. Isso significa que não há sobrecarga de performance durante a execução.

O processamento é feito usando expressões regulares para garantir que apenas palavras completas sejam substituídas, evitando problemas com substrings em identificadores ou strings.

### Como Funciona a Tradução

A tradução ocorre em duas etapas:

1. Para palavras-chave e identificadores, usamos expressões regulares para garantir que apenas palavras completas sejam substituídas.
2. Para operadores lógicos (`e`, `ou`, `nao`), buscamos por padrões específicos que incluem espaços ao redor.

Esta abordagem garante que a tradução seja precisa, mas requer que operadores lógicos sejam escritos com espaços ao redor.

## Desenvolvendo com NajaPt

Para desenvolvedores que desejam estender o módulo NajaPt:

1. O mapeamento de palavras-chave está definido na função `_import_najaPt()` no arquivo `interpreter.py`.
2. A função de pré-processamento é registrada durante a importação do módulo e aplicada a todo código fonte subsequente.
3. Para adicionar novas palavras-chave em português, atualize o dicionário `pt_to_naja` no arquivo `interpreter.py`. 