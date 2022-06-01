#伺服器模板

def getNewGuildData(guild_id): #建立新伺服器模板
    guild_data = {}
    guild_data['name'] = "AzurTactics"
    guild_data['admin_role'] = []
    guild_data['guildsID'] = guild_id
    return guild_data

def getNewMemberData(member_id): #建立新玩家模板
    member_data = {}
    member_data["member_id"] = str(member_id)
    member_data["gamble_coin"] = 0
    member_data["daily_streak"] = 0
    member_data["daily_total_seconds"] = 0
    member_data["total_daily"] = 0
    member_data["today_daily"] = 0
    member_data["cmd_cd_list"] = {"daily": -1,"giverep": -1}
    member_data["stats"] = {}
    return member_data

