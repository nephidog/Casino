import discord
from discord.ext import commands
from discord.ui import Button, View
import json, asyncio, os
import asyncio
from MongoDB import *

EXT_PATH = "cmds"

if __name__ == "__main__":
    
    constData = None
    with open('json/const.json', mode = 'r', encoding = 'utf8') as jfile:
        constData = json.load(jfile)
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    bot = commands.Bot(command_prefix="~",intents=intents,case_insensitive = True)
    bot_Chocola = commands.Bot(command_prefix="dl.",intents=intents,case_insensitive = True)
    bot_Vanilla = commands.Bot(command_prefix="dl.",intents=intents,case_insensitive = True)
    bot_Azuki = commands.Bot(command_prefix="dl.",intents=intents,case_insensitive = True)
    bot_Cinnamon = commands.Bot(command_prefix="dl.",intents=intents,case_insensitive = True)
    bot_Maple = commands.Bot(command_prefix="dl.",intents=intents,case_insensitive = True)
    bot_Coconut = commands.Bot(command_prefix="dl.",intents=intents,case_insensitive = True)

    bot.remove_command("help") # remove default help

    @bot.event
    async def on_ready():
        print(">> Bot is online <<")

    @bot_Chocola.event
    async def on_ready():
        print(">> bot_Chocola is online <<")    

    @bot_Vanilla.event
    async def on_ready():
        print(">> bot_Vanilla is online <<")

    @bot_Maple.event
    async def on_ready():
        print(">> bot_Maple is online <<")    

    @bot_Cinnamon.event
    async def on_ready():
        print(">> bot_Cinnamon is online <<")  

    @bot_Azuki.event
    async def on_ready():
        print(">> bot_Azuki is online <<") 

    @bot_Coconut.event
    async def on_ready():
        print(">> bot_Coconut is online <<")    

    @bot.command()
    async def load(ctx,extension):
        bot.load_extension(f"cmds.{extension}")
        await ctx.send(f"Loaded {extension} done.")

    @bot.command()
    async def unload(ctx,extension):
        bot.unload_extension(f"cmds.{extension}")
        await ctx.send(f"Un - Loaded {extension} done.")

    @bot.command()
    async def reload(ctx,extension):
        bot.reload_extension(f"cmds.{extension}")
        await ctx.send(f"Re - Loaded {extension} done.")

    @bot.command()
    async def getsuperuser(ctx):
        guild_owner = bot.get_user(int(ctx.guild.owner.id))
        await ctx.send(f'The owner of this server is: {guild_owner.id}')

    @bot.command()
    async def getserver(ctx): #伺服器ID
        Server = ctx.guild.id
        await ctx.send(f"ServerId =  {Server} ")

    @bot.command()
    async def guild_msg(ctx,Channel_ID:int):
        channel = bot.get_channel(Channel_ID)
        await channel.send(f'跨伺服器測試')

    @bot.command()
    async def isbot(ctx,id):
        member = await bot.fetch_user(int(id))
        await ctx.send(f"姓名: {member.mention} {member.name}\nID:{member.id} isbot:{member.bot} \n") #top_role:{member.top_role}
        await ctx.send(member.top_role)

    @bot.command() #類別名稱
    async def category(ctx):
        category = ctx.channel.category
        await ctx.send(f"類別名稱:{category.name} 類別ID:{category.id}")

    @bot.command()
    async def name(ctx):
        
        id = ctx.author.id #使用者ID
        print (f"author:{ctx.author}, {type(ctx.author)}")
        print(f"ID:{id}{type(id)}")
        author = await bot.fetch_user(id)
        print(author,type(author))
        print(author.name,type(author))
        print(author.id,type(author))

    @bot.command()
    async def log(ctx,LogChannel:discord.TextChannel):
        await ctx.message.delete()
        await ctx.send(f"頻道名稱:{LogChannel.name},ID:{LogChannel.id}")

    @bot.command()
    async def role(ctx):
        Guild = ctx.guild
        # role_id = [role.id for role in ctx.author.roles]
        # await ctx.send(f"使用者:{ctx.author.mention},身分組:{role_id}")
        guildroles = [role.id for role in ctx.guild.roles]
        guildroles.reverse()
        msg = ""
        for i in guildroles:
            msg += Guild.get_role(i).mention + ":"+ str(i) + "\n"
        await ctx.send(f"伺服器:{ctx.guild.name} 身分組:\n{msg}")
        
    @bot.command()
    async def data(ctx,member: discord.Member):
        await ctx.send(f"身分組: {member.top_role}\n姓名: {member.mention} {member.name}\nID:{member.id} isbot:{member.bot}\n\
            身分組: {ctx.author.top_role}\n姓名: {ctx.author.mention} {ctx.author.name}\nID:{ctx.author.id} isbot:{ctx.author.bot}\n")#標記使用者

    bot.db = MongoDB()
    # 打開資料庫
    bot.constSettings = constData
    myClient = pymongo.MongoClient("mongodb://localhost:27017/")
    bot.myDB = myClient["AzurTactics"]
    # MData = MongoDB().queryItem("bot", "name", "AzurTactics")
    # view = View()
    # bot.EMBED_BUTTON_VIEW = view

    async def load_extensions():
        for file in os.listdir(EXT_PATH):
            if file.endswith(".py"):
                await bot.load_extension(f"{EXT_PATH}.{file[:-3]}") 

    async def main():
        
        async with bot:
            await load_extensions()
            token = bot.db.queryItem("bot", "name", "AzurTactics", f"TOKEN")
            await bot.start(token)
        #     await bot.start(MData["TOKEN"])
        # await bot_Chocola.start(MData["TOKEN_Chocola"])
        # await bot_Vanilla.start(MData["TOKEN_Vanilla"])
        # await bot_Maple.start(MData["TOKEN_Maple"])
        # await bot_Cinnamon.start(MData["TOKEN_Cinnamon"])
        # await bot_Azuki.start(MData["TOKEN_Azuki"])
        # await bot_Coconut.start(MData["TOKEN_Coconut"])
    asyncio.run(main())


    

