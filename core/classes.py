# import discord
from discord.ext import commands

class Cog_Extension(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

# class ExtensionBase(commands.Cog):
#     def __init__(self, bot, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.bot = bot