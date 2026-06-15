import speech_recognition as sr
from difflib import SequenceMatcher


def analyze_pronunciation(
    audio_path,
    expected_word
):

    recognizer = sr.Recognizer()

    try:

        with sr.AudioFile(
            audio_path
        ) as source:

            audio = (
                recognizer.record(
                    source
                )
            )

        spoken = (
            recognizer
            .recognize_google(
                audio
            )
            .lower()
        )

        score = int(

            SequenceMatcher(
                None,
                spoken,
                expected_word.lower()
            ).ratio()

            * 100

        )

        return {

            "spoken": spoken,

            "score": score

        }

    except sr.UnknownValueError:

        return {

            "spoken": "not recognized",

            "score": 0

        }

    except sr.RequestError:

        return {

            "spoken": "speech service unavailable",

            "score": 0

        }

    except FileNotFoundError:

        return {

            "spoken": "audio file not found",

            "score": 0

        }
