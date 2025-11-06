from log import logger
import threading
import playsound

def play(sound):
    logger.debug(f"Playing sound: {sound}")
    try:
        threading.Thread(target=lambda:playsound.playsound(sound), daemon=True).start()
        logger.info(f"Sound played: {sound}")
    except Exception as e:
        logger.error(f"Failed to play sound {sound}: {e}")