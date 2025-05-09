#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PIL import Image

print("Redimensionando ícone para o instalador NajaScript...")

# Caminho para o ícone original e redimensionado
original_icon = "assets/najascript_icon.ico"
resized_icon = "assets/najascript_setup_icon.ico"

try:
    # Verificar se o Pillow está instalado
    try:
        from PIL import Image
    except ImportError:
        print("Instalando biblioteca Pillow necessária para processamento de imagens...")
        import subprocess
        subprocess.call([sys.executable, "-m", "pip", "install", "pillow"])
        from PIL import Image
    
    # Verificar se o arquivo de ícone original existe
    if not os.path.exists(original_icon):
        print(f"ERRO: Arquivo de ícone original não encontrado em {original_icon}")
        exit(1)
    
    # Abrir o ícone original
    img = Image.open(original_icon)
    
    # Configurar tamanhos padrão para ícones de instalador
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    
    # Salvar como novo arquivo ico com tamanhos reduzidos
    img.save(resized_icon, sizes=icon_sizes)
    
    print(f"Ícone redimensionado salvo com sucesso em {resized_icon}")
    print("Agora você pode atualizar o setup_windows.iss para usar este ícone redimensionado.")
    print("Edite a linha: SetupIconFile=assets\\najascript_setup_icon.ico")
    
except Exception as e:
    print(f"Erro ao processar o ícone: {e}")
    print("Tentando método alternativo...")
    
    try:
        # Método alternativo se o primeiro falhar
        import subprocess
        
        # Verificar se o ImageMagick está instalado
        print("Verificando se o ImageMagick está instalado...")
        try:
            subprocess.run(["magick", "--version"], check=True, capture_output=True)
            has_imagemagick = True
        except (subprocess.SubprocessError, FileNotFoundError):
            has_imagemagick = False
        
        if has_imagemagick:
            print("Usando ImageMagick para redimensionar o ícone...")
            # Criar ícones de diferentes tamanhos
            for size in [(16, 16), (32, 32), (48, 48), (64, 64)]:
                subprocess.run([
                    "magick", "convert", original_icon, 
                    "-resize", f"{size[0]}x{size[1]}", 
                    f"assets/icon_{size[0]}x{size[1]}.png"
                ])
            
            # Combinar em um único ícone
            subprocess.run([
                "magick", "convert", 
                "assets/icon_16x16.png", 
                "assets/icon_32x32.png", 
                "assets/icon_48x48.png", 
                "assets/icon_64x64.png", 
                resized_icon
            ])
            
            # Limpar arquivos temporários
            for size in [(16, 16), (32, 32), (48, 48), (64, 64)]:
                os.remove(f"assets/icon_{size[0]}x{size[1]}.png")
            
            print(f"Ícone redimensionado salvo com sucesso em {resized_icon}")
        else:
            print("ImageMagick não encontrado. Não foi possível redimensionar o ícone.")
            print("Por favor, instale o Pillow (pip install pillow) ou ImageMagick")
            print("e tente novamente.")
    except Exception as e2:
        print(f"Erro no método alternativo: {e2}")
        print("Não foi possível redimensionar o ícone.")
        print("Recomendação: edite o arquivo setup_windows.iss e remova a linha:")
        print("SetupIconFile=assets\\najascript_icon.ico") 