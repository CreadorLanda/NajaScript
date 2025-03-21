#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para executar o Editor NajaScript com melhorias visuais e funcionais.
Este script carrega o editor existente e aplica modificações visuais para criar
uma experiência similar ao IntelliJ IDEA, com tema escuro e interface moderna.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from importlib.util import spec_from_file_location, module_from_spec
import re

# Verificar se o arquivo original do editor existe
EDITOR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "naja_editor.py")
if not os.path.exists(EDITOR_PATH):
    messagebox.showerror(
        "Erro", 
        "Arquivo naja_editor.py não encontrado. Verifique se você está no diretório correto."
    )
    sys.exit(1)

# Importar o módulo original do editor de forma dinâmica
try:
    spec = spec_from_file_location("naja_editor", EDITOR_PATH)
    editor_module = module_from_spec(spec)
    spec.loader.exec_module(editor_module)
except Exception as e:
    messagebox.showerror("Erro ao carregar o editor", str(e))
    sys.exit(1)

# Classes para as novas funcionalidades
class ProjectExplorer(ttk.Frame):
    """Implementa o explorador de projetos para o editor NajaScript."""
    
    def __init__(self, parent, editor):
        super().__init__(parent)
        self.editor = editor
        
        # Título do explorador
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(header_frame, text="Explorador de Projetos", 
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT)
                 
        # Botão para atualizar a árvore
        ttk.Button(header_frame, text="↻", width=3, 
                  command=self.refresh_tree).pack(side=tk.RIGHT)
        
        # Árvore de arquivos
        self.tree = ttk.Treeview(self, selectmode="browse", show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar para a árvore
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Configurar evento de clique duplo para abrir arquivos
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # Configurar menu de contexto
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Abrir", command=self.open_selected)
        self.context_menu.add_command(label="Renomear", command=self.rename_selected)
        self.context_menu.add_command(label="Excluir", command=self.delete_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Novo Arquivo", command=self.new_file)
        self.context_menu.add_command(label="Nova Pasta", command=self.new_directory)
        
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # Diretório atual
        self.current_directory = os.getcwd()
        
        # Popular a árvore inicialmente
        self.populate_tree()
    
    def populate_tree(self):
        """Popula a árvore com os arquivos e diretórios do diretório atual."""
        # Limpar a árvore existente
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar diretório raiz
        root = self.tree.insert("", "end", text=os.path.basename(self.current_directory), 
                               open=True, values=(self.current_directory,))
        
        # Função recursiva para adicionar diretórios e arquivos
        self._populate_directory(root, self.current_directory)
    
    def _populate_directory(self, parent, path):
        """Popula recursivamente os diretórios e arquivos."""
        try:
            # Ordenar para diretórios aparecerem primeiro, depois arquivos
            items = os.listdir(path)
            dirs = []
            files = []
            
            for item in items:
                if item.startswith('.'):  # Ignorar arquivos ocultos
                    continue
                    
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    dirs.append((item, full_path))
                else:
                    files.append((item, full_path))
            
            # Adicionar diretórios
            for item, full_path in sorted(dirs):
                dir_item = self.tree.insert(parent, "end", text=item, values=(full_path,))
                self._populate_directory(dir_item, full_path)
            
            # Adicionar arquivos (apenas arquivos NajaScript ou Python)
            for item, full_path in sorted(files):
                if item.endswith(('.naja', '.py')):
                    self.tree.insert(parent, "end", text=item, values=(full_path,))
        
        except Exception as e:
            print(f"Erro ao popular diretório {path}: {e}")
    
    def refresh_tree(self):
        """Atualiza a árvore de arquivos."""
        self.populate_tree()
    
    def on_item_double_click(self, event):
        """Manipula o evento de clique duplo em um item da árvore."""
        item = self.tree.focus()
        if item:
            file_path = self.tree.item(item, "values")[0]
            if os.path.isfile(file_path):
                self.editor.open_specific_file(file_path)
    
    def show_context_menu(self, event):
        """Exibe o menu de contexto."""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def open_selected(self):
        """Abre o arquivo selecionado."""
        item = self.tree.focus()
        if item:
            file_path = self.tree.item(item, "values")[0]
            if os.path.isfile(file_path):
                self.editor.open_specific_file(file_path)
    
    def rename_selected(self):
        """Renomeia o arquivo ou diretório selecionado."""
        # Esta funcionalidade pode ser implementada posteriormente
        pass
    
    def delete_selected(self):
        """Exclui o arquivo ou diretório selecionado."""
        # Esta funcionalidade pode ser implementada posteriormente
        pass
    
    def new_file(self):
        """Cria um novo arquivo."""
        # Esta funcionalidade pode ser implementada posteriormente
        pass
    
    def new_directory(self):
        """Cria um novo diretório."""
        # Esta funcionalidade pode ser implementada posteriormente
        pass

class EditorTabs(ttk.Notebook):
    """Implementa o sistema de abas para o editor NajaScript."""
    
    def __init__(self, parent, editor):
        super().__init__(parent)
        self.editor = editor
        
        # Dicionário para armazenar informações sobre as abas
        # {tab_id: {'editor': widget, 'line_numbers': widget, 'file': path, 'modified': bool}}
        self.tabs = {}
        
        # Configurar evento para detectar mudança de aba
        self.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        
        # Configurar menu de contexto
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Fechar", command=self._close_current_tab)
        self.context_menu.add_command(label="Fechar Outros", command=self._close_other_tabs)
        self.context_menu.add_command(label="Fechar Todos", command=self._close_all_tabs)
        
        self.bind("<Button-3>", self._show_context_menu)
    
    def add_tab(self, file_path=None, content=None):
        """Adiciona uma nova aba ao editor."""
        # Criar frame para a aba
        tab_frame = ttk.Frame(self)
        
        # Criar painel para o editor e números de linha
        editor_frame = ttk.Frame(tab_frame)
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # Criar widget para números de linha
        line_numbers = tk.Text(editor_frame, width=4, padx=4, 
                              bg=self.editor.colors['line_numbers_bg'],
                              fg=self.editor.colors['line_numbers_fg'],
                              font=self.editor.font,
                              state=tk.DISABLED,
                              takefocus=0,
                              cursor="arrow",
                              relief=tk.FLAT,
                              borderwidth=0)
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Criar editor de texto com fonte monospaced para programação
        text_editor = tk.Text(editor_frame, 
                             wrap=tk.NONE,
                             font=self.editor.font,
                             undo=True,
                             maxundo=0,
                             bg=self.editor.colors['bg_text'],
                             fg=self.editor.colors['fg_text'],
                             insertbackground=self.editor.colors['fg_text'],
                             selectbackground=self.editor.colors['selection_bg'],
                             relief=tk.FLAT,
                             borderwidth=0,
                             padx=5,
                             pady=3)
        text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Adicionar scrollbars com estilo moderno
        y_scrollbar = ttk.Scrollbar(editor_frame, orient=tk.VERTICAL, 
                                  command=text_editor.yview,
                                  style="Vertical.TScrollbar")
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_editor.configure(yscrollcommand=y_scrollbar.set)
        
        x_scrollbar = ttk.Scrollbar(tab_frame, orient=tk.HORIZONTAL, 
                                  command=text_editor.xview,
                                  style="Horizontal.TScrollbar")
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        text_editor.configure(xscrollcommand=x_scrollbar.set)
        
        # Adicionar aba ao notebook
        tab_name = os.path.basename(file_path) if file_path else "Novo Arquivo"
        self.add(tab_frame, text=tab_name)
        
        # Configurar destaque de sintaxe para o editor
        self.editor.setup_editor_highlighting(text_editor)
        
        # Adicionar eventos para atualizar sintaxe e números de linha
        text_editor.bind("<KeyRelease>", lambda e: self.editor.update_syntax(e, text_editor))
        text_editor.bind("<KeyRelease>", lambda e: self._update_line_numbers(tab_frame), add="+")
        
        # Adicionar evento para destacar a linha atual
        text_editor.bind("<KeyRelease>", lambda e: self.editor._highlight_current_line(text_editor), add="+")
        text_editor.bind("<Button-1>", lambda e: self.editor._highlight_current_line(text_editor), add="+")
        
        # Adicionar evento para autocompletar
        text_editor.bind("<KeyRelease>", lambda e: self.editor._show_autocomplete(e, text_editor), add="+")
        
        # Adicionar evento para detectar modificações
        text_editor.bind("<<Modified>>", lambda e: self._on_text_modified(tab_frame))
        
        # Armazenar informações da aba
        self.tabs[str(tab_frame)] = {
            'editor': text_editor,
            'line_numbers': line_numbers,
            'file': file_path,
            'modified': False
        }
        
        # Selecionar a nova aba
        self.select(tab_frame)
        
        # Se houver conteúdo, inseri-lo no editor
        if content:
            text_editor.insert(1.0, content)
            text_editor.edit_reset()  # Resetar o estado de modificação
            
        # Atualizar números de linha
        self._update_line_numbers(tab_frame)
        
        # Aplicar destaque de sintaxe
        self.editor.update_syntax(editor=text_editor)
        
        # Destacar a linha atual
        self.editor._highlight_current_line(text_editor)
        
        # Focar no editor
        text_editor.focus_set()
        
        return tab_frame, text_editor
    
    def _update_line_numbers(self, tab_frame):
        """Atualiza os números de linha para a aba especificada."""
        tab_info = self.tabs.get(str(tab_frame))
        if not tab_info:
            return
            
        editor = tab_info['editor']
        line_numbers = tab_info['line_numbers']
        
        # Calcular número total de linhas
        total_lines = editor.index(tk.END).split('.')[0]
        
        # Habilitar edição dos números de linha
        line_numbers.config(state=tk.NORMAL)
        line_numbers.delete(1.0, tk.END)
        
        # Adicionar números de linha
        for i in range(1, int(total_lines)):
            line_numbers.insert(tk.END, f"{i}\n")
            
        # Desabilitar edição dos números de linha
        line_numbers.config(state=tk.DISABLED)
    
    def _on_tab_changed(self, event):
        """Manipula o evento de mudança de aba."""
        current = self.select()
        if current:
            tab_info = self.tabs.get(str(current))
            if tab_info:
                # Atualizar referências no editor principal para retro-compatibilidade
                self.editor.text_editor = tab_info['editor']
                self.editor.line_numbers = tab_info['line_numbers']
                
                # Atualizar o título da janela
                self.editor.current_file = tab_info['file']
                self.editor.current_file_name = os.path.basename(tab_info['file']) if tab_info['file'] else "Novo Arquivo"
                self.editor.modified = tab_info['modified']
                self.editor.update_title()
                
                # Focar no editor
                tab_info['editor'].focus_set()
    
    def _on_text_modified(self, tab_frame):
        """Manipula o evento de modificação de texto."""
        tab_info = self.tabs.get(str(tab_frame))
        if not tab_info:
            return
            
        editor = tab_info['editor']
        
        # Verificar se o texto foi modificado
        if editor.edit_modified():
            # Marcar como modificado se ainda não estiver
            if not tab_info['modified']:
                tab_info['modified'] = True
                
                # Adicionar indicador de modificação ao título da aba
                current_text = self.tab(tab_frame, "text")
                if not current_text.startswith("*"):
                    self.tab(tab_frame, text=f"*{current_text}")
                    
                # Atualizar o estado modificado no editor principal se esta for a aba atual
                if str(self.select()) == str(tab_frame):
                    self.editor.modified = True
                    self.editor.update_title()
                    
            # Resetar o sinalizador de modificação
            editor.edit_modified(False)
    
    def _close_current_tab(self):
        """Fecha a aba atual."""
        current = self.select()
        if current and len(self.tabs) > 1:  # Garantir que sempre haja pelo menos uma aba
            # Verificar se há modificações não salvas
            tab_info = self.tabs.get(str(current))
            if tab_info and tab_info['modified']:
                # Perguntar se deseja salvar as alterações
                response = messagebox.askyesnocancel(
                    "Salvar alterações",
                    f"Deseja salvar as alterações em {self.tab(current, 'text').lstrip('*')}?"
                )
                
                if response is None:  # Cancelar
                    return
                elif response:  # Sim
                    # Tentar salvar o arquivo
                    if not self._save_tab(current):
                        return  # Cancelar o fechamento se o salvamento falhar
            
            # Remover a aba do dicionário
            del self.tabs[str(current)]
            
            # Remover a aba do notebook
            self.forget(current)
    
    def _close_other_tabs(self):
        """Fecha todas as abas exceto a atual."""
        current = self.select()
        if current:
            tabs_to_close = [tab for tab in self.tabs if tab != str(current)]
            for tab in tabs_to_close:
                tab_widget = self.nametowidget(tab)
                
                # Verificar se há modificações não salvas
                tab_info = self.tabs.get(tab)
                if tab_info and tab_info['modified']:
                    # Selecionar a aba para mostrar ao usuário
                    self.select(tab_widget)
                    
                    # Perguntar se deseja salvar as alterações
                    response = messagebox.askyesnocancel(
                        "Salvar alterações",
                        f"Deseja salvar as alterações em {self.tab(tab_widget, 'text').lstrip('*')}?"
                    )
                    
                    if response is None:  # Cancelar
                        continue
                    elif response:  # Sim
                        # Tentar salvar o arquivo
                        if not self._save_tab(tab_widget):
                            continue  # Pular para a próxima aba se o salvamento falhar
                
                # Remover a aba do dicionário
                del self.tabs[tab]
                
                # Remover a aba do notebook
                self.forget(tab_widget)
            
            # Selecionar a aba atual
            self.select(current)
    
    def _close_all_tabs(self):
        """Fecha todas as abas e cria uma nova em branco."""
        # Verificar cada aba por modificações não salvas
        for tab, tab_info in list(self.tabs.items()):
            if tab_info['modified']:
                # Selecionar a aba para mostrar ao usuário
                tab_widget = self.nametowidget(tab)
                self.select(tab_widget)
                
                # Perguntar se deseja salvar as alterações
                response = messagebox.askyesnocancel(
                    "Salvar alterações",
                    f"Deseja salvar as alterações em {self.tab(tab_widget, 'text').lstrip('*')}?"
                )
                
                if response is None:  # Cancelar
                    return
                elif response:  # Sim
                    # Tentar salvar o arquivo
                    if not self._save_tab(tab_widget):
                        return  # Cancelar o fechamento se o salvamento falhar
        
        # Remover todas as abas
        for tab in list(self.tabs.keys()):
            tab_widget = self.nametowidget(tab)
            self.forget(tab_widget)
        
        # Limpar o dicionário de abas
        self.tabs.clear()
        
        # Criar uma nova aba em branco
        self.add_tab()
    
    def _save_tab(self, tab_widget):
        """Salva o conteúdo da aba especificada."""
        tab_info = self.tabs.get(str(tab_widget))
        if not tab_info:
            return False
            
        file_path = tab_info['file']
        
        # Se o arquivo já tem um caminho, salvar diretamente
        if file_path:
            return self.editor._save_to_file(file_path, tab_info['editor'])
        else:
            # Caso contrário, solicitar um caminho
            new_path = self.editor._ask_save_file_path()
            if new_path:
                result = self.editor._save_to_file(new_path, tab_info['editor'])
                if result:
                    # Atualizar informações da aba
                    tab_info['file'] = new_path
                    tab_info['modified'] = False
                    
                    # Atualizar o nome da aba
                    self.tab(tab_widget, text=os.path.basename(new_path))
                    
                    return True
            return False
    
    def _show_context_menu(self, event):
        """Exibe o menu de contexto para as abas."""
        self.context_menu.post(event.x_root, event.y_root)
    
    def save_current_tab(self):
        """Salva a aba atual."""
        current = self.select()
        if current:
            return self._save_tab(current)
        return False


# Modificar a classe NajaScriptEditor para aplicar melhorias
class NajaScriptEditorMelhorado(editor_module.NajaScriptEditor):
    """Versão melhorada do Editor NajaScript com tema escuro e layout moderno."""
    
    def __init__(self, root):
        # Atribuir a raiz
        self.root = root
        
        # Outras inicializações básicas
        self.current_file = None
        self.current_file_name = "Novo Arquivo"
        self.modified = False
        self.font = ("Fira Code", 11)  # Fonte melhor para programação
        
        # Padrões de destaque de sintaxe (inicializado antecipadamente)
        self.patterns = []
        
        # Inicializar variáveis de processo
        self.process = None
        self.process_running = False
        
        # Configurar o estilo visual
        self.configure_style()
        
        # Criar os componentes da interface na ordem correta
        self.create_status_bar()  # Status bar antes para estar disponível
        self.create_menu()        # Menu precisa ser criado antes dos outros componentes
        self.create_toolbar()     # Toolbar após o menu
        self.create_main_area()   # Área principal com editor e saída
        
        # Configurar eventos e atalhos
        self.bind_events()
        self.setup_keyboard_shortcuts()
        
        # Configurar destaque de sintaxe
        self.setup_syntax_highlighting()
        
        # Dicionário para autocompletar
        self.setup_autocompletion()
        
        # Mensagem de boas-vindas
        welcome_msg = """Bem-vindo ao Editor NajaScript Melhorado!
        
Esta versão do editor inclui:
- Tema escuro inspirado no VS Code
- Sistema de abas para editar múltiplos arquivos
- Explorador de projetos
- Destaque de sintaxe aprimorado com cores diferenciadas
- Autocomplete para palavras-chave NajaScript
- Realce da linha atual e linhas de indentação
        
Para começar, use o menu Arquivo para abrir um código existente
ou crie um novo arquivo."""
        
        # Atualizar título
        self.update_title()
        
        # Inserir mensagem de boas-vindas depois que o editor estiver pronto
        if hasattr(self, 'text_editor'):
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(1.0, welcome_msg.strip())
            self.text_editor.edit_reset()  # Resetar o estado de modificação
    
    def configure_style(self):
        """Configura o estilo visual do editor para um tema moderno"""
        style = ttk.Style()
        style.theme_use('clam')  # Pode ser 'clam', 'alt', 'default', 'classic'
        
        # Configuração de cores para tema dark+ do VSCode - cores mais diferenciadas
        self.colors = {
            # Cores base
            'bg_main': '#1e1e1e',             # Fundo principal (padrão VSCode)
            'bg_panel': '#252526',            # Fundo de painéis (VSCode)
            'bg_text': '#1e1e1e',             # Fundo de área de texto
            'bg_current_line': '#2d2d2d',     # Cor da linha atual
            'fg_text': '#d4d4d4',             # Texto normal
            'selection_bg': '#264f78',        # Fundo da seleção
            
            # Cores para tipos de sintaxe (muito mais categorias)
            'fg_keyword': '#569cd6',          # Palavras-chave (azul - var, const)
            'fg_control': '#c586c0',          # Estruturas de controle (roxo - se, senao)
            'fg_loop': '#d7ba7d',             # Estruturas de loop (amarelo - para, enquanto)
            'fg_conditional': '#c586c0',      # Condicionais (roxo - se, senao)
            'fg_exception': '#f44747',        # Exceções (vermelho - tente, capture)
            'fg_builtin': '#4ec9b0',          # Funções integradas (verde-água)
            'fg_string': '#ce9178',           # Strings (laranja claro)
            'fg_number': '#b5cea8',           # Números (verde claro)
            'fg_comment': '#6a9955',          # Comentários (verde médio)
            'fg_module': '#dcdcaa',           # Módulos e funções (amarelo)
            'fg_literal': '#569cd6',          # Literais (azul - verdadeiro, falso)
            'fg_class': '#4ec9b0',            # Nomes de classes (verde-água)
            'fg_function': '#dcdcaa',         # Declarações de função (amarelo)
            'fg_import': '#9cdcfe',           # Importações (azul claro)
            'fg_operator': '#d4d4d4',         # Operadores (branco)
            'fg_brackets': '#d4d4d4',         # Parênteses/colchetes (branco)
            'fg_decorator': '#c586c0',        # Decoradores (roxo)
            
            # Cores de interface
            'line_numbers_bg': '#1e1e1e',     # Fundo dos números de linha
            'line_numbers_fg': '#858585',     # Cor dos números de linha
            'indent_guide': '#404040',        # Linhas de indentação
            'matching_bracket': '#6c6c6c',    # Parênteses correspondentes
            'search_result': '#515c6a',       # Destaque para resultados de busca
            'toolbar_bg': '#333333',          # Fundo da barra de ferramentas
            'tab_active': '#1e1e1e',          # Aba ativa
            'tab_inactive': '#2d2d2d',        # Aba inativa
            'status_bar_bg': '#007acc',       # Barra de status (azul VSCode)
            'status_bar_fg': '#ffffff',       # Texto da barra de status
            'button_bg': '#0e639c',           # Fundo dos botões (azul mais forte)
            'button_fg': '#ffffff',           # Texto dos botões (branco)
            'error_color': '#f48771',         # Cor para erros (vermelho VSCode)
            'warning_color': '#cca700',       # Cor para avisos (amarelo VSCode)
            'info_color': '#3794ff',          # Cor para informações (azul claro)
            'hint_color': '#008000',          # Cor para dicas (verde)
            'autocomplete_bg': '#252526',     # Fundo das sugestões de autocompletar 
            'autocomplete_fg': '#d4d4d4',     # Texto das sugestões
            'autocomplete_select_bg': '#062f4a',  # Fundo da seleção no autocompletar
            'scrollbar_bg': '#3e3e42',        # Fundo da barra de rolagem
            'scrollbar_fg': '#686868',        # Cor da barra de rolagem
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
                      background='#13a10e',  # Verde mais vibrante
                      foreground='white',
                      font=('Segoe UI', 9, 'bold'),
                      padding=5)
        
        # Botão grande de execução
        style.configure('BigRun.TButton',
                      background='#13a10e',  # Verde mais vibrante
                      foreground='white',
                      font=('Segoe UI', 12, 'bold'),
                      padding=8)
        
        # Botão de interrupção
        style.configure('Stop.TButton',
                      background='#c50f1f',  # Vermelho mais vibrante
                      foreground='white',
                      font=('Segoe UI', 12, 'bold'),
                      padding=8)
        
        # Botão de destaque para caixas de diálogo
        style.configure('Accent.TButton',
                      background='#0e639c',  # Azul mais forte
                      foreground='white',
                      font=('Segoe UI', 10, 'bold'),
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
        
        # Estilos para scrollbar melhorada
        style.configure("Vertical.TScrollbar", 
                      background=self.colors['scrollbar_bg'],
                      troughcolor=self.colors['bg_panel'],
                      borderwidth=0,
                      arrowsize=13)
        style.map("Vertical.TScrollbar",
                background=[("active", self.colors['scrollbar_fg']), 
                          ("!active", self.colors['scrollbar_bg'])])
                          
        style.configure("Horizontal.TScrollbar", 
                      background=self.colors['scrollbar_bg'],
                      troughcolor=self.colors['bg_panel'],
                      borderwidth=0,
                      arrowsize=13)
        style.map("Horizontal.TScrollbar",
                background=[("active", self.colors['scrollbar_fg']), 
                          ("!active", self.colors['scrollbar_bg'])])
        
        # Configurar a interface principal
        self.root.configure(background=self.colors['bg_main'])
        
        # Configurar o menu (apenas se existir)
        if hasattr(self, 'menu_bar'):
            self.menu_bar.config(bg=self.colors['bg_panel'], fg=self.colors['fg_text'])
        
        # Aplicar estilo à barra de status
        if hasattr(self, 'status_bar'):
            self.status_bar.config(bg=self.colors['status_bar_bg'])
            if hasattr(self, 'status_label'):
                self.status_label.config(bg=self.colors['status_bar_bg'], fg=self.colors['status_bar_fg'])
            if hasattr(self, 'position_label'):
                self.position_label.config(bg=self.colors['status_bar_bg'], fg=self.colors['status_bar_fg'])
    
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
        self.output_text = tk.scrolledtext.ScrolledText(output_frame, wrap=tk.WORD,
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
    
    # Métodos auxiliares para destaque de sintaxe
    def setup_editor_highlighting(self, editor):
        """Configura o destaque de sintaxe para um editor específico"""
        # Palavras-chave e construções da linguagem (muito mais categorias)
        editor.tag_configure("keyword", foreground=self.colors['fg_keyword'])
        editor.tag_configure("control", foreground=self.colors['fg_control'])
        editor.tag_configure("loop", foreground=self.colors['fg_loop'])
        editor.tag_configure("conditional", foreground=self.colors['fg_conditional'])
        editor.tag_configure("exception", foreground=self.colors['fg_exception'])
        editor.tag_configure("builtin", foreground=self.colors['fg_builtin'])
        editor.tag_configure("literal", foreground=self.colors['fg_literal'])
        editor.tag_configure("comment", foreground=self.colors['fg_comment'], font=(self.font[0], self.font[1], "italic"))
        editor.tag_configure("string", foreground=self.colors['fg_string'])
        editor.tag_configure("number", foreground=self.colors['fg_number'])
        editor.tag_configure("module", foreground=self.colors['fg_module'])
        editor.tag_configure("function", foreground=self.colors['fg_function'])
        editor.tag_configure("operator", foreground=self.colors['fg_operator'])
        editor.tag_configure("brackets", foreground=self.colors['fg_brackets'])
        editor.tag_configure("class", foreground=self.colors['fg_class'])
        editor.tag_configure("import", foreground=self.colors['fg_import'])
        editor.tag_configure("error", foreground=self.colors['error_color'], underline=True)
        
        # Tags para realce visual
        editor.tag_configure("current_line", background=self.colors['bg_current_line'])
        editor.tag_configure("matching_bracket", background=self.colors['matching_bracket'])
        
        # Configurar o fundo do editor e outras propriedades
        editor.config(
            bg=self.colors['bg_text'], 
            fg=self.colors['fg_text'], 
            insertbackground=self.colors['fg_text'],
            selectbackground=self.colors['selection_bg'],
            selectforeground=self.colors['fg_text'],
            insertwidth=2,  # Cursor mais largo
            insertofftime=500,  # Piscar mais lento
            insertontime=500,
            wrap=tk.NONE,
            relief=tk.FLAT,  # Borda plana para aparência moderna
            borderwidth=0,
            padx=5,  # Padding horizontal para não colar nas bordas
            pady=3   # Padding vertical para melhor espaçamento
        )
        
        # Adicionar eventos para o editor
        editor.bind("<KeyRelease>", lambda e: self._highlight_current_line(editor))
        editor.bind("<Button-1>", lambda e: self._highlight_current_line(editor))
        editor.bind("<Tab>", lambda e: self._handle_tab(e, editor))
        editor.bind("<KeyRelease>", lambda e: self._show_autocomplete(e, editor), add="+")
    
    # Método auxiliar para abrir arquivos específicos
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
    
    # Sobrescrever os métodos de manipulação de arquivos
    def open_file(self):
        """Abre um arquivo existente em uma nova aba"""
        file_path = tk.filedialog.askopenfilename(
            defaultextension=".naja",
            filetypes=[("Arquivos NajaScript", "*.naja"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            return self.open_specific_file(file_path)
        
        return False
    
    def new_file(self):
        """Cria um novo arquivo em uma nova aba"""
        self.tabs.add_tab()
        self.status_label.config(text="Novo arquivo criado")
        return True
    
    def save_file(self):
        """Salva o arquivo atual usando o sistema de abas"""
        return self.tabs.save_current_tab()
    
    def save_file_as(self):
        """Salva o arquivo atual com um novo nome."""
        file_path = self._ask_save_file_path()
        if file_path:
            return self._save_to_file(file_path)
        return False
    
    def _ask_save_file_path(self):
        """Solicita o caminho para salvar o arquivo."""
        return tk.filedialog.asksaveasfilename(
            defaultextension=".naja",
            filetypes=[("Arquivos NajaScript", "*.naja"), ("Todos os arquivos", "*.*")]
        )
    
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

    def create_menu(self):
        """Cria a barra de menu do editor"""
        self.menu_bar = tk.Menu(self.root, bg=self.colors['bg_panel'], fg=self.colors['fg_text'])
        self.root.config(menu=self.menu_bar)
        
        # Menu Arquivo
        file_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.colors['bg_panel'], 
                          fg=self.colors['fg_text'])
        file_menu.add_command(label="Novo", command=self.new_file, 
                            accelerator="Ctrl+N")
        file_menu.add_command(label="Abrir...", command=self.open_file, 
                            accelerator="Ctrl+O")
        file_menu.add_command(label="Salvar", command=self.save_file, 
                            accelerator="Ctrl+S")
        file_menu.add_command(label="Salvar como...", command=self.save_file_as, 
                            accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.exit_editor, 
                            accelerator="Alt+F4")
        self.menu_bar.add_cascade(label="Arquivo", menu=file_menu)
        
        # Menu Editar
        edit_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.colors['bg_panel'], 
                          fg=self.colors['fg_text'])
        edit_menu.add_command(label="Desfazer", command=self.undo, 
                            accelerator="Ctrl+Z")
        edit_menu.add_command(label="Refazer", command=self.redo, 
                            accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Recortar", command=self.cut, 
                            accelerator="Ctrl+X")
        edit_menu.add_command(label="Copiar", command=self.copy, 
                            accelerator="Ctrl+C")
        edit_menu.add_command(label="Colar", command=self.paste, 
                            accelerator="Ctrl+V")
        self.menu_bar.add_cascade(label="Editar", menu=edit_menu)
        
        # Menu Executar
        run_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.colors['bg_panel'], 
                         fg=self.colors['fg_text'])
        run_menu.add_command(label="Executar Script", command=self.run_script, 
                           accelerator="F5")
        self.menu_bar.add_cascade(label="Executar", menu=run_menu)
        
        # Menu Ajuda
        help_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.colors['bg_panel'], 
                          fg=self.colors['fg_text'])
        help_menu.add_command(label="Sobre", command=self.show_about)
        self.menu_bar.add_cascade(label="Ajuda", menu=help_menu)

    def create_toolbar(self):
        """Cria a barra de ferramentas do editor"""
        self.toolbar = ttk.Frame(self.root, style='Toolbar.TFrame')
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Botões da barra de ferramentas
        ttk.Button(self.toolbar, text="Novo", command=self.new_file).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(self.toolbar, text="Abrir", command=self.open_file).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(self.toolbar, text="Salvar", command=self.save_file).pack(side=tk.LEFT, padx=2, pady=2)
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, pady=2, fill=tk.Y)
        
        ttk.Button(self.toolbar, text="Executar", command=self.run_script, style='Run.TButton').pack(side=tk.LEFT, padx=2, pady=2)

    def create_status_bar(self):
        """Cria a barra de status do editor"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="Pronto", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)
        
        self.position_label = ttk.Label(self.status_bar, text="Lin: 1, Col: 1", anchor=tk.E)
        self.position_label.pack(side=tk.RIGHT, padx=5, pady=2)

    def bind_events(self):
        """Configura os eventos do editor"""
        # Adicionar vinculações de eventos conforme necessário
        self.root.protocol("WM_DELETE_WINDOW", self.exit_editor)

    def setup_keyboard_shortcuts(self):
        """Configura atalhos de teclado"""
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-Shift-s>", lambda e: self.save_file_as())
        self.root.bind("<F5>", lambda e: self.run_script())

    def setup_syntax_highlighting(self):
        """Configura os padrões de destaque de sintaxe com expressões regulares melhoradas"""
        # Palavras-chave de definição (var, const, funcao, etc.)
        keywords = r"\b(var|const|este|super|estatico|privado|publico|protegido)\b"
        
        # Declarações de função e classe
        function_declarations = r"\b(funcao|classe|retorna)\b"
        
        # Estruturas de controle específicas para cada tipo
        conditionals = r"\b(se|senao)\b"
        loops = r"\b(para|enquanto|repetir|ate|fazer)\b"
        exceptions = r"\b(tente|capture|finalmente|lance)\b"
        other_control = r"\b(quebrar|continuar|retornar)\b"
        
        # Importações e exportações
        imports = r"\b(importar|exportar|de|como|implementa|estende)\b"
        
        # Funções e métodos integrados (mais organizados por tipo)
        builtins_io = r"\b(imprimir|entrada)\b"
        builtins_conversion = r"\b(inteiro|decimal|texto|booleano|converter|tipo)\b"
        builtins_collection = r"\b(lista|dicionario|conjunto|comprimento|obterChaves|obterValores)\b"
        builtins_string = r"\b(adicionar|remover|ordenar|inverte|junta|divideTexto|maiusculo|minusculo)\b"
        
        # Literais e constantes
        literals = r"\b(verdadeiro|falso|nulo)\b"
        
        # Classes e interfaces (sem usar lookbehind de tamanho variável)
        classes = r"\bclasse\s+([A-Za-z_][A-Za-z0-9_]*)\b"
        
        # Funções - captura nome após a palavra "funcao"
        functions = r"\bfuncao\s+([A-Za-z_][A-Za-z0-9_]*)\b"
        
        # Operadores aritméticos, lógicos e de atribuição
        operators = r"(\+|\-|\*|\/|\%|\=|\+=|\-=|\*=|\/=|\%=|\=\=|\!\=|\<|\>|\<=|\>=|\&\&|\|\||\!)"
        
        # Parênteses, colchetes e chaves
        brackets = r"(\(|\)|\[|\]|\{|\})"
        
        # Outros padrões de sintaxe
        self.patterns = [
            (keywords, "keyword"),
            (function_declarations, "function"),
            (conditionals, "conditional"),
            (loops, "loop"),
            (exceptions, "exception"),
            (other_control, "control"),
            (imports, "import"),
            (builtins_io, "builtin"),
            (builtins_conversion, "builtin"),
            (builtins_collection, "builtin"),
            (builtins_string, "builtin"),
            (literals, "literal"),
            (classes, "class"),
            (functions, "function"),
            (r"#.*$", "comment"),
            (r'"[^"]*"', "string"),
            (r'\'[^\']*\'', "string"),
            (r"\b\d+(\.\d+)?\b", "number"),  # Inteiros e decimais
            (operators, "operator"),
            (brackets, "brackets"),
            (r"\b[A-Za-z_][A-Za-z0-9_]*\b", "module"),  # Identificadores
        ]
        
        # Palavras-chave para autocompletar (organizadas por categoria para o menu)
        self.autocomplete_words = {
            "Declarações": ["var", "const", "funcao", "classe", "retorna"],
            "Estruturas de Controle": ["se", "senao", "para", "enquanto", "repetir", "ate", "fazer", 
                                     "tente", "capture", "finalmente", "lance", 
                                     "quebrar", "continuar", "retornar"],
            "Módulos": ["importar", "exportar", "de", "como", "implementa", "estende"],
            "Funções I/O": ["imprimir", "entrada"],
            "Conversões": ["inteiro", "decimal", "texto", "booleano", "converter", "tipo"],
            "Coleções": ["lista", "dicionario", "conjunto", "comprimento", "obterChaves", "obterValores"],
            "Métodos String": ["adicionar", "remover", "ordenar", "inverte", "junta", "divideTexto", 
                             "maiusculo", "minusculo"],
            "Constantes": ["verdadeiro", "falso", "nulo"],
            "Orientação a Objetos": ["este", "super", "estatico", "privado", "publico", "protegido"]
        }
        
        # Lista plana de todas as palavras para autocompletar
        self.all_autocomplete_words = []
        for category, words in self.autocomplete_words.items():
            self.all_autocomplete_words.extend(words)

    def update_title(self):
        """Atualiza o título da janela"""
        if self.current_file:
            title = f"{self.current_file_name} - NajaScript Editor"
            if self.modified:
                title = f"*{title}"
        else:
            title = "NajaScript Editor - Versão Melhorada"
            if self.modified:
                title = f"*{self.current_file_name} - {title}"
        self.root.title(title)

    def exit_editor(self):
        """Fecha o editor"""
        # Verificar arquivos não salvos antes de fechar
        if self.modified:
            response = messagebox.askyesnocancel(
                "Arquivo não salvo",
                "Deseja salvar as alterações antes de sair?"
            )
            
            if response is None:  # Cancelar
                return
            elif response:  # Sim
                if not self.save_file():
                    return
        
        self.root.destroy()

    def undo(self):
        """Desfaz a última operação de edição"""
        if hasattr(self, 'text_editor') and self.text_editor:
            try:
                self.text_editor.edit_undo()
            except:
                pass

    def redo(self):
        """Refaz a última operação desfeita"""
        if hasattr(self, 'text_editor') and self.text_editor:
            try:
                self.text_editor.edit_redo()
            except:
                pass

    def cut(self):
        """Recorta o texto selecionado"""
        if hasattr(self, 'text_editor') and self.text_editor:
            self.text_editor.event_generate("<<Cut>>")

    def copy(self):
        """Copia o texto selecionado"""
        if hasattr(self, 'text_editor') and self.text_editor:
            self.text_editor.event_generate("<<Copy>>")

    def paste(self):
        """Cola o texto da área de transferência"""
        if hasattr(self, 'text_editor') and self.text_editor:
            self.text_editor.event_generate("<<Paste>>")

    def show_about(self):
        """Exibe informações sobre o editor"""
        messagebox.showinfo(
            "Sobre o NajaScript Editor",
            "NajaScript Editor - Versão Melhorada\n\n"
            "Um editor moderno para a linguagem NajaScript\n"
            "Inspirado no IntelliJ IDEA\n\n"
            "© 2023 Equipe NajaScript"
        )

    def clear_output(self):
        """Limpa a área de saída"""
        if hasattr(self, 'output_text') and self.output_text:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.config(state=tk.DISABLED)

    def add_output(self, text, tag=None):
        """Adiciona texto à área de saída"""
        if hasattr(self, 'output_text') and self.output_text:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, text, tag if tag else "")
            self.output_text.see(tk.END)
            self.output_text.config(state=tk.DISABLED)

    def run_script(self):
        """Executa o script atual usando o interpretador NajaScript"""
        if not hasattr(self, 'text_editor') or not self.text_editor:
            return
        
        # Verificar se o arquivo foi modificado e perguntar se deseja salvar
        if self.modified:
            response = messagebox.askyesnocancel(
                "Arquivo não salvo",
                "Deseja salvar as alterações antes de executar?"
            )
            
            if response is None:  # Cancelar
                return
            elif response:  # Sim
                if not self.save_file():
                    return
        
        # Limpar a área de saída
        self.clear_output()
        
        # Preparar para execução
        self.add_output("=== Executando script NajaScript ===\n", "system")
        
        script_file = None
        temp_file = None
        
        try:
            # Determinar qual arquivo executar
            if self.current_file and os.path.exists(self.current_file):
                # Usar o arquivo atual se já estiver salvo
                script_file = self.current_file
                self.add_output(f"Arquivo: {os.path.basename(script_file)}\n", "info")
            else:
                # Criar um arquivo temporário
                import tempfile
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.naja', mode='w', encoding='utf-8')
                content = self.text_editor.get(1.0, tk.END)
                temp_file.write(content)
                temp_file.close()
                script_file = temp_file.name
                self.add_output("Executando código temporário...\n", "info")
            
            # Adicionar botão de interrupção
            if hasattr(self, 'stop_button') and not self.stop_button.winfo_ismapped():
                self.stop_button.pack(side=tk.RIGHT, padx=5, pady=2)
                self.run_button.pack_forget()  # Esconder o botão de execução
            
            # Verificar se o interpretador najascript.py existe
            najascript_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "najascript.py")
            if not os.path.exists(najascript_path):
                # Se o interpretador não existe, mostrar mensagem simulada para testes
                self.add_output("Nota: Interpretador najascript.py não encontrado. Simulando execução para fins de demonstração.\n", "system")
                self.add_output("Olá, NajaScript!\n")
                self.add_output("Bem-vindo ao NajaScript versão 1.0\n")
                self.add_output("Contagem: 0\n")
                self.add_output("Contagem: 1\n")
                self.add_output("Contagem: 2\n")
                self.add_output("Contagem: 3\n")
                self.add_output("Contagem: 4\n")
                self.add_output("\nLista de frutas:\n")
                self.add_output("0: maçã\n")
                self.add_output("1: banana\n")
                self.add_output("2: laranja\n")
                self.add_output("3: uva\n")
                self.add_output("\nInformações da pessoa:\n")
                self.add_output("nome: Maria\n")
                self.add_output("idade: 30\n")
                self.add_output("cidade: São Paulo\n")
                self.add_output("\nTestando tratamento de exceções:\n")
                self.add_output("Ocorreu um erro: Divisão por zero\n", "error")
                self.add_output("\nFim do programa!\n")
                
                # Simular um processo terminado
                self.root.after(1000, self.process_complete)
                return
            
            # Configurar o processo
            import subprocess, threading, queue
            
            # Criar filas para comunicação entre threads
            output_queue = queue.Queue()
            error_queue = queue.Queue()
            
            # Flag para controlar se o processo ainda está em execução
            self.process_running = True
            
            # Iniciar o processo
            self.process = subprocess.Popen(
                ["python", najascript_path, script_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Funções para ler saída e erro em threads separadas
            def read_output():
                try:
                    for line in iter(self.process.stdout.readline, ''):
                        if line:
                            output_queue.put(("output", line))
                        if not self.process_running:
                            break
                except ValueError:  # Arquivo fechado
                    pass
                except Exception as e:
                    print(f"Erro ao ler saída: {e}")
            
            def read_error():
                try:
                    for line in iter(self.process.stderr.readline, ''):
                        if line:
                            error_queue.put(("error", line))
                        if not self.process_running:
                            break
                except ValueError:  # Arquivo fechado
                    pass
                except Exception as e:
                    print(f"Erro ao ler erro: {e}")
            
            # Função para processar as filas de saída e atualizar a UI
            def update_output():
                if not self.process_running:
                    return  # Sair se o processo não estiver mais em execução
                    
                # Processar saída padrão
                try:
                    while not output_queue.empty():
                        msg_type, msg = output_queue.get_nowait()
                        self.add_output(msg, None)
                        output_queue.task_done()
                except queue.Empty:
                    pass
                
                # Processar saída de erro
                try:
                    while not error_queue.empty():
                        msg_type, msg = error_queue.get_nowait()
                        self.add_output(msg, "error")
                        error_queue.task_done()
                except queue.Empty:
                    pass
                
                # Verificar se o processo ainda está em execução
                if self.process_running and self.process and self.process.poll() is None:
                    # Ainda em execução, agendar nova verificação
                    self.root.after(100, update_output)
                elif self.process_running and self.process:
                    # Processo terminou
                    self.process_running = False
                    
                    # Capturar qualquer saída final
                    try:
                        remaining_out, remaining_err = self.process.communicate(timeout=1)
                        if remaining_out:
                            self.add_output(remaining_out, None)
                        if remaining_err:
                            self.add_output(remaining_err, "error")
                        
                        # Mostrar código de saída
                        exit_code = self.process.returncode
                        if exit_code == 0:
                            self.add_output(f"\n=== Script finalizado com sucesso (código de saída: {exit_code}) ===\n", "system")
                        else:
                            self.add_output(f"\n=== Script finalizado com erros (código de saída: {exit_code}) ===\n", "error")
                    except Exception as e:
                        self.add_output(f"\nErro ao finalizar processo: {str(e)}\n", "error")
                    
                    # Chamar a função de finalização
                    self.process_complete()
            
            # Iniciar threads de leitura
            output_thread = threading.Thread(target=read_output, daemon=True)
            error_thread = threading.Thread(target=read_error, daemon=True)
            output_thread.start()
            error_thread.start()
            
            # Iniciar processamento da saída
            update_output()
            
        except Exception as e:
            self.add_output(f"Erro ao executar script: {str(e)}\n", "error")
            self.process_running = False
            self.process_complete()
        finally:
            # Limpar arquivos temporários se necessário
            if temp_file and os.path.exists(temp_file.name):
                try:
                    os.unlink(temp_file.name)
                except:
                    pass

    def process_complete(self):
        """Método chamado quando o processo de execução termina"""
        # Restaurar a interface
        if hasattr(self, 'stop_button') and self.stop_button.winfo_ismapped():
            self.stop_button.pack_forget()
        
        if hasattr(self, 'run_button') and not self.run_button.winfo_ismapped():
            self.run_button.pack(side=tk.RIGHT, padx=10, pady=2)
        
        # Garantir que o processo está encerrado
        if hasattr(self, 'process') and self.process:
            try:
                if self.process.poll() is None:
                    self.process.terminate()
                    self.process.wait(timeout=1)
            except:
                pass
            
        # Marcar que não estamos mais executando
        self.process_running = False
            
        # Atualizar barra de status
        self.status_label.config(text="Execução concluída")

    def stop_execution(self):
        """Interrompe a execução do script"""
        if hasattr(self, 'process') and self.process and self.process.poll() is None:
            try:
                # Tenta terminar o processo de forma organizada
                import signal
                self.process.send_signal(signal.SIGTERM)
                
                # Aguarda um pouco
                self.process.wait(timeout=1)
                
                # Se ainda estiver em execução, força o término
                if self.process.poll() is None:
                    self.process.kill()
                    
                self.add_output("\n=== Execução interrompida pelo usuário ===\n", "system")
            except Exception as e:
                self.add_output(f"\nErro ao interromper processo: {str(e)}\n", "error")
            finally:
                # Certifica-se de que a UI é restaurada
                self.process_running = False
                self.process_complete()

    def _handle_repl_input(self, event=None):
        """Manipula a entrada no modo REPL"""
        # Este método seria implementado para lidar com entrada interativa
        pass

    def highlight_pattern(self, pattern, tag, editor=None):
        """Aplica um padrão de destaque de sintaxe ao texto com melhor desempenho"""
        # Se não for especificado um editor, usa o editor atual
        if editor is None:
            editor = self.text_editor
        
        # Usar o método finditer para encontrar todas as ocorrências
        content = editor.get("1.0", "end-1c")
        
        try:
            # Encontrar todas as ocorrências do padrão
            for match in re.finditer(pattern, content, re.MULTILINE):
                start_index = "1.0 + %dc" % match.start()
                end_index = "1.0 + %dc" % match.end()
                
                # Adicionar a tag correspondente ao texto
                editor.tag_add(tag, start_index, end_index)
        except Exception as e:
            # Em caso de erro na expressão regular, apenas continue
            print(f"Erro ao aplicar padrão {pattern}: {e}")
            pass

    def update_syntax(self, event=None, editor=None):
        """Atualiza o destaque de sintaxe no editor"""
        # Se não for especificado um editor, usa o editor atual
        if editor is None:
            editor = self.text_editor
            
        # Remover todas as tags existentes (exceto tags visuais)
        for tag_name in ["keyword", "control", "loop", "conditional", "exception", 
                        "builtin", "literal", "comment", "string", "number", "module", 
                        "function", "operator", "brackets", "class", "import", "error"]:
            editor.tag_remove(tag_name, "1.0", "end")
            
        # Aplicar destaque para cada padrão
        for pattern, tag in self.patterns:
            self.highlight_pattern(pattern, tag, editor)
            
        # Desenhar linhas de indentação
        self._draw_indent_guides(editor)
        
        # Destacar a linha atual
        self._highlight_current_line(editor)
    
    def _highlight_current_line(self, editor):
        """Destaca a linha atual no editor"""
        # Remover destaque anterior
        editor.tag_remove("current_line", "1.0", "end")
        
        # Obter posição atual do cursor
        cursor_pos = editor.index(tk.INSERT)
        line = cursor_pos.split('.')[0]
        
        # Destacar a linha inteira
        editor.tag_add("current_line", f"{line}.0", f"{line}.end+1c")
    
    def _draw_indent_guides(self, editor):
        """Desenha linhas de indentação no editor"""
        # Remover linhas existentes
        editor.tag_remove("indent_guides", "1.0", "end")
        
        # Definir largura do tab (em espaços)
        tab_width = 4
        
        # Iterar por todas as linhas
        content = editor.get("1.0", "end")
        lines = content.split("\n")
        
        for i, line in enumerate(lines):
            # Calcular o nível de indentação
            indent_level = 0
            for char in line:
                if char == ' ':
                    indent_level += 1
                elif char == '\t':
                    indent_level += tab_width
                else:
                    break
            
            # Desenhar linhas para cada nível de indentação (a cada tab_width espaços)
            for level in range(tab_width, indent_level, tab_width):
                col = level
                editor.tag_add("indent_guides", f"{i+1}.{col}")
        
        # Configurar a aparência da linha de indentação
        editor.tag_configure("indent_guides", foreground=self.colors['indent_guide'])
    
    def setup_autocompletion(self):
        """Configura o sistema de autocompletar"""
        # Criar o widget de sugestões (inicialmente oculto)
        self.autocomplete_window = None
        self.autocomplete_listbox = None
    
    def _show_autocomplete(self, event, editor):
        """Exibe sugestões de autocompletar"""
        # Verificar se a tecla pressionada é útil para autocompletar
        if not (event.char.isalnum() or event.char == '_'):
            # Fechar qualquer janela de autocompletar existente se não for Enter
            if event.keysym != 'Return' and self.autocomplete_window:
                self.autocomplete_window.destroy()
                self.autocomplete_window = None
            return
        
        # Obter palavra atual sob o cursor
        cursor_pos = editor.index(tk.INSERT)
        line, col = map(int, cursor_pos.split('.'))
        
        # Obter a linha até o cursor
        line_text = editor.get(f"{line}.0", cursor_pos)
        
        # Extrair a palavra atual (caracteres alfanuméricos e underscore)
        word_match = re.search(r'[A-Za-z0-9_]*$', line_text)
        if not word_match:
            return
            
        current_word = word_match.group(0)
        
        # Se a palavra for muito curta, não mostrar sugestões
        if len(current_word) < 2:
            if self.autocomplete_window:
                self.autocomplete_window.destroy()
                self.autocomplete_window = None
            return
        
        # Encontrar sugestões que correspondam à palavra atual
        suggestions = []
        for word in self.all_autocomplete_words:
            if word.startswith(current_word) and word != current_word:
                suggestions.append(word)
        
        # Se não houver sugestões, fechar a janela
        if not suggestions:
            if self.autocomplete_window:
                self.autocomplete_window.destroy()
                self.autocomplete_window = None
            return
        
        # Obter as coordenadas da posição atual do cursor
        bbox = editor.bbox(cursor_pos)
        if not bbox:
            return
            
        x, y, width, height = bbox
        
        # Criar ou atualizar a janela de sugestões
        if not self.autocomplete_window:
            self.autocomplete_window = tk.Toplevel(editor)
            self.autocomplete_window.overrideredirect(True)  # Sem decoração de janela
            self.autocomplete_window.attributes('-topmost', True)  # Sempre no topo
            
            # Listbox para mostrar sugestões
            self.autocomplete_listbox = tk.Listbox(
                self.autocomplete_window,
                font=self.font,
                bg=self.colors['autocomplete_bg'],
                fg=self.colors['autocomplete_fg'],
                selectbackground=self.colors['autocomplete_select_bg'],
                selectforeground=self.colors['fg_text'],
                height=min(10, len(suggestions)),
                width=max([len(s) for s in suggestions]) + 5,
                relief=tk.FLAT,
                borderwidth=1
            )
            self.autocomplete_listbox.pack(fill=tk.BOTH, expand=True)
            
            # Adicionar scrollbar
            scrollbar = ttk.Scrollbar(self.autocomplete_listbox, orient=tk.VERTICAL)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.autocomplete_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.autocomplete_listbox.yview)
            
            # Vincular eventos
            self.autocomplete_listbox.bind("<Double-Button-1>", lambda e: self._insert_suggestion(editor))
            self.autocomplete_listbox.bind("<Return>", lambda e: self._insert_suggestion(editor))
            self.autocomplete_listbox.bind("<Escape>", lambda e: self.autocomplete_window.destroy())
            
            # Clicar fora fecha a janela
            editor.bind("<Button-1>", lambda e: self._close_autocomplete())
        
        # Limpar e adicionar sugestões
        self.autocomplete_listbox.delete(0, tk.END)
        for suggestion in suggestions:
            self.autocomplete_listbox.insert(tk.END, suggestion)
        
        # Selecionar a primeira sugestão
        self.autocomplete_listbox.selection_set(0)
        self.autocomplete_listbox.activate(0)
        
        # Posicionar a janela abaixo do cursor
        editor_x = editor.winfo_rootx() + x
        editor_y = editor.winfo_rooty() + y + height
        
        self.autocomplete_window.geometry(f"+{editor_x}+{editor_y}")
        self.autocomplete_window.lift()  # Trazer para frente
    
    def _close_autocomplete(self):
        """Fecha a janela de autocompletar"""
        if self.autocomplete_window:
            self.autocomplete_window.destroy()
            self.autocomplete_window = None
    
    def _insert_suggestion(self, editor):
        """Insere a sugestão selecionada no editor"""
        if not self.autocomplete_window or not self.autocomplete_listbox:
            return
            
        # Obter a sugestão selecionada
        selection = self.autocomplete_listbox.curselection()
        if not selection:
            return
            
        suggestion = self.autocomplete_listbox.get(selection[0])
        
        # Obter a posição atual e a palavra parcial
        cursor_pos = editor.index(tk.INSERT)
        line, col = map(int, cursor_pos.split('.'))
        line_text = editor.get(f"{line}.0", cursor_pos)
        
        # Extrair a palavra atual
        word_match = re.search(r'[A-Za-z0-9_]*$', line_text)
        if not word_match:
            return
            
        current_word = word_match.group(0)
        
        # Calcular posição para apagar a palavra parcial
        start_pos = f"{line}.{col - len(current_word)}"
        
        # Apagar a palavra parcial e inserir a sugestão
        editor.delete(start_pos, cursor_pos)
        editor.insert(start_pos, suggestion)
        
        # Fechar a janela de sugestões
        self._close_autocomplete()
        
        # Atualizar a sintaxe
        self.update_syntax(editor=editor)
        
        # Retornar o foco ao editor
        editor.focus_set()
    
    def _handle_tab(self, event, editor):
        """Manipula a tecla Tab para indentação elegante"""
        # Impedir o comportamento padrão
        editor.tag_remove("sel", "1.0", "end")
        
        # Inserir quatro espaços (ou tab configurado)
        editor.insert(tk.INSERT, "    ")
        
        # Atualizar a visualização
        self._draw_indent_guides(editor)
        
        # Impedir o comportamento padrão da tecla tab
        return "break"


def main():
    """Função principal para iniciar o editor melhorado"""
    try:
        # Configurar interface gráfica
        root = tk.Tk()
        root.title("NajaScript Editor - Versão Melhorada")
        root.geometry("1200x800")
        
        # Criar o editor melhorado
        app = NajaScriptEditorMelhorado(root)
        
        # Iniciar o loop principal
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Erro ao iniciar o editor", str(e))


if __name__ == "__main__":
    main() 