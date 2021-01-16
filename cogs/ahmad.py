import discord

from discord.ext import commands, tasks

class Ahmad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.guild_only()
    def connect_channel(self, args):


def setup(bot):
    bot.add_cog(Ahmad(bot))