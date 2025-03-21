# Guia de Melhorias para o NajaScript Editor

Este documento descreve as melhorias sugeridas para o NajaScript Editor, transformando-o em uma IDE mais moderna e funcional, semelhante ao IntelliJ IDEA.

## Visão Geral das Melhorias

1. **Tema Escuro Moderno**
   - Paleta de cores semelhante ao IntelliJ IDEA
   - Melhor contraste e legibilidade
   - Destaque de sintaxe aprimorado

2. **Explorador de Projetos**
   - Navegação em árvore de arquivos e pastas
   - Operações de arquivo (criar, excluir, renomear)
   - Exibição de metadados (tamanho, data de modificação)

3. **Sistema de Abas**
   - Edição de múltiplos arquivos
   - Indicadores de modificação
   - Menu de contexto para operações com abas

4. **Layout Flexível**
   - Painéis redimensionáveis
   - Melhor organização do espaço de trabalho
   - Interface mais intuitiva

## Implementação

### 1. Adicionar Novas Classes

Já adicionamos duas novas classes principais:

- `ProjectExplorer`: Implementa o explorador de projetos
- `EditorTabs`: Implementa o sistema de abas para edição de múltiplos arquivos

### 2. Modificar o Método `configure_style()`

Atualize o método `configure_style()` na classe `NajaScriptEditor` para implementar o tema escuro:

```python
def configure_style(self):
    """Configura o estilo visual do editor para um tema moderno"""
    style = ttk.Style()
    style.theme_use('clam')  # Pode ser 'clam', 'alt', 'default', 'classic'
    
    # Configuração de cores para tema escuro semelhante ao IntelliJ IDEA
    self.colors = {
        'bg_main': '#2b2b2b',             # Fundo principal
        'bg_panel': '#3c3f41',            # Fundo de painéis
        'bg_text': '#2b2b2b',             # Fundo de área de texto
        'fg_text': '#a9b7c6',             # Texto normal
        'fg_keyword': '#cc7832',          # Palavras-chave (laranja)
        'fg_builtin': '#a9b7c6',          # Funções integradas
        'fg_string': '#6a8759',           # Strings (verde)
        'fg_number': '#6897bb',           # Números (azul)
        'fg_comment': '#808080',          # Comentários (cinza)
        'fg_module': '#ffc66d',           # Módulos (amarelo)
        'fg_literal': '#9876aa',          # Literais como true, false (roxo)
        'selection_bg': '#214283',        # Fundo da seleção (azul escuro)
        'line_numbers_bg': '#313335',     # Fundo dos números de linha
        'line_numbers_fg': '#606366',     # Cor dos números de linha
        'highlight_line': '#323232',      # Linha atual
        'toolbar_bg': '#3c3f41',          # Fundo da barra de ferramentas
        'tab_active': '#4e5254',          # Aba ativa
        'tab_inactive': '#3c3f41',        # Aba inativa
        'status_bar_bg': '#3c3f41',       # Fundo da barra de status
        'button_bg': '#4c5052',           # Fundo dos botões
        'button_fg': '#a9b7c6',           # Texto dos botões
    }
    
    # Configuração geral dos elementos da interface
    style.configure('TFrame', background=self.colors['bg_panel'])
    style.configure('TLabel', background=self.colors['bg_panel'], foreground=self.colors['fg_text'])
    style.configure('TButton', 
                   background=self.colors['button_bg'], 
                   foreground=self.colors['button_fg'],
                   padding=5)
    
    # Configuração para a barra de ferramentas
    style.configure('Toolbar.TFrame', background=self.colors['toolbar_bg'])
    
    # Botão de execução destacado
    style.configure('Run.TButton', 
                  background='#365880',
                  foreground='white',
                  font=('Helvetica', 9, 'bold'),
                  padding=5)
    
    # Botão grande de execução
    style.configure('BigRun.TButton',
                  background='#365880',
                  foreground='white',
                  font=('Helvetica', 12, 'bold'),
                  padding=8)
    
    # Botão de interrupção
    style.configure('Stop.TButton',
                  background='#a1424a',
                  foreground='white',
                  font=('Helvetica', 12, 'bold'),
                  padding=8)
    
    # Botão de destaque para caixas de diálogo
    style.configure('Accent.TButton',
                  background='#365880',
                  foreground='white',
                  font=('Helvetica', 10, 'bold'),
                  padding=6)
    
    # Configurações para outros widgets
    style.configure('TNotebook', background=self.colors['bg_panel'])
    style.configure('TNotebook.Tab', background=self.colors['tab_inactive'], 
                  foreground=self.colors['fg_text'], padding=[10, 2])
    style.map('TNotebook.Tab', 
            background=[('selected', self.colors['tab_active'])],
            foreground=[('selected', self.colors['fg_text'])])
    
    # Configurações para o Treeview (explorador de projetos)
    style.configure('Treeview', 
                  background=self.colors['bg_panel'],
                  foreground=self.colors['fg_text'],
                  fieldbackground=self.colors['bg_panel'])
    style.map('Treeview', 
            background=[('selected', self.colors['selection_bg'])],
            foreground=[('selected', self.colors['fg_text'])])
```

### 3. Modificar o Método `create_main_area()`

Atualize o método `create_main_area()` para implementar o layout dividido:

```python
def create_main_area(self):
    """Cria a área principal do editor com layout moderno"""
    # Criar painel principal horizontal para dividir explorador e editor
    self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
    self.main_paned.pack(fill=tk.BOTH, expand=True)
    
    # Painel esquerdo - Explorador de Projetos
    self.left_panel = ttk.Frame(self.main_paned)
    self.main_paned.add(self.left_panel, weight=1)
    
    # Criar explorador de projetos
    self.project_explorer = ProjectExplorer(self.left_panel, self)
    self.project_explorer.pack(fill=tk.BOTH, expand=True)
    
    # Painel direito - Editor e Saída
    self.right_panel = ttk.Frame(self.main_paned)
    self.main_paned.add(self.right_panel, weight=4)
    
    # Criar painel vertical para dividir editor e saída
    self.editor_output_paned = ttk.PanedWindow(self.right_panel, orient=tk.VERTICAL)
    self.editor_output_paned.pack(fill=tk.BOTH, expand=True)
    
    # Área do editor (agora com abas)
    self.editor_frame = ttk.Frame(self.editor_output_paned)
    self.editor_output_paned.add(self.editor_frame, weight=3)
    
    # Criar sistema de abas
    self.tabs = EditorTabs(self.editor_frame, self)
    self.tabs.pack(fill=tk.BOTH, expand=True)
    
    # Criar uma primeira aba vazia
    tab_frame, editor = self.tabs.add_tab()
    
    # Define as referências iniciais para compatibilidade
    self.text_editor = editor
    self.line_numbers = self.tabs.tabs[str(tab_frame)]['line_numbers']
    
    # Área de saída
    output_frame = ttk.Frame(self.editor_output_paned)
    self.editor_output_paned.add(output_frame, weight=1)
    
    # Título da área de saída
    output_header = ttk.Frame(output_frame)
    output_header.pack(fill=tk.X)
    
    ttk.Label(output_header, text="Saída:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5, pady=2)
    
    # Botão de limpar saída
    ttk.Button(output_header, text="Limpar", command=self.clear_output).pack(side=tk.RIGHT, padx=5, pady=2)
    
    # Botão para interromper a execução (inicialmente não exibido)
    self.stop_button = ttk.Button(
        output_header,
        text="INTERROMPER",
        command=self.stop_execution,
        style='Stop.TButton'
    )
    
    # Botão grande e visível para executar script
    self.run_button = ttk.Button(
        output_header, 
        text="EXECUTAR SCRIPT", 
        command=self.run_script, 
        style='BigRun.TButton'
    )
    self.run_button.pack(side=tk.RIGHT, padx=10, pady=2)
    
    # Texto de saída com rolagem
    self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD,
                                               state=tk.DISABLED, height=8,
                                               font=("Consolas", 10),
                                               bg=self.colors['bg_text'],
                                               fg=self.colors['fg_text'])
    self.output_text.pack(fill=tk.BOTH, expand=True)
    
    # Configurar tags para estilizar o texto na área de saída
    self.output_text.tag_configure("input", foreground="#6495ED", font=("Consolas", 10, "bold"))
    self.output_text.tag_configure("prompt", foreground="#6A9955", font=("Consolas", 10, "bold"))
    self.output_text.tag_configure("error", foreground="#F14C4C")
    self.output_text.tag_configure("system", foreground="#C586C0", font=("Consolas", 10, "italic"))
    
    # Adicionar evento para capturar entrada de texto quando em modo REPL
    self.output_text.bind("<Return>", self._handle_repl_input)
    
    # Variáveis para controle de modo REPL
    self.repl_mode = False  # Indica se estamos em modo de espera por input
    self.input_start = "0.0"  # Marca o início da região de input atual
```

### 4. Adicionar Métodos para Manipulação de Arquivos

Adicione novos métodos e modifique os existentes para trabalhar com o sistema de abas:

```python
# Método atualizado para salvar um arquivo
def _save_to_file(self, file_path, editor=None):
    """Salva o conteúdo do editor no arquivo especificado"""
    try:
        # Se não for especificado um editor, usa o editor atual
        if editor is None:
            editor = self.text_editor
            
        with open(file_path, 'w', encoding='utf-8') as file:
            content = editor.get(1.0, tk.END)
            file.write(content)
        
        self.current_file = file_path
        self.current_file_name = os.path.basename(file_path)
        self.modified = False
        self.update_title()
        self.status_label.config(text=f"Arquivo salvo: {self.current_file_name}")
        
        # Notificar a atualização do explorador de projetos, se existir
        if hasattr(self, 'project_explorer'):
            self.project_explorer.refresh_tree()
            
        return True
    except Exception as e:
        messagebox.showerror("Erro ao salvar arquivo", str(e))
        return False

# Novo método para abrir um arquivo específico (chamado pelo explorador de projetos)
def open_specific_file(self, file_path):
    """Abre um arquivo específico no editor"""
    if not os.path.exists(file_path):
        messagebox.showerror("Erro", f"Arquivo não encontrado: {file_path}")
        return False
    
    try:
        # Verificar se o arquivo já está aberto em alguma aba
        for tab_id, tab_info in self.tabs.tabs.items():
            if tab_info['file'] == file_path:
                # Selecionar a aba correspondente
                tab_widget = self.tabs.nametowidget(tab_id)
                self.tabs.select(tab_widget)
                return True
        
        # Se chegou aqui, o arquivo não está aberto, então abre em uma nova aba
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Adicionar uma nova aba com o conteúdo do arquivo
        self.tabs.add_tab(file_path, content)
        
        self.status_label.config(text=f"Arquivo aberto: {os.path.basename(file_path)}")
        return True
        
    except Exception as e:
        messagebox.showerror("Erro ao abrir arquivo", str(e))
        return False

# Método modificado para open_file usar o sistema de abas
def open_file(self):
    """Abre um arquivo existente em uma nova aba"""
    file_path = filedialog.askopenfilename(
        defaultextension=".naja",
        filetypes=[("Arquivos NajaScript", "*.naja"), ("Todos os arquivos", "*.*")]
    )
    
    if file_path:
        return self.open_specific_file(file_path)
    
    return False

# Método modificado para new_file criar uma nova aba
def new_file(self):
    """Cria um novo arquivo em uma nova aba"""
    self.tabs.add_tab()
    self.status_label.config(text="Novo arquivo criado")
    return True

# Método modificado para save_file usar o sistema de abas
def save_file(self):
    """Salva o arquivo atual usando o sistema de abas"""
    return self.tabs.save_current_tab()

# Método modificado para save_file_as usar o sistema de abas
def save_file_as(self):
    """Salva o arquivo atual com um novo nome"""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".naja",
        filetypes=[("Arquivos NajaScript", "*.naja"), ("Todos os arquivos", "*.*")]
    )
    
    if file_path:
        current_tab = self.tabs.select()
        if current_tab:
            tab_info = self.tabs.tabs.get(str(current_tab))
            if tab_info:
                result = self._save_to_file(file_path, tab_info['editor'])
                if result:
                    # Atualizar informações da aba
                    tab_info['file'] = file_path
                    tab_info['modified'] = False
                    
                    # Atualizar o nome da aba
                    self.tabs.tab(current_tab, text=os.path.basename(file_path))
                    
                    return True
    return False
```

### 5. Métodos para Destaque de Sintaxe em Múltiplos Editores

Modifique os métodos de destaque de sintaxe para funcionar com múltiplos editores:

```python
# Método auxiliar para configurar o highlighting em cada editor
def setup_editor_highlighting(self, editor):
    """Configura o destaque de sintaxe para um editor específico"""
    editor.tag_configure("keyword", foreground=self.colors['fg_keyword'])
    editor.tag_configure("builtin", foreground=self.colors['fg_builtin'])
    editor.tag_configure("literal", foreground=self.colors['fg_literal'])
    editor.tag_configure("comment", foreground=self.colors['fg_comment'], font=("Consolas", 11, "italic"))
    editor.tag_configure("string", foreground=self.colors['fg_string'])
    editor.tag_configure("number", foreground=self.colors['fg_number'])
    editor.tag_configure("module", foreground=self.colors['fg_module'])
    
    # Configurar o fundo do editor
    editor.config(bg=self.colors['bg_text'], fg=self.colors['fg_text'], 
                insertbackground=self.colors['fg_text'],
                selectbackground=self.colors['selection_bg'])

# Método modificado para atualizar a sintaxe em um editor específico
def update_syntax(self, event=None, editor=None):
    """Atualiza o destaque de sintaxe quando o texto é modificado"""
    # Se não for especificado um editor, usa o editor atual
    if editor is None:
        editor = self.text_editor
        
    # Remove todas as tags existentes
    for tag in ["keyword", "builtin", "literal", "comment", "string", "number", "module"]:
        editor.tag_remove(tag, "1.0", "end")
    
    # Aplicar destaque de sintaxe
    for pattern, tag in self.patterns:
        self.highlight_pattern(pattern, tag, editor)

def highlight_pattern(self, pattern, tag, editor=None):
    """Aplica um padrão de destaque de sintaxe ao texto"""
    # Se não for especificado um editor, usa o editor atual
    if editor is None:
        editor = self.text_editor
        
    content = editor.get("1.0", "end-1c")
    
    # Encontra todas as ocorrências do padrão
    for match in re.finditer(pattern, content, re.MULTILINE):
        start_index = "1.0 + %dc" % match.start()
        end_index = "1.0 + %dc" % match.end()
        editor.tag_add(tag, start_index, end_index)
```

## Conclusão

Implementando estas melhorias, você transformará o NajaScript Editor em uma IDE mais moderna e funcional, oferecendo uma experiência de usuário muito melhor para os desenvolvedores NajaScript.

A implementação completa pode ser feita diretamente no arquivo `naja_editor.py` ou criando uma nova versão baseada nele chamada `naja_editor_melhorado.py`. 