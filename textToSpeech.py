import os
from google.cloud import texttospeech
import asyncio

credential_path = "creds.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path


def tts(lang, rawText):

    client = texttospeech.TextToSpeechClient()

    text_input = texttospeech.SynthesisInput(text=rawText)

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang,
        name=f"{lang}-Wavenet-A",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=text_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')