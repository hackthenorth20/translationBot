import discord

from discord.ext import commands, tasks

class Farhan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(Farhan(bot))