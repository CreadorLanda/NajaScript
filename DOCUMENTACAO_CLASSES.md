# Documentação das Classes e Componentes do Editor NajaScript Melhorado

Este documento detalha as classes e componentes implementados nas melhorias do Editor NajaScript, fornecendo documentação técnica para desenvolvedores que desejem entender ou estender o código.

## Visão Geral da Arquitetura

O editor melhorado utiliza uma arquitetura baseada em componentes, onde cada funcionalidade principal é implementada como uma classe separada que interage com o controlador principal (`NajaScriptEditorMelhorado`). A estrutura principal consiste em:

1. `NajaScriptEditorMelhorado` - Classe principal que estende o editor original
2. `ProjectExplorer` - Componente para navegação em árvore de arquivos
3. `EditorTabs` - Componente para gerenciamento de múltiplas abas de edição

Esta arquitetura modular facilita a manutenção e extensão do código, permitindo adicionar novas funcionalidades sem alterar significativamente o núcleo do editor.

## Classe: NajaScriptEditorMelhorado

Esta classe estende `NajaScriptEditor` original, sobrescrevendo métodos específicos para implementar o tema escuro e o layout moderno.

### Principais Métodos Sobrescritos

#### `configure_style()`
Configura o estilo visual do editor, implementando um tema escuro inspirado no IntelliJ IDEA.

**Detalhes Técnicos:**
- Utiliza o tema 'clam' do ttk como base
- Define uma paleta de cores para diferentes elementos da interface
- Configura estilos específicos para widgets como frames, botões, abas e árvores

#### `create_main_area()`
Cria o layout principal do editor com painéis divididos.

**Detalhes Técnicos:**
- Utiliza `ttk.PanedWindow` para criar painéis redimensionáveis
- Implementa um layout dividido horizontalmente entre explorador de projetos e área de edição
- Implementa um layout dividido verticalmente na área de edição entre o editor e a saída
- Integra o sistema de abas para permitir a edição de múltiplos arquivos

#### Métodos de Manipulação de Arquivos
Vários métodos são sobrescritos para trabalhar com o sistema de abas:

- `open_file()` - Abre arquivos em novas abas
- `new_file()` - Cria novas abas vazias
- `save_file()` - Salva o conteúdo da aba atual
- `_save_to_file()` - Implementação do salvamento que suporta múltiplos editores

### Novos Métodos Adicionados

#### `setup_editor_highlighting(editor)`
Configura o destaque de sintaxe para um editor específico.

**Parâmetros:**
- `editor` - O widget de texto do editor a ser configurado

#### `open_specific_file(file_path)`
Abre um arquivo específico no editor, verificando se já está aberto em alguma aba.

**Parâmetros:**
- `file_path` - O caminho completo do arquivo a ser aberto

**Retorno:**
- `True` se a operação for bem-sucedida
- `False` em caso de erro

## Classe: ProjectExplorer

Implementa o explorador de projetos que exibe a estrutura de arquivos e diretórios.

### Atributos Principais

- `editor` - Referência ao editor principal
- `tree` - Widget Treeview que exibe a estrutura de arquivos
- `context_menu` - Menu de contexto para operações com arquivos
- `current_directory` - Diretório atual exibido no explorador

### Métodos Principais

#### `__init__(parent, editor)`
Inicializa o explorador de projetos.

**Parâmetros:**
- `parent` - Widget pai onde o explorador será inserido
- `editor` - Referência ao editor principal

#### `populate_tree()`
Popula a árvore com os arquivos e diretórios do diretório atual.

#### `_populate_directory(parent, path)`
Método auxiliar para popular recursivamente um diretório na árvore.

**Parâmetros:**
- `parent` - Item pai na árvore
- `path` - Caminho do diretório a ser populado

#### `refresh_tree()`
Atualiza a árvore de arquivos, recarregando os itens.

#### `on_item_double_click(event)`
Manipula o evento de clique duplo em um item da árvore, abrindo o arquivo correspondente.

**Parâmetros:**
- `event` - Objeto de evento do Tkinter

#### `show_context_menu(event)`
Exibe o menu de contexto para o item selecionado.

**Parâmetros:**
- `event` - Objeto de evento do Tkinter

#### Operações de Arquivo
Métodos para manipular arquivos e diretórios:

- `open_selected()` - Abre o arquivo selecionado
- `rename_selected()` - Renomeia o arquivo ou diretório selecionado
- `delete_selected()` - Exclui o arquivo ou diretório selecionado
- `new_file()` - Cria um novo arquivo
- `new_directory()` - Cria um novo diretório

## Classe: EditorTabs

Implementa o sistema de abas para edição de múltiplos arquivos.

### Atributos Principais

- `editor` - Referência ao editor principal
- `tabs` - Dicionário que armazena informações sobre as abas, com a seguinte estrutura:
  ```
  {
      'tab_id': {
          'editor': widget,       # Widget do editor de texto
          'line_numbers': widget, # Widget de números de linha
          'file': path,           # Caminho do arquivo aberto na aba
          'modified': bool        # Indica se o conteúdo foi modificado
      }
  }
  ```
- `context_menu` - Menu de contexto para operações com abas

### Métodos Principais

#### `__init__(parent, editor)`
Inicializa o sistema de abas.

**Parâmetros:**
- `parent` - Widget pai onde as abas serão inseridas
- `editor` - Referência ao editor principal

#### `add_tab(file_path=None, content=None)`
Adiciona uma nova aba ao editor.

**Parâmetros:**
- `file_path` - Caminho do arquivo a ser aberto (opcional)
- `content` - Conteúdo inicial do editor (opcional)

**Retorno:**
- Tupla contendo (frame da aba, widget do editor)

#### `_update_line_numbers(tab_frame)`
Atualiza os números de linha para a aba especificada.

**Parâmetros:**
- `tab_frame` - Frame da aba a ser atualizada

#### `_on_tab_changed(event)`
Manipula o evento de mudança de aba, atualizando as referências no editor principal.

**Parâmetros:**
- `event` - Objeto de evento do Tkinter

#### `_on_text_modified(tab_frame)`
Manipula o evento de modificação de texto, atualizando o estado modificado da aba.

**Parâmetros:**
- `tab_frame` - Frame da aba que foi modificada

#### Operações com Abas
Métodos para gerenciar as abas:

- `_close_current_tab()` - Fecha a aba atual
- `_close_other_tabs()` - Fecha todas as abas exceto a atual
- `_close_all_tabs()` - Fecha todas as abas e cria uma nova em branco
- `_save_tab(tab_widget)` - Salva o conteúdo da aba especificada
- `save_current_tab()` - Salva a aba atual

## Diagrama de Classes Simplificado

```
NajaScriptEditor (original)
    |
    +-- NajaScriptEditorMelhorado
           |
           +-- usa ProjectExplorer
           |
           +-- usa EditorTabs
```

## Fluxos de Interação

### Abertura de Arquivo
1. Usuário solicita abertura de arquivo (menu ou explorador)
2. `open_file()` ou `open_specific_file()` é chamado
3. O sistema verifica se o arquivo já está aberto em alguma aba
4. Se não estiver, uma nova aba é criada com o conteúdo do arquivo
5. A aba é selecionada e o foco é dado ao editor

### Salvamento de Arquivo
1. Usuário solicita salvamento (menu ou atalho)
2. `save_file()` é chamado, que delega para `save_current_tab()` do sistema de abas
3. Se o arquivo ainda não tem um caminho, é solicitado um novo caminho
4. O conteúdo é salvo e o estado da aba é atualizado
5. O explorador de projetos é atualizado para refletir as mudanças

### Destaque de Sintaxe
1. Usuário edita texto em um editor
2. O evento `<KeyRelease>` aciona `update_syntax()`
3. As tags existentes são removidas
4. Novos padrões são aplicados ao texto
5. A visualização é atualizada com as cores corretas

## Extensibilidade

O design modular facilita a extensão do editor com novas funcionalidades. Para adicionar novos recursos:

1. **Novos Widgets:** Podem ser adicionados como componentes separados que interagem com o editor principal.
2. **Novos Padrões de Sintaxe:** Podem ser adicionados modificando o método `setup_patterns()`.
3. **Novos Temas:** Podem ser implementados criando variações do método `configure_style()`.
4. **Novas Operações de Arquivo:** Podem ser adicionadas estendendo as classes existentes.

## Conclusão

Esta arquitetura modular proporciona um editor flexível e extensível, permitindo que desenvolvedores adicionem novas funcionalidades ou modifiquem o comportamento existente sem alterar significativamente o núcleo do sistema. 