import discord
import datetime
from pathlib import Path
import asyncio
import os
import ctypes
import speech_recognition
import ctypes.util
import time
import wave
import threading
from discord.ext import commands, tasks

discord.opus.load_opus(ctypes.util.find_library('opus'))
discord.opus.is_loaded()

user_audioMap = {}
async def speachToText(ctx,file_name,j):
    global user_audioMap
    if os.stat(file_name).st_size == 0 and len(user_audioMap[str(ctx.author.id)]) != 0:
        local_map = user_audioMap[str(ctx.author.id)]
        user_audioMap[str(ctx.author.id)] = []
        recognizer = speech_recognition.Recognizer()
        audios = []
        for i in local_map:
            w = wave.open(i, 'rb')
            audios.append( [w.getparams(), w.readframes(w.getnframes())] )
            w.close()
        os.system(f"rm TEST{j}.wav")
        output = wave.open(f"TEST{j}.wav", 'wb')
        output.setparams(audios[0][0])

        for i in range(len(audios)):
            output.writeframes(audios[i][1])
        output.close()

        fp = open(f"TEST{j}.wav","rb")
        with speech_recognition.AudioFile(fp) as source:
            sr_audio_data = recognizer.record(source)

        await ctx.send(recognizer.recognize_google(sr_audio_data, language='en-US'))    
       
    elif os.stat(file_name).st_size != 0:
        user_audioMap[str(ctx.author.id)].append(file_name)

class Ahmad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def join(self,ctx):
        start = datetime.datetime.now()
        channel = ctx.guild.get_channel(ctx.message.author.voice.channel.id)
        vc = await channel.connect()
        (Path.cwd() / 'waves').mkdir(exist_ok=True)
        i = 0
        global user_audioMap
        user_audioMap[str(ctx.author.id)] = []
        while True:
            (Path.cwd() / f'waves/wave{i}.wav').touch(exist_ok=True)
            fp = (Path.cwd() / f'waves/wave{i}.wav').open('rb')
            vc.listen(discord.UserFilter(discord.WaveSink(f'waves/wave{i}.wav'), ctx.author))
            await asyncio.sleep(1.5)
            vc.stop_listening()
            asyncio.get_event_loop().create_task(speachToText(ctx,f'waves/wave{i}.wav',i))
            i += 1
        

    @commands.command()
    @commands.guild_only()
    async def leave(self,ctx):
        await ctx.voice_client.disconnect()


def setup(bot):
    bot.add_cog(Ahmad(bot))