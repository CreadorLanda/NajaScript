#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste do NajaScript Package Manager
Script para testar todas as funcionalidades do package manager
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Adicionar o diretório atual ao path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_package_manager():
    """Testar todas as funcionalidades do package manager"""
    
    print("🧪 Testando NajaScript Package Manager")
    print("=" * 50)
    
    # Criar diretório temporário para testes
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir) / "test_project"
        test_dir.mkdir()
        
        print(f"📁 Diretório de teste: {test_dir}")
        
        # Mover para o diretório de teste
        original_cwd = os.getcwd()
        os.chdir(test_dir)
        
        try:
            from naja_github_package_manager import NajaGitHubPackageManager
            
            # Criar instância do package manager
            pm = NajaGitHubPackageManager()
            
            # Teste 1: Inicializar projeto
            print("\n1️⃣ Testando inicialização de projeto...")
            success = pm.init("projeto-teste")
            print(f"   Resultado: {'✅' if success else '❌'}")
            
            # Verificar se os arquivos foram criados
            if (test_dir / "naja_packages.json").exists():
                print("   ✅ naja_packages.json criado")
            else:
                print("   ❌ naja_packages.json não encontrado")
            
            if (test_dir / "main.naja").exists():
                print("   ✅ main.naja criado")
            else:
                print("   ❌ main.naja não encontrado")
            
            # Teste 2: Listar pacotes (deve estar vazio)
            print("\n2️⃣ Testando listagem de pacotes...")
            pm.list_packages()
            
            # Teste 3: Tentar instalar um pacote (vai criar template)
            print("\n3️⃣ Testando instalação de pacote...")
            success = pm.install("pacote-teste", "1.0.0")
            print(f"   Resultado: {'✅' if success else '❌'}")
            
            # Verificar se o pacote foi "instalado" (template criado)
            from naja_github_package_manager import NAJA_PACKAGES_DIR
            package_dir = test_dir / NAJA_PACKAGES_DIR / "pacote-teste"
            if package_dir.exists():
                print("   ✅ Diretório do pacote criado")
                
                if (package_dir / "index.naja").exists():
                    print("   ✅ index.naja do pacote criado")
                else:
                    print("   ❌ index.naja do pacote não encontrado")
            else:
                print("   ❌ Diretório do pacote não criado")
            
            # Teste 4: Listar pacotes novamente (deve mostrar o pacote instalado)
            print("\n4️⃣ Testando listagem após instalação...")
            pm.list_packages()
            
            # Teste 5: Pesquisar pacotes
            print("\n5️⃣ Testando pesquisa de pacotes...")
            pm.search("exemplo")
            
            # Teste 6: Desinstalar pacote
            print("\n6️⃣ Testando desinstalação de pacote...")
            success = pm.uninstall("pacote-teste")
            print(f"   Resultado: {'✅' if success else '❌'}")
            
            # Verificar se o pacote foi removido
            if not package_dir.exists():
                print("   ✅ Pacote removido com sucesso")
            else:
                print("   ❌ Pacote ainda existe")
            
            # Teste 7: Verificar configuração
            print("\n7️⃣ Testando configuração...")
            config = pm.config
            if config.get("registry", {}).get("url") == "https://github.com/NajaScript/Naja":
                print("   ✅ URL do registry configurada corretamente")
            else:
                print("   ❌ URL do registry incorreta")
            
            print("\n🎉 Testes concluídos!")
            
        except Exception as e:
            print(f"\n❌ Erro durante os testes: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            # Voltar para o diretório original
            os.chdir(original_cwd)

def test_cli():
    """Testar interface de linha de comando"""
    
    print("\n🖥️ Testando Interface de Linha de Comando")
    print("=" * 50)
    
    # Importar e testar o CLI
    try:
        from naja_github_package_manager import main
        
        # Simular argumentos da linha de comando
        test_commands = [
            ["--help"],
            ["init", "--help"],
            ["install", "--help"],
            ["search", "--help"]
        ]
        
        for cmd in test_commands:
            print(f"\n🔸 Testando: {' '.join(cmd)}")
            
            # Simular sys.argv
            old_argv = sys.argv
            sys.argv = ["naja_pkg"] + cmd
            
            try:
                main()
                print("   ✅ Comando executado sem erro")
            except SystemExit:
                # Esperado para comandos --help
                print("   ✅ Comando help exibido")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
            finally:
                sys.argv = old_argv
                
    except Exception as e:
        print(f"❌ Erro ao testar CLI: {e}")

def main():
    """Função principal de teste"""
    
    print("🚀 Iniciando testes do NajaScript Package Manager")
    print("=" * 60)
    
    # Verificar se os módulos necessários estão disponíveis
    try:
        from naja_github_package_manager import NajaGitHubPackageManager
        print("✅ Módulo do package manager importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar o package manager: {e}")
        return
    
    # Executar testes
    test_package_manager()
    test_cli()
    
    print("\n" + "=" * 60)
    print("🏁 Testes finalizados!")
    print("\n📋 Para usar o package manager:")
    print("   python naja_pkg init meu-projeto")
    print("   python naja_pkg install exemplo-basico")
    print("   python naja_pkg list")
    print("   python naja_pkg search utilitarios")

if __name__ == "__main__":
    main() 