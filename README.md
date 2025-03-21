# NajaScript Editor & Interpretador

Este pacote inclui um editor moderno para a linguagem NajaScript com recursos avançados e interface amigável, além do interpretador para execução de scripts.

## Recursos principais

- **Editor completo** com tema escuro e interface moderna
  - Destacamento de sintaxe com cores distintas
  - Sistema de abas para editar múltiplos arquivos
  - Explorador de projetos para navegar facilmente
  - Autocompletar para palavras-chave
  - Execução integrada de scripts

- **Interpretador independente** para execução via linha de comando
  - Execute scripts NajaScript diretamente do terminal
  - Integração com o sistema operacional para associação de arquivos .naja
  - Documentação e exemplos incluídos

## Instalação

### Opção 1: Instalador (recomendado)

1. Baixe o arquivo `NajaScriptEditor_Setup.exe`
2. Execute o instalador e siga as instruções
3. Durante a instalação, você pode optar por:
   - Associar arquivos .naja ao interpretador
   - Adicionar o interpretador ao PATH do sistema
4. Após a instalação, o editor e o interpretador estarão disponíveis através do Menu Iniciar

### Opção 2: Versão portátil

1. Baixe os arquivos `NajaScriptEditor.exe` e `najascript.exe` da pasta `dist`
2. Coloque-os em uma pasta junto com arquivos de exemplo (`.naja`)
3. Execute os executáveis diretamente sem necessidade de instalação

## Usando o Editor

1. Abra o NajaScript Editor
2. Crie um novo arquivo ou abra um exemplo existente
3. Escreva seu código NajaScript
4. Salve o arquivo com a extensão `.naja`
5. Execute o script usando o botão "Executar" ou a tecla F5

## Usando o Interpretador (linha de comando)

```bash
# Executar um script
najascript caminho/para/script.naja

# Obter ajuda
najascript --help

# Verificar a versão
najascript --version
```

## Exemplo de código

```naja
# Exemplo simples de NajaScript
var mensagem = "Olá, mundo!"
imprimir(mensagem)

para (var i = 1; i <= 5; i = i + 1) {
    imprimir("Contagem: " + i)
}
```

## Recursos adicionais

- Documentação da linguagem NajaScript
- Exemplos e tutoriais
- Módulos e bibliotecas

## Desenvolvimento

O NajaScript Editor e o interpretador foram desenvolvidos usando Python. Para contribuir com o desenvolvimento:

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute `python executar_editor_melhorado.py` para testar o editor
4. Execute `python najascript.py arquivo.naja` para testar o interpretador 

## Licença

Este projeto é licenciado sob a licença MIT.

