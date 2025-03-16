#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste direto do Pygame para verificar se a biblioteca está funcionando corretamente
"""

import pygame
import sys
import time

def main():
    # Inicializa o Pygame
    pygame.init()
    
    # Configurações da janela
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Teste Direto Pygame")
    
    # Cores
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    
    # Clock para controlar FPS
    clock = pygame.time.Clock()
    
    # Fonte para texto
    font = pygame.font.SysFont(None, 36)
    
    print("Pygame inicializado! Verificando se a janela aparece...")
    
    # Loop principal
    running = True
    start_time = time.time()
    
    while running:
        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Limpa a tela
        screen.fill(BLACK)
        
        # Desenha um retângulo azul no centro
        pygame.draw.rect(screen, BLUE, (350, 250, 100, 100))
        
        # Desenha texto
        text = font.render("Teste Direto do Pygame", True, WHITE)
        screen.blit(text, (10, 10))
        
        # Atualiza a tela
        pygame.display.flip()
        
        # Limita a 60 FPS
        clock.tick(60)
        
        # Encerra após 2 segundos
        if time.time() - start_time > 2:
            print("Teste concluído após 2 segundos. Encerrando...")
            running = False
    
    pygame.quit()
    print("Pygame encerrado com sucesso!")

if __name__ == "__main__":
    main() 