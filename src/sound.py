from log import logger
import threading
import playsound
import pygame
import os

def play(sound):
    logger.debug(f"Playing sound: {sound}")
    if os.name == "nt": # Windows
        try:
            threading.Thread(target=lambda:playsound.playsound(sound), daemon=True).start()
            logger.info(f"Sound played: {sound}")
        except Exception as e:
            logger.error(f"Failed to play sound {sound}: {e}")
    if os.name == "posix": # Linux/Mac
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(sound)
            pygame.mixer.music.play()
            logger.info(f"Sound played: {sound}")
        except Exception as e:
            logger.error(f"Failed to play sound {sound}: {e}")
    """
    I DONT KNOW WHY THIS HAPPENS BUT PLAYSOUND DOESN'T WORK ON LINUX
    SO I SWITCHED TO PYGAME FOR LINUX. IF YOU KNOW WHY PLAYSOUND DOESN'T WORK ON LINUXPLEASE TELL ME.
    """