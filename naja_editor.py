#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import subprocess
import os
import sys
import re
import time

# Definindo classes para os novos componentes
class ProjectExplorer(ttk.Frame):
    """Explorador de projetos para navegar na estrutura de arquivos"""
    def __init__(self, master, editor_instance, **kwargs):
        super().__init__(master, **kwargs)
        self.editor = editor_instance
        
        # Título do explorador
        title_frame = ttk.Frame(self)
        title_frame.pack(side=tk.TOP, fill=tk.X)
        
        ttk.Label(title_frame, text="Explorador de Projetos", 
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5, pady=2)
        
        # Botões de ação
        refresh_btn = ttk.Button(title_frame, text="⟳", width=2, 
                               command=self.refresh_tree)
        refresh_btn.pack(side=tk.RIGHT, padx=2, pady=2)
        
        # Treeview para mostrar arquivos
        self.tree = ttk.Treeview(self, selectmode="browse")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar para o Treeview
        tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        # Configurar colunas
        self.tree["columns"] = ("size", "modified")
        self.tree.column("#0", width=200, minwidth=150)
        self.tree.column("size", width=70, anchor='e')
        self.tree.column("modified", width=120)
        
        # Configurar cabeçalhos
        self.tree.heading("#0", text="Nome", anchor='w')
        self.tree.heading("size", text="Tamanho", anchor='e')
        self.tree.heading("modified", text="Modificado")
        
        # Vincular eventos
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<ButtonRelease-1>", self.on_select)
        
        # Configurar menu de contexto
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Abrir", command=self.open_selected)
        self.context_menu.add_command(label="Novo Arquivo", command=self.new_file)
        self.context_menu.add_command(label="Nova Pasta", command=self.new_folder)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Renomear", command=self.rename_item)
        self.context_menu.add_command(label="Excluir", command=self.delete_item)
        
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # Armazenar path atual
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        
        # Ícones para diferentes tipos de arquivo
        self.file_icons = {
            ".naja": "🐍",
            ".py": "🐍",
            ".txt": "📄",
            ".md": "📝",
            ".json": "📋",
            ".html": "🌐",
            ".css": "🎨",
            ".js": "📜"
        }
        
        # Inicializa o explorador
        self.refresh_tree()
    
    def refresh_tree(self):
        """Atualiza a árvore de arquivos/pastas"""
        # Limpar a árvore
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar o diretório raiz
        root_name = os.path.basename(self.current_path)
        root = self.tree.insert("", 0, text=f"📂 {root_name}", 
                             values=("", ""), open=True)
        
        # Popular a árvore com arquivos e pastas
        self.populate_tree(root, self.current_path)
    
    def populate_tree(self, parent, path):
        """Popula a árvore com arquivos e pastas do caminho especificado"""
        try:
            # Listar diretórios primeiro, depois arquivos
            items = os.listdir(path)
            dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
            files = [item for item in items if not os.path.isdir(os.path.join(path, item))]
            
            # Ordenar alfabeticamente
            dirs.sort()
            files.sort()
            
            # Adicionar diretórios
            for dir_name in dirs:
                full_path = os.path.join(path, dir_name)
                dir_id = self.tree.insert(parent, "end", text=f"📂 {dir_name}", 
                                       values=("", ""))
                # Recursivamente popular o subdiretório
                self.populate_tree(dir_id, full_path)
            
            # Adicionar arquivos
            for file_name in files:
                full_path = os.path.join(path, file_name)
                
                # Obter tamanho do arquivo
                size = os.path.getsize(full_path)
                size_str = self.format_size(size)
                
                # Obter data de modificação
                mod_time = os.path.getmtime(full_path)
                mod_time_str = time.strftime("%Y-%m-%d %H:%M", 
                                          time.localtime(mod_time))
                
                # Determinar ícone baseado na extensão
                ext = os.path.splitext(file_name)[1]
                icon = self.file_icons.get(ext, "📄")
                
                self.tree.insert(parent, "end", text=f"{icon} {file_name}", 
                              values=(size_str, mod_time_str),
                              tags=("file",))
        
        except Exception as e:
            print(f"Erro ao popular árvore: {str(e)}")
    
    def format_size(self, size_bytes):
        """Formata o tamanho de bytes para formato legível"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes/1024:.1f} KB"
        else:
            return f"{size_bytes/(1024*1024):.1f} MB"
    
    def on_double_click(self, event):
        """Manipula o evento de duplo clique em um item da árvore"""
        self.open_selected()
    
    def on_select(self, event):
        """Manipula o evento de seleção de um item na árvore"""
        selected_item = self.tree.selection()
        if selected_item:
            item = selected_item[0]
            # Atualizar a barra de status do editor
            item_text = self.tree.item(item, "text")
            # Remover o ícone do texto
            file_name = item_text[2:] if item_text.startswith(("📂", "📄", "🐍")) else item_text
            self.editor.status_label.config(text=f"Selecionado: {file_name}")
    
    def open_selected(self):
        """Abre o arquivo selecionado no editor"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        item = selected_item[0]
        item_text = self.tree.item(item, "text")
        
        # Verificar se é um arquivo ou diretório
        if item_text.startswith("📂"):
            # É um diretório, expandir ou colapsar
            if self.tree.item(item, "open"):
                self.tree.item(item, open=False)
            else:
                self.tree.item(item, open=True)
        else:
            # É um arquivo, abrir no editor
            # Obter caminho completo através da navegação na árvore
            file_path = self.get_item_path(item)
            if file_path and os.path.isfile(file_path):
                self.editor.open_specific_file(file_path)
    
    def get_item_path(self, item):
        """Obtém o caminho completo de um item na árvore"""
        path_parts = []
        
        # Adicionar nome do item atual (sem o ícone)
        item_text = self.tree.item(item, "text")
        file_name = item_text[2:] if item_text.startswith(("📂", "📄", "🐍")) else item_text
        path_parts.append(file_name)
        
        # Subir na árvore até o nó raiz
        parent = self.tree.parent(item)
        while parent:
            parent_text = self.tree.item(parent, "text")
            parent_name = parent_text[2:] if parent_text.startswith(("📂", "📄", "🐍")) else parent_text
            path_parts.insert(0, parent_name)
            parent = self.tree.parent(parent)
        
        # O nó raiz representa o diretório base
        if len(path_parts) == 1:
            # Se estamos no nível raiz + 1, o caminho é relativo ao diretório base
            return os.path.join(self.current_path, path_parts[0])
        else:
            # Construir o caminho a partir das partes
            subdirs = path_parts[:-1]  # Todos exceto o último (que é o arquivo)
            base_dir = os.path.dirname(self.current_path)
            full_path = os.path.join(base_dir, *subdirs, path_parts[-1])
            return full_path
    
    def show_context_menu(self, event):
        """Exibe o menu de contexto ao clicar com o botão direito"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def new_file(self):
        """Cria um novo arquivo no diretório selecionado"""
        selected_item = self.tree.selection()
        if not selected_item:
            target_dir = self.current_path
        else:
            item = selected_item[0]
            item_text = self.tree.item(item, "text")
            
            if item_text.startswith("📂"):
                # Se for diretório, cria arquivo nele
                target_dir = self.get_item_path(item)
            else:
                # Se for arquivo, cria no mesmo diretório do arquivo
                parent = self.tree.parent(item)
                if parent:
                    target_dir = self.get_item_path(parent)
                else:
                    target_dir = self.current_path
        
        # Pedir nome do arquivo
        file_name = tk.simpledialog.askstring("Novo Arquivo", 
                                           "Nome do arquivo (com extensão):")
        if file_name:
            file_path = os.path.join(target_dir, file_name)
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("// Novo arquivo NajaScript\n")
                
                # Atualizar a árvore
                self.refresh_tree()
                
                # Abrir o novo arquivo
                self.editor.open_specific_file(file_path)
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar arquivo: {str(e)}")
    
    def new_folder(self):
        """Cria uma nova pasta no diretório selecionado"""
        selected_item = self.tree.selection()
        if not selected_item:
            target_dir = self.current_path
        else:
            item = selected_item[0]
            item_text = self.tree.item(item, "text")
            
            if item_text.startswith("📂"):
                # Se for diretório, cria pasta nele
                target_dir = self.get_item_path(item)
            else:
                # Se for arquivo, cria no mesmo diretório do arquivo
                parent = self.tree.parent(item)
                if parent:
                    target_dir = self.get_item_path(parent)
                else:
                    target_dir = self.current_path
        
        # Pedir nome da pasta
        folder_name = tk.simpledialog.askstring("Nova Pasta", "Nome da pasta:")
        if folder_name:
            folder_path = os.path.join(target_dir, folder_name)
            try:
                os.makedirs(folder_path, exist_ok=True)
                
                # Atualizar a árvore
                self.refresh_tree()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar pasta: {str(e)}")
    
    def rename_item(self):
        """Renomeia um arquivo ou pasta"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        item = selected_item[0]
        item_text = self.tree.item(item, "text")
        
        # Remover o ícone do nome
        old_name = item_text[2:] if item_text.startswith(("📂", "📄", "🐍")) else item_text
        item_path = self.get_item_path(item)
        
        # Pedir novo nome
        new_name = tk.simpledialog.askstring("Renomear", "Novo nome:", initialvalue=old_name)
        if new_name and new_name != old_name:
            parent_dir = os.path.dirname(item_path)
            new_path = os.path.join(parent_dir, new_name)
            
            try:
                os.rename(item_path, new_path)
                
                # Atualizar a árvore
                self.refresh_tree()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao renomear: {str(e)}")
    
    def delete_item(self):
        """Exclui um arquivo ou pasta"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        item = selected_item[0]
        item_text = self.tree.item(item, "text")
        
        # Remover o ícone do nome
        name = item_text[2:] if item_text.startswith(("📂", "📄", "🐍")) else item_text
        item_path = self.get_item_path(item)
        
        # Confirmar exclusão
        is_dir = os.path.isdir(item_path)
        msg = f"Excluir {'pasta' if is_dir else 'arquivo'} '{name}'?"
        if is_dir:
            msg += " Todos os arquivos dentro serão excluídos!"
            
        confirm = messagebox.askyesno("Confirmar Exclusão", msg)
        if confirm:
            try:
                if is_dir:
                    import shutil
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
                
                # Atualizar a árvore
                self.refresh_tree()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")

class EditorTabs(ttk.Notebook):
    """Componente de abas para editar múltiplos arquivos"""
    def __init__(self, master, editor_instance, **kwargs):
        super().__init__(master, **kwargs)
        self.editor = editor_instance
        
        # Dicionário para rastrear abas e arquivos
        self.tabs = {}  # {tab_id: {'file': file_path, 'editor': editor_widget}}
        
        # Configurar eventos
        self.bind("<ButtonRelease-1>", self.on_tab_select)
        
        # Menu de contexto para abas
        self.tab_menu = tk.Menu(self, tearoff=0)
        self.tab_menu.add_command(label="Fechar", command=self.close_current_tab)
        self.tab_menu.add_command(label="Fechar Outros", command=self.close_other_tabs)
        self.tab_menu.add_command(label="Fechar Todos", command=self.close_all_tabs)
        
        self.bind("<Button-3>", self.show_tab_menu)
    
    def add_tab(self, file_path=None, content=""):
        """Adiciona uma nova aba para edição"""
        # Criar frame para a aba
        tab_frame = ttk.Frame(self)
        
        # Criar editor de texto com rolagem para esta aba
        line_numbers = tk.Text(tab_frame, width=4, padx=3, takefocus=0, 
                             border=0, background='#f0f0f0', 
                             state='disabled')
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        text_editor = scrolledtext.ScrolledText(tab_frame, wrap=tk.WORD,
                                             undo=True, font=("Consolas", 11))
        text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Inserir conteúdo
        text_editor.insert(tk.END, content)
        
        # Determinar o nome da aba
        if file_path:
            tab_name = os.path.basename(file_path)
        else:
            tab_name = "Sem título"
        
        # Adicionar a aba
        self.add(tab_frame, text=tab_name)
        
        # Selecionar a nova aba
        self.select(tab_frame)
        
        # Armazenar informações da aba
        self.tabs[str(tab_frame)] = {
            'file': file_path,
            'editor': text_editor,
            'line_numbers': line_numbers,
            'modified': False
        }
        
        # Configurar eventos para esta aba
        text_editor.bind("<KeyPress>", lambda e, tf=tab_frame: self.on_text_modified(e, tf))
        text_editor.bind("<KeyRelease>", lambda e, tf=tab_frame: self.editor.update_syntax(e, text_editor))
        
        # Inicializar highlighting para esta aba
        self.editor.setup_editor_highlighting(text_editor)
        
        return tab_frame, text_editor
    
    def on_text_modified(self, event, tab_frame):
        """Chamado quando o texto em uma aba é modificado"""
        tab_info = self.tabs.get(str(tab_frame))
        if tab_info and not tab_info['modified']:
            tab_info['modified'] = True
            
            # Atualizar o título da aba com indicador de modificação
            current_text = self.tab(tab_frame, "text")
            if not current_text.startswith("*"):
                self.tab(tab_frame, text=f"*{current_text}")
            
            # Atualizar o título da janela
            self.editor.update_title()
    
    def on_tab_select(self, event):
        """Chamado quando uma aba é selecionada"""
        current_tab = self.select()
        if current_tab:
            tab_info = self.tabs.get(str(current_tab))
            if tab_info:
                # Atualizar referências no editor principal
                self.editor.current_file = tab_info['file']
                self.editor.current_file_name = os.path.basename(tab_info['file']) if tab_info['file'] else "Sem título"
                self.editor.modified = tab_info['modified']
                self.editor.text_editor = tab_info['editor']
                self.editor.line_numbers = tab_info['line_numbers']
                
                # Atualizar título
                self.editor.update_title()
                
                # Atualizar o status
                if tab_info['file']:
                    self.editor.status_label.config(text=f"Arquivo: {self.editor.current_file_name}")
                else:
                    self.editor.status_label.config(text="Novo arquivo")
    
    def save_current_tab(self):
        """Salva o conteúdo da aba atual"""
        current_tab = self.select()
        if not current_tab:
            return False
        
        tab_info = self.tabs.get(str(current_tab))
        if not tab_info:
            return False
        
        if tab_info['file']:
            # Salvar no arquivo existente
            return self.editor._save_to_file(tab_info['file'], tab_info['editor'])
        else:
            # Salvar como novo arquivo
            file_path = filedialog.asksaveasfilename(
                defaultextension=".naja",
                filetypes=[("Arquivos NajaScript", "*.naja"), ("Todos os arquivos", "*.*")]
            )
            
            if file_path:
                result = self.editor._save_to_file(file_path, tab_info['editor'])
                if result:
                    # Atualizar informações da aba
                    tab_info['file'] = file_path
                    tab_info['modified'] = False
                    
                    # Atualizar o nome da aba
                    self.tab(current_tab, text=os.path.basename(file_path))
                    
                    # Atualizar referências no editor principal
                    self.editor.current_file = file_path
                    self.editor.current_file_name = os.path.basename(file_path)
                    self.editor.modified = False
                    
                    # Atualizar título
                    self.editor.update_title()
                    
                return result
            return False
    
    def close_current_tab(self):
        """Fecha a aba atual"""
        current_tab = self.select()
        if not current_tab:
            return
        
        tab_info = self.tabs.get(str(current_tab))
        if not tab_info:
            return
        
        # Verificar se há modificações não salvas
        if tab_info['modified']:
            tab_name = self.tab(current_tab, "text").replace("*", "")
            response = messagebox.askyesnocancel(
                "Arquivo modificado", 
                f"O arquivo '{tab_name}' foi modificado. Deseja salvar as alterações?"
            )
            
            if response is None:  # Cancelar
                return
            if response:  # Sim
                if not self.save_current_tab():
                    return
        
        # Remover a aba
        self.forget(current_tab)
        del self.tabs[str(current_tab)]
        
        # Se não houver mais abas, criar uma nova vazia
        if not self.tabs:
            self.add_tab()
            
        # Atualizar referências para a nova aba selecionada
        self.on_tab_select(None)
    
    def close_other_tabs(self):
        """Fecha todas as abas exceto a atual"""
        current_tab = self.select()
        if not current_tab:
            return
        
        tabs_to_close = [tab for tab in self.tabs if tab != str(current_tab)]
        
        for tab_id in tabs_to_close:
            tab_info = self.tabs.get(tab_id)
            if tab_info['modified']:
                tab_index = self.index(tab_id)
                tab_name = self.tab(tab_index, "text").replace("*", "")
                
                response = messagebox.askyesnocancel(
                    "Arquivo modificado", 
                    f"O arquivo '{tab_name}' foi modificado. Deseja salvar as alterações?"
                )
                
                if response is None:  # Cancelar para esta aba
                    continue
                if response:  # Sim
                    # Selecionar temporariamente esta aba para salvá-la
                    self.select(tab_id)
                    if not self.save_current_tab():
                        continue
            
            # Remover a aba
            tab_widget = self.nametowidget(tab_id)
            self.forget(tab_widget)
            del self.tabs[tab_id]
        
        # Selecionar a aba que sobrou
        self.select(current_tab)
        self.on_tab_select(None)
    
    def close_all_tabs(self):
        """Fecha todas as abas"""
        # Verificar cada aba por modificações não salvas
        for tab_id, tab_info in list(self.tabs.items()):
            if tab_info['modified']:
                tab_widget = self.nametowidget(tab_id)
                tab_index = self.index(tab_widget)
                tab_name = self.tab(tab_index, "text").replace("*", "")
                
                response = messagebox.askyesnocancel(
                    "Arquivo modificado", 
                    f"O arquivo '{tab_name}' foi modificado. Deseja salvar as alterações?"
                )
                
                if response is None:  # Cancelar para esta aba
                    continue
                if response:  # Sim
                    # Selecionar temporariamente esta aba para salvá-la
                    self.select(tab_widget)
                    if not self.save_current_tab():
                        continue
            
            # Remover a aba
            tab_widget = self.nametowidget(tab_id)
            self.forget(tab_widget)
            del self.tabs[tab_id]
        
        # Criar uma nova aba vazia
        if not self.tabs:
            self.add_tab()
            self.on_tab_select(None)
    
    def show_tab_menu(self, event):
        """Exibe o menu de contexto da aba"""
        clicked_tab = self.identify(event.x, event.y)
        if clicked_tab:
            self.select(clicked_tab)
            self.tab_menu.post(event.x_root, event.y_root)

class AutocompleteListbox(tk.Listbox):
    """Listbox personalizada para exibir sugestões de autocompletar"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            height=10,
            width=30,
            font=("Consolas", 10),
            selectbackground="#4a6984",
            selectforeground="white"
        )

class NajaScriptEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("NajaScript Editor")
        self.root.geometry("1200x800")  # Aumentado para acomodar o explorador de projetos
        
        # Configurar tema
        self.configure_style()
        
        # Variáveis para informações do arquivo atual
        self.current_file = None
        self.current_file_name = "Sem título"
        
        # Variável para controlar se o arquivo foi modificado
        self.modified = False
        
        # Importar módulo simpledialog para uso nos componentes
        import tkinter.simpledialog
        
        self.update_title()
        
        # Criar menu
        self.create_menu()
        
        # Criar barra de ferramentas
        self.create_toolbar()
        
        # Criar área principal
        self.create_main_area()
        
        # Criar barra de status
        self.create_status_bar()
        
        # Configurar atalhos de teclado
        self.setup_keyboard_shortcuts()
        
        # Vincular eventos
        self.bind_events()
        
        # Configurar destaque de sintaxe
        self.setup_syntax_highlighting()
        
        # Configurar autocompletar
        self.setup_autocomplete()
    
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
    
    def create_menu(self):
        """Cria a barra de menu do editor"""
        self.menu_bar = tk.Menu(self.root)
        
        # Menu Arquivo
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Novo", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Abrir...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Salvar", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Salvar como...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.exit_editor, accelerator="Alt+F4")
        self.menu_bar.add_cascade(label="Arquivo", menu=file_menu)
        
        # Menu Editar
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Desfazer", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Refazer", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Recortar", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copiar", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Colar", command=self.paste, accelerator="Ctrl+V")
        self.menu_bar.add_cascade(label="Editar", menu=edit_menu)
        
        # Menu Executar
        run_menu = tk.Menu(self.menu_bar, tearoff=0)
        run_menu.add_command(label="Executar", command=self.run_script, accelerator="F5")
        self.menu_bar.add_cascade(label="Executar", menu=run_menu)
        
        # Menu Exemplos
        examples_menu = tk.Menu(self.menu_bar, tearoff=0)
        examples_menu.add_command(label="Teste de Input", command=self.run_input_test)
        examples_menu.add_command(label="Exemplo Math", command=self.create_math_example)
        examples_menu.add_command(label="Exemplo Random", command=self.create_random_example)
        self.menu_bar.add_cascade(label="Exemplos", menu=examples_menu)
        
        # Menu Ajuda
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Sobre", command=self.show_about)
        self.menu_bar.add_cascade(label="Ajuda", menu=help_menu)
        
        self.root.config(menu=self.menu_bar)
    
    def create_toolbar(self):
        """Cria a barra de ferramentas do editor"""
        self.toolbar = ttk.Frame(self.root, style='Toolbar.TFrame')
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Botões de arquivo
        new_button = ttk.Button(self.toolbar, text="Novo", command=self.new_file)
        new_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        open_button = ttk.Button(self.toolbar, text="Abrir", command=self.open_file)
        open_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        save_button = ttk.Button(self.toolbar, text="Salvar", command=self.save_file)
        save_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Separador
        ttk.Separator(self.toolbar, orient='vertical').pack(side=tk.LEFT, padx=5, pady=2, fill='y')
        
        # Botões de edição
        cut_button = ttk.Button(self.toolbar, text="Recortar", command=self.cut)
        cut_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        copy_button = ttk.Button(self.toolbar, text="Copiar", command=self.copy)
        copy_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        paste_button = ttk.Button(self.toolbar, text="Colar", command=self.paste)
        paste_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Separador
        ttk.Separator(self.toolbar, orient='vertical').pack(side=tk.LEFT, padx=5, pady=2, fill='y')
        
        # Botão de execução com ícone ou cor destacada
        run_button = ttk.Button(self.toolbar, text="Executar", command=self.run_script, style='Run.TButton')
        run_button.pack(side=tk.LEFT, padx=2, pady=2)
    
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
    
    def create_status_bar(self):
        """Cria a barra de status do editor"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Rótulo para mostrar informações de status
        self.status_label = ttk.Label(self.status_bar, text="Pronto")
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Rótulo para mostrar a posição do cursor
        self.cursor_position_label = ttk.Label(self.status_bar, text="Ln 1, Col 1")
        self.cursor_position_label.pack(side=tk.RIGHT, padx=5, pady=2)
    
    def setup_keyboard_shortcuts(self):
        """Configurar atalhos de teclado"""
        self.text_editor.bind("<Control-n>", lambda event: self.new_file())
        self.text_editor.bind("<Control-o>", lambda event: self.open_file())
        self.text_editor.bind("<Control-s>", lambda event: self.save_file())
        self.text_editor.bind("<Control-Shift-s>", lambda event: self.save_file_as())
        self.text_editor.bind("<F5>", lambda event: self.run_script())
        self.text_editor.bind("<Key>", self.key_pressed)
        self.text_editor.bind("<ButtonRelease-1>", self.update_cursor_position)
    
    def bind_events(self):
        """Vincular eventos adicionais"""
        self.text_editor.bind("<<Modified>>", self.text_modified)
    
    def setup_autocomplete(self):
        """Configura a funcionalidade de autocompletar"""
        # Lista de palavras para autocompletar
        self.autocomplete_keywords = [
            "int", "float", "string", "bool", "dict", "null", "void", "const", "fun", 
            "return", "if", "else", "elif", "for", "while", "do", "break", "continue", 
            "switch", "case", "default", "vecto", "list", "flux", "type", "any",
            "import", "from", "as"  # Adicionando palavras-chave para imports
        ]
        
        self.autocomplete_functions = [
            "print", "println", "input", "type", "min", "max", "vecto", "list", "dict", 
            "onChange", "printChange"
        ]
        
        self.autocomplete_literals = ["true", "false", "null"]
        
        # Módulos Python úteis para importar
        self.autocomplete_modules = [
            "math", "random", "time", "datetime", "json", "re", "os", "sys",
            "collections", "statistics", "itertools"
        ]
        
        # Funções matemáticas comuns (do módulo math)
        self.autocomplete_math_functions = [
            "math.sin", "math.cos", "math.tan", "math.asin", "math.acos", "math.atan",
            "math.sqrt", "math.pow", "math.exp", "math.log", "math.log10",
            "math.floor", "math.ceil", "math.fabs", "math.factorial", "math.gcd", 
            "math.radians", "math.degrees", "math.pi", "math.e"
        ]
        
        # Funções de random
        self.autocomplete_random_functions = [
            "random.random", "random.randint", "random.choice", "random.shuffle",
            "random.sample", "random.uniform"
        ]
        
        # Funções de time e datetime
        self.autocomplete_time_functions = [
            "time.time", "time.sleep", "datetime.now", "datetime.date", "datetime.timedelta"
        ]
        
        # Todas as palavras disponíveis para autocompletar
        self.autocomplete_words = (
            self.autocomplete_keywords + 
            self.autocomplete_functions + 
            self.autocomplete_literals +
            self.autocomplete_modules +
            self.autocomplete_math_functions +
            self.autocomplete_random_functions +
            self.autocomplete_time_functions
        )
        
        # Criar a listbox de autocompletar (inicialmente oculta)
        self.autocomplete_listbox = AutocompleteListbox(
            self.root,
            selectmode=tk.SINGLE
        )
        
        # Configurar eventos para autocompletar
        self.text_editor.bind("<KeyRelease>", self.check_autocomplete)
        self.text_editor.bind("<Tab>", self.handle_tab)
        self.text_editor.bind("<Escape>", self.hide_autocomplete)
        self.text_editor.bind("<Up>", self.navigate_autocomplete)
        self.text_editor.bind("<Down>", self.navigate_autocomplete)
        self.text_editor.bind("<Return>", self.apply_autocomplete)
        
        # Quando o usuário clica em uma sugestão
        self.autocomplete_listbox.bind("<ButtonRelease-1>", self.apply_autocomplete)
        self.autocomplete_listbox.bind("<Double-Button-1>", self.apply_autocomplete)
        
        # Flag para controlar se o autocompletar está ativo
        self.autocomplete_active = False
    
    def navigate_autocomplete(self, event):
        """Navega pela lista de sugestões de autocompletar"""
        if not self.autocomplete_active:
            return
        
        # Trata as teclas de seta para navegar na lista
        if event.keysym == "Up":
            # Move a seleção para cima
            if self.autocomplete_listbox.curselection():
                current_selection = self.autocomplete_listbox.curselection()[0]
                if current_selection > 0:
                    self.autocomplete_listbox.selection_clear(0, tk.END)
                    self.autocomplete_listbox.selection_set(current_selection - 1)
                    self.autocomplete_listbox.see(current_selection - 1)
            return "break"  # Impede o comportamento padrão
        
        elif event.keysym == "Down":
            # Move a seleção para baixo
            if self.autocomplete_listbox.curselection():
                current_selection = self.autocomplete_listbox.curselection()[0]
                if current_selection < self.autocomplete_listbox.size() - 1:
                    self.autocomplete_listbox.selection_clear(0, tk.END)
                    self.autocomplete_listbox.selection_set(current_selection + 1)
                    self.autocomplete_listbox.see(current_selection + 1)
            else:
                # Se não houver seleção, seleciona o primeiro item
                if self.autocomplete_listbox.size() > 0:
                    self.autocomplete_listbox.selection_set(0)
            return "break"  # Impede o comportamento padrão
    
    def handle_tab(self, event):
        """Gerencia a tecla Tab para autocompletar"""
        if self.autocomplete_active:
            self.apply_autocomplete(event)
            return "break"  # Impede que o tab seja inserido
        return None  # Permite o comportamento padrão do tab
    
    def check_autocomplete(self, event):
        """Verifica se deve exibir sugestões de autocompletar"""
        # Atualiza o destaque de sintaxe
        self.update_syntax(event)
        
        # Apenas mostra autocompletar para teclas alfanuméricas ou backspace
        if event.keysym in [
            "Escape", "Return", "Tab", "Up", "Down", "Left", "Right",
            "Control_L", "Control_R", "Alt_L", "Alt_R", "Shift_L", "Shift_R"
        ]:
            return
        
        # Obtém a posição atual do cursor
        current_pos = self.text_editor.index(tk.INSERT)
        line, col = map(int, current_pos.split('.'))
        
        # Obtém a linha atual completa
        line_text = self.text_editor.get(f"{line}.0", f"{line}.end")
        
        # Encontra a palavra parcial que está sendo digitada
        if col > 0:
            # Pega o texto antes do cursor na linha atual
            text_before_cursor = line_text[:col]
            
            # Encontra a última palavra parcial
            match = re.search(r'[a-zA-Z0-9_]+$', text_before_cursor)
            
            if match:
                partial_word = match.group(0)
                
                # Se a palavra parcial tiver pelo menos 2 caracteres
                if len(partial_word) >= 2:
                    # Filtra as palavras que começam com a palavra parcial
                    matches = [word for word in self.autocomplete_words if word.startswith(partial_word)]
                    
                    if matches:
                        # Atualiza e exibe a lista de sugestões
                        self.show_autocomplete(matches, current_pos, len(partial_word))
                        return
        
        # Se não encontrou sugestões ou não deve mostrar, esconde a lista
        self.hide_autocomplete(None)
    
    def show_autocomplete(self, suggestions, position, word_length):
        """Mostra a lista de sugestões de autocompletar"""
        # Limpa a lista atual
        self.autocomplete_listbox.delete(0, tk.END)
        
        # Adiciona as sugestões à lista
        for suggestion in suggestions:
            self.autocomplete_listbox.insert(tk.END, suggestion)
        
        # Seleciona o primeiro item
        if self.autocomplete_listbox.size() > 0:
            self.autocomplete_listbox.selection_set(0)
        
        # Posiciona a listbox logo abaixo da palavra atual
        x, y, width, height = self.text_editor.bbox(position)
        
        # Ajusta a posição para ficar logo abaixo do texto
        listbox_x = self.text_editor.winfo_rootx() + x
        listbox_y = self.text_editor.winfo_rooty() + y + height
        
        # Define a largura baseada no tamanho das sugestões
        max_len = max(len(s) for s in suggestions)
        self.autocomplete_listbox.config(width=max(30, max_len + 2))
        
        # Posiciona e exibe a listbox
        self.autocomplete_listbox.place(x=x, y=y+height+5)
        self.autocomplete_listbox.lift()
        
        # Salva a posição e o comprimento da palavra parcial para uso posterior
        self.autocomplete_position = position
        self.autocomplete_word_length = word_length
        self.autocomplete_active = True
    
    def hide_autocomplete(self, event=None):
        """Esconde a lista de sugestões de autocompletar"""
        self.autocomplete_listbox.place_forget()
        self.autocomplete_active = False
        return "break" if event else None
    
    def apply_autocomplete(self, event):
        """Aplica a sugestão selecionada"""
        if not self.autocomplete_active:
            return None
        
        # Obtém a sugestão selecionada
        if self.autocomplete_listbox.curselection():
            selected_index = self.autocomplete_listbox.curselection()[0]
            suggestion = self.autocomplete_listbox.get(selected_index)
            
            # Calcula a posição para substituir a palavra parcial
            line, col = map(int, self.autocomplete_position.split('.'))
            start_pos = f"{line}.{col - self.autocomplete_word_length}"
            
            # Substitui a palavra parcial pela sugestão completa
            self.text_editor.delete(start_pos, tk.INSERT)
            self.text_editor.insert(start_pos, suggestion)
            
            # Esconde a lista de sugestões
            self.hide_autocomplete()
            
            # Foca novamente no editor
            self.text_editor.focus_set()
            
            return "break"  # Impede o comportamento padrão da tecla
        return None
    
    def text_modified(self, event=None):
        """Chamado quando o texto é modificado"""
        if not self.modified:
            self.modified = True
            self.update_title()
        self.text_editor.edit_modified(False)  # Reinicia o sinalizador de modificação
    
    def key_pressed(self, event=None):
        """Manipulador para quando uma tecla é pressionada"""
        self.update_cursor_position()
    
    def update_cursor_position(self, event=None):
        """Atualiza a posição do cursor na barra de status"""
        cursor_pos = self.text_editor.index(tk.INSERT).split('.')
        line_num = cursor_pos[0]
        col_num = cursor_pos[1]
        self.cursor_position_label.config(text=f"Ln {line_num}, Col {col_num}")
    
    def update_title(self):
        """Atualiza o título da janela com o nome do arquivo atual"""
        modified_indicator = "*" if self.modified else ""
        self.root.title(f"{modified_indicator}{self.current_file_name} - NajaScript Editor")
    
    def clear_output(self):
        """Limpa a área de saída"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def add_output(self, text, tag=None):
        """Adiciona texto à área de saída com a tag especificada"""
        try:
            # Verifica se o widget de saída ainda existe
            if hasattr(self, 'output_text') and self.output_text.winfo_exists():
                self.output_text.config(state=tk.NORMAL)
                if tag:
                    self.output_text.insert(tk.END, text, tag)
                else:
                    self.output_text.insert(tk.END, text)
                self.output_text.see(tk.END)  # Rola para mostrar o último texto adicionado
                
                # Se não estivermos em modo REPL, desabilita a edição
                if not self.repl_mode:
                    self.output_text.config(state=tk.DISABLED)
        except (tk.TclError, RuntimeError, AttributeError) as e:
            # Log do erro para depuração sem quebrar a aplicação
            print(f"Erro ao adicionar saída: {str(e)}")
    
    def new_file(self):
        """Cria um novo arquivo"""
        if self.modified:
            response = messagebox.askyesnocancel("Arquivo modificado", 
                                              "O arquivo atual foi modificado. Deseja salvar as alterações?")
            if response is None:  # Cancelar
                return
            if response:  # Sim
                if not self.save_file():
                    return
        
        self.text_editor.delete(1.0, tk.END)
        self.current_file = None
        self.current_file_name = "Sem título"
        self.modified = False
        self.update_title()
        self.status_label.config(text="Novo arquivo criado")
    
    def open_file(self):
        """Abre um arquivo existente em uma nova aba"""
        file_path = filedialog.askopenfilename(
            defaultextension=".naja",
            filetypes=[("Arquivos NajaScript", "*.naja"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            return self.open_specific_file(file_path)
        
        return False
    
    def save_file(self):
        """Salva o arquivo atual usando o sistema de abas"""
        return self.tabs.save_current_tab()
    
    def save_file_as(self):
        """Salva o arquivo atual com um novo nome"""
        # Será tratado pelo sistema de abas
        return self.tabs.save_current_tab()
    
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
    
    def run_script(self):
        """Executa o script atual usando o interpretador"""
        # Atualiza a UI para mostrar que está iniciando
        self.run_button.pack_forget()
        self.stop_button.pack(side=tk.RIGHT, padx=10, pady=2)
        
        # Executa o script
        self._run_with_option()
    
    def _run_with_option(self, option=None):
        """Executa o script com a opção especificada"""
        if self.modified or not self.current_file:
            response = messagebox.askyesno("Arquivo não salvo", 
                                         "É necessário salvar o arquivo antes de executá-lo. Deseja salvar agora?")
            if response:
                if not self.save_file():
                    # Restaura os botões se cancelar
                    self.stop_button.pack_forget()
                    self.run_button.pack(side=tk.RIGHT, padx=10, pady=2)
                    return
            else:
                # Restaura os botões se cancelar
                self.stop_button.pack_forget()
                self.run_button.pack(side=tk.RIGHT, padx=10, pady=2)
                return
        
        if self.current_file:
            self.clear_output()
            self.status_label.config(text="Executando script...")
            
            # Destaca o painel de saída para mostrar que está executando
            self.output_text.config(background="#f5f5dc")
            self.add_output(">>> INICIANDO EXECUÇÃO DO SCRIPT...\n")
            self.add_output(">>> Se você precisar fornecer dados, uma caixa de diálogo aparecerá.\n")
            self.add_output(">>> Para interromper a execução, clique no botão INTERROMPER.\n\n")
            
            # Obter caminho do script najascript.py
            najascript_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "najascript.py")
            
            try:
                # Preparar o comando - remover a opção se não for necessária
                cmd = ["python", najascript_path, self.current_file]
                if option:
                    cmd.append(option)
                
                # Executar o processo
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    text=True,
                    bufsize=1,  # Line buffered
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
                )
                
                # Guardar referência ao processo atual
                self.current_process = process
                
                # Adicionar informação de diagnóstico
                self.add_output(f">>> Executando comando: {' '.join(cmd)}\n\n")
                
                # Nova função para lidar com entrada/saída de forma interativa
                self._handle_interactive_io(process)
                
                # Restaura a UI quando terminar
                self.stop_button.pack_forget()
                self.run_button.pack(side=tk.RIGHT, padx=10, pady=2)
                
                # Retorna a cor de fundo normal
                self.output_text.config(background="white")
                
                # Limpar a referência ao processo
                self.current_process = None
                
                # Mostrar resultado da execução
                if process.returncode == 0:
                    self.status_label.config(text="Execução concluída com sucesso")
                    self.add_output("\n>>> Execução concluída com sucesso.\n")
                else:
                    self.status_label.config(text=f"Execução falhou com código: {process.returncode}")
                    self.add_output(f"\n>>> Execução falhou com código de saída: {process.returncode}\n")
            
            except Exception as e:
                # Restaura a UI em caso de erro
                self.stop_button.pack_forget()
                self.run_button.pack(side=tk.RIGHT, padx=10, pady=2)
                
                error_msg = str(e)
                self.add_output(f"\n>>> ERRO AO EXECUTAR: {error_msg}\n")
                messagebox.showerror("Erro ao executar script", error_msg)
                self.status_label.config(text="Erro ao executar script")
                self.output_text.config(background="white")
                
                # Limpar a referência ao processo
                self.current_process = None
    
    def _handle_interactive_io(self, process):
        """Gerencia entrada/saída interativa com o processo"""
        import threading
        import time
        from queue import Queue, Empty
        
        # Flag para indicar se devemos continuar processando
        processing_active = True
        
        # Filas para comunicação entre threads
        stdout_queue = Queue()
        stderr_queue = Queue()
        
        # Contadores e flags para controle
        waiting_message_limit = 5  # Limite de mensagens "Aguardando saída"
        waiting_messages_shown = 0
        help_message_shown = False
        no_data_count = 0
        start_time = time.time()
        timeout = 60  # Timeout em segundos (1 minuto)
        last_input_check_time = 0  # Para limitar a frequência de verificações
        accumulated_output = ""  # Para acumular saída e buscar padrões
        
        # Função para ler continuamente a saída do processo
        def reader_thread(stream, queue):
            try:
                for line in iter(stream.readline, ''):
                    if line and processing_active:
                        queue.put(line)
            except Exception as e:
                if processing_active:
                    queue.put(f"ERRO DE LEITURA: {str(e)}\n")
            finally:
                try:
                    stream.close()
                except:
                    pass
        
        # Inicia threads para ler stdout e stderr
        stdout_thread = threading.Thread(target=reader_thread, args=(process.stdout, stdout_queue), daemon=True)
        stderr_thread = threading.Thread(target=reader_thread, args=(process.stderr, stderr_queue), daemon=True)
        stdout_thread.start()
        stderr_thread.start()
        
        # Buffer para armazenar linhas recentes (para detectar padrões de prompt)
        recent_output = []
        max_recent_lines = 5  # Aumentamos para armazenar mais linhas recentes
        
        # Adiciona uma mensagem de debug
        self.add_output(">>> Aguardando saída do programa...\n", "system")
        
        # Função auxiliar para verificar se uma string parece um prompt de input
        def looks_like_input_prompt(text):
            # Lista expandida de palavras-chave que indicam solicitação de input
            input_keywords = [
                "input", "digite", "informe", "entre", "insira", "forneça", 
                "valor", "nome", "idade", "resposta", "número", "numero",
                "qual", "quem", "quando", "onde", "como", "por que", "quanto",
                "escolha", "opção", "opcao", "selecione", "confirme", "confirma",
                "sim/não", "s/n", "y/n", "continuar", "prosseguir", "deseja"
            ]
            
            # Verifica presença de palavras-chave
            for keyword in input_keywords:
                if keyword in text.lower():
                    return True
                
            # Verifica sintaxe de chamada de função input()
            if "input(" in text:
                return True
            
            # Verifica terminação típica de prompt
            if (text.strip().endswith(':') or text.strip().endswith('?') or 
                text.strip().endswith('...') or text.strip().endswith('>')):
                return True
            
            # Verifica se parece uma pergunta
            if '?' in text and len(text.strip()) < 100:  # Perguntas são geralmente curtas
                return True
            
            # Verifica outras características de prompts
            if text.strip() and len(text.strip().split()) < 10 and not text.strip().endswith('.'):
                return True
            
            return False
        
        # Processa a saída enquanto o processo estiver em execução
        try:
            while process.poll() is None:
                # Verificar timeout
                if time.time() - start_time > timeout:
                    self.add_output("\n>>> AVISO: Execução demorada detectada (mais de 1 minuto).\n", "system")
                    self.add_output(">>> Se o programa estiver em loop infinito, use o botão INTERROMPER.\n\n", "system")
                    # Reseta o tempo para não mostrar esta mensagem novamente
                    start_time = float('inf')
                
                data_received = False
                
                # Processa stdout
                try:
                    while True:
                        try:
                            line = stdout_queue.get_nowait()
                            data_received = True
                            waiting_messages_shown = 0  # Resetar contador quando receber dados
                            help_message_shown = False  # Resetar flag de mensagem de ajuda
                            self.add_output(line)
                            
                            # Adiciona ao buffer de saída recente
                            recent_output.append(line)
                            if len(recent_output) > max_recent_lines:
                                recent_output.pop(0)
                            
                            # Acumula saída para verificação posterior
                            accumulated_output += line
                            if len(accumulated_output) > 1000:  # Limita o tamanho
                                accumulated_output = accumulated_output[-1000:]
                            
                            # Verifica diretamente se a linha atual parece um prompt
                            is_input_prompt = looks_like_input_prompt(line)
                            
                            # Se não for um prompt claro, verifica as últimas linhas acumuladas
                            if not is_input_prompt and time.time() - last_input_check_time > 0.5:
                                # Cria uma string com as últimas linhas
                                recent_buffer = ''.join(recent_output)
                                is_input_prompt = looks_like_input_prompt(recent_buffer)
                                last_input_check_time = time.time()
                            
                            if is_input_prompt:
                                # Aguarda um pouco para garantir que todo o prompt seja exibido
                                self.root.update()
                                time.sleep(0.1)
                                
                                # Adiciona uma mensagem explícita na área de saída com destaque
                                self.add_output("\n>>> AGUARDANDO ENTRADA: ", "system")
                                
                                # Determina o texto do prompt a mostrar
                                prompt_text = line.strip()
                                if len(prompt_text) < 5 or not looks_like_input_prompt(prompt_text):
                                    # Se a linha atual for muito curta, usa o buffer recente
                                    prompt_text = recent_buffer.strip()
                                
                                # Ativa o modo REPL para entrada direta na área de saída
                                self.prompt_for_input(prompt_text)
                                
                                # Espera em um loop até que o usuário forneça a entrada
                                input_processed = False
                                input_timeout = time.time() + 300  # 5 minutos para timeout
                                
                                while not input_processed and time.time() < input_timeout:
                                    # Verifica se ainda estamos em modo REPL
                                    if not self.repl_mode:
                                        input_processed = True
                                    
                                    # Atualiza a interface para manter a responsividade
                                    self.root.update()
                                    time.sleep(0.1)
                                
                                # Se atingir o timeout, sai do modo REPL
                                if not input_processed:
                                    self.repl_mode = False
                                    self.output_text.config(state=tk.DISABLED)
                                    self.add_output("\n>>> TIMEOUT: Entrada não fornecida a tempo.\n", "error")
                                
                                # Reinicia contadores
                                no_data_count = 0
                                waiting_messages_shown = 0
                                help_message_shown = False
                                start_time = time.time()  # Reinicia o tempo de timeout
                                
                                # Limpa o buffer acumulado após o input
                                accumulated_output = ""
                                recent_output = []
                        except Empty:
                            break
                except Exception as e:
                    self.add_output(f"ERRO: {str(e)}\n", "error")
                
                # Processa stderr
                try:
                    while True:
                        try:
                            line = stderr_queue.get_nowait()
                            data_received = True
                            waiting_messages_shown = 0  # Resetar contador quando receber dados
                            help_message_shown = False  # Resetar flag de mensagem de ajuda
                            self.add_output(f"ERRO: {line}", "error")
                        except Empty:
                            break
                except Exception as e:
                    self.add_output(f"ERRO: {str(e)}\n", "error")
                
                # Se nenhum dado foi recebido neste ciclo, incrementa o contador
                if not data_received:
                    no_data_count += 1
                else:
                    no_data_count = 0
                    
                # Verificação adicional periódica para casos onde não temos nova saída,
                # mas já pode existir um prompt na saída acumulada esperando por input
                if no_data_count >= 5 and accumulated_output and time.time() - last_input_check_time > 1.0:
                    last_input_check_time = time.time()
                    # Verifica se a saída acumulada parece conter um prompt de input
                    if looks_like_input_prompt(accumulated_output):
                        self.add_output("\n>>> Possível solicitação de entrada detectada na saída anterior.\n", "system")
                        
                        # Ativa o modo REPL para entrada direta na área de saída
                        self.prompt_for_input(accumulated_output.strip())
                        
                        # Espera em um loop até que o usuário forneça a entrada
                        input_processed = False
                        input_timeout = time.time() + 300  # 5 minutos para timeout
                        
                        while not input_processed and time.time() < input_timeout:
                            # Verifica se ainda estamos em modo REPL
                            if not self.repl_mode:
                                input_processed = True
                            
                            # Atualiza a interface para manter a responsividade
                            self.root.update()
                            time.sleep(0.1)
                        
                        # Se atingir o timeout, sai do modo REPL
                        if not input_processed:
                            self.repl_mode = False
                            self.output_text.config(state=tk.DISABLED)
                            self.add_output("\n>>> TIMEOUT: Entrada não fornecida a tempo.\n", "error")
                        
                        # Reinicia contadores
                        no_data_count = 0
                        waiting_messages_shown = 0
                        help_message_shown = False
                        
                        # Limpa o buffer acumulado após o input
                        accumulated_output = ""
                        recent_output = []
                    
                # Se não receber dados por muito tempo e o processo ainda estiver rodando,
                # adiciona indicadores de que está aguardando
                if no_data_count >= 10:  # ~1 segundo sem dados
                    no_data_count = 0
                    
                    # Limita o número de mensagens "Aguardando saída"
                    if waiting_messages_shown < waiting_message_limit:
                        waiting_messages_shown += 1
                        self.add_output(">>> Aguardando saída ou término do programa...\n", "system")
                    elif not help_message_shown:
                        # Após alcançar o limite, mostrar mensagem de ajuda
                        self.add_output("\n>>> O programa parece estar preso num loop infinito.\n", "system")
                        self.add_output(">>> Se o programa não está respondendo, clique no botão INTERROMPER\n", "system")
                        self.add_output(">>> para encerrar a execução e tente novamente.\n\n", "system")
                        help_message_shown = True
                
                # Atualiza a interface para manter a responsividade
                try:
                    self.root.update()
                except:
                    # Se a janela foi fechada, interrompe o processamento
                    processing_active = False
                    break
                    
                time.sleep(0.1)
            
            # Marca que não estamos mais processando ativamente
            processing_active = False
            
            # Certifica-se de coletar qualquer saída restante
            time.sleep(0.5)
            
            # Verifica se ainda há dados nas filas
            try:
                while not stdout_queue.empty():
                    line = stdout_queue.get_nowait()
                    self.add_output(line)
            except Exception as e:
                self.add_output(f"ERRO: {str(e)}\n", "error")
                
            try:
                while not stderr_queue.empty():
                    line = stderr_queue.get_nowait()
                    self.add_output(f"ERRO: {line}", "error")
            except Exception as e:
                self.add_output(f"ERRO: {str(e)}\n", "error")
            
            # Aguarda as threads terminarem com limite de tempo
            stdout_thread.join(timeout=1)
            stderr_thread.join(timeout=1)
        
        except Exception as e:
            processing_active = False
            self.add_output(f"\n>>> ERRO NO PROCESSAMENTO DE E/S: {str(e)}\n", "error")
        
        finally:
            # Garantir que as threads de leitura sejam interrompidas
            processing_active = False
            
            # Certifique-se de que não estamos mais no modo REPL
            self.repl_mode = False
            self.output_text.config(state=tk.DISABLED)
    
    def _handle_repl_input(self, event=None):
        """Lida com o evento de pressionar Enter no modo REPL"""
        if not self.repl_mode or not hasattr(self, 'current_process'):
            return
        
        try:
            # Obter o texto da área de entrada
            input_text = self.output_text.get(self.input_start, "end-1c")
            
            # Verificar se há um prompt no início e removê-lo
            if input_text.startswith(">>> "):
                input_text = input_text[4:]
            
            # Adicionar uma nova linha após o input
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "\n")
            self.output_text.config(state=tk.DISABLED)
            
            # Enviar o texto para o processo
            if hasattr(self, 'current_process') and self.current_process and self.current_process.poll() is None:
                self.current_process.stdin.write(input_text + "\n")
                self.current_process.stdin.flush()
            
            # Sair do modo REPL
            self.repl_mode = False
            
            # Desativar edição da área de saída
            self.output_text.config(state=tk.DISABLED)
            
            return "break"  # Impede o comportamento padrão da tecla Enter
        except Exception as e:
            self.add_output(f"\nERRO AO PROCESSAR ENTRADA: {str(e)}\n", "error")
            self.repl_mode = False
            self.output_text.config(state=tk.DISABLED)
            return "break"
    
    def prompt_for_input(self, prompt_text=""):
        """Exibe um prompt na área de saída e habilita a entrada de texto"""
        # Adiciona o prompt visível
        if not prompt_text:
            prompt_text = "Entrada requerida"
        
        self.add_output("\n>>> ", "prompt")
        
        # Marca o início da região de input
        self.input_start = self.output_text.index(tk.END)
        
        # Ativa o modo REPL
        self.repl_mode = True
        
        # Habilita a edição da área de saída
        self.output_text.config(state=tk.NORMAL)
        
        # Foca na área de saída
        self.output_text.focus_set()
    
    def exit_editor(self):
        """Sai do editor"""
        if self.modified:
            response = messagebox.askyesnocancel("Arquivo modificado", 
                                               "O arquivo atual foi modificado. Deseja salvar as alterações?")
            if response is None:  # Cancelar
                return
            if response:  # Sim
                if not self.save_file():
                    return
        
        self.root.destroy()
    
    def undo(self):
        """Desfaz a última operação de edição"""
        try:
            self.text_editor.edit_undo()
        except tk.TclError:
            pass
    
    def redo(self):
        """Refaz a última operação desfeita"""
        try:
            self.text_editor.edit_redo()
        except tk.TclError:
            pass
    
    def cut(self):
        """Recorta o texto selecionado"""
        try:
            self.text_editor.event_generate("<<Cut>>")
        except:
            pass
    
    def copy(self):
        """Copia o texto selecionado"""
        try:
            self.text_editor.event_generate("<<Copy>>")
        except:
            pass
    
    def paste(self):
        """Cola o texto da área de transferência"""
        try:
            self.text_editor.event_generate("<<Paste>>")
        except:
            pass
    
    def show_about(self):
        """Mostra informações sobre o editor"""
        messagebox.showinfo("Sobre o NajaScript Editor", 
                          "NajaScript Editor v1.0\n\n"
                          "Um ambiente de desenvolvimento integrado (IDE) simples para a linguagem NajaScript.\n\n"
                          "©2023 NajaScript Team")
    
    def setup_syntax_highlighting(self):
        """Configura o destaque de sintaxe para NajaScript"""
        # Palavras-chave da linguagem
        keywords = [
            "int", "float", "string", "bool", "dict", "null", "void", "const", "fun", 
            "return", "if", "else", "elif", "for", "while", "do", "break", "continue", 
            "switch", "case", "default", "vecto", "list", "flux", "type", "any",
            "import", "from", "as"  # Adicionando palavras-chave para imports
        ]
        
        # Funções nativas
        builtins = [
            "print", "println", "input", "type", "min", "max", "vecto", "list", "dict", 
            "onChange", "printChange"
        ]
        
        # Valores literais
        literals = ["true", "false", "null"]
        
        # Módulos
        modules = [
            "math", "random", "time", "datetime", "json", "re", "os", "sys",
            "collections", "statistics", "itertools"
        ]
        
        # Configurar as tags para coloração
        self.text_editor.tag_configure("keyword", foreground="#0000FF")  # Azul para palavras-chave
        self.text_editor.tag_configure("builtin", foreground="#8A2BE2")  # Roxo para funções nativas
        self.text_editor.tag_configure("literal", foreground="#008000")  # Verde para literais
        self.text_editor.tag_configure("comment", foreground="#808080", font=("Consolas", 11, "italic"))  # Cinza itálico para comentários
        self.text_editor.tag_configure("string", foreground="#A31515")  # Vermelho escuro para strings
        self.text_editor.tag_configure("number", foreground="#008080")  # Verde azulado para números
        self.text_editor.tag_configure("module", foreground="#FF8C00")  # Laranja para módulos
        
        # Padrões para expressões regulares
        self.patterns = [
            (r'\b(' + '|'.join(keywords) + r')\b', "keyword"),
            (r'\b(' + '|'.join(builtins) + r')\b', "builtin"),
            (r'\b(' + '|'.join(literals) + r')\b', "literal"),
            (r'\b(' + '|'.join(modules) + r')\b', "module"),  # Módulos em laranja
            (r'//.*$', "comment"),  # Comentários de linha única
            (r'\"([^\"]*)\"', "string"),  # Strings com aspas duplas
            (r'\'([^\']*)\'', "string"),  # Strings com aspas simples
            (r'\b\d+\b', "number"),  # Números inteiros
            (r'\b\d+\.\d+\b', "number")  # Números de ponto flutuante
        ]
        
        # Adicionar tratamento de eventos para atualizar a coloração da sintaxe
        self.text_editor.bind("<KeyRelease>", self.update_syntax)
    
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
    
    def run_input_test(self):
        """Executa o arquivo de teste de input"""
        # Verifica se o arquivo de teste existe
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "teste_input.naja")
        
        if os.path.exists(test_file):
            # Salva o arquivo atual se necessário
            if self.modified:
                save_current = messagebox.askyesno(
                    "Arquivo modificado",
                    "O arquivo atual foi modificado. Deseja salvá-lo antes de executar o teste?"
                )
                if save_current and not self.save_file():
                    return
            
            # Abre o arquivo de teste
            try:
                with open(test_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Salva o estado atual
                old_file = self.current_file
                old_file_name = self.current_file_name
                
                # Carrega o arquivo de teste
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, content)
                
                self.current_file = test_file
                self.current_file_name = os.path.basename(test_file)
                self.modified = False
                self.update_title()
                
                # Executa o teste
                self.run_script()
                
                # Pergunta se deseja restaurar o arquivo anterior
                if old_file and old_file != test_file:
                    restore = messagebox.askyesno(
                        "Restaurar arquivo",
                        "Deseja restaurar o arquivo anterior?"
                    )
                    if restore:
                        with open(old_file, 'r', encoding='utf-8') as file:
                            content = file.read()
                        
                        self.text_editor.delete(1.0, tk.END)
                        self.text_editor.insert(tk.END, content)
                        
                        self.current_file = old_file
                        self.current_file_name = old_file_name
                        self.modified = False
                        self.update_title()
            
            except Exception as e:
                messagebox.showerror("Erro ao executar teste", str(e))
        else:
            messagebox.showwarning(
                "Arquivo de teste não encontrado",
                f"O arquivo de teste '{test_file}' não foi encontrado. Criando um novo arquivo de teste."
            )
            
            # Cria o arquivo de teste com a sintaxe correta para NajaScript
            # Sem função main e sem comentários no início
            test_content = """println("Teste de funcionalidade de input interativo");

string nome = input("Digite seu nome: ");
println("Olá, " + nome + "!");

string idade_str = input("Digite sua idade: ");
int idade = int(idade_str);

if (idade >= 18) {
    println("Você é maior de idade.");
} else {
    println("Você é menor de idade.");
}

println("Teste concluído com sucesso!");"""
            
            try:
                with open(test_file, 'w', encoding='utf-8') as file:
                    file.write(test_content)
                
                # Carrega o arquivo de teste
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, test_content)
                
                self.current_file = test_file
                self.current_file_name = os.path.basename(test_file)
                self.modified = False
                self.update_title()
                
                messagebox.showinfo(
                    "Arquivo de teste criado",
                    "Um novo arquivo de teste foi criado. Clique em Executar para testá-lo."
                )
            except Exception as e:
                messagebox.showerror("Erro ao criar arquivo de teste", str(e))
    
    def create_math_example(self):
        """Cria um exemplo de script que demonstra o uso do módulo math"""
        math_example_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exemplo_math.naja")
        
        # Pergunta se deseja salvar o arquivo atual, se modificado
        if self.modified:
            save_current = messagebox.askyesno(
                "Arquivo modificado",
                "O arquivo atual foi modificado. Deseja salvá-lo antes de criar o exemplo?"
            )
            if save_current and not self.save_file():
                return
        
        # Conteúdo do exemplo
        example_content = """// Exemplo de uso do módulo math em NajaScript
import math;  // Importa o módulo math

println("Demonstração de funções matemáticas:");
println("---------------------------------");

// Funções trigonométricas
println("Seno de 45 graus: " + math.sin(math.radians(45)));
println("Cosseno de 60 graus: " + math.cos(math.radians(60)));
println("Tangente de 30 graus: " + math.tan(math.radians(30)));

println("\\nConstantes matemáticas:");
println("Pi (π): " + math.pi);
println("Euler (e): " + math.e);

// Cálculos com input do usuário
println("\\nVamos calcular a raiz quadrada de um número!");
string input_num = input("Digite um número positivo: ");
float num = float(input_num);

if (num >= 0) {
    println("Raiz quadrada de " + num + " é: " + math.sqrt(num));
    println("Seu valor ao quadrado é: " + math.pow(num, 2));
    println("Seu valor ao cubo é: " + math.pow(num, 3));
} else {
    println("Não é possível calcular a raiz quadrada de um número negativo em reais.");
}

// Arredondamento
float valor_decimal = 3.14159;
println("\\nArredondamento de " + valor_decimal + ":");
println("Arredondado para baixo: " + math.floor(valor_decimal));
println("Arredondado para cima: " + math.ceil(valor_decimal));

// Cálculo de fatorial
println("\\nVamos calcular um fatorial!");
string input_fat = input("Digite um número para calcular seu fatorial: ");
int fat_num = int(input_fat);

if (fat_num >= 0 && fat_num <= 20) {
    println(fat_num + "! = " + math.factorial(fat_num));
} else {
    println("Por favor, digite um número entre 0 e 20.");
}

println("\\nExemplo concluído com sucesso!");"""
        
        try:
            # Salva o exemplo em arquivo
            with open(math_example_file, 'w', encoding='utf-8') as file:
                file.write(example_content)
            
            # Carrega o exemplo no editor
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(tk.END, example_content)
            
            self.current_file = math_example_file
            self.current_file_name = os.path.basename(math_example_file)
            self.modified = False
            self.update_title()
            
            messagebox.showinfo(
                "Exemplo Criado",
                "O exemplo de uso do módulo math foi criado com sucesso. Você pode executá-lo agora para ver as funções matemáticas em ação."
            )
        except Exception as e:
            messagebox.showerror("Erro ao criar exemplo", str(e))
    
    def create_random_example(self):
        """Cria um exemplo de script que demonstra o uso do módulo random"""
        random_example_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exemplo_random.naja")
        
        # Pergunta se deseja salvar o arquivo atual, se modificado
        if self.modified:
            save_current = messagebox.askyesno(
                "Arquivo modificado",
                "O arquivo atual foi modificado. Deseja salvá-lo antes de criar o exemplo?"
            )
            if save_current and not self.save_file():
                return
        
        # Conteúdo do exemplo
        example_content = """// Exemplo de uso do módulo random em NajaScript
import random;  // Importa o módulo random

println("Demonstração de funções aleatórias:");
println("---------------------------------");

// Número aleatório entre 0 e 1
println("Número aleatório entre 0 e 1: " + random.random());

// Inteiro aleatório em um intervalo
int min = 1;
int max = 100;
println("Número inteiro entre " + min + " e " + max + ": " + random.randint(min, max));

// Simular jogadas de dados
println("\\nSimulação de 5 jogadas de um dado de 6 faces:");
for (int i = 0; i < 5; i++) {
    println("Jogada " + (i+1) + ": " + random.randint(1, 6));
}

// Escolher um item aleatório de uma lista
println("\\nEscolhendo um item aleatório de uma lista:");
string[] frutas = ["maçã", "banana", "laranja", "uva", "morango", "abacaxi"];
println("Frutas disponíveis: ");
for (int i = 0; i < frutas.length; i++) {
    println((i+1) + ". " + frutas[i]);
}
println("\\nFruta escolhida aleatoriamente: " + random.choice(frutas));

// Gerar uma senha aleatória
println("\\nGerando uma senha aleatória de 8 caracteres:");
string caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*";
string senha = "";
for (int i = 0; i < 8; i++) {
    int indice = random.randint(0, caracteres.length - 1);
    senha = senha + caracteres[indice];
}
println("Senha gerada: " + senha);

// Jogo de adivinhação
println("\\nVamos jogar um jogo de adivinhação!");
int numero_secreto = random.randint(1, 100);
println("Pensei em um número entre 1 e 100.");
println("Tente adivinhar!");

bool acertou = false;
int tentativas = 0;
int max_tentativas = 7;

while (!acertou && tentativas < max_tentativas) {
    tentativas++;
    string palpite_str = input("\\nTentativa " + tentativas + "/" + max_tentativas + ": Digite seu palpite: ");
    int palpite = int(palpite_str);
    
    if (palpite == numero_secreto) {
        println("PARABÉNS! Você acertou em " + tentativas + " tentativas!");
        acertou = true;
    } else if (palpite < numero_secreto) {
        println("O número secreto é MAIOR que " + palpite);
    } else {
        println("O número secreto é MENOR que " + palpite);
    }
}

if (!acertou) {
    println("\\nAh, que pena! Suas tentativas acabaram. O número secreto era: " + numero_secreto);
}

println("\\nExemplo concluído com sucesso!");"""
        
        try:
            # Salva o exemplo em arquivo
            with open(random_example_file, 'w', encoding='utf-8') as file:
                file.write(example_content)
            
            # Carrega o exemplo no editor
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(tk.END, example_content)
            
            self.current_file = random_example_file
            self.current_file_name = os.path.basename(random_example_file)
            self.modified = False
            self.update_title()
            
            messagebox.showinfo(
                "Exemplo Criado",
                "O exemplo de uso do módulo random foi criado com sucesso. Você pode executá-lo agora para ver as funções de aleatoriedade em ação."
            )
        except Exception as e:
            messagebox.showerror("Erro ao criar exemplo", str(e))
    
    def stop_execution(self):
        """Interrompe a execução do processo atual"""
        try:
            if hasattr(self, 'current_process') and self.current_process and self.current_process.poll() is None:
                try:
                    self.add_output("\n>>> Interrompendo execução...\n", "system")
                    # Em Windows, use taskkill para matar o processo com mais confiabilidade
                    if os.name == 'nt':
                        subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.current_process.pid)], 
                                      stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                    else:
                        self.current_process.kill()
                    
                    # Aguarde um pouco para o processo ser encerrado
                    for _ in range(5):
                        if self.current_process.poll() is not None:
                            break
                        time.sleep(0.2)
                        
                    # Se ainda estiver executando, forçar encerramento
                    if self.current_process.poll() is None:
                        if os.name == 'nt':
                            os.kill(self.current_process.pid, 9)  # SIGKILL equivalente
                        else:
                            os.kill(self.current_process.pid, 9)  # SIGKILL
                    
                    # Limpar a referência ao processo
                    self.current_process = None
                    
                    # Atualizar a interface
                    if hasattr(self, 'run_button') and self.run_button.winfo_exists():
                        self.run_button.pack(side=tk.RIGHT, padx=10, pady=2)
                    if hasattr(self, 'stop_button') and self.stop_button.winfo_exists():
                        self.stop_button.pack_forget()
                    
                    # Atualizar o status
                    if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                        self.status_label.config(text="Execução interrompida pelo usuário")
                    if hasattr(self, 'output_text') and self.output_text.winfo_exists():
                        self.output_text.config(background="white")
                    self.add_output("\n>>> Execução interrompida pelo usuário\n", "system")
                except Exception as e:
                    print(f"Erro ao interromper processo: {str(e)}")
                    self.add_output(f"\n>>> Erro ao interromper: {str(e)}\n", "error")
        except Exception as e:
            print(f"Erro no método stop_execution: {str(e)}")
    
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
    
    def setup_autocomplete(self):
        """Configura a funcionalidade de autocompletar"""
        # Lista de palavras para autocompletar
        self.autocomplete_keywords = [
            "int", "float", "string", "bool", "dict", "null", "void", "const", "fun", 
            "return", "if", "else", "elif", "for", "while", "do", "break", "continue", 
            "switch", "case", "default", "vecto", "list", "flux", "type", "any",
            "import", "from", "as"  # Adicionando palavras-chave para imports
        ]
        
        self.autocomplete_functions = [
            "print", "println", "input", "type", "min", "max", "vecto", "list", "dict", 
            "onChange", "printChange"
        ]
        
        self.autocomplete_literals = ["true", "false", "null"]
        
        # Módulos Python úteis para importar
        self.autocomplete_modules = [
            "math", "random", "time", "datetime", "json", "re", "os", "sys",
            "collections", "statistics", "itertools"
        ]
        
        # Funções matemáticas comuns (do módulo math)
        self.autocomplete_math_functions = [
            "math.sin", "math.cos", "math.tan", "math.asin", "math.acos", "math.atan",
            "math.sqrt", "math.pow", "math.exp", "math.log", "math.log10",
            "math.floor", "math.ceil", "math.fabs", "math.factorial", "math.gcd", 
            "math.radians", "math.degrees", "math.pi", "math.e"
        ]
        
        # Funções de random
        self.autocomplete_random_functions = [
            "random.random", "random.randint", "random.choice", "random.shuffle",
            "random.sample", "random.uniform"
        ]
        
        # Funções de time e datetime
        self.autocomplete_time_functions = [
            "time.time", "time.sleep", "datetime.now", "datetime.date", "datetime.timedelta"
        ]
        
        # Todas as palavras disponíveis para autocompletar
        self.autocomplete_words = (
            self.autocomplete_keywords + 
            self.autocomplete_functions + 
            self.autocomplete_literals +
            self.autocomplete_modules +
            self.autocomplete_math_functions +
            self.autocomplete_random_functions +
            self.autocomplete_time_functions
        )
        
        # Criar a listbox de autocompletar (inicialmente oculta)
        self.autocomplete_listbox = AutocompleteListbox(
            self.root,
            selectmode=tk.SINGLE
        )
        
        # Configurar eventos para autocompletar
        self.text_editor.bind("<KeyRelease>", self.check_autocomplete)
        self.text_editor.bind("<Tab>", self.handle_tab)
        self.text_editor.bind("<Escape>", self.hide_autocomplete)
        self.text_editor.bind("<Up>", self.navigate_autocomplete)
        self.text_editor.bind("<Down>", self.navigate_autocomplete)
        self.text_editor.bind("<Return>", self.apply_autocomplete)
        
        # Quando o usuário clica em uma sugestão
        self.autocomplete_listbox.bind("<ButtonRelease-1>", self.apply_autocomplete)
        self.autocomplete_listbox.bind("<Double-Button-1>", self.apply_autocomplete)
        
        # Flag para controlar se o autocompletar está ativo
        self.autocomplete_active = False
    
    def navigate_autocomplete(self, event):
        """Navega pela lista de sugestões de autocompletar"""
        if not self.autocomplete_active:
            return
        
        # Trata as teclas de seta para navegar na lista
        if event.keysym == "Up":
            # Move a seleção para cima
            if self.autocomplete_listbox.curselection():
                current_selection = self.autocomplete_listbox.curselection()[0]
                if current_selection > 0:
                    self.autocomplete_listbox.selection_clear(0, tk.END)
                    self.autocomplete_listbox.selection_set(current_selection - 1)
                    self.autocomplete_listbox.see(current_selection - 1)
            return "break"  # Impede o comportamento padrão
        
        elif event.keysym == "Down":
            # Move a seleção para baixo
            if self.autocomplete_listbox.curselection():
                current_selection = self.autocomplete_listbox.curselection()[0]
                if current_selection < self.autocomplete_listbox.size() - 1:
                    self.autocomplete_listbox.selection_clear(0, tk.END)
                    self.autocomplete_listbox.selection_set(current_selection + 1)
                    self.autocomplete_listbox.see(current_selection + 1)
            else:
                # Se não houver seleção, seleciona o primeiro item
                if self.autocomplete_listbox.size() > 0:
                    self.autocomplete_listbox.selection_set(0)
            return "break"  # Impede o comportamento padrão
    
    def handle_tab(self, event):
        """Gerencia a tecla Tab para autocompletar"""
        if self.autocomplete_active:
            self.apply_autocomplete(event)
            return "break"  # Impede que o tab seja inserido
        return None  # Permite o comportamento padrão do tab
    
    def check_autocomplete(self, event):
        """Verifica se deve exibir sugestões de autocompletar"""
        # Atualiza o destaque de sintaxe
        self.update_syntax(event)
        
        # Apenas mostra autocompletar para teclas alfanuméricas ou backspace
        if event.keysym in [
            "Escape", "Return", "Tab", "Up", "Down", "Left", "Right",
            "Control_L", "Control_R", "Alt_L", "Alt_R", "Shift_L", "Shift_R"
        ]:
            return
        
        # Obtém a posição atual do cursor
        current_pos = self.text_editor.index(tk.INSERT)
        line, col = map(int, current_pos.split('.'))
        
        # Obtém a linha atual completa
        line_text = self.text_editor.get(f"{line}.0", f"{line}.end")
        
        # Encontra a palavra parcial que está sendo digitada
        if col > 0:
            # Pega o texto antes do cursor na linha atual
            text_before_cursor = line_text[:col]
            
            # Encontra a última palavra parcial
            match = re.search(r'[a-zA-Z0-9_]+$', text_before_cursor)
            
            if match:
                partial_word = match.group(0)
                
                # Se a palavra parcial tiver pelo menos 2 caracteres
                if len(partial_word) >= 2:
                    # Filtra as palavras que começam com a palavra parcial
                    matches = [word for word in self.autocomplete_words if word.startswith(partial_word)]
                    
                    if matches:
                        # Atualiza e exibe a lista de sugestões
                        self.show_autocomplete(matches, current_pos, len(partial_word))
                        return
        
        # Se não encontrou sugestões ou não deve mostrar, esconde a lista
        self.hide_autocomplete(None)
    
    def show_autocomplete(self, suggestions, position, word_length):
        """Mostra a lista de sugestões de autocompletar"""
        # Limpa a lista atual
        self.autocomplete_listbox.delete(0, tk.END)
        
        # Adiciona as sugestões à lista
        for suggestion in suggestions:
            self.autocomplete_listbox.insert(tk.END, suggestion)
        
        # Seleciona o primeiro item
        if self.autocomplete_listbox.size() > 0:
            self.autocomplete_listbox.selection_set(0)
        
        # Posiciona a listbox logo abaixo da palavra atual
        x, y, width, height = self.text_editor.bbox(position)
        
        # Ajusta a posição para ficar logo abaixo do texto
        listbox_x = self.text_editor.winfo_rootx() + x
        listbox_y = self.text_editor.winfo_rooty() + y + height
        
        # Define a largura baseada no tamanho das sugestões
        max_len = max(len(s) for s in suggestions)
        self.autocomplete_listbox.config(width=max(30, max_len + 2))
        
        # Posiciona e exibe a listbox
        self.autocomplete_listbox.place(x=x, y=y+height+5)
        self.autocomplete_listbox.lift()
        
        # Salva a posição e o comprimento da palavra parcial para uso posterior
        self.autocomplete_position = position
        self.autocomplete_word_length = word_length
        self.autocomplete_active = True
    
    def hide_autocomplete(self, event=None):
        """Esconde a lista de sugestões de autocompletar"""
        self.autocomplete_listbox.place_forget()
        self.autocomplete_active = False
        return "break" if event else None
    
    def apply_autocomplete(self, event):
        """Aplica a sugestão selecionada"""
        if not self.autocomplete_active:
            return None
        
        # Obtém a sugestão selecionada
        if self.autocomplete_listbox.curselection():
            selected_index = self.autocomplete_listbox.curselection()[0]
            suggestion = self.autocomplete_listbox.get(selected_index)
            
            # Calcula a posição para substituir a palavra parcial
            line, col = map(int, self.autocomplete_position.split('.'))
            start_pos = f"{line}.{col - self.autocomplete_word_length}"
            
            # Substitui a palavra parcial pela sugestão completa
            self.text_editor.delete(start_pos, tk.INSERT)
            self.text_editor.insert(start_pos, suggestion)
            
            # Esconde a lista de sugestões
            self.hide_autocomplete()
            
            # Foca novamente no editor
            self.text_editor.focus_set()
            
            return "break"  # Impede o comportamento padrão da tecla
        return None
    
    def text_modified(self, event=None):
        """Chamado quando o texto é modificado"""
        if not self.modified:
            self.modified = True
            self.update_title()
        self.text_editor.edit_modified(False)  # Reinicia o sinalizador de modificação
    
    def key_pressed(self, event=None):
        """Manipulador para quando uma tecla é pressionada"""
        self.update_cursor_position()
    
    def update_cursor_position(self, event=None):
        """Atualiza a posição do cursor na barra de status"""
        cursor_pos = self.text_editor.index(tk.INSERT).split('.')
        line_num = cursor_pos[0]
        col_num = cursor_pos[1]
        self.cursor_position_label.config(text=f"Ln {line_num}, Col {col_num}")
    
    def update_title(self):
        """Atualiza o título da janela com o nome do arquivo atual"""
        modified_indicator = "*" if self.modified else ""
        self.root.title(f"{modified_indicator}{self.current_file_name} - NajaScript Editor")
    
    def clear_output(self):
        """Limpa a área de saída"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def add_output(self, text, tag=None):
        """Adiciona texto à área de saída com a tag especificada"""
        try:
            # Verifica se o widget de saída ainda existe
            if hasattr(self, 'output_text') and self.output_text.winfo_exists():
                self.output_text.config(state=tk.NORMAL)
                if tag:
                    self.output_text.insert(tk.END, text, tag)
                else:
                    self.output_text.insert(tk.END, text)
                self.output_text.see(tk.END)  # Rola para mostrar o último texto adicionado
                
                # Se não estivermos em modo REPL, desabilita a edição
                if not self.repl_mode:
                    self.output_text.config(state=tk.DISABLED)
        except (tk.TclError, RuntimeError, AttributeError) as e:
            # Log do erro para depuração sem quebrar a aplicação
            print(f"Erro ao adicionar saída: {str(e)}")
    
    def new_file(self):
        """Cria um novo arquivo em uma nova aba"""
        self.tabs.add_tab()
        self.status_label.config(text="Novo arquivo criado")
        return True
    
    def open_file(self):
        """Abre um arquivo existente em uma nova aba"""
        file_path = filedialog.askopenfilename(
            defaultextension=".naja",
            filetypes=[("Arquivos NajaScript", "*.naja"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            return self.open_specific_file(file_path)
        
        return False
    
    def save_file(self):
        """Salva o arquivo atual usando o sistema de abas"""
        return self.tabs.save_current_tab()
    
    def save_file_as(self):
        """Salva o arquivo atual com um novo nome"""
        # Será tratado pelo sistema de abas
        return self.tabs.save_current_tab()
    
    def run_script(self):
        """Executa o script atual usando o interpretador"""
        # Atualiza a UI para mostrar que está iniciando
        self.run_button.pack_forget()
        self.stop_button.pack(side=tk.RIGHT, padx=10, pady=2)
        
        # Executa o script
        self._run_with_option()
    
    def _run_with_option(self, option=None):
        """Executa o script com a opção especificada"""
        if self.modified or not self.current_file:
            response = messagebox.askyesno("Arquivo não salvo", 
                                         "É necessário salvar o arquivo antes de executá-lo. Deseja salvar agora?")
            if response:
                if not self.save_file():
                    # Restaura os botões se cancelar
                    self.stop_button.pack_forget()
                    self.run_button.pack(side=tk.RIGHT, padx=10, pady=2)
                    return
            else:
                # Restaura os botões se cancelar
                self.stop_button.pack_forget()
                self.run_button.pack(side=tk.RIGHT, padx=10, pady=2)
                return
        
        if self.current_file:
            self.clear_output()
            self.status_label.config(text="Executando script...")
            
            # Destaca o painel de saída para mostrar que está executando
            self.output_text.config(background="#f5f5dc")
            self.add_output(">>> INICIANDO EXECUÇÃO DO SCRIPT...\n")
            self.add_output(">>> Se você precisar fornecer dados, uma caixa de diálogo aparecerá.\n")
            self.add_output(">>> Para interromper a execução, clique no botão INTERROMPER.\n\n")
            
            # Obter caminho do script najascript.py
            najascript_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "najascript.py")
            
            try:
                # Preparar o comando - remover a opção se não for necessária
                cmd = ["python", najascript_path, self.current_file]
                if option:
                    cmd.append(option)
                
                # Executar o processo
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    text=True,
                    bufsize=1,  # Line buffered
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
                )
                
                # Guardar referência ao processo atual
                self.current_process = process
                
                # Adicionar informação de diagnóstico
                self.add_output(f">>> Executando comando: {' '.join(cmd)}\n\n")
                
                # Nova função para lidar com entrada/saída de forma interativa
                self._handle_interactive_io(process)
                
                # Restaura a UI quando terminar
                self.stop_button.pack_forget()
                self.run_button.pack(side=tk.RIGHT, padx=10, pady=2)
                
                # Retorna a cor de fundo normal
                self.output_text.config(background="white")
                
                # Limpar a referência ao processo
                self.current_process = None
                
                # Mostrar resultado da execução
                if process.returncode == 0:
                    self.status_label.config(text="Execução concluída com sucesso")
                    self.add_output("\n>>> Execução concluída com sucesso.\n")
                else:
                    self.status_label.config(text=f"Execução falhou com código: {process.returncode}")
                    self.add_output(f"\n>>> Execução falhou com código de saída: {process.returncode}\n")
            
            except Exception as e:
                # Restaura a UI em caso de erro
                self.stop_button.pack_forget()
                self.run_button.pack(side=tk.RIGHT, padx=10, pady=2)
                
                error_msg = str(e)
                self.add_output(f"\n>>> ERRO AO EXECUTAR: {error_msg}\n")
                messagebox.showerror("Erro ao executar script", error_msg)
                self.status_label.config(text="Erro ao executar script")
                self.output_text.config(background="white")
                
                # Limpar a referência ao processo
                self.current_process = None
    
    def _handle_interactive_io(self, process):
        """Gerencia entrada/saída interativa com o processo"""
        import threading
        import time
        from queue import Queue, Empty
        
        # Flag para indicar se devemos continuar processando
        processing_active = True
        
        # Filas para comunicação entre threads
        stdout_queue = Queue()
        stderr_queue = Queue()
        
        # Contadores e flags para controle
        waiting_message_limit = 5  # Limite de mensagens "Aguardando saída"
        waiting_messages_shown = 0
        help_message_shown = False
        no_data_count = 0
        start_time = time.time()
        timeout = 60  # Timeout em segundos (1 minuto)
        last_input_check_time = 0  # Para limitar a frequência de verificações
        accumulated_output = ""  # Para acumular saída e buscar padrões
        
        # Função para ler continuamente a saída do processo
        def reader_thread(stream, queue):
            try:
                for line in iter(stream.readline, ''):
                    if line and processing_active:
                        queue.put(line)
            except Exception as e:
                if processing_active:
                    queue.put(f"ERRO DE LEITURA: {str(e)}\n")
            finally:
                try:
                    stream.close()
                except:
                    pass
        
        # Inicia threads para ler stdout e stderr
        stdout_thread = threading.Thread(target=reader_thread, args=(process.stdout, stdout_queue), daemon=True)
        stderr_thread = threading.Thread(target=reader_thread, args=(process.stderr, stderr_queue), daemon=True)
        stdout_thread.start()
        stderr_thread.start()
        
        # Buffer para armazenar linhas recentes (para detectar padrões de prompt)
        recent_output = []
        max_recent_lines = 5  # Aumentamos para armazenar mais linhas recentes
        
        # Adiciona uma mensagem de debug
        self.add_output(">>> Aguardando saída do programa...\n", "system")
        
        # Função auxiliar para verificar se uma string parece um prompt de input
        def looks_like_input_prompt(text):
            # Lista expandida de palavras-chave que indicam solicitação de input
            input_keywords = [
                "input", "digite", "informe", "entre", "insira", "forneça", 
                "valor", "nome", "idade", "resposta", "número", "numero",
                "qual", "quem", "quando", "onde", "como", "por que", "quanto",
                "escolha", "opção", "opcao", "selecione", "confirme", "confirma",
                "sim/não", "s/n", "y/n", "continuar", "prosseguir", "deseja"
            ]
            
            # Verifica presença de palavras-chave
            for keyword in input_keywords:
                if keyword in text.lower():
                    return True
                
            # Verifica sintaxe de chamada de função input()
            if "input(" in text:
                return True
            
            # Verifica terminação típica de prompt
            if (text.strip().endswith(':') or text.strip().endswith('?') or 
                text.strip().endswith('...') or text.strip().endswith('>')):
                return True
            
            # Verifica se parece uma pergunta
            if '?' in text and len(text.strip()) < 100:  # Perguntas são geralmente curtas
                return True
            
            # Verifica outras características de prompts
            if text.strip() and len(text.strip().split()) < 10 and not text.strip().endswith('.'):
                return True
            
            return False
        
        # Processa a saída enquanto o processo estiver em execução
        try:
            while process.poll() is None:
                # Verificar timeout
                if time.time() - start_time > timeout:
                    self.add_output("\n>>> AVISO: Execução demorada detectada (mais de 1 minuto).\n", "system")
                    self.add_output(">>> Se o programa estiver em loop infinito, use o botão INTERROMPER.\n\n", "system")
                    # Reseta o tempo para não mostrar esta mensagem novamente
                    start_time = float('inf')
                
                data_received = False
                
                # Processa stdout
                try:
                    while True:
                        try:
                            line = stdout_queue.get_nowait()
                            data_received = True
                            waiting_messages_shown = 0  # Resetar contador quando receber dados
                            help_message_shown = False  # Resetar flag de mensagem de ajuda
                            self.add_output(line)
                            
                            # Adiciona ao buffer de saída recente
                            recent_output.append(line)
                            if len(recent_output) > max_recent_lines:
                                recent_output.pop(0)
                            
                            # Acumula saída para verificação posterior
                            accumulated_output += line
                            if len(accumulated_output) > 1000:  # Limita o tamanho
                                accumulated_output = accumulated_output[-1000:]
                            
                            # Verifica diretamente se a linha atual parece um prompt
                            is_input_prompt = looks_like_input_prompt(line)
                            
                            # Se não for um prompt claro, verifica as últimas linhas acumuladas
                            if not is_input_prompt and time.time() - last_input_check_time > 0.5:
                                # Cria uma string com as últimas linhas
                                recent_buffer = ''.join(recent_output)
                                is_input_prompt = looks_like_input_prompt(recent_buffer)
                                last_input_check_time = time.time()
                            
                            if is_input_prompt:
                                # Aguarda um pouco para garantir que todo o prompt seja exibido
                                self.root.update()
                                time.sleep(0.1)
                                
                                # Adiciona uma mensagem explícita na área de saída com destaque
                                self.add_output("\n>>> AGUARDANDO ENTRADA: ", "system")
                                
                                # Determina o texto do prompt a mostrar
                                prompt_text = line.strip()
                                if len(prompt_text) < 5 or not looks_like_input_prompt(prompt_text):
                                    # Se a linha atual for muito curta, usa o buffer recente
                                    prompt_text = recent_buffer.strip()
                                
                                # Ativa o modo REPL para entrada direta na área de saída
                                self.prompt_for_input(prompt_text)
                                
                                # Espera em um loop até que o usuário forneça a entrada
                                input_processed = False
                                input_timeout = time.time() + 300  # 5 minutos para timeout
                                
                                while not input_processed and time.time() < input_timeout:
                                    # Verifica se ainda estamos em modo REPL
                                    if not self.repl_mode:
                                        input_processed = True
                                    
                                    # Atualiza a interface para manter a responsividade
                                    self.root.update()
                                    time.sleep(0.1)
                                
                                # Se atingir o timeout, sai do modo REPL
                                if not input_processed:
                                    self.repl_mode = False
                                    self.output_text.config(state=tk.DISABLED)
                                    self.add_output("\n>>> TIMEOUT: Entrada não fornecida a tempo.\n", "error")
                                
                                # Reinicia contadores
                                no_data_count = 0
                                waiting_messages_shown = 0
                                help_message_shown = False
                                start_time = time.time()  # Reinicia o tempo de timeout
                                
                                # Limpa o buffer acumulado após o input
                                accumulated_output = ""
                                recent_output = []
                        except Empty:
                            break
                except Exception as e:
                    self.add_output(f"ERRO: {str(e)}\n", "error")
                
                # Processa stderr
                try:
                    while True:
                        try:
                            line = stderr_queue.get_nowait()
                            data_received = True
                            waiting_messages_shown = 0  # Resetar contador quando receber dados
                            help_message_shown = False  # Resetar flag de mensagem de ajuda
                            self.add_output(f"ERRO: {line}", "error")
                        except Empty:
                            break
                except Exception as e:
                    self.add_output(f"ERRO: {str(e)}\n", "error")
                
                # Se nenhum dado foi recebido neste ciclo, incrementa o contador
                if not data_received:
                    no_data_count += 1
                else:
                    no_data_count = 0
                    
                # Verificação adicional periódica para casos onde não temos nova saída,
                # mas já pode existir um prompt na saída acumulada esperando por input
                if no_data_count >= 5 and accumulated_output and time.time() - last_input_check_time > 1.0:
                    last_input_check_time = time.time()
                    # Verifica se a saída acumulada parece conter um prompt de input
                    if looks_like_input_prompt(accumulated_output):
                        self.add_output("\n>>> Possível solicitação de entrada detectada na saída anterior.\n", "system")
                        
                        # Ativa o modo REPL para entrada direta na área de saída
                        self.prompt_for_input(accumulated_output.strip())
                        
                        # Espera em um loop até que o usuário forneça a entrada
                        input_processed = False
                        input_timeout = time.time() + 300  # 5 minutos para timeout
                        
                        while not input_processed and time.time() < input_timeout:
                            # Verifica se ainda estamos em modo REPL
                            if not self.repl_mode:
                                input_processed = True
                            
                            # Atualiza a interface para manter a responsividade
                            self.root.update()
                            time.sleep(0.1)
                        
                        # Se atingir o timeout, sai do modo REPL
                        if not input_processed:
                            self.repl_mode = False
                            self.output_text.config(state=tk.DISABLED)
                            self.add_output("\n>>> TIMEOUT: Entrada não fornecida a tempo.\n", "error")
                        
                        # Reinicia contadores
                        no_data_count = 0
                        waiting_messages_shown = 0
                        help_message_shown = False
                        
                        # Limpa o buffer acumulado após o input
                        accumulated_output = ""
                        recent_output = []
                    
                # Se não receber dados por muito tempo e o processo ainda estiver rodando,
                # adiciona indicadores de que está aguardando
                if no_data_count >= 10:  # ~1 segundo sem dados
                    no_data_count = 0
                    
                    # Limita o número de mensagens "Aguardando saída"
                    if waiting_messages_shown < waiting_message_limit:
                        waiting_messages_shown += 1
                        self.add_output(">>> Aguardando saída ou término do programa...\n", "system")
                    elif not help_message_shown:
                        # Após alcançar o limite, mostrar mensagem de ajuda
                        self.add_output("\n>>> O programa parece estar preso num loop infinito.\n", "system")
                        self.add_output(">>> Se o programa não está respondendo, clique no botão INTERROMPER\n", "system")
                        self.add_output(">>> para encerrar a execução e tente novamente.\n\n", "system")
                        help_message_shown = True
                
                # Atualiza a interface para manter a responsividade
                try:
                    self.root.update()
                except:
                    # Se a janela foi fechada, interrompe o processamento
                    processing_active = False
                    break
                    
                time.sleep(0.1)
            
            # Marca que não estamos mais processando ativamente
            processing_active = False
            
            # Certifica-se de coletar qualquer saída restante
            time.sleep(0.5)
            
            # Verifica se ainda há dados nas filas
            try:
                while not stdout_queue.empty():
                    line = stdout_queue.get_nowait()
                    self.add_output(line)
            except Exception as e:
                self.add_output(f"ERRO: {str(e)}\n", "error")
                
            try:
                while not stderr_queue.empty():
                    line = stderr_queue.get_nowait()
                    self.add_output(f"ERRO: {line}", "error")
            except Exception as e:
                self.add_output(f"ERRO: {str(e)}\n", "error")
            
            # Aguarda as threads terminarem com limite de tempo
            stdout_thread.join(timeout=1)
            stderr_thread.join(timeout=1)
        
        except Exception as e:
            processing_active = False
            self.add_output(f"\n>>> ERRO NO PROCESSAMENTO DE E/S: {str(e)}\n", "error")
        
        finally:
            # Garantir que as threads de leitura sejam interrompidas
            processing_active = False
            
            # Certifique-se de que não estamos mais no modo REPL
            self.repl_mode = False
            self.output_text.config(state=tk.DISABLED)
    
    def _handle_repl_input(self, event=None):
        """Lida com o evento de pressionar Enter no modo REPL"""
        if not self.repl_mode or not hasattr(self, 'current_process'):
            return
        
        try:
            # Obter o texto da área de entrada
            input_text = self.output_text.get(self.input_start, "end-1c")
            
            # Verificar se há um prompt no início e removê-lo
            if input_text.startswith(">>> "):
                input_text = input_text[4:]
            
            # Adicionar uma nova linha após o input
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "\n")
            self.output_text.config(state=tk.DISABLED)
            
            # Enviar o texto para o processo
            if hasattr(self, 'current_process') and self.current_process and self.current_process.poll() is None:
                self.current_process.stdin.write(input_text + "\n")
                self.current_process.stdin.flush()
            
            # Sair do modo REPL
            self.repl_mode = False
            
            # Desativar edição da área de saída
            self.output_text.config(state=tk.DISABLED)
            
            return "break"  # Impede o comportamento padrão da tecla Enter
        except Exception as e:
            self.add_output(f"\nERRO AO PROCESSAR ENTRADA: {str(e)}\n", "error")
            self.repl_mode = False
            self.output_text.config(state=tk.DISABLED)
            return "break"
    
    def prompt_for_input(self, prompt_text=""):
        """Exibe um prompt na área de saída e habilita a entrada de texto"""
        # Adiciona o prompt visível
        if not prompt_text:
            prompt_text = "Entrada requerida"
        
        self.add_output("\n>>> ", "prompt")
        
        # Marca o início da região de input
        self.input_start = self.output_text.index(tk.END)
        
        # Ativa o modo REPL
        self.repl_mode = True
        
        # Habilita a edição da área de saída
        self.output_text.config(state=tk.NORMAL)
        
        # Foca na área de saída
        self.output_text.focus_set()
    
    def exit_editor(self):
        """Sai do editor"""
        if self.modified:
            response = messagebox.askyesnocancel("Arquivo modificado", 
                                              "O arquivo atual foi modificado. Deseja salvar as alterações?")
            if response is None:  # Cancelar
                return
            if response:  # Sim
                if not self.save_file():
                    return
        
        self.root.destroy()
    
    def undo(self):
        """Desfaz a última operação de edição"""
        try:
            self.text_editor.edit_undo()
        except tk.TclError:
            pass
    
    def redo(self):
        """Refaz a última operação desfeita"""
        try:
            self.text_editor.edit_redo()
        except tk.TclError:
            pass
    
    def cut(self):
        """Recorta o texto selecionado"""
        try:
            self.text_editor.event_generate("<<Cut>>")
        except:
            pass
    
    def copy(self):
        """Copia o texto selecionado"""
        try:
            self.text_editor.event_generate("<<Copy>>")
        except:
            pass
    
    def paste(self):
        """Cola o texto da área de transferência"""
        try:
            self.text_editor.event_generate("<<Paste>>")
        except:
            pass
    
    def show_about(self):
        """Mostra informações sobre o editor"""
        messagebox.showinfo("Sobre o NajaScript Editor", 
                          "NajaScript Editor v1.0\n\n"
                          "Um ambiente de desenvolvimento integrado (IDE) simples para a linguagem NajaScript.\n\n"
                          "©2023 NajaScript Team")
    
    def setup_syntax_highlighting(self):
        """Configura o destaque de sintaxe para NajaScript"""
        # Palavras-chave da linguagem
        keywords = [
            "int", "float", "string", "bool", "dict", "null", "void", "const", "fun", 
            "return", "if", "else", "elif", "for", "while", "do", "break", "continue", 
            "switch", "case", "default", "vecto", "list", "flux", "type", "any",
            "import", "from", "as"  # Adicionando palavras-chave para imports
        ]
        
        # Funções nativas
        builtins = [
            "print", "println", "input", "type", "min", "max", "vecto", "list", "dict", 
            "onChange", "printChange"
        ]
        
        # Valores literais
        literals = ["true", "false", "null"]
        
        # Módulos
        modules = [
            "math", "random", "time", "datetime", "json", "re", "os", "sys",
            "collections", "statistics", "itertools"
        ]
        
        # Configurar as tags para coloração
        self.text_editor.tag_configure("keyword", foreground="#0000FF")  # Azul para palavras-chave
        self.text_editor.tag_configure("builtin", foreground="#8A2BE2")  # Roxo para funções nativas
        self.text_editor.tag_configure("literal", foreground="#008000")  # Verde para literais
        self.text_editor.tag_configure("comment", foreground="#808080", font=("Consolas", 11, "italic"))  # Cinza itálico para comentários
        self.text_editor.tag_configure("string", foreground="#A31515")  # Vermelho escuro para strings
        self.text_editor.tag_configure("number", foreground="#008080")  # Verde azulado para números
        self.text_editor.tag_configure("module", foreground="#FF8C00")  # Laranja para módulos
        
        # Padrões para expressões regulares
        self.patterns = [
            (r'\b(' + '|'.join(keywords) + r')\b', "keyword"),
            (r'\b(' + '|'.join(builtins) + r')\b', "builtin"),
            (r'\b(' + '|'.join(literals) + r')\b', "literal"),
            (r'\b(' + '|'.join(modules) + r')\b', "module"),  # Módulos em laranja
            (r'//.*$', "comment"),  # Comentários de linha única
            (r'\"([^\"]*)\"', "string"),  # Strings com aspas duplas
            (r'\'([^\']*)\'', "string"),  # Strings com aspas simples
            (r'\b\d+\b', "number"),  # Números inteiros
            (r'\b\d+\.\d+\b', "number")  # Números de ponto flutuante
        ]
        
        # Adicionar tratamento de eventos para atualizar a coloração da sintaxe
        self.text_editor.bind("<KeyRelease>", self.update_syntax)
    
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
    
    def run_input_test(self):
        """Executa o arquivo de teste de input"""
        # Verifica se o arquivo de teste existe
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "teste_input.naja")
        
        if os.path.exists(test_file):
            # Salva o arquivo atual se necessário
            if self.modified:
                save_current = messagebox.askyesno(
                    "Arquivo modificado",
                    "O arquivo atual foi modificado. Deseja salvá-lo antes de executar o teste?"
                )
                if save_current and not self.save_file():
                    return
            
            # Abre o arquivo de teste
            try:
                with open(test_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Salva o estado atual
                old_file = self.current_file
                old_file_name = self.current_file_name
                
                # Carrega o arquivo de teste
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, content)
                
                self.current_file = test_file
                self.current_file_name = os.path.basename(test_file)
                self.modified = False
                self.update_title()
                
                # Executa o teste
                self.run_script()
                
                # Pergunta se deseja restaurar o arquivo anterior
                if old_file and old_file != test_file:
                    restore = messagebox.askyesno(
                        "Restaurar arquivo",
                        "Deseja restaurar o arquivo anterior?"
                    )
                    if restore:
                        with open(old_file, 'r', encoding='utf-8') as file:
                            content = file.read()
                        
                        self.text_editor.delete(1.0, tk.END)
                        self.text_editor.insert(tk.END, content)
                        
                        self.current_file = old_file
                        self.current_file_name = old_file_name
                        self.modified = False
                        self.update_title()
            
            except Exception as e:
                messagebox.showerror("Erro ao executar teste", str(e))
        else:
            messagebox.showwarning(
                "Arquivo de teste não encontrado",
                f"O arquivo de teste '{test_file}' não foi encontrado. Criando um novo arquivo de teste."
            )
            
            # Cria o arquivo de teste com a sintaxe correta para NajaScript
            # Sem função main e sem comentários no início
            test_content = """println("Teste de funcionalidade de input interativo");

string nome = input("Digite seu nome: ");
println("Olá, " + nome + "!");

string idade_str = input("Digite sua idade: ");
int idade = int(idade_str);

if (idade >= 18) {
    println("Você é maior de idade.");
} else {
    println("Você é menor de idade.");
}

println("Teste concluído com sucesso!");"""
            
            try:
                with open(test_file, 'w', encoding='utf-8') as file:
                    file.write(test_content)
                
                # Carrega o arquivo de teste
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, test_content)
                
                self.current_file = test_file
                self.current_file_name = os.path.basename(test_file)
                self.modified = False
                self.update_title()
                
                messagebox.showinfo(
                    "Arquivo de teste criado",
                    "Um novo arquivo de teste foi criado. Clique em Executar para testá-lo."
                )
            except Exception as e:
                messagebox.showerror("Erro ao criar arquivo de teste", str(e))
    
    def create_math_example(self):
        """Cria um exemplo de script que demonstra o uso do módulo math"""
        math_example_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exemplo_math.naja")
        
        # Pergunta se deseja salvar o arquivo atual, se modificado
        if self.modified:
            save_current = messagebox.askyesno(
                "Arquivo modificado",
                "O arquivo atual foi modificado. Deseja salvá-lo antes de criar o exemplo?"
            )
            if save_current and not self.save_file():
                return
        
        # Conteúdo do exemplo
        example_content = """// Exemplo de uso do módulo math em NajaScript
import math;  // Importa o módulo math

println("Demonstração de funções matemáticas:");
println("---------------------------------");

// Funções trigonométricas
println("Seno de 45 graus: " + math.sin(math.radians(45)));
println("Cosseno de 60 graus: " + math.cos(math.radians(60)));
println("Tangente de 30 graus: " + math.tan(math.radians(30)));

println("\\nConstantes matemáticas:");
println("Pi (π): " + math.pi);
println("Euler (e): " + math.e);

// Cálculos com input do usuário
println("\\nVamos calcular a raiz quadrada de um número!");
string input_num = input("Digite um número positivo: ");
float num = float(input_num);

if (num >= 0) {
    println("Raiz quadrada de " + num + " é: " + math.sqrt(num));
    println("Seu valor ao quadrado é: " + math.pow(num, 2));
    println("Seu valor ao cubo é: " + math.pow(num, 3));
} else {
    println("Não é possível calcular a raiz quadrada de um número negativo em reais.");
}

// Arredondamento
float valor_decimal = 3.14159;
println("\\nArredondamento de " + valor_decimal + ":");
println("Arredondado para baixo: " + math.floor(valor_decimal));
println("Arredondado para cima: " + math.ceil(valor_decimal));

// Cálculo de fatorial
println("\\nVamos calcular um fatorial!");
string input_fat = input("Digite um número para calcular seu fatorial: ");
int fat_num = int(input_fat);

if (fat_num >= 0 && fat_num <= 20) {
    println(fat_num + "! = " + math.factorial(fat_num));
} else {
    println("Por favor, digite um número entre 0 e 20.");
}

println("\\nExemplo concluído com sucesso!");"""
        
        try:
            # Salva o exemplo em arquivo
            with open(math_example_file, 'w', encoding='utf-8') as file:
                file.write(example_content)
            
            # Carrega o exemplo no editor
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(tk.END, example_content)
            
            self.current_file = math_example_file
            self.current_file_name = os.path.basename(math_example_file)
            self.modified = False
            self.update_title()
            
            messagebox.showinfo(
                "Exemplo Criado",
                "O exemplo de uso do módulo math foi criado com sucesso. Você pode executá-lo agora para ver as funções matemáticas em ação."
            )
        except Exception as e:
            messagebox.showerror("Erro ao criar exemplo", str(e))
    
    def create_random_example(self):
        """Cria um exemplo de script que demonstra o uso do módulo random"""
        random_example_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exemplo_random.naja")
        
        # Pergunta se deseja salvar o arquivo atual, se modificado
        if self.modified:
            save_current = messagebox.askyesno(
                "Arquivo modificado",
                "O arquivo atual foi modificado. Deseja salvá-lo antes de criar o exemplo?"
            )
            if save_current and not self.save_file():
                return
        
        # Conteúdo do exemplo
        example_content = """// Exemplo de uso do módulo random em NajaScript
import random;  // Importa o módulo random

println("Demonstração de funções aleatórias:");
println("---------------------------------");

// Número aleatório entre 0 e 1
println("Número aleatório entre 0 e 1: " + random.random());

// Inteiro aleatório em um intervalo
int min = 1;
int max = 100;
println("Número inteiro entre " + min + " e " + max + ": " + random.randint(min, max));

// Simular jogadas de dados
println("\\nSimulação de 5 jogadas de um dado de 6 faces:");
for (int i = 0; i < 5; i++) {
    println("Jogada " + (i+1) + ": " + random.randint(1, 6));
}

// Escolher um item aleatório de uma lista
println("\\nEscolhendo um item aleatório de uma lista:");
string[] frutas = ["maçã", "banana", "laranja", "uva", "morango", "abacaxi"];
println("Frutas disponíveis: ");
for (int i = 0; i < frutas.length; i++) {
    println((i+1) + ". " + frutas[i]);
}
println("\\nFruta escolhida aleatoriamente: " + random.choice(frutas));

// Gerar uma senha aleatória
println("\\nGerando uma senha aleatória de 8 caracteres:");
string caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*";
string senha = "";
for (int i = 0; i < 8; i++) {
    int indice = random.randint(0, caracteres.length - 1);
    senha = senha + caracteres[indice];
}
println("Senha gerada: " + senha);

// Jogo de adivinhação
println("\\nVamos jogar um jogo de adivinhação!");
int numero_secreto = random.randint(1, 100);
println("Pensei em um número entre 1 e 100.");
println("Tente adivinhar!");

bool acertou = false;
int tentativas = 0;
int max_tentativas = 7;

while (!acertou && tentativas < max_tentativas) {
    tentativas++;
    string palpite_str = input("\\nTentativa " + tentativas + "/" + max_tentativas + ": Digite seu palpite: ");
    int palpite = int(palpite_str);
    
    if (palpite == numero_secreto) {
        println("PARABÉNS! Você acertou em " + tentativas + " tentativas!");
        acertou = true;
    } else if (palpite < numero_secreto) {
        println("O número secreto é MAIOR que " + palpite);
    } else {
        println("O número secreto é MENOR que " + palpite);
    }
}

if (!acertou) {
    println("\\nAh, que pena! Suas tentativas acabaram. O número secreto era: " + numero_secreto);
}

println("\\nExemplo concluído com sucesso!");"""
        
        try:
            # Salva o exemplo em arquivo
            with open(random_example_file, 'w', encoding='utf-8') as file:
                file.write(example_content)
            
            # Carrega o exemplo no editor
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(tk.END, example_content)
            
            self.current_file = random_example_file
            self.current_file_name = os.path.basename(random_example_file)
            self.modified = False
            self.update_title()
            
            messagebox.showinfo(
                "Exemplo Criado",
                "O exemplo de uso do módulo random foi criado com sucesso. Você pode executá-lo agora para ver as funções de aleatoriedade em ação."
            )
        except Exception as e:
            messagebox.showerror("Erro ao criar exemplo", str(e))
    
    def stop_execution(self):
        """Interrompe a execução do processo atual"""
        try:
            if hasattr(self, 'current_process') and self.current_process and self.current_process.poll() is None:
                try:
                    self.add_output("\n>>> Interrompendo execução...\n", "system")
                    # Em Windows, use taskkill para matar o processo com mais confiabilidade
                    if os.name == 'nt':
                        subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.current_process.pid)], 
                                      stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                    else:
                        self.current_process.kill()
                    
                    # Aguarde um pouco para o processo ser encerrado
                    for _ in range(5):
                        if self.current_process.poll() is not None:
                            break
                        time.sleep(0.2)
                        
                    # Se ainda estiver executando, forçar encerramento
                    if self.current_process.poll() is None:
                        if os.name == 'nt':
                            os.kill(self.current_process.pid, 9)  # SIGKILL equivalente
                        else:
                            os.kill(self.current_process.pid, 9)  # SIGKILL
                    
                    # Limpar a referência ao processo
                    self.current_process = None
                    
                    # Atualizar a interface
                    if hasattr(self, 'run_button') and self.run_button.winfo_exists():
                        self.run_button.pack(side=tk.RIGHT, padx=10, pady=2)
                    if hasattr(self, 'stop_button') and self.stop_button.winfo_exists():
                        self.stop_button.pack_forget()
                    
                    # Atualizar o status
                    if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                        self.status_label.config(text="Execução interrompida pelo usuário")
                    if hasattr(self, 'output_text') and self.output_text.winfo_exists():
                        self.output_text.config(background="white")
                    self.add_output("\n>>> Execução interrompida pelo usuário\n", "system")
                except Exception as e:
                    print(f"Erro ao interromper processo: {str(e)}")
                    self.add_output(f"\n>>> Erro ao interromper: {str(e)}\n", "error")
        except Exception as e:
            print(f"Erro no método stop_execution: {str(e)}")

def main():
    root = tk.Tk()
    app = NajaScriptEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main() 