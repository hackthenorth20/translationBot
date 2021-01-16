from datetime import datetime, timedelta
from translation import translateText
import discord

from discord.ext import commands, tasks
from discord.ext.commands import cog

class Farhan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def far(self,ctx, text:str):
        await ctx.send(translateText(text, "fr"))

def setup(bot):
    bot.add_cog(Farhan(bot))