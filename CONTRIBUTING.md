# Guia de Contribuição - NajaScript

Obrigado por seu interesse em contribuir com o NajaScript! Este documento fornece diretrizes e informações para contribuidores.

## 🤝 Como Contribuir

### Reportando Bugs

1. Verifique se o bug já foi reportado nas [Issues](https://github.com/seu-usuario/najascript/issues)
2. Se não, abra uma nova issue com:
   - Título descritivo
   - Passos para reproduzir o bug
   - Comportamento esperado vs. atual
   - Informações do sistema (OS, versão do Python)
   - Código de exemplo (se aplicável)

### Sugerindo Melhorias

1. Abra uma issue com label "enhancement"
2. Descreva claramente:
   - O que você gostaria de ver
   - Por que seria útil
   - Exemplos de uso (se aplicável)

### Contribuindo com Código

1. **Fork** o repositório
2. **Clone** seu fork:
   ```bash
   git clone https://github.com/seu-usuario/najascript.git
   ```
3. Crie uma **branch** para sua feature:
   ```bash
   git checkout -b feature/minha-feature
   ```
4. Faça suas mudanças
5. **Teste** suas mudanças
6. **Commit** com mensagens descritivas:
   ```bash
   git commit -am 'Adiciona suporte para X'
   ```
7. **Push** para sua branch:
   ```bash
   git push origin feature/minha-feature
   ```
8. Abra um **Pull Request**

## 📋 Padrões de Código

### Python

- Use Python 3.7+ 
- Siga PEP 8 para formatação
- Use type hints quando possível
- Documente funções e classes
- Máximo 100 caracteres por linha

```python
def minha_funcao(param: str) -> int:
    """
    Descrição da função.
    
    Args:
        param: Descrição do parâmetro
        
    Returns:
        Descrição do retorno
    """
    return len(param)
```

### NajaScript

- Use camelCase para funções e variáveis
- Use PascalCase para classes
- Indentação com 4 espaços
- Comentários em português ou inglês

```naja
// Exemplo de código NajaScript
class MinhaClasse {
    private int valor;
    
    constructor(int valorInicial) {
        this.valor = valorInicial;
    }
    
    public int getValor() {
        return this.valor;
    }
}
```

## 🧪 Testes

### Executando Testes

```bash
# Executar todos os testes
python -m pytest tests/

# Executar testes específicos
python -m pytest tests/test_interpreter.py

# Executar com cobertura
python -m pytest --cov=najascript tests/
```

### Criando Testes

1. Crie arquivos de teste em `tests/`
2. Use o prefixo `test_` para funções de teste
3. Use `pytest` para assertions
4. Teste casos normais e casos extremos

```python
def test_minha_funcao():
    # Arrange
    entrada = "teste"
    esperado = 5
    
    # Act
    resultado = minha_funcao(entrada)
    
    # Assert
    assert resultado == esperado
```

## 🚀 Configuração do Ambiente

### Pré-requisitos

- Python 3.7+
- pip
- git

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/najascript.git
cd najascript/NajaScript

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Instale dependências de desenvolvimento
pip install -r requirements-dev.txt
```

### Estrutura do Projeto

```
NajaScript/
├── interpreter.py          # Interpretador principal
├── lexer.py               # Analisador léxico
├── parser_naja.py         # Analisador sintático
├── ast_nodes.py           # Nós da AST
├── environment.py         # Ambiente de execução
├── naja_editor.py         # Editor/IDE
├── modules/               # Módulos integrados
│   ├── NajaGame.naja      # Engine de jogos
│   └── NajaPt.naja        # Suporte ao português
├── exemplos/              # Exemplos de código
├── tests/                 # Testes automatizados
└── docs/                  # Documentação
```

## 📝 Documentação

### Atualizando Documentação

- Documente novas features
- Atualize exemplos
- Mantenha README.md atualizado
- Use comentários claros no código

### Formato de Documentação

```markdown
# Título da Funcionalidade

## Descrição

Breve descrição da funcionalidade.

## Sintaxe

```naja
// Exemplo de código
```

## Parâmetros

- `param1`: Descrição do parâmetro
- `param2`: Descrição do parâmetro

## Retorno

Descrição do que é retornado.

## Exemplo

```naja
// Exemplo prático
```
```

## 🌐 Internacionalização

### Adicionando Suporte a Idiomas

1. Adicione palavras-chave no arquivo apropriado
2. Teste com exemplos
3. Documente as mudanças
4. Atualize testes

### Padrões de Tradução

- Mantenha consistência com traduções existentes
- Use termos comuns na programação
- Teste com falantes nativos quando possível

## 🔄 Processo de Review

### Pull Requests

1. **Título descritivo**: Use verbos no imperativo
2. **Descrição clara**: Explique o que foi feito e por quê
3. **Testes**: Inclua testes para novas funcionalidades
4. **Documentação**: Atualize docs quando necessário
5. **Commits limpos**: Use commits atômicos e descritivos

### Checklist para PRs

- [ ] Código segue padrões do projeto
- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Sem conflitos de merge
- [ ] Funcionality testada manualmente

## 📊 Métricas de Qualidade

### Cobertura de Testes

Mantenha cobertura de testes acima de 80%.

### Qualidade do Código

- Use ferramentas como `pylint`, `flake8`, `black`
- Resolva warnings e erros
- Mantenha complexidade ciclomática baixa

## 🏷️ Versionamento

- Seguimos [Semantic Versioning](https://semver.org/)
- MAJOR.MINOR.PATCH
- Use tags para releases

## 🎯 Prioridades

### Alta Prioridade

- Correção de bugs críticos
- Melhorias de performance
- Recursos essenciais

### Média Prioridade

- Novas funcionalidades
- Melhorias de usabilidade
- Documentação

### Baixa Prioridade

- Recursos avançados
- Otimizações menores
- Recursos experimentais

## 🤖 Automação

### CI/CD

- Testes executam automaticamente
- Linting é verificado
- Builds são testados

### Hooks

```bash
# Instalar hooks de pre-commit
pip install pre-commit
pre-commit install
```

## 🌟 Reconhecimento

Contribuidores são reconhecidos:
- No arquivo AUTHORS.md
- Na seção de contribuidores do GitHub
- Em releases notes

## 📬 Contato

- **Issues**: Para bugs e sugestões
- **Discussions**: Para discussões gerais
- **Email**: Para contato direto com mantenedores

## 🎉 Primeiros Passos

### Issues para Iniciantes

Procure por issues com labels:
- `good-first-issue`
- `help-wanted`
- `beginner-friendly`

### Mentoria

- Estamos disponíveis para ajudar novos contribuidores
- Não hesite em fazer perguntas
- Feedback construtivo é sempre bem-vindo

## 📚 Recursos Úteis

- [Guia de Sintaxe](SINTAXE_NAJASCRIPT.md)
- [Documentação da API](docs/)
- [Exemplos de Código](exemplos/)
- [Testes Existentes](tests/)

---

**Obrigado por contribuir com o NajaScript! 🐍** 