from pydub import AudioSegment


def webm_to_wav(
    input_file,
    output_file
):

    audio = (
        AudioSegment
        .from_file(
            input_file,
            format="webm"
        )
    )

    audio.export(
        output_file,
        format="wav"
    )
