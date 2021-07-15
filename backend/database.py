from rich import print
from rich import pretty
import dateutil.parser as ps
import re
import datetime
import json
import math
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
                     user["password"], user["isp"], user["admin"])

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
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * from User WHERE email=%s", (user["email"],))
        result = mycursor.fetchall()
        if len(result) > 0:
            return result[0]
        return None

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
            dirct = clean_cache_control(reqHeader["cache_control"])
            sql = "INSERT INTO `mydtbs`.`Header` ( `content_type`, `age`, `cache_control`,`private`, `public`, `immutable`, `no-cache`, `no-store`, `max-age`, `max-stale`, `min-fresh`, `pragma`, `expires`, `last_modified`, `host`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            val = (
                if_empty_string_then_none(reqHeader["content_type"]),
                if_empty_string_then_none(reqHeader["age"]),
                if_empty_string_then_none(reqHeader["cache_control"]),
                dirct["private"],
                dirct["public"],
                dirct["immutable"],
                dirct["no-cache"],
                dirct["no-store"],
                dirct["max-age"],
                dirct["max-stale"],
                dirct["min-fresh"],
                if_empty_string_then_none(reqHeader["pragma"]),
                modify_expires_date(reqHeader["expires"]),
                modify_expires_date(reqHeader["last_modified"]),
                if_empty_string_then_none(reqHeader["host"]))

            mycursor.execute(sql, val)
            reqHeaderID = mycursor.lastrowid  # Keeping the id of the created row

            # Constructing and Inserting a Header row
            resHeader = entry["ResHeaders"]
            dirct = clean_cache_control(resHeader["cache_control"])

            sql = "INSERT INTO `mydtbs`.`Header` ( `content_type`, `age`, `cache_control`,`private`, `public`, `immutable`, `no-cache`, `no-store`, `max-age`, `max-stale`, `min-fresh`, `pragma`, `expires`, `last_modified`, `host`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            val = (
                if_empty_string_then_none(resHeader["content_type"]),
                if_empty_string_then_none(resHeader["age"]),
                if_empty_string_then_none(resHeader["cache_control"]),
                dirct["private"],
                dirct["public"],
                dirct["immutable"],
                dirct["no-cache"],
                dirct["no-store"],
                dirct["max-age"],
                dirct["max-stale"],
                dirct["min-fresh"],
                if_empty_string_then_none(resHeader["pragma"]),
                modify_expires_date(resHeader["expires"]),
                modify_expires_date(resHeader["last_modified"]),
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
                                 (res["country"], res["city"],  res["lat"], res["lon"], res["query"]))

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
        max_count = 0
        for row in emails:
            print("Emails: ", row["email"])
            sql = """
            select CONVERT(SUM(count) , UNSIGNED) as count, serverIPAddress, server_city, server_x, server_y from (select count(User.email) as count, Entry.serverIPAddress, entry_ip.city as server_city, entry_ip.x as server_x, entry_ip.y as server_y \
            from User Join Entry on Entry.email=User.email 
            left Join Ip on Ip.ip=User.ip  
            left Join Ip as entry_ip on entry_ip.ip=Entry.serverIPAddress 
            where User.email=%s group by User.ip, Entry.serverIPAddress, Entry.email) as ok
            group by ok.server_x, ok.server_y order by count DESC;
            """

            val = (row["email"],)
            mycursor.execute(sql, val)
            data = mycursor.fetchall()
            print(row["email"])
            print(data)
            #Find maximum count so that we can normalize it for visualization
            
            if len(data) > 0 and data[0]["count"] > max_count:
                max_count = data[0]["count"]

            new_structure.append({"servers": data, "user": row})

        print("MAX COUNT",max_count)
        # Normalize Count values and assign them a color
        for i in range(len(new_structure)):
            for j in range(len(new_structure[i]["servers"])):
                normalized = math.ceil(8 * new_structure[i]["servers"][j]["count"] / max_count ) + 1
                new_structure[i]["servers"][j]["count"] = normalized
                print(new_structure[i]["servers"][j]["count"])
                if normalized < 3: new_structure[i]["servers"][j]["color"] = "#33cc00"
                elif normalized < 6: new_structure[i]["servers"][j]["color"] = "#2db300"
                else: new_structure[i]["servers"][j]["color"] = "#269900"

        return new_structure

            #Admin 1

    def count_users(self):  #admin 1.a
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute(
            """
                SELECT COUNT(User.email) AS user_counter
                FROM User;
            """)
        response = mycursor.fetchall()
        user_counter = response[0]['user_counter']
        return user_counter

    def entries_per_method(self):  #admin 1.b
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute(
            """
                SELECT  Entry.method,count(*) AS entries
                FROM Entry
                GROUP BY method;
            """)
        response = mycursor.fetchall()
        return response

    def entries_per_status(self):  #admin 1.c
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute(
            """
                SELECT  Entry.status,count(*) AS entries
                FROM Entry
                GROUP BY status;
            """)
        response = mycursor.fetchall()
        return response

    def count_domains(self):  #admin 1.d
            mycursor = self.mydb.cursor(dictionary=True)
            mycursor.execute(
                """
                    SELECT COUNT(DISTINCT Entry.domain) AS domain_counter
                    FROM Entry;
                """)
            response = mycursor.fetchall()
            domain_counter = response[0]['domain_counter']
            return domain_counter


    def count_providers(self):  #admin 1.e
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute(
            """
                SELECT COUNT(DISTINCT User.ISP) AS provider_counter
                FROM User;
            """)
        response = mycursor.fetchall()
        provider_counter = response[0]['provider_counter']
        return provider_counter


    def avg_entry_age_per_type(self):  #admin 1.f
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute(                                   #Cast float
            """
                SELECT Header.content_type, cast(avg(Header.age) as FLOAT) as average_object_age
                FROM Header
                WHERE age IS NOT NULL
                GROUP BY content_type;
            """)
        response = mycursor.fetchall()
        return response

    #Admin 2

    def request_timings(self, args):  #admin 2.a, 2.b, 2.c, 2.d
        mycursor = self.mydb.cursor(dictionary=True)

        mycursor.callproc('Proc2', args)

        response = []
        for result in mycursor.stored_results():
            response.append(result.fetchall())

        return response[0]

    def ttl(self, args):  #admin 3.a
        mycursor = self.mydb.cursor(dictionary=True)

        mycursor.callproc('Proc3a', args)

        response = []
        for result in mycursor.stored_results():
            response.append(result.fetchall())

        return response[0]

    def max_staled_or_min_fresh(self, args):  #admin 3.b
        mycursor = self.mydb.cursor(dictionary=True)

        mycursor.callproc('Proc3b', args)

        response = []
        for result in mycursor.stored_results():
            response.append(result.fetchall())

        return response[0][0]["max_stale_or_min_fresh"]

    def cacheability(self, args):  #admin 3.c
        mycursor = self.mydb.cursor(dictionary=True)

        mycursor.callproc('Proc3c', args)

        response = []
        for result in mycursor.stored_results():
            response.append(result.fetchall())

        return response[0][0]["cashed"] 

    def distinct_attributes(self):  #admin 2
            mycursor = self.mydb.cursor(dictionary=True)
            mycursor.callproc('Proc2_da')

            response = {'ISP': [], 'method': [],'content_type': []}
            for count,result in enumerate(mycursor.stored_results()):
                dicts = result.fetchall()
               
                if count == 0:
                    key='ISP'
                elif count ==1:
                    key='method'
                elif count ==2:
                    key = 'content_type'
                else: print("Something went wrong")

                for dict in dicts:
                    if dict[key] is not None:
                        response[key].append(dict[key])
            return response

    def change_password(self, user, new_password):
            mycursor = self.mydb.cursor()
            sql = """
                    UPDATE User
                    SET password = %s
                    WHERE email = %s
                """
            val = (new_password, user['email'])
            mycursor.execute(sql,val)
            self.mydb.commit()
            print(mycursor.rowcount, "record(s) affected")

    def change_username(self, user, new_username):
        mycursor = self.mydb.cursor()
        sql = """
                UPDATE User
                SET username = %s
                WHERE email = %s
              """
        val = (new_username, user['email'])
        mycursor.execute(sql,val)
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) affected")

    def update_last_upload(self, user):
        mycursor = self.mydb.cursor()
        sql = """
                UPDATE User
                SET last_upload = CURRENT_TIMESTAMP()
                WHERE email = %s
              """
        val = (user['email'],)
        mycursor.execute(sql,val)
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) affected")





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


# Fri, 19 Nov 2021 22:11:49 GMT
def modify_expires_date(dt):
    # Expires field converter
    if len(dt) < 5:
        return None

    dt = ps.parse("19 Nov 2021 22:11:49 GMT", ignoretz=True)

    return dt.strftime('%Y-%m-%d %H:%M:%S')


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

# print(modify_expires_date(" Fri, 19 Nov 2021 22:11:49 GMT"))


# obj = re.match(r"(public)?.*(private)?.*(immutable)?.*(max-age)=(.*)?.*((stale-while-revalidate=)(.*))?.*",
#                "public, private, immutable, max-age=31536000, stale-while-revalidate=6,")

# print(obj)
# print(obj.groups())


def clean_cache_control(cache_control):

    obj = re.match(
        r"^(?=.*(private))?(?=.*(public))?(?=.*(immutable))?(?=.*(no-cache))?(?=.*(no-store))?(?=.*(max-age)=([0-9]*))?(?=.*(min-fresh)=([0-9]*))?(?=.*(max-stale)=([0-9]*))?.+",
        cache_control)

    directives = {
        "private": None,
        "public": None,
        "immutable": None,
        "no-cache": None,
        "no-store": None,
        "max-age": None,
        "min-fresh": None,
        "max-stale": None
    }
    if obj:

        i = 1
        for directive in directives.keys():
            if obj.group(i):
                directives[directive] = "true"
            if obj.group(i) == "max-age":
                i += 1
                directives["max-age"] = obj.group(i)
            if obj.group(i) == "min-fresh":
                i += 1
                directives["max-stale"] = obj.group(i)
            i += 1

    return directives


# db = MySQL()

# data = db.entries_per_method()