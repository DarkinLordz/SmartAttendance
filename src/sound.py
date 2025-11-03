from log import logger
import playsound

def play(sound):
    logger.debug(f"Playing sound: {sound}")
    try:
        playsound.playsound(sound)
        logger.info(f"Sound played: {sound}")
    except Exception as e:
        logger.error(f"Failed to play sound {sound}: {e}")