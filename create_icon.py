#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para criar um ícone simples para o NajaScript Editor.
Requer a biblioteca Pillow (PIL).
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size=256):
    # Criar uma imagem com fundo escuro
    img = Image.new('RGBA', (size, size), (30, 30, 30, 255))
    draw = ImageDraw.Draw(img)
    
    # Desenhar um círculo como fundo
    circle_margin = size // 10
    circle_size = size - (2 * circle_margin)
    draw.ellipse((circle_margin, circle_margin, circle_margin + circle_size, circle_margin + circle_size), 
                 fill=(50, 120, 200, 255))
    
    # Desenhar a letra "N" no centro
    try:
        # Tentar usar uma fonte instalada no sistema
        font_size = size // 2
        font = ImageFont.truetype("Arial Bold", font_size)
    except IOError:
        # Se não encontrar a fonte, usar a fonte padrão
        font = ImageFont.load_default()
        font_size = size // 4
    
    text = "N"
    text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (font_size, font_size)
    position = ((size - text_width) // 2, (size - text_height) // 2)
    
    # Desenhar o texto em branco
    draw.text(position, text, fill=(255, 255, 255, 255), font=font)
    
    # Salvar como ícone
    img.save('icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    
    print(f"Ícone criado: {os.path.abspath('icon.ico')}")

if __name__ == "__main__":
    try:
        create_icon()
    except Exception as e:
        print(f"Erro ao criar ícone: {e}")
        
        # Se falhar, criar um ícone muito simples
        try:
            img = Image.new('RGB', (256, 256), (30, 30, 30))
            img.save('icon.ico', format='ICO')
            print(f"Ícone básico criado: {os.path.abspath('icon.ico')}")
        except:
            print("Não foi possível criar nem mesmo um ícone básico.") 