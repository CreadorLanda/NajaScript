# NajaScript

NajaScript é uma linguagem de programação moderna e fácil de aprender, com suporte a programação orientada a objetos, módulos e mais.

## Instalação

### Requisitos
- Python 3.13 ou superior
- Windows 10 ou superior

### Instalador
1. Baixe o arquivo `NajaScript_Setup.exe` da pasta `Instalador`
2. Execute o instalador
3. Siga as instruções na tela
4. O NajaScript será instalado com um atalho no menu Iniciar e na área de trabalho

### Instalação Manual
1. Clone ou baixe este repositório
2. Certifique-se de que o Python 3.13 está instalado
3. Execute `naja.bat` para iniciar o REPL

## Uso

### REPL (Read-Eval-Print Loop)
O REPL do NajaScript permite que você execute código interativamente. Para iniciar:

1. Abra o NajaScript pelo menu Iniciar ou área de trabalho
2. Ou execute `naja.bat` na pasta do projeto

### Comandos do REPL
- `sair()` - Encerra o REPL
- `ajuda()` - Mostra os comandos disponíveis
- `limpar()` - Limpa a tela
- `historico()` - Mostra o histórico de comandos
- `reset()` - Reseta o ambiente de execução

### Exemplos de Código

```naja
// Variáveis
int idade = 25;
float altura = 1.75;
string nome = "João";

// Funções
fun calcularIMC(float peso, float altura) {
    return peso / (altura * altura);
}

// Classes
class Pessoa {
    private string nome;
    public int idade;
    
    constructor(string nome, int idade) {
        this.nome = nome;
        this.idade = idade;
    }
    
    public fun getNome() {
        return this.nome;
    }
}

// Estruturas de Controle
if (idade >= 18) {
    print("Maior de idade");
} else {
    print("Menor de idade");
}

// Loops
for (int i = 0; i < 5; i++) {
    print(i);
}

// Listas e Dicionários
list numeros = [1, 2, 3, 4, 5];
dict pessoa = {
    "nome": "Maria",
    "idade": 30
};
```

### Executando Arquivos
Para executar um arquivo .naja:

```bash
python najascript.py arquivo.naja
```

## Recursos

- Sintaxe moderna e intuitiva
- Suporte a programação orientada a objetos
- Sistema de módulos
- Tipagem estática opcional
- Estruturas de dados nativas (listas, dicionários, vetores)
- Tratamento de exceções
- Suporte a programação assíncrona
- REPL interativo

## Contribuindo

Contribuições são bem-vindas! Por favor, leia o arquivo CONTRIBUTING.md para detalhes sobre nosso código de conduta e o processo para enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

