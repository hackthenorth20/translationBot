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

async def speechToText(file_name, j, vc, author, listenerLang, logging):
    global user_audioMap
    if os.stat(file_name).st_size == 0 and len(user_audioMap[str(author.id)]) != 0:
        local_map = user_audioMap[str(author.id)]
        user_audioMap[str(author.id)] = []
        recognizer = speech_recognition.Recognizer()
        audios = []

        for f in local_map:
            audios.append(AudioSegment.from_file(f, format="wav"))
            audios.append(AudioSegment.silent(duration=50))

        combined = sum(audios)
        file_handle = combined.export(
            f"combined_audio/{author.id}_{j}.wav", format="wav"
        )

        fp = open(f"combined_audio/{author.id}_{j}.wav", "rb")
        with speech_recognition.AudioFile(fp) as source:
            sr_audio_data = recognizer.record(source)

        text = recognizer.recognize_google(sr_audio_data, language=author.roles[1].name)
        await logging.send(text)
        translatedText = translateText(text, listenerLang[:2])
        await logging.send(translatedText)
        tts(listenerLang, translatedText)
        audio_source = discord.FFmpegPCMAudio("output.mp3")

        while vc.is_playing():
            pass

        vc.play(audio_source, after=None)

    elif os.stat(file_name).st_size != 0:
        user_audioMap[str(author.id)].append(file_name)

class Ahmad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def join(self, ctx):
        voiceChannel = ctx.author.voice.channel
        (Path.cwd() / "waves").mkdir(exist_ok=True)
        (Path.cwd() / "combined_audio").mkdir(exist_ok=True)
        if len(voiceChannel.members) != 2:
            await ctx.send("Only two members in a VC is allowed")
        else:
            msg = await ctx.send("React to the microphone to speak")
            await msg.add_reaction("🎙️")


    # @commands.command()
    # @commands.guild_only()
    # async def test(self, ctx):
    #     voiceChannel = ctx.author.voice.channel
    #     userTwo = (
    #         voiceChannel.members[0]
    #         if voiceChannel.members[1] == ctx.author
    #         else ctx.author
    #     )
    #     await ctx.send(userTwo)

    @commands.command()
    @commands.guild_only()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()


    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_add(self, payload):
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.bot.guilds)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if payload.emoji.name == "🎙️" and message.reactions[0].count == 2:
            micHolder = guild.get_member(payload.user_id)
            voiceChannel = micHolder.voice.channel
            logging = guild.get_channel(800234160458956830)
            listener = None
            for member in  voiceChannel.members:
                if member != micHolder:
                    listener = member

            vc = await voiceChannel.connect()
            i = 0
            global user_audioMap
            user_audioMap[str(micHolder.id)] = []
            while message.reactions[0].count != 1:
                (Path.cwd() / f"waves/{micHolder.id}_{i}.wav").touch(exist_ok=True)
                fp = (Path.cwd() / f"waves/{micHolder.id}_{i}.wav").open("rb")
                vc.listen(
                    discord.UserFilter(discord.WaveSink(f"waves/{micHolder.id}_{i}.wav"), micHolder)
                )
                await asyncio.sleep(2)
                vc.stop_listening()
                asyncio.get_event_loop().create_task(
                    speechToText(f"waves/{micHolder.id}_{i}.wav", i, vc, micHolder, listener.roles[1].name, logging)
                )
                i += 1
                message = await channel.fetch_message(payload.message_id)
            await vc.disconnect()
        elif message.reactions[0].count > 2 and channel.id != 800177711423160360:
            member = guild.get_member(payload.user_id)
            await message.remove_reaction(payload.emoji, member)
        elif payload.emoji.name != "🎙️" and channel.id != 800177711423160360:
            await message.clear_reaction(payload.emoji)



def setup(bot):
    bot.add_cog(Ahmad(bot))