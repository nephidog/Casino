import pymongo

class MongoDB:
    myClient = None
    myDB = None

    def __init__(self):
        self.myClient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.myDB = self.myClient["AzurTactics"]
        # self.myDB = self.myClient["dreamcoder"]

    #查詢表格
    def queryTable(self, table_name):
        table = self.myDB[table_name]
        result = table.find()
        return result # object
    
    # 查詢表格中資料
    def queryItem(self, table_name, key, value, key_name=None): #members, member_id, id -> return member data
        table = self.myDB[table_name]
        if key_name:            
            result = table.find_one({key:value}, {key_name:1})[key_name]
        else:
            result = table.find_one({key:value})
        return result # dict or none

    # key_list example: [ {"guildsID": "308012136993521676"}, {"admin_list": {"$in": [250508597182595070]}} ]
    def checkInLst(self, table_name, key_list):
        table = self.myDB[table_name]
        resultLen = len(list(table.find({"$and": key_list}, {"_id": 1})))
        if resultLen > 0:
            return True
        return False

    #插入子表單
    def insertOneItem(self, table_name, data): 
        table = self.myDB[table_name]
        result = table.insert_one(data)
        return result

    #插入多個項目
    def insertManyItem(self, table_name, data_list): 
        table = self.myDB[table_name]
        result = table.insert_many(data_list)
        return result

    #插入列表(資料表名,確認用key,確認用value,新增的key,新增的value)
    def insertListValue(self, table_name, key, value, key_name, key_value): 
        table = self.myDB[table_name]
        result = table.update_one({key:value}, {"$push":{key_name:key_value}})
        return result

    #刪除列表中項目
    def deleteListValue(self, table_name, key, value, key_name, key_value): 
        table = self.myDB[table_name]
        result = table.update_one({key:value}, {"$pull":{key_name:key_value}})
        return result

    #刪除字典
    # dictionary delete key
    def deleteOneItem(self, table_name, key, value, key_name=None):
        table = self.myDB[table_name]
        if key_name:
            result = table.update_one({key:value}, {"$unset":{key_name:1}})
        else:
            result = table.delete_one({key:value})
        return result

    #刪除多個項目
    def deleteManyItem(self, table_name, key, value):
        table = self.myDB[table_name]
        result = table.delete_many({key:value})
        return result

    # 刪除多值
    def deleteManyValue(self, table_name, key_name, key=None, value=None):
        where = {key:value} if key and value else {}
        table = self.myDB[table_name]
        result = table.update_many(where, {"$unset":{key_name:1}})
        return result

    #更新資料
    # MongoDB().updateOneValue("casino","name","AzurTactics",f"games.{0}.limit", None)
    # dictionary add key value
    #建立/更新一個值在表格中
    def updateOneValue(self, table_name, key, value, key_name, key_value):
        table = self.myDB[table_name]
        result = table.update_one({key:value}, {"$set":{key_name:key_value}})
        return result

    def updateOneValueMode(self, mode, table_name, key, value, key_name, key_value):
        table = self.myDB[table_name]
        result = table.update_one({key: value}, {mode: {key_name: key_value}})
        return result
        
    def updateManyValue(self, table_name, key_name, key_value, key=None, value=None):
        where = {key:value} if key and value else {}
        table = self.myDB[table_name]
        result = table.update_many(where, {"$set":{key_name:key_value}})
        return result

    # mode: "$inc"-increase key_value, "$gt"-大於, "$lt"-小於, "$gte"-大於等於, "$lte"-小於等於
    def updateManyValueMode(self, mode, table_name, key_name, key_value, key=None, value=None):
        where = {key: value} if key and value else {}
        table = self.myDB[table_name]
        result = table.update_many(where, {mode: {key_name: key_value}})
        return result
    
    # 更新整個物件
    def updateObject(self, table_name, key, value, object):
        table = self.myDB[table_name]
        result = table.update_one({key: value}, {"$set": object})
        return result

    def dropTable(self, table_name):
        table = self.myDB[table_name]
        result = table.drop()
        return result
    
