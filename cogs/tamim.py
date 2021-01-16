import discord

from discord.ext import commands, tasks

import os
from google.cloud import texttospeech
import asyncio

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./infinite-deck-301919-b01ae1f84f82.json"

async def tts(lang, rawText):

    client = texttospeech.TextToSpeechClient()

    text_input = texttospeech.SynthesisInput(text = rawText)

    voice = texttospeech.VoiceSelectionParams(
    language_code=lang,
    name=f'{lang}-Wavenet-C',
    ssml_gender=texttospeech.SsmlVoiceGender.MALE)

    audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3)

    response = await client.synthesize_speech(
        input=text_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

class Tamim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Tamim(bot))