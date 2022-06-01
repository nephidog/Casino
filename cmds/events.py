import discord
from discord.ext import commands
from core.classes import Cog_Extension
import math
import json,asyncio,datetime,pytz,random
from cmds.admin import * 
class Event(Cog_Extension):
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        notberr = '{}: {}'.format(type(err).__name__, err)
        if isinstance(err, commands.CommandOnCooldown):
            self.log(ctx, 'err', content=notberr, reason=f'密令正在冷卻')
            total_seconds = math.ceil(err.retry_after)
            hours = (total_seconds // 3600) % 24
            cd_time = ""
            if hours > 0:
                cd_time += f"{hours} 時"
            minutes = (total_seconds // 60) % 60
            if minutes > 0:
                cd_time += f" {minutes} 分"
            seconds = total_seconds % 60
            if seconds > 0:
                cd_time += f" {seconds} 秒"
            await ctx.send(f"{ctx.author.mention} 指令 `{ctx.command}` 冷卻中，**{cd_time}後**，再次使用", delete_after=5)
            return True
 

            
    def log(self, ctx=None, type: str = 'debug', **kwargs) -> None:
        """
        Log
        Usage: log(ctx, type='debug', [content, reason])
        ·log(ctx, 'general')
        ·log(ctx, 'error', reason='reason', content='content')
        ·debug: log(content='content') (DEFAULT)
        """
        type = type.lower()
        if not ctx:
            pass
        elif isinstance(ctx.channel, discord.TextChannel):
            guild_name = ctx.guild.name
            channel_name = "#" + ctx.channel.name
        elif isinstance(ctx.channel, discord.DMChannel):
            guild_name = "Personal DM"
            channel_name = ctx.channel.recipient
        elif isinstance(ctx.channel, discord.GroupChannel):
            guild_name = "Group DM"
            channel_name = str(ctx.channel)

        if type == "general" or type == "gen":
            self.sprint(f'{guild_name}({channel_name}), {ctx.author} > {ctx.message.content}\n')
        elif type == 'error' or type == "err":
            content = str(kwargs.get('content', ''))
            objs = f'{guild_name} {ctx.guild.id}|{channel_name}|{ctx.author} {ctx.author.id}: "{ctx.message.content}" -\n' + 'Error has been ignored{}: \n'.format(' because '+kwargs.get('reason', ''))
            content = content if content.endswith('\n') else content + '\n'
            self.sprint(objs, (content))
            return objs, content
        elif type == "debug" or type == "d":
            self.sprint("Debug: {}".format(kwargs.get('content', '')))

        return "", ""

    def sprint(self, *objects, **kwargs) -> None:
        """
        Safe Print
        Just like print function, but it will escape non-bmp characters if console doesn't support it.
        Usage: sprint(value, ..., sep=' ', end='\\n', file=sys.stdout, flush=False)
        """
        new_objects = []
        for obj in objects:
            new_objects.append(obj)
        print(*new_objects, **kwargs)

    async def updateinvites(self, member):
        return
        guild_id = str(member.guild.id)
        guild_data = self.bot.db.queryItem('guilds', 'guildsID', guild_id)
        invites = await member.guild.invites()
        # save all invite usage data
        old_invs = guild_data['invites']
        new_invs = []
        if old_invs:
            for invite in invites:
                found = False
                for i, old_inv in enumerate(old_invs):
                    # if in old data -> update
                    if old_inv["code"] == invite.code:
                        old_invs[i]["uses"] = invite.uses
                        new_invs.append(old_invs[i])
                        found = True
                        break
                if not found:  # add in
                    result = {
                        "inviter_name": invite.inviter,
                        "inviter_id": invite.inviter.id,
                        "code": invite.code,
                        "uses": invite.uses
                    }
                    new_invs.append(result)
        else:  # init
            for invite in invites:
                result = {
                    "inviter_name": invite.inviter.name,
                    "inviter_id": invite.inviter.id,
                    "code": invite.code,
                    "uses": invite.uses
                }
                new_invs.append(result)

        guild_data['invites'] = new_invs
        # with open('setting.json', mode='w', encoding='utf8') as jfile:
        #    json.dump(self.bot.settings, jfile, indent=4, ensure_ascii=False)
        self.bot.db.updateObject('bot', 'guildsID', guild_id, guild_data)

    
async def setup(bot):
    await bot.add_cog(Event(bot))