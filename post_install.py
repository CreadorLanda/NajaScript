import os
import sys
import subprocess
import venv

def setup_environment():
    # Obtém o diretório de instalação
    install_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Cria o ambiente virtual
    venv_path = os.path.join(install_dir, 'venv')
    if not os.path.exists(venv_path):
        print("Criando ambiente virtual...")
        venv.create(venv_path, with_pip=True)
    
    # Obtém o caminho do pip no ambiente virtual
    if sys.platform == 'win32':
        pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe')
    else:
        pip_path = os.path.join(venv_path, 'bin', 'pip')
    
    # Instala as dependências
    print("Instalando dependências...")
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)
    
    # Copia os módulos para o ambiente virtual
    print("Configurando módulos...")
    site_packages = os.path.join(venv_path, 'Lib', 'site-packages')
    for module in ['lexer.py', 'parser_naja.py', 'interpreter.py', 'ast_nodes.py', 
                  'naja_bytecode.py', 'environment.py']:
        src = os.path.join(install_dir, module)
        dst = os.path.join(site_packages, module)
        if os.path.exists(src):
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print("Configuração concluída!")

if __name__ == '__main__':
    setup_environment() 