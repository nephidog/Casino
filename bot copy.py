import discord
from discord.ext import commands
import json, asyncio, os
import asyncio
from MongoDB import *

# with open("setting.json","r",encoding="utf8") as jfile:
    # jdata = json.load(jfile)

intents = discord.Intents().all()
# bot = commands.Bot(command_prefix="~") #command_prefix 呼叫自首
# client = discord.Client()
EXT_PATH = "cmds"
bot = commands.Bot(command_prefix="~", intents=intents) #command_prefix 呼叫自首
bot_Chocola = commands.Bot(command_prefix="~1", intents=intents)
bot_Vanilla = commands.Bot(command_prefix="~2", intents=intents)
bot_Maple = commands.Bot(command_prefix="~3", intents=intents)
bot_Cinnamon = commands.Bot(command_prefix="~4", intents=intents)
bot_Azuki = commands.Bot(command_prefix="~5", intents=intents)
bot_Coconut = commands.Bot(command_prefix="~6", intents=intents) #description = 'Example'

bot.remove_command("help") # 移除內建help
# bot_Chocola.remove_command("help")
# bot_Vanilla.remove_command("help")

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
        msg += Guild.get_role(i).mention
    await ctx.send(f"伺服器:{ctx.guild.name},身分組:{msg}")
    
@bot.command()
async def data(ctx,member: discord.Member):
    await ctx.send(f"身分組: {member.top_role}\n姓名: {member.mention} {member.name}\nID:{member.id} isbot:{member.bot}\n\n\
身分組: {ctx.author.top_role}\n姓名: {ctx.author.mention} {ctx.author.name}\nID:{ctx.author.id} isbot:{ctx.author.bot}\n")#標記使用者

for Filename in os.listdir("./cmds"): #
    if Filename.endswith(".py"):
        bot.load_extension(F"cmds.{Filename[:-3]}")
        # bot_Chocola.load_extension(F"cmds.{Filename[:-3]}")
        # bot_Vanilla.load_extension(F"cmds.{Filename[:-3]}")
        # bot_Maple.load_extension(F"cmds.{Filename[:-3]}")
        # bot_Cinnamon.load_extension(F"cmds.{Filename[:-3]}")
        # bot_Azuki.load_extension(F"cmds.{Filename[:-3]}")
        # bot_Coconut.load_extension(F"cmds.{Filename[:-3]}")
if __name__ == "__main__":


    for Filename in os.listdir("./cmds"): #
        if Filename.endswith(".py"):
            bot.load_extension(F"cmds.{Filename[:-3]}")


    MData = MongoDB().queryItem("bot", "name", "AzurTactics")

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(MData["TOKEN"]))
    loop.create_task(bot_Chocola.start(MData["TOKEN_Chocola"]))
    loop.create_task(bot_Vanilla.start(MData["TOKEN_Vanilla"]))
    loop.create_task(bot_Maple.start(MData["TOKEN_Maple"]))
    loop.create_task(bot_Cinnamon.start(MData["TOKEN_Cinnamon"]))
    loop.create_task(bot_Azuki.start(MData["TOKEN_Azuki"]))
    loop.create_task(bot_Coconut.start(MData["TOKEN_Coconut"]))
    loop.run_forever()


    

