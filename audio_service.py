from gtts import gTTS
import os


def generate_audio(word):

    folder = "app/static/audio"

    os.makedirs(
        folder,
        exist_ok=True
    )

    filename = f"{word}.mp3"

    path = os.path.join(
        folder,
        filename
    )

    if not os.path.exists(path):

        audio = gTTS(
            text=word,
            lang="en"
        )

        audio.save(path)

    return f"audio/{filename}"
