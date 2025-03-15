# NajaPt: Programação em Português com NajaScript

O NajaPt é uma extensão do NajaScript que permite programar em português, tornando a linguagem de programação mais acessível para falantes nativos de português, especialmente estudantes e iniciantes.

## Instalação e Uso

Para utilizar o NajaPt, basta import a biblioteca no início do seu código:

```naja
import "NajaPt";
```

Após import, você pode escrever seu código usando as palavras-chave e funções em português.

## Palavras-Chave em Português

| Português | NajaScript Original |
|-----------|---------------------|
| `se`      | `if`                |
| `senao`   | `else`              |
| `para`    | `for`               |
| `enquanto`| `while`             |
| `funcao`  | `fun`               |
| `retornar`| `return`            |
| `verdadeiro` | `true`           |
| `falso`   | `false`             |
| `em`      | `in`                |
| `paracada`| `forin`             |
| `nulo`    | `null`              |
| `continuar` | `continue`        |
| `parar`   | `break`             |

## Tipos de Dados

| Português   | NajaScript Original |
|-------------|---------------------|
| `inteiro`   | `int`               |
| `decimal`   | `float`             |
| `texto`     | `string`            |
| `booleano`  | `bool`              |
| `lista`     | `list`              |
| `dicionario`| `dict`              |
| `qualquer`  | `any`               |

## Funções Integradas

| Português              | NajaScript Original |
|------------------------|---------------------|
| `escrever()`           | `print()`           |
| `escreverln()`         | `println()`         |
| `comprimento()`        | `length()`          |
| `converter_para_texto()`| `toString()`        |
| `converter_para_inteiro()`| `toInt()`         |
| `converter_para_decimal()`| `toFloat()`       |

## Exemplos de Código

### Exemplo 1: Olá Mundo

```naja
import "NajaPt";

funcao principal() {
    escreverln("Olá Mundo!");
}

principal();
```

### Exemplo 2: Calculadora Simples

```naja
import "NajaPt";

funcao calculadora(inteiro a, inteiro b, texto operacao) {
    se (operacao == "soma") {
        retornar a + b;
    } senao se (operacao == "subtracao") {
        retornar a - b;
    } senao se (operacao == "multiplicacao") {
        retornar a * b;
    } senao se (operacao == "divisao") {
        se (b == 0) {
            escreverln("Erro: Divisão por zero!");
            retornar 0;
        }
        retornar a / b;
    } senao {
        escreverln("Operação desconhecida!");
        retornar 0;
    }
}

escreverln("Resultado: " + calculadora(10, 5, "soma"));        // 15
escreverln("Resultado: " + calculadora(10, 5, "subtracao"));   // 5
escreverln("Resultado: " + calculadora(10, 5, "multiplicacao")); // 50
escreverln("Resultado: " + calculadora(10, 5, "divisao"));     // 2
```

### Exemplo 3: Estruturas de Controle

```naja
import "NajaPt";

funcao exemploEstruturasControle() {
    // Exemplo de loop para
    escreverln("Contagem de 1 a 5:");
    para (inteiro i = 1; i <= 5; i = i + 1) {
        escrever(i + " ");
    }
    escreverln("");
    
    // Exemplo de loop enquanto
    escreverln("Contagem regressiva:");
    inteiro contador = 5;
    enquanto (contador > 0) {
        escrever(contador + " ");
        contador = contador - 1;
    }
    escreverln("");
    
    // Exemplo de condicional
    inteiro idade = 18;
    se (idade >= 18) {
        escreverln("Maior de idade");
    } senao {
        escreverln("Menor de idade");
    }
    
    // Exemplo de loop paracada com lista
    lista numeros = [1, 2, 3, 4, 5];
    inteiro soma = 0;
    paracada (num em numeros) {
        soma = soma + num;
    }
    escreverln("Soma dos números: " + soma);
}

exemploEstruturasControle();
```

### Exemplo 4: Manipulação de Listas e Dicionários

```naja
import "NajaPt";

funcao exemploColecoes() {
    // Lista
    lista frutas = ["maçã", "banana", "laranja"];
    escreverln("Frutas: " + frutas);
    
    frutas.adicionar("uva");
    escreverln("Frutas após adicionar uva: " + frutas);
    
    frutas.remover(1);  // Remove banana
    escreverln("Frutas após remover banana: " + frutas);
    
    // Dicionário
    dicionario pessoa = {
        nome: "João",
        idade: 30,
        cidade: "São Paulo"
    };
    
    escreverln("Pessoa: " + pessoa);
    escreverln("Nome: " + pessoa.obter("nome"));
    
    pessoa.adicionar("profissao", "Programador");
    escreverln("Pessoa após adicionar profissão: " + pessoa);
    
    pessoa.remover("cidade");
    escreverln("Pessoa após remover cidade: " + pessoa);
}

exemploColecoes();
```

## Uso com NajaGame2D

O NajaPt é totalmente compatível com NajaGame2D, permitindo que você desenvolva jogos usando português:

```naja
import "NajaPt";
import "NajaGame2D";

// Constantes do jogo
decimal GRAVIDADE = 980;
inteiro LARGURA_TELA = 800;
inteiro ALTURA_TELA = 600;

// Variáveis globais
dicionario jogo;
dicionario jogador;

// Função principal do jogo
funcao iniciarJogo() {
    // Inicializa o jogo
    jogo = iniciarJogo(LARGURA_TELA, ALTURA_TELA, "Meu Primeiro Jogo");
    
    // Carrega sprites
    dicionario sprite_jogador = criarSprite("imagens/jogador.png", 64, 64);
    
    // Cria o jogador
    jogador = criarObjeto("jogador", 100, 100, sprite_jogador);
    jogador.velocidade_x = 0;
    jogador.velocidade_y = 0;
    
    // Cria a cena
    dicionario cena_principal = criarCena("principal", atualizarJogo, renderizarJogo);
    adicionarObjetoACena(cena_principal, jogador);
    
    // Adiciona cena ao jogo
    adicionarCena(jogo, cena_principal);
    
    // Inicia o jogo
    comecarJogo(jogo);
}

// Atualiza o jogo
funcao atualizarJogo(dicionario jogo, decimal delta_tempo) {
    // Processa entrada
    se (teclaEstaPressionada(jogo, "direita")) {
        jogador.velocidade_x = 200;
    } senao se (teclaEstaPressionada(jogo, "esquerda")) {
        jogador.velocidade_x = -200;
    } senao {
        jogador.velocidade_x = 0;
    }
    
    se (teclaEstaPressionada(jogo, "cima")) {
        jogador.velocidade_y = -200;
    } senao se (teclaEstaPressionada(jogo, "baixo")) {
        jogador.velocidade_y = 200;
    } senao {
        jogador.velocidade_y = 0;
    }
    
    // Atualiza posição do jogador
    atualizarObjeto(jogador, delta_tempo);
}

// Renderiza o jogo
funcao renderizarJogo(dicionario jogo) {
    dicionario cena = jogo.cenas.obter(jogo.cena_atual);
    
    // Renderiza todos os objetos da cena
    paracada (objeto em cena.objetos) {
        renderizarObjeto(jogo, objeto);
    }
    
    // Renderiza texto na tela
    desenharTexto("Use as setas para mover", 20, 20, "branco", "20px Arial");
}

// Inicia o jogo
iniciarJogo();
```

## Como o NajaPt Funciona

O NajaPt realiza a tradução das palavras-chave em português para as equivalentes em NajaScript em tempo de execução. Isso é feito através de:

1. Um pré-processador que analisa o código fonte
2. Substituição das palavras-chave em português pelas equivalentes em NajaScript
3. Execução do código transformado pelo interpretador NajaScript

## Considerações Finais

O NajaPt torna a programação mais acessível para falantes de português, especialmente para iniciantes e estudantes, removendo a barreira do idioma inglês. Todas as funcionalidades do NajaScript estão disponíveis em português, permitindo uma experiência de programação completa e educativa.

Para mais informações sobre as funções e recursos disponíveis, consulte a documentação completa do NajaScript, lembrando de utilizar as palavras-chave em português conforme documentado aqui. 