import discord
import json
from discord.ext import commands, tasks

botID = 799857466367541258
guildID = 766020518620299265


def role_select(guild, emoji):

    role = None
    if emoji == "1️⃣":
        role = discord.utils.get(guild.roles, name="en-US")
    elif emoji == "2️⃣":
        role = discord.utils.get(guild.roles, name="fr-CA")
    elif emoji == "3️⃣":
        role = discord.utils.get(guild.roles, name="es-ES")
    print(role)
    # elif emoji == "4️⃣":
    #     role = discord.utils.get(guild.roles, name="4th Year")
    return role


class Tamim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #### Add team-roles on Reaction ####
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_add(self, payload):

        # if payload.channel.id != json_object["channel"]:
        #     return

        if payload.user_id == botID:
            return

        guild = discord.utils.find(lambda g: g.id == guildID, self.bot.guilds)

        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        if member is None:
            print("Member not found.")
            return

        roleName = None
        print(payload.emoji.name)
        role = role_select(guild, payload.emoji.name)

        # Create Embed
        confirm_embed = discord.Embed(
            title=f"Roles assigned for {member}", color=0x2AF761
        )
        confirm_embed.add_field(name="Member ID:", value=f"{member.id}")
        confirm_embed.add_field(name="Added:", value=f"{role}", inline=False)
        confirm_embed.set_thumbnail(url=f"{member.avatar_url}")

        if role is None:
            print("Role not found")
        else:
            await member.add_roles(role)
            await member.send(embed=confirm_embed)

    #### Add team-roles on Reaction ####
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_remove(self, payload):

        # Excludes bot from role requests
        if payload.user_id == botID:
            return

        guild = discord.utils.find(lambda g: g.id == guildID, self.bot.guilds)

        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        if member is None:
            print("Member not found.")
            return

        role = role_select(guild, payload.emoji.name)

        # Create Embed
        confirm_embed = discord.Embed(
            title=f"Roles removed for {member}", color=0x2AF761
        )
        confirm_embed.add_field(name="Member ID:", value=f"{member.id}")
        confirm_embed.add_field(name="Removed:", value=f"{role}", inline=False)
        confirm_embed.set_thumbnail(url=f"{member.avatar_url}")

        if role is None:
            print("Role not found")
        else:
            await member.remove_roles(role)
            await member.send(embed=confirm_embed)

    # Sets up channel for role reactions
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def lang_setup(self, ctx, message_content=None):

        guild = discord.utils.find(lambda g: g.id == guildID, self.bot.guilds)

        message = None
        if message_content is None:
            message = await ctx.send("Choose a default language below.")
        else:
            message = await ctx.send(f"{message_content}:")

        langs = ["en-US", "fr-CA", "es-ES"]
        emojis = ["1️⃣", "2️⃣", "3️⃣"]

        # Edit initial message
        new_message_content = "Choose a default language below."
        for i in range(len(langs)):
            await message.add_reaction(emojis[i])
            new_message_content += "\n" + f"{emojis[i]} => {langs[i]}"
            role = discord.utils.get(guild.roles, name=langs[i])
            if role is None:
                try:
                    role = await guild.create_role(
                        name=f"{langs[i]}", colour=discord.Colour(0xFFFFFF)
                    )
                except:
                    await ctx.send("Failed to create Role.")
                    return

        await message.edit(content=new_message_content)


def setup(bot):
    bot.add_cog(Tamim(bot))