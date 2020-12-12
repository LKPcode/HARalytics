import json
import mysql.connector

# Difine the Database Class


class MySQL:

    # Python Constructor
    def __init__(self):
        # Change the parameters so they reflect your own system
        self.mydb = mysql.connector.connect(
            host="localhost",
            port="3307",  # default 3306
            user="root",
            password="password",
            database="mydtbs"
        )

    # Inserting a user to the database
    def create_user(self, user):

        mycursor = self.mydb.cursor()

        # Constructing and Inserting a User row
        entry_sql = "INSERT INTO `mydtbs`.`User` (`email`, `ip`, `username`, `password`, `ISP`, `admin`) VALUES (%s,%s,%s,%s,%s,%s);"
        entry_val = (user["email"], user["ip"], user["name"],
                     user["password"], user["isp"], "0")

        mycursor.execute(entry_sql, entry_val)
        print(mycursor.lastrowid)
        self.mydb.commit()

    def user_exists(self, user):
        mycursor = self.mydb.cursor()

        mycursor.execute("SELECT * from User WHERE email=%s", (user["email"],))
        if len(mycursor.fetchall()) > 0:
            return True
        return False

    # Method to insert data, for now we load them from a file just for simplicity

    def insert_data(self, data, user):
        # Load the test.json data into the "data" variable
        # with open('./uploads/test2.json') as json_file:
        #     data = json.load(json_file)

        mycursor = self.mydb.cursor()
        email = user["email"]

        # Going through every entry in the JSON array
        for entry in data["new_json"]:

            # Constructing and Inserting a Header row
            reqHeader = entry["ReqHeaders"]
            sql = "INSERT INTO `mydtbs`.`Header` ( `content_type`, `age`, `cache_control`, `pragma`, `expires`, `last_modified`, `host`) VALUES(%s,%s,%s,%s,%s,%s,%s);"
            val = (reqHeader["content_type"], if_empty_string_then_none(reqHeader["age"]), reqHeader["cache_control"],
                   reqHeader["pragma"], None  # reqHeader["expires"]
                   , None  # reqHeader["last_modified"]
                   , reqHeader["host"])
            mycursor.execute(sql, val)
            resHeaderID = mycursor.lastrowid  # Keeping the id of the created row

            # Constructing and Inserting a Header row
            resHeader = entry["ResHeaders"]
            sql = "INSERT INTO `mydtbs`.`Header` ( `content_type`, `age`, `cache_control`, `pragma`, `expires`, `last_modified`, `host`) VALUES(%s,%s,%s,%s,%s,%s,%s);"
            val = (resHeader["content_type"], if_empty_string_then_none(resHeader["age"]), resHeader["cache_control"],
                   resHeader["pragma"], None  # resHeader["expires"]
                   , None  # resHeader["last_modified"]
                   , resHeader["host"])
            mycursor.execute(sql, val)
            resHeaderID = mycursor.lastrowid  # Keeping the id of the created row

            mycursor.execute("SELECT * FROM Ip WHERE ip=%s",
                             (entry["serverIPAddress"],))

            if len(mycursor.fetchall()) == 0:
                # Constructing and Inserting an IP row
                sql = "INSERT INTO `mydtbs`.`Ip` (`ip`) VALUES (%s)"
                val = (entry["serverIPAddress"],)
                mycursor.execute(sql, val)

            # Constructing and Inserting an Entry row
            sql = """INSERT INTO `mydtbs`.`Entry` (`email`, `serverIPAddress`, `reqHeader`, `resHeader`, `method`, `startedDateTime`, `wait`, `url`, `status`, `statusText`, `day`)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
            val = (email, entry["serverIPAddress"], resHeaderID, resHeaderID, entry["method"],
                   clean_datetime(entry["startedDateTime"]), entry["timings"],
                   entry["url"].split(("?"), 1)[0], entry["status"], entry["statusText"], "monday")
            mycursor.execute(sql, val)

        # Commit to the database so our inserted data gets saved permanently
        self.mydb.commit()
        print("Data Inserted Successfully!")


def clean_datetime(datetime):
    date = datetime.split("T", 1)[0]
    time = datetime.split("T", 1)[1].split("Z", 1)[0][0:-4]
    return date + " " + time


def if_empty_string_then_none(string):
    if len(string) == 0:
        return None
    return string

#{"serverIPAddress":"104.248.50.87","startedDateTime":"2020-11-22T22:30:24.913Z","timings":218.69900000024336,"method":"GET","url":"https://vuejs.org/","ReqHeaders":{"content_type":"","cache_control":""},"status":200,"statusText":"","ResHeaders":{"content_type":"","cache_control":"public, max-age=0, must-revalidate"}}


# db = MySQL()

# db.insert_data("dlp@gmail.com")

# db.create_user({"email": "e@ppp.com", "username": "yoyo",
#                 "password": "password", "ip": "1.1.1.1", "isp": "Wind"})

# print(clean_datetime("2020-11-22T22:30:24.913Z"))
