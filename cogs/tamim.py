import discord
import json
from discord.ext import commands, tasks

def read_json():
    with open("languages.json", "r") as read_file:
        try:
            json_object = json.load(read_file)
        except:
            print("JSON read error")
    return json_object


def write_json(json_object):
    with open("languages.json", "w") as write_file:
        try:
            json.dump(json_object, write_file)
        except:
            print("JSON write error")


class Tamim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Sets up channel for role reactions
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def lang_setup(self, ctx, message_content=None):

        json_object = read_json()

        json_object["channel"] = ctx.channel.id

        guild = discord.utils.find(
            lambda g: g.id == ctx.guild.id, self.client.guilds)

        message = None
        if message_content is None:
            message = await ctx.send("Please provide the message content.")
        else:
            message = await ctx.send(f"{message_content}:")

        for lang in json_object['languages']:
            emoji = discord.utils.get(
                guild.emojis, name=json_object['languagess'][lang]["emojiID"])
            await message.add_reaction(emoji)

        json_object["message"] = message.id
        json_object["messageContent"] = message.content

        write_json(json_object)

        # Edit initial message
        new_message_content = json_object['messageContent']
        for lang in json_object['languages']:
            emoji = discord.utils.get(
                guild.emojis, name=json_object['languages'][lang]["emojiID"])
            new_message_content += '\n' + \
                f'{emoji} => {lang}'
        await message.edit(content=new_message_content)
    

def setup(bot):
    bot.add_cog(Tamim(bot))