import json
import pymongo


class MongoDB:

    def __init__(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["entries"]
        self.col = mydb["everything"]

    # USER
    def user_exists(self, user):
        exists = self.col.find(
            {"$and": [{"name": {"$eq": user["name"]}}, {"password": user["password"]}]}, {"name": 1})
        try:
            if exists[0]:
                return True
        except:
            return False

    def create_user(self, user):
        if not self.user_exists(user):
            self.col.insert_one(
                {"name": user["name"], "password": user["password"], "state": "user"})
            return True
        else:
            return False

    def insert_entries(self, user, entries):

        self.col.update({"name": user["name"]}, {
                        "$push": {"entries": {"$each": entries}}})


# db = MongoDB()

# x = db.user_exists({"name": "nikos", "password": "1234"})

# y = db.create_user({"name": "nikos", "password": "1234"})

#   PUSH NEW ENTRIES OF USER
# db.everything.update({ name: "loukas"} , { $push : { entries : { $each [ { hello: "hey"}, {yo: "sup"} ]  }} )


# with open('/home/spectator/Desktop/test (2).json') as json_file:
#     data = json.load(json_file)

# print(data["new_json"])

# mycol.update({"name": "loukas"}, {
#     "$push": {"entries": {"$each": data["new_json"]}}})

# ips = mycol.aggregate([
#     {"$match": {"name": "loukas"}},
#     {"$unwind": "$entries"},
#     {"$project": {"entries.serverIPAddress": 1}},
#     {"$group": {"_id": "$entries.serverIPAddress", "count": {"$sum": 1}}}
# ])

# for ip in ips:
#     print(ip)
