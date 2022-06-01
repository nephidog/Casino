import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json,asyncio,datetime,pytz,random,time
from cmds.admin import *
from cmds.create import *  
from core.helper import createEmbed, getTotalSeconds,getTwTimeNow
class Economy(Cog_Extension):
    
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs) # 重讀取父類別
        async def Auto_Check_Daily():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed(): # 若機器人啟動中
                current_time_seconds = getTotalSeconds("now")
                members_data = self.bot.db.queryTable("members")
                for member_data in members_data:
                    daily_t_s = member_data['daily_total_seconds']
                    if daily_t_s + 165600 > current_time_seconds: 
                        continue
                    # 如果一天後都沒登入, 連續登入設為 0
                    self.bot.db.updateOneValue("members", "member_id", member_data['member_id'], "daily_streak", 0)
                await asyncio.sleep(600) #600秒檢查一次

        self.bg_task = self.bot.loop.create_task(Auto_Check_Daily()) 

    @commands.command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def daily(self, ctx):
        member_id = str(ctx.author.id)
        await Create.add_member_user(self,ctx)
        member_data = self.bot.db.queryItem("members", "member_id", member_id)
        current_time_seconds = getTotalSeconds("now")

        #換日時清除本日簽到
        if member_data["total_daily"] > 0:
            oldtime = (datetime.datetime.fromtimestamp(member_data["daily_total_seconds"])).strftime("%m/%d/%Y")
            nowtime = (datetime.datetime.now()+datetime.timedelta(hours=+8)).strftime("%m/%d/%Y")
            #判斷是否同一天
            if (nowtime!= oldtime): 
                self.bot.db.updateOneValue("members", "member_id", member_id, "today_daily", 0, )
                self.bot.db.updateOneValue("members", "member_id", member_id, "cmd_cd_list.daily", -1)
                member_data['today_daily'] = 0
                
  
        now = getTwTimeNow()
        last_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)\
        + datetime.timedelta(hours=23, minutes=59, seconds=59)
        cdtime = int((last_today-now).total_seconds())
        if member_data["today_daily"] < 5: #每日簽到
            if member_data['cmd_cd_list']['daily'] != -1 and member_data['cmd_cd_list']['daily'] > current_time_seconds:
                cdtime_2 = member_data['cmd_cd_list']['daily']-current_time_seconds
                cdtime_2 = cdtime_2 if cdtime_2 < cdtime else cdtime
                raise commands.errors.CommandOnCooldown(f"冷卻時間", retry_after=cdtime_2,type=commands.BucketType.user)
            
            self.bot.db.updateOneValue("members", "member_id", member_id, "cmd_cd_list.daily", getTotalSeconds("4h")) #簽到冷卻時間
            daily_streak = member_data['daily_streak'] 
            gamble_coin = 1000 + 500 * daily_streak if daily_streak <= 4 else 3000
            currentSecs = getTotalSeconds("now")
            #增加賭幣
            self.bot.db.updateManyValueMode("$inc", "members", "gamble_coin", gamble_coin, "member_id", member_id)
            member_data['gamble_coin'] += gamble_coin
            #更新簽到秒數
            self.bot.db.updateOneValue("members", "member_id", member_id, "daily_total_seconds", currentSecs)
            member_data["daily_total_seconds"] = currentSecs

            if member_data['today_daily'] == 0:
                #連續簽到
                self.bot.db.updateManyValueMode("$inc", "members", "daily_streak", 1, "member_id", member_id)
                member_data['daily_streak'] += 1
                #總簽到次數
                self.bot.db.updateManyValueMode("$inc", "members", "total_daily", 1, "member_id", member_id)
                member_data['total_daily'] += 1

            #本日簽到
            self.bot.db.updateManyValueMode("$inc", "members", "today_daily", 1, "member_id", member_id)
            member_data['today_daily'] += 1

            content = f"\n\n 本次領取賭幣 {gamble_coin} <:material_gamble_coin:967714841013915649>"
            content += f"\n本日還可簽到 {5-member_data['today_daily']} 次" if member_data["today_daily"] < 5 else "/本日簽到已完成"
            footerContent = f"總簽到次數 {member_data['total_daily']} 天"
            streak_title = f"連續 {member_data['daily_streak']}天簽到" if member_data['daily_streak'] >= 2 else ""
            embed = createEmbed(f"{ctx.author.name}'s Daily 每日簽到 🗓 "+streak_title, content, footerContent=footerContent, thumbnailUrl=self.bot.constSettings['dc_logo_url'], titleIconUrl=self.bot.constSettings['dl_logo_url'])
        
            await ctx.send(embed=embed)
        
        # await ctx.send(embed=embed, view=self.bot.EMBED_BUTTON_VIEW)
        else:
            raise commands.errors.CommandOnCooldown(f"本日簽到已完成，冷卻時間", retry_after=cdtime,type=commands.BucketType.user)




async def setup(bot):
    await bot.add_cog(Economy(bot))