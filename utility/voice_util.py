"""
Cross-platform text-to-speech using pyttsx3 (Windows, macOS, Linux).
"""

import platform

import pyttsx3

_engine = None


def _init_engine():
    system = platform.system()
    driver_order = []
    if system == "Windows":
        driver_order.append("sapi5")
    elif system == "Darwin":
        driver_order.append("nsss")
    else:
        driver_order.append("espeak")

    last_error = None
    for driver in driver_order:
        try:
            return pyttsx3.init(driver)
        except Exception as e:
            last_error = e
    try:
        return pyttsx3.init()
    except Exception as e:
        if last_error is not None:
            raise last_error from e
        raise


def _get_engine():
    global _engine
    if _engine is None:
        _engine = _init_engine()
    return _engine


def text_to_speech(text):
    """Speak text aloud on Windows, macOS, or Linux (requires a supported TTS backend)."""
    if text is None:
        return
    utterance = str(text).strip()
    if not utterance:
        return
    try:
        engine = _get_engine()
        engine.say(utterance)
        engine.runAndWait()
    except Exception as exc:
        print(f"Text-to-speech failed ({exc}). Install optional speech packages if on Linux.")


if __name__ == "__main__":
    text_to_speech("Hello, how are you?")
