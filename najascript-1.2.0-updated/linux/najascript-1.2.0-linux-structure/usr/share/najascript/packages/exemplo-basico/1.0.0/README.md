# Exemplo Básico

Pacote de exemplo básico para demonstrar a estrutura de pacotes NajaScript.

## Instalação

```bash
naja_pkg install exemplo-basico
```

## Uso

```naja
import "exemplo-basico";

// Usar o pacote
string saudacao = exemploBasico.saudar("Mundo");
println(saudacao);

int resultado = exemploBasico.calcular(5, 3);
println("Resultado: " + resultado);

dicionario info = exemploBasico.info();
println("Pacote: " + info.obter("nome"));
```

## API

### Métodos

- `saudar(string nome)` - Retorna uma saudação personalizada
- `calcular(int a, int b)` - Soma dois números
- `info()` - Retorna informações do pacote

## Licença

MIT
