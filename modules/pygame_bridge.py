#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pygame_bridge.py - Bridge module between NajaScript and Pygame
"""

import pygame
import time
import sys
from interpreter import Function
import random as py_random

# Initialize Pygame
pygame.init()
pygame.font.init()

# Global game state
game_state = {
    "screen": None,
    "clock": pygame.time.Clock(),
    "running": False,
    "font": pygame.font.SysFont(None, 24),
    "keys": {},
    "images": {}
}

def init_game_wrapper(interpreter, args):
    """Wrapper for init_game that handles arguments correctly"""
    # Verifica se args é uma lista ou tupla
    if not isinstance(args, (list, tuple)):
        return False
    
    # Verifica se temos argumentos suficientes
    if len(args) < 3:
        return False
    
    # Extrai os argumentos
    width, height, title = args[0], args[1], args[2]
    
    # Inicializa o jogo
    try:
        global game_state
        game_state["screen"] = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        game_state["running"] = True
        
        # Define o ícone padrão como o logo do NajaScript
        try:
            # Tenta carregar o logo do NajaScript como ícone padrão
            logo_path = "assets/logoNajaGame.png"
            if pygame.image.get_extended():
                icon = pygame.image.load(logo_path)
                pygame.display.set_icon(icon)
            else:
                pass
        except Exception as e:
            pass
        
        return True
    except Exception as e:
        return False

def update_window_wrapper(interpreter, args):
    """Wrapper for update_window that handles arguments correctly"""
    global game_state
    
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state["running"] = False
            pygame.quit()
            return False
        elif event.type == pygame.KEYDOWN:
            game_state["keys"][pygame.key.name(event.key).upper()] = True
        elif event.type == pygame.KEYUP:
            game_state["keys"][pygame.key.name(event.key).upper()] = False
    
    # Update display
    pygame.display.flip()
    game_state["clock"].tick(60)
    return game_state["running"]

def draw_rect_wrapper(interpreter, args):
    """Wrapper para a função drawRect"""
    try:
        if len(args) >= 4:
            x, y, width, height, *color_args = args
            
            if color_args:
                if len(color_args) == 1:
                    # Se for um único argumento (lista de cores ou valor de cinza)
                    color = color_args[0]
                    if hasattr(color, '_elements'):
                        # Lista do NajaScript
                        r, g, b = [int(e) for e in color._elements[:3]]
                    elif isinstance(color, list):
                        # Lista Python normal
                        r, g, b = [int(e) for e in color[:3]]
                    else:
                        # Valor único (cinza)
                        r = g = b = int(color)
                elif len(color_args) >= 3:
                    # Se forem argumentos separados r, g, b
                    r, g, b = [int(e) for e in color_args[:3]]
                else:
                    # Padrão
                    r, g, b = 255, 255, 255
            else:
                # Cor padrão: branco
                r, g, b = 255, 255, 255
                
            # Confirma que temos uma superfície válida
            surface = pygame.display.get_surface()
            if not surface:
                return None
                
            # Desenha o retângulo
            pygame.draw.rect(surface, (r, g, b), (int(x), int(y), int(width), int(height)))
            
            return None
        else:
            return None
    except Exception as e:
        return None

def clear_screen_wrapper(interpreter, args):
    """Wrapper para a função clearScreen"""
    try:
        if len(args) == 1:
            color = args[0]
            if hasattr(color, '_elements'):
                # Se for uma lista do NajaScript
                r, g, b = [int(e) for e in color._elements[:3]]
            elif isinstance(color, list):
                # Lista Python normal
                r, g, b = [int(e) for e in color[:3]]
            else:
                # Valor único (cinza)
                r = g = b = int(color)
        elif len(args) == 3:
            # Se forem argumentos separados
            r, g, b = [int(e) for e in args[:3]]
        else:
            # Padrão: preto
            r, g, b = 0, 0, 0
        
        # Confirma que temos uma superfície válida
        surface = pygame.display.get_surface()
        if not surface:
            return None
            
        # Limpa a tela
        surface.fill((r, g, b))
        
        return None
    except Exception as e:
        return None

def is_key_pressed_wrapper(interpreter, args):
    """Wrapper for is_key_pressed that handles arguments correctly"""
    key = args[0]
    global game_state
    return game_state["keys"].get(key.upper(), False)

def get_mouse_pos_wrapper(interpreter, args):
    """Wrapper for get_mouse_pos that handles arguments correctly"""
    return pygame.mouse.get_pos()

def is_mouse_pressed_wrapper(interpreter, args):
    """Wrapper for is_mouse_pressed that handles arguments correctly"""
    button = args[0]
    return pygame.mouse.get_pressed()[button]

def draw_text_wrapper(interpreter, args):
    """Wrapper para a função drawText"""
    try:
        if len(args) == 4:
            text, x, y, color = args
            size = 20  # Tamanho padrão
            
            # Tratamento para diferentes tipos de cores
            if hasattr(color, '_elements'):
                # Lista do NajaScript
                r, g, b = [int(e) for e in color._elements[:3]]
            elif isinstance(color, list):
                # Lista Python normal
                r, g, b = [int(e) for e in color[:3]]
            else:
                # Valor único (cinza)
                r = g = b = int(color)
                
        elif len(args) >= 5:
            text, x, y, size, *color_args = args
            
            if len(color_args) == 1:
                color = color_args[0]
                if hasattr(color, '_elements'):
                    # Lista do NajaScript
                    r, g, b = [int(e) for e in color._elements[:3]]
                elif isinstance(color, list):
                    # Lista Python normal
                    r, g, b = [int(e) for e in color[:3]]
                else:
                    # Valor único (cinza)
                    r = g = b = int(color)
            elif len(color_args) >= 3:
                # Argumentos separados para R, G, B
                r, g, b = [int(e) for e in color_args[:3]]
            else:
                raise ValueError("Argumentos de cor insuficientes")
        else:
            raise ValueError("Número insuficiente de argumentos para drawText")
        
        # Confirma que temos uma superfície válida
        surface = pygame.display.get_surface()
        if not surface:
            return None
            
        # Cria uma fonte
        font = pygame.font.SysFont(None, int(size))
        
        # Renderiza o texto
        text_surface = font.render(str(text), True, (r, g, b))
        
        # Desenha na tela
        surface.blit(text_surface, (int(x), int(y)))
        
        return None
    except Exception as e:
        return None

def load_image_wrapper(interpreter, args):
    """Wrapper for load_image that handles arguments correctly"""
    image_file = args[0]
    global game_state
    try:
        if image_file not in game_state["images"]:
            game_state["images"][image_file] = pygame.image.load(image_file)
        return image_file
    except pygame.error:
        return None

def draw_image_wrapper(interpreter, args):
    """Wrapper for draw_image that handles arguments correctly"""
    
    if len(args) == 3:
        # Formato básico: imagem, x, y
        image, x, y = args
        width = None
        height = None
    elif len(args) == 5:
        # Formato com tamanho: imagem, x, y, largura, altura
        image, x, y, width, height = args
    else:
        return None
    
    global game_state
    if image in game_state["images"]:
        img = game_state["images"][image]
        
        # Se largura e altura foram especificadas, redimensiona a imagem
        if width is not None and height is not None:
            try:
                img = pygame.transform.scale(img, (int(width), int(height)))
            except Exception as e:
                pass
        
        game_state["screen"].blit(img, (int(x), int(y)))
    else:
        pass

def quit_game_wrapper(interpreter, args):
    """Wrapper for quit_game that handles arguments correctly"""
    global game_state
    game_state["running"] = False
    pygame.quit()

def time_wrapper(interpreter, args):
    """Wrapper for time function that returns current time in seconds"""
    return time.time()

def set_icon_wrapper(interpreter, args):
    """Wrapper para definir o ícone da janela do jogo"""
    image_file = args[0]
    global game_state
    
    try:
        # Carrega a imagem do ícone
        icon = pygame.image.load(image_file)
        pygame.display.set_icon(icon)
        return True
    except Exception as e:
        return False

def random_wrapper(args):
    """Wrapper para a função random"""
    try:
        if len(args) >= 2:
            min_val, max_val = args[:2]
            return py_random.randint(int(min_val), int(max_val))
        else:
            return 0
    except Exception as e:
        return 0

# Create Function objects for each wrapper
class DummyDeclaration:
    def __init__(self, name):
        self.name = name
        self.parameters = []
        self.body = []

class NajaGameFunction(Function):
    def __init__(self, name, wrapper):
        super().__init__(DummyDeclaration(name), None)
        self.wrapper = wrapper
        self.name = name
    
    def __call__(self, interpreter, arguments):
        try:
            return self.wrapper(interpreter, arguments)
        except Exception as e:
            return None
    
    # Adiciona este método para evitar o erro "not subscriptable"
    def __getitem__(self, key):
        return None

# Export functions to NajaScript
naja_exports = {}

# Cria as funções e define seus wrappers
for name, wrapper in [
    ("initGame", init_game_wrapper),
    ("updateWindow", update_window_wrapper),
    ("drawRect", draw_rect_wrapper),
    ("clearScreen", clear_screen_wrapper),
    ("isKeyPressed", is_key_pressed_wrapper),
    ("getMousePos", get_mouse_pos_wrapper),
    ("isMousePressed", is_mouse_pressed_wrapper),
    ("drawText", draw_text_wrapper),
    ("loadImage", load_image_wrapper),
    ("drawImage", draw_image_wrapper),
    ("quitGame", quit_game_wrapper),
    ("time", time_wrapper),
    ("setIcon", set_icon_wrapper),
    ("random", random_wrapper)
]:
    naja_exports[name] = NajaGameFunction(name, wrapper)

print("Pygame bridge module loaded!") 