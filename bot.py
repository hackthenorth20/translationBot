import discord
import os

from discord.ext import commands, tasks
from discord.utils import get
from SECRET import TOKEN


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    activity = discord.Game("Translating languages")
    await bot.change_presence(status=discord.Status.online, activity=activity)


# Commands
@bot.command()
@commands.has_guild_permissions(administrator=True)
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send("Cog has been loaded")


@bot.command()
@commands.has_guild_permissions(administrator=True)
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send("Cog has been unloaded")


@bot.command()
@commands.has_guild_permissions(manage_messages=True)
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension} has been loaded ✅")


# Initial Cog Loading
if __name__ == "__main__":
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")


@bot.command()
async def stop(ctx):
    await bot.logout()


bot.run(TOKEN)
