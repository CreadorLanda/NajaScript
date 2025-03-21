import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import re
import os

class AutocompleteListbox(tk.Listbox):
    """Custom listbox for autocomplete suggestions"""
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
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NajaScript Editor")
        self.root.geometry("1000x700")
        
        # Current file info
        self.current_file = None
        self.current_file_name = "Untitled"
        self.modified = False
        
        # Setup UI components
        self.create_menu()
        self.create_toolbar() 
        self.create_main_area()
        self.create_status_bar()
        
        # Configure syntax highlighting
        self.setup_syntax_highlighting()
        
        # Configure autocomplete
        self.setup_autocomplete()
        
        # Bind events
        self.bind_events()

    def create_menu(self):
        """Creates the application's menu"""
        self.menu_bar = tk.Menu(self.root)
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_editor)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=self.menu_bar)
    
    def create_toolbar(self):
        """Creates the toolbar for the editor"""
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        # Example buttons
        new_btn = ttk.Button(self.toolbar, text="New", command=self.new_file)
        new_btn.pack(side=tk.LEFT, padx=2, pady=2)
        open_btn = ttk.Button(self.toolbar, text="Open", command=self.open_file)
        open_btn.pack(side=tk.LEFT, padx=2, pady=2)
        save_btn = ttk.Button(self.toolbar, text="Save", command=self.save_file)
        save_btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def create_main_area(self):
        """Creates the main editor area with line numbers and output panel"""
        # Main split pane
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)
        
        # Editor frame with line numbers
        editor_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(editor_frame, weight=3)
        
        # Line numbers
        self.line_numbers = tk.Text(editor_frame, width=4, padx=3, takefocus=0,
                                  border=0, background='#f0f0f0',
                                  state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Main text editor
        self.text_editor = scrolledtext.ScrolledText(
            editor_frame, 
            wrap=tk.WORD,
            undo=True,
            font=("Consolas", 11)
        )
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Output area
        output_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(output_frame, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            height=8,
            font=("Consolas", 10)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def create_status_bar(self):
        """Creates a status bar at the bottom of the window"""
        self.status_bar = ttk.Label(self.root, text="Ready", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_syntax_highlighting(self):
        """Configure NajaScript syntax highlighting"""
        # Keywords
        self.keywords = [
            "int", "float", "string", "bool", "dict", "null", "void", 
            "const", "fun", "return", "if", "else", "elif", "while", 
            "for", "break", "continue", "import", "from", "as"
        ]
        
        # Built-in functions
        self.builtins = [
            "print", "println", "input", "type", "min", "max",
            "list", "dict", "int", "float", "string", "bool"
        ]

        # Configure tags
        self.text_editor.tag_configure("keyword", foreground="#0000FF")
        self.text_editor.tag_configure("builtin", foreground="#8A2BE2")
        self.text_editor.tag_configure("string", foreground="#A31515")
        self.text_editor.tag_configure("comment", foreground="#008000")
        self.text_editor.tag_configure("number", foreground="#098658")

        # Bind syntax highlighting event
        self.text_editor.bind("<KeyRelease>", self.highlight_syntax)

    def setup_autocomplete(self):
        """Setup autocomplete functionality"""
        self.autocomplete_words = (
            self.keywords + 
            self.builtins + 
            ["true", "false", "null"]
        )
        
        self.autocomplete_listbox = AutocompleteListbox(
            self.root,
            selectmode=tk.SINGLE
        )
        
        # Bind autocomplete events
        self.text_editor.bind("<KeyRelease>", self.check_autocomplete)
        self.text_editor.bind("<Tab>", self.handle_tab)
        self.text_editor.bind("<Escape>", self.hide_autocomplete)

    def bind_events(self):
        """Bind additional events such as text modifications"""
        self.text_editor.bind("<<Modified>>", self.text_modified)

    def highlight_syntax(self, event=None):
        """Update syntax highlighting"""
        # Remove existing tags
        for tag in ["keyword", "builtin", "string", "comment", "number"]:
            self.text_editor.tag_remove(tag, "1.0", tk.END)

        content = self.text_editor.get("1.0", tk.END)
        
        # Highlight keywords
        for keyword in self.keywords:
            self.highlight_pattern(f"\\b{keyword}\\b", "keyword")
            
        # Highlight built-in functions
        for builtin in self.builtins:
            self.highlight_pattern(f"\\b{builtin}\\b", "builtin")
            
        # Highlight strings
        self.highlight_pattern(r'"[^"]*"', "string")
        self.highlight_pattern(r"'[^']*'", "string")
        
        # Highlight comments
        self.highlight_pattern(r"//.*$", "comment")
        
        # Highlight numbers
        self.highlight_pattern(r"\b\d+\b", "number")
        self.highlight_pattern(r"\b\d*\.\d+\b", "number")

    def highlight_pattern(self, pattern, tag):
        """Apply syntax highlighting pattern"""
        content = self.text_editor.get("1.0", tk.END)
        for match in re.finditer(pattern, content, re.MULTILINE):
            start = "1.0 + %dc" % match.start()
            end = "1.0 + %dc" % match.end()
            self.text_editor.tag_add(tag, start, end)

    # Placeholder methods for missing functionality

    def new_file(self):
        """Creates a new file"""
        self.text_editor.delete("1.0", tk.END)
        self.current_file = None
        self.current_file_name = "Untitled"
        self.modified = False
        self.status_bar.config(text="New file created")

    def open_file(self):
        """Opens an existing file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("NajaScript Files", "*.naja"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert(tk.END, content)
            self.current_file = file_path
            self.current_file_name = os.path.basename(file_path)
            self.modified = False
            self.status_bar.config(text=f"Opened {self.current_file_name}")

    def save_file(self):
        """Saves the current file"""
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        """Saves the file with a new name"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".naja",
            filetypes=[("NajaScript Files", "*.naja"), ("All Files", "*.*")]
        )
        if file_path:
            self._save_to_file(file_path)
            self.current_file = file_path
            self.current_file_name = os.path.basename(file_path)
            self.status_bar.config(text=f"Saved as {self.current_file_name}")

    def _save_to_file(self, file_path):
        """Helper to write current text to file"""
        content = self.text_editor.get("1.0", tk.END)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        self.modified = False

    def exit_editor(self):
        """Exits the editor"""
        self.root.quit()

    def text_modified(self, event=None):
        """Handles the modified state of the document"""
        self.modified = self.text_editor.edit_modified()
        self.text_editor.edit_modified(False)
    
    def check_autocomplete(self, event):
        """Stub for autocomplete checking"""
        # Real implementation would filter self.autocomplete_words based on current word
        pass

    def handle_tab(self, event):
        """Stub for Tab key handling during autocomplete"""
        # Real implementation would insert the completion
        return "break"

    def hide_autocomplete(self, event=None):
        """Stub to hide autocomplete suggestions"""
        self.autocomplete_listbox.place_forget()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    editor = NajaScriptEditor()
    editor.run()