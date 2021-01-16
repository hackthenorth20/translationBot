import discord
import datetime
from pathlib import Path
import asyncio
import os
import ctypes
import speech_recognition
import ctypes.util
import time
import threading
from discord.ext import commands, tasks
from translation import translateText
from textToSpeech import tts
from pydub import AudioSegment


discord.opus.load_opus(ctypes.util.find_library("opus"))
discord.opus.is_loaded()

user_audioMap = {}


async def speechToText(ctx, file_name, j, vc):
    global user_audioMap
    if os.stat(file_name).st_size == 0 and len(user_audioMap[str(ctx.author.id)]) != 0:
        local_map = user_audioMap[str(ctx.author.id)]
        user_audioMap[str(ctx.author.id)] = []
        recognizer = speech_recognition.Recognizer()
        audios = []

        for f in local_map:
            audios.append(AudioSegment.from_file(f, format="wav"))
            audios.append(AudioSegment.silent(duration=50))

        combined = sum(audios)
        file_handle = combined.export(
            f"combined_audio/{ctx.author.id}_{j}.wav", format="wav"
        )

        fp = open(f"combined_audio/{ctx.author.id}_{j}.wav", "rb")
        with speech_recognition.AudioFile(fp) as source:
            sr_audio_data = recognizer.record(source)

        text = recognizer.recognize_google(sr_audio_data, language="en-US")
        await ctx.send(text)
        # await speech.transcribe_streaming(ctx,f"combined_audio/{ctx.author.id}_{j}.wav")
        translatedText = translateText(text, "en")
        await ctx.send(translatedText)
        tts("en-US", translatedText)
        audio_source = discord.FFmpegPCMAudio("output.mp3")

        if not vc.is_playing():
            vc.play(audio_source, after=None)

    elif os.stat(file_name).st_size != 0:
        user_audioMap[str(ctx.author.id)].append(file_name)


class Ahmad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def join(self, ctx):
        voiceChannel = ctx.author.voice.channel
        vc = await voiceChannel.connect()
        (Path.cwd() / "waves").mkdir(exist_ok=True)
        (Path.cwd() / "combined_audio").mkdir(exist_ok=True)
        i = 0
        global user_audioMap
        user_audioMap[str(ctx.author.id)] = []
        while True:
            (Path.cwd() / f"waves/wave{i}.wav").touch(exist_ok=True)
            fp = (Path.cwd() / f"waves/wave{i}.wav").open("rb")
            vc.listen(
                discord.UserFilter(discord.WaveSink(f"waves/wave{i}.wav"), ctx.author)
            )
            await asyncio.sleep(2)
            vc.stop_listening()
            asyncio.get_event_loop().create_task(
                speechToText(ctx, f"waves/wave{i}.wav", i, vc)
            )
            i += 1

    @commands.command()
    @commands.guild_only()
    async def test(self, ctx):
        voiceChannel = ctx.author.voice.channel
        userTwo = (
            voiceChannel.members[0]
            if voiceChannel.members[1] == ctx.author
            else ctx.author
        )
        await ctx.send(userTwo)

    @commands.command()
    @commands.guild_only()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()


def setup(bot):
    bot.add_cog(Ahmad(bot))