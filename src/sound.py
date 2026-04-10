from log import logger
import threading
import pygame
import os

def play(sound):
    logger.debug(f"Playing sound: {sound}")
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        logger.info(f"Sound played: {sound}")
    except Exception as e:
        logger.error(f"Failed to play sound {sound}: {e}")