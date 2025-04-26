#!/usr/bin/env python3
import os
from PIL import Image

def convert_png_to_ico(png_file, ico_file, sizes=[16, 32, 48, 64, 128, 256]):
    """
    Converte uma imagem PNG para o formato ICO do Windows com múltiplos tamanhos
    """
    try:
        # Verificar se o Pillow está instalado
        from PIL import Image
    except ImportError:
        print("Pillow não está instalado. Instalando...")
        os.system("pip install pillow")
        from PIL import Image
    
    print(f"Convertendo {png_file} para {ico_file}...")
    
    # Abrir a imagem original
    img = Image.open(png_file)
    
    # Criar versões de diferentes tamanhos
    icon_sizes = []
    for size in sizes:
        resized_img = img.resize((size, size), Image.LANCZOS)
        icon_sizes.append(resized_img)
    
    # Salvar como ICO
    icon_sizes[0].save(
        ico_file,
        format='ICO',
        sizes=[(size, size) for size in sizes],
        append_images=icon_sizes[1:]
    )
    
    print(f"Ícone convertido com sucesso para {ico_file}")
    return ico_file

if __name__ == "__main__":
    # Converter o ícone do NajaScript
    convert_png_to_ico(
        "assets/najascript_icon.png", 
        "assets/najascript_icon.ico"
    ) 