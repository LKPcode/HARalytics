import re
import datetime
import json
import mysql.connector
from IPrequest import get_ips_data_array

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

        mycursor.execute("SELECT * FROM Ip WHERE ip=%s",
                         (user["ip"],))

        if len(mycursor.fetchall()) == 0:
            # Constructing and Inserting an IP row
            sql = "INSERT INTO `mydtbs`.`Ip` (`ip`) VALUES (%s)"
            val = (user["ip"],)
            mycursor.execute(sql, val)

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
            val = (
                if_empty_string_then_none(reqHeader["content_type"]),
                if_empty_string_then_none(reqHeader["age"]),
                if_empty_string_then_none(reqHeader["cache_control"]),
                if_empty_string_then_none(reqHeader["pragma"]),
                modify_expires_date(reqHeader["expires"]),
                None,  # reqHeader["last_modified"]
                if_empty_string_then_none(reqHeader["host"]))

            mycursor.execute(sql, val)
            reqHeaderID = mycursor.lastrowid  # Keeping the id of the created row

            # Constructing and Inserting a Header row
            resHeader = entry["ResHeaders"]
            sql = "INSERT INTO `mydtbs`.`Header` ( `content_type`, `age`, `cache_control`, `pragma`, `expires`, `last_modified`, `host`) VALUES(%s,%s,%s,%s,%s,%s,%s);"
            val = (
                if_empty_string_then_none(resHeader["content_type"]),
                if_empty_string_then_none(resHeader["age"]),
                if_empty_string_then_none(resHeader["cache_control"]),
                if_empty_string_then_none(resHeader["pragma"]),
                modify_expires_date(resHeader["expires"]),
                None,  # resHeader["last_modified"]
                if_empty_string_then_none(resHeader["host"]))

            mycursor.execute(sql, val)
            resHeaderID = mycursor.lastrowid  # Keeping the id of the created row

            entry["serverIPAddress"] = clean_ip(entry["serverIPAddress"])

            mycursor.execute("SELECT * FROM Ip WHERE ip=%s",
                             (entry["serverIPAddress"],))

            if len(mycursor.fetchall()) == 0:
                # Constructing and Inserting an IP row
                sql = "INSERT INTO `mydtbs`.`Ip` (`ip`) VALUES (%s)"
                val = (entry["serverIPAddress"],)
                mycursor.execute(sql, val)

            if len(entry["serverIPAddress"]) == 0:
                continue

            # Constructing and Inserting an Entry row
            sql = """INSERT INTO `mydtbs`.`Entry` (`email`, `serverIPAddress`, `reqHeader`, `resHeader`, `method`, `startedDateTime`, `wait`, `url`,  `domain`,`is_page`, `status`, `statusText`, `day`)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
            val = (email,
                   entry["serverIPAddress"],
                   reqHeaderID,
                   resHeaderID,
                   entry["method"],
                   clean_datetime(entry["startedDateTime"]),
                   entry["timings"],
                   entry["url"].split(("?"), 1)[0][0:500],
                   get_domain(entry["url"]),
                   url_is_page(entry["url"]),
                   entry["status"],
                   entry["statusText"],
                   get_day_of_week(clean_datetime(entry["startedDateTime"])))

            mycursor.execute(sql, val)

        # Commit to the database so our inserted data gets saved permanently
        self.mydb.commit()
        self.get_ip_data()
        print("Data Inserted Successfully!")

    def get_ip_data(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM Ip WHERE city IS NULL;")

        ips = []
        for row in mycursor.fetchall():
            ips.append(row[0])

        ip_data = get_ips_data_array(ips)

        for res in ip_data:

            if len(res) > 1:
                mycursor.execute("UPDATE Ip SET country=%s, city=%s, x=%s, y=%s WHERE ip=%s",
                                 (res["country_name"], res["city"],  res["latitude"], res["longitude"], res["ip"]))

        self.mydb.commit()

        print("New IPs where updated")

    def get_heatmap_data_of_user(self, email):

        mycursor = self.mydb.cursor(dictionary=True)

        sql = "select distinct Entry.domain , Ip.ip , Ip.country,  Ip.city, Ip.x, Ip.y  from Entry JOIN Ip ON Entry.serverIPAddress = Ip.ip where Entry.is_page='true' AND Entry.email=%s;"
        val = (email,)

        mycursor.execute(sql, val)

        data = mycursor.fetchall()

        return data

    def get_server_graph_data(self):

        mycursor = self.mydb.cursor(dictionary=True)

        mycursor.execute(
            "SELECT User.email, User.ip , Ip.city as ip_city , Ip.x as ip_x , Ip.y as ip_y  from User left Join Ip on Ip.ip=User.ip;")
        emails = mycursor.fetchall()

        new_structure = []
        for row in emails:
            print("Emails: ", row["email"])
            sql = "select count(User.email) as count, Entry.serverIPAddress, entry_ip.city as server_city,   entry_ip.x as server_x, entry_ip.y as server_y \
                from User Join Entry on Entry.email=User.email \
                left Join Ip on Ip.ip=User.ip  \
                left Join Ip as entry_ip on entry_ip.ip=Entry.serverIPAddress \
                where User.email=%s group by User.ip, Entry.serverIPAddress, Entry.email "

            val = (row["email"],)
            mycursor.execute(sql, val)
            data = mycursor.fetchall()

            new_structure.append({"servers": data, "user": row})

        return new_structure


# DATA CLEANING FUNCTIONS


def clean_datetime(dt):
    date = dt[0:10]
    time = dt[11:19]
    dat = date + " " + time
    return dat


def get_day_of_week(dat):
    weekday = datetime.datetime.strptime(
        dat, "%Y-%m-%d %H:%M:%S").strftime("%A")
    return weekday.lower()


def if_empty_string_then_none(string):
    if len(string) == 0:
        return None
    return string


def modify_expires_date(dt):
    # Expires field converter
    if len(dt) < 5:
        return None
    return datetime.datetime.strptime(
        dt, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d %H:%M:%S')


# Fri, 19 Nov 2021 22:11:49 GMT

# {"serverIPAddress":"104.248.50.87","startedDateTime":"2020-11-22T22:30:24.913Z","timings":218.69900000024336,"method":"GET","url":"https://vuejs.org/","ReqHeaders":{"content_type":"","cache_control":""},"status":200,"statusText":"","ResHeaders":{"content_type":"","cache_control":"public, max-age=0, must-revalidate"}}


# db = MySQL()
# print(db.get_server_graph_data())


# db.get_heatmap_data_of_user("simpleanon@tutanota.com")
# db.get_ip_data()
# db.insert_data("dlp@gmail.com")

# db.create_user({"email": "e@ppp.com", "username": "yoyo",
#                 "password": "password", "ip": "1.1.1.1", "isp": "Wind"})

# print(clean_datetime("2020-11-22T22:30:24.913Z"))


# clean = clean_datetime("2020-11-22T22:30:24.913Z")
# print(clean)
# get_day_of_week(clean)

# # Load the test.json data into the "data" variable
# with open('./uploads/test2.json') as json_file:
#     data = json.load(json_file)
#     for entry in data["new_json"]:
#         resHeader = entry["ResHeaders"]
#         if resHeader["last_modified"] != "":
#             print(resHeader["last_modified"])

def url_is_page(url):
    obj = re.match(r"(.*//[a-z\.]*)/?([^.]*)(\.html|\.asp|\.jsp|\.php|).*",
                   url)

    if obj is None:
        return "false"

    if obj.group(3) != "":
        return "true"
    elif obj.group(2) == "" and obj.group(3) == "":
        return "true"
    return "false"


def get_domain(url):
    obj = re.match(r".*//([a-z\.0-9\-]*)/?.*",
                   url)
    return obj.group(1)


def clean_ip(ip):
    obj = re.match(r"\[(.*)\]", ip)
    if obj:
        ip = obj.group(1)
    return ip


# print(url_is_page("https://vuejs.org"))

# print(get_domain("https://vuejs.org/djsk"))


# print(clean_ip("[2a00:1450:4001:824::200e]"))
