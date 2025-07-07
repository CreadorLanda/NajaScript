import os
import shutil
import datetime

class FileSystemModule:
    """Módulo para manipulação de arquivos e diretórios no sistema de arquivos"""
    
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self._register_functions()
    
    def _register_functions(self):
        # Registrar todas as funções nativas do sistema de arquivos
        fs_functions = {
            "_fs_getDirAtual": self.get_dir_atual,
            "_fs_setDirAtual": self.set_dir_atual,
            "_fs_listarArquivos": self.listar_arquivos,
            "_fs_listarDiretorios": self.listar_diretorios,
            "_fs_listarTudo": self.listar_tudo,
            "_fs_existe": self.existe,
            "_fs_ehArquivo": self.eh_arquivo,
            "_fs_ehDiretorio": self.eh_diretorio,
            "_fs_criarDiretorio": self.criar_diretorio,
            "_fs_removerDiretorio": self.remover_diretorio,
            "_fs_lerArquivo": self.ler_arquivo,
            "_fs_escreverArquivo": self.escrever_arquivo,
            "_fs_copiarArquivo": self.copiar_arquivo,
            "_fs_moverArquivo": self.mover_arquivo,
            "_fs_removerArquivo": self.remover_arquivo,
            "_fs_infoArquivo": self.info_arquivo
        }
        
        for name, func in fs_functions.items():
            self.interpreter._native_functions[name] = func
    
    def get_dir_atual(self):
        """Obtém o diretório de trabalho atual"""
        return os.getcwd()
    
    def set_dir_atual(self, path):
        """Define o diretório de trabalho atual"""
        try:
            os.chdir(path)
            return True
        except Exception as e:
            return False
    
    def listar_arquivos(self, directory):
        """Lista os arquivos em um diretório"""
        try:
            return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        except Exception as e:
            return []
    
    def listar_diretorios(self, directory):
        """Lista os diretórios em um caminho"""
        try:
            return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
        except Exception as e:
            return []
    
    def listar_tudo(self, directory):
        """Lista todos os arquivos e diretórios em um caminho"""
        try:
            return os.listdir(directory)
        except Exception as e:
            return []
    
    def existe(self, path):
        """Verifica se um caminho existe"""
        return os.path.exists(path)
    
    def eh_arquivo(self, path):
        """Verifica se um caminho é um arquivo"""
        return os.path.isfile(path)
    
    def eh_diretorio(self, path):
        """Verifica se um caminho é um diretório"""
        return os.path.isdir(path)
    
    def criar_diretorio(self, path):
        """Cria um novo diretório"""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            return False
    
    def remover_diretorio(self, path, recursive=False):
        """Remove um diretório"""
        try:
            if recursive:
                shutil.rmtree(path)
            else:
                os.rmdir(path)
            return True
        except Exception as e:
            return False
    
    def ler_arquivo(self, path):
        """Lê o conteúdo de um arquivo como texto"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return None
    
    def escrever_arquivo(self, path, content, append=False):
        """Escreve texto em um arquivo"""
        try:
            mode = 'a' if append else 'w'
            with open(path, mode, encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False
    
    def copiar_arquivo(self, source, destination):
        """Copia um arquivo"""
        try:
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            return False
    
    def mover_arquivo(self, source, destination):
        """Move um arquivo"""
        try:
            shutil.move(source, destination)
            return True
        except Exception as e:
            return False
    
    def remover_arquivo(self, path):
        """Remove um arquivo"""
        try:
            os.remove(path)
            return True
        except Exception as e:
            return False
    
    def info_arquivo(self, path):
        """Obtém informações sobre um arquivo"""
        try:
            stats = os.stat(path)
            return {
                "tamanho": stats.st_size,
                "criado": datetime.datetime.fromtimestamp(stats.st_ctime).isoformat(),
                "modificado": datetime.datetime.fromtimestamp(stats.st_mtime).isoformat(),
                "acessado": datetime.datetime.fromtimestamp(stats.st_atime).isoformat()
            }
        except Exception as e:
            return None 