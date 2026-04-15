"""
Support utilities for asset loading and other helpers
"""
import pygame
from os import listdir
from os.path import isfile, join

def import_folder(path):
    """
    Load all PNG images from a folder and return them as a list.
    Useful for animations and sprite sheets.
    """
    surface_list = []
    try:
        for img_name in sorted(listdir(path)):
            if img_name.endswith('.png'):
                full_path = join(path, img_name)
                if isfile(full_path):
                    img = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(img)
    except FileNotFoundError:
        print(f"Warning: Folder not found: {path}")
    
    return surface_list


def import_image(path):
    """
    Load a single image file.
    """
    try:
        return pygame.image.load(path).convert_alpha()
    except FileNotFoundError:
        print(f"Warning: Image not found: {path}")
        return None
