from curses.ascii import NL
import discord
import requests
from discord.ext import commands
import logging
from re import M
from datetime import date
from datetime import datetime
from statistics import mode
import mysql.connector
from threading import Timer
import threading
from threading import Thread 
import time 

#mijn modules:
import default_plan_pwa
import premium_plan_pwa

prefix = "!weerbot."
intents = discord.Intents.default()
bot = discord.Client(intents=discord.Intents.default())

#Hier komen de server die premium hebben
list_premium_servers = [1002208148930691172, 444581384745648146]

messaged = []

#DB creds en getting ready discord
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening , name="!weer.help"))
    global cursor
    global db
    db = mysql.connector.connect(
    host="localhost",
    user="USERNAME_HERE",
    password="PASSWORD_HERE",
    database="DB_HERE",
    auth_plugin="mysql_native_password"
    )
    cursor = db.cursor(buffered=True)
    logging.info("{0.user} is ready to rock!!!".format(bot))
    print("{0.user} is ready to rock!!!".format(bot))
     
     

#Update de server counter naar de DB, voor de website
class EverySoOften(Thread): 
    def __init__(self, seconds):   
        super().__init__()  
        self.delay = seconds 
        self.is_done = False 
    def done(self): 
        self.is_done = True 
    def run(self): 
        while not self.is_done: 
            time.sleep(self.delay)
            global cursor
            global db
            server_count = str(len(bot.guilds))
            cursor.execute("UPDATE weerbot SET server_count = " + str(server_count))
            db.commit()
        print('thread done') 
t = EverySoOften(30) 
t.start() 
    
#Leegt ieder minuut de count in de DB
class EverySoOften(Thread): 
    def __init__(self, seconds):   
        super().__init__()  
        self.delay = seconds 
        self.is_done = False 
    def done(self): 
        self.is_done = True 
    def run(self): 
        while not self.is_done: 
            time.sleep(self.delay) 
            global cursor
            global db
            server_id = cursor.execute("UPDATE weerbot_rate_limiter set server_command_count = '0'")
            db.commit()            
        print('thread done') 
t = EverySoOften(60) 
t.start()      
     




#Rate limiet !weer
async def rate_limit(m, server_id_from_m, author_message):
    global cursor
    global db
    cursor.execute("SELECT server_command_id FROM weerbot_rate_limiter WHERE server_command_id='" + str (server_id_from_m) + str ("'"))
    db.commit()
    result = cursor.fetchall()
    print(result)
    if len(result) == 0:
        print("nieuwe server")
        cursor.execute("INSERT INTO weerbot_rate_limiter(server_command_id, server_command_count) VALUES ("+ str(server_id_from_m) + ", " + str("1") + ")")
        db.commit()
        if server_id_from_m in list_premium_servers:
            await premium_plan_pwa.weather_NL_general(m)
        else:
            await default_plan_pwa.weather_NL_general(m)
    else:
        cursor.execute("SELECT server_command_count FROM weerbot_rate_limiter WHERE server_command_id='" + str (server_id_from_m) + str ("'"))
        count = cursor.fetchall()
        count = count[0][0]
        count_to_db = count + 1
        cursor.execute("UPDATE weerbot_rate_limiter set server_command_count = '{0}' WHERE server_command_id = '{1}'".format(count_to_db, server_id_from_m))
        db.commit()
                
        if server_id_from_m in list_premium_servers:
            rate_cap = 8
        else:
            rate_cap = 5

        if count >= rate_cap:
            await m.channel.send("Cooldown 1 minuut")
            print("Er is een cooldown actief in de server: {} door user {}".format(m.guild.name, m.author.name))
        elif count < rate_cap:
            if server_id_from_m in list_premium_servers:
                cursor.execute("SELECT city_set FROM weerbot_default_city WHERE city_set_author_id='" + str (author_message) + str ("'"))
                db.commit()
                result_city = cursor.fetchall()
                
                print("Resultaat van je stad: ", result_city)
                result_city = result_city[0][0]
                print(result_city)
                await premium_plan_pwa.weather_NL_general(m, result_city)
            else:
                await default_plan_pwa.weather_NL_general(m, result_city)
            
            
            
#Rate limiet !weer stadnaam
async def rate_limit2(m, server_id_from_m, city_user_input):
    global cursor
    global db
    global weather_NL_city
    cursor.execute("SELECT server_command_id FROM weerbot_rate_limiter WHERE server_command_id='" + str (server_id_from_m) + str ("'"))
    db.commit()
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.execute("INSERT INTO weerbot_rate_limiter(server_command_id, server_command_count) VALUES ("+ str(server_id_from_m) + ", " + str("1") + ")")
        db.commit()
        if server_id_from_m in list_premium_servers:
            await premium_plan_pwa.weather_NL_city(m, city_user_input, server_id_from_m)
        else:
            await default_plan_pwa.weather_NL_city(m, city_user_input, server_id_from_m)
    else:
        cursor.execute("SELECT server_command_count FROM weerbot_rate_limiter WHERE server_command_id='" + str (server_id_from_m) + str ("'"))
        count = cursor.fetchall()
        count = count[0][0]
        count_to_db = count + 1
        cursor.execute("UPDATE weerbot_rate_limiter set server_command_count = '{0}' WHERE server_command_id = '{1}'".format(count_to_db, server_id_from_m))
        db.commit()
        
        if server_id_from_m in list_premium_servers:
            rate_cap = 8
        else:
            rate_cap = 5
                    
        if count >= rate_cap:
            await m.channel.send("Cooldown 1 minuut")
            print("Er is een cooldown actief in de server: {} door user {}".format(m.guild.name, m.author.name))
            
        elif count < rate_cap:
            if server_id_from_m in list_premium_servers:
                await premium_plan_pwa.weather_NL_city(m, city_user_input, server_id_from_m)
            else:
                await default_plan_pwa.weather_NL_city(m, city_user_input, server_id_from_m)
       
       
#Rate limiet !weer stadnaam morgen             
async def rate_limit3(m, server_id_from_m, city_user_input, weather_time_user_input):
    global cursor
    global db
    cursor.execute("SELECT server_command_id FROM weerbot_rate_limiter WHERE server_command_id='" + str (server_id_from_m) + str ("'"))
    db.commit()
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.execute("INSERT INTO weerbot_rate_limiter(server_command_id, server_command_count) VALUES ("+ str(server_id_from_m) + ", " + str("1") + ")")
        db.commit()
        if server_id_from_m in list_premium_servers:
            await premium_plan_pwa.weather_NL_city_tomorrow(m, city_user_input, weather_time_user_input)
        else:
            await default_plan_pwa.weather_NL_city_tomorrow(m, city_user_input, weather_time_user_input)
    else:
        cursor.execute("SELECT server_command_count FROM weerbot_rate_limiter WHERE server_command_id='" + str (server_id_from_m) + str ("'"))
        count = cursor.fetchall()
        count = count[0][0]
        count_to_db = count + 1
        cursor.execute("UPDATE weerbot_rate_limiter set server_command_count = '{0}' WHERE server_command_id = '{1}'".format(count_to_db, server_id_from_m))
        db.commit()
        
        if server_id_from_m in list_premium_servers:
            rate_cap = 8
        else:
            rate_cap = 5
                            
        if count >= rate_cap:
            await m.channel.send("Cooldown 1 minuut")
            print("Er is een cooldown actief in de server: {} door user {}".format(m.guild.name, m.author.name))
            
        elif count < rate_cap:
            if server_id_from_m in list_premium_servers:
                await premium_plan_pwa.weather_NL_city_tomorrow(m, city_user_input, weather_time_user_input)
            else:
                await default_plan_pwa.weather_NL_city_tomorrow(m, city_user_input, weather_time_user_input)
      
   

#start commands
@bot.event
async def on_message(m):
    global messaged
    global server_id_from_m
    
    if m.content.lower().startswith("!weer.help"):
        if m.guild.id in list_premium_servers:
            await premium_plan_pwa.send_help_embed(m)
        else: 
            await default_plan_pwa.send_help_embed(m)
            
      
    elif m.content.lower().startswith("!weer.servers"):
            await m.channel.send("Ik zit in " + str(len(bot.guilds)) + " servers!")
            
    elif m.content.lower().startswith("!standaard.stad"):
            if m.guild.id in list_premium_servers:
                server_id_from_m = m.guild.id
                user_city =  m.content.split(" ")[1]
                user_id = m.author.id
                author_message = m.author.id
                await default_city_users(m, user_id, user_city)   
            else:
                await m.channel.send("Je hebt premium nodig om deze funtie te kunnen uitvoeren!")
    
    elif m.content.lower().startswith("!weer"):
            server_id_from_m = m.guild.id
            author_message = m.author.id
            count_spaces_start = m.content
            count_spaces_start = str(m.content)
            count=0
            for i in count_spaces_start:
                if(i.isspace()):
                    count=count+1
            list_count_spaces = [0,1,2]        
            if count in list_count_spaces:
                
                if count == 0:
                    await rate_limit(m, server_id_from_m, author_message)                    
                    print("User {} in server {} entered start command: !weer".format(m.author.name, m.guild.name))
                
                elif count == 1:
                    city_user_input = m.content.split(" ")[1]
                    server_id_from_m = m.guild.id
                    await rate_limit2(m, server_id_from_m, city_user_input)                    
                    print("User {} in server {} entered start command: !weer {}".format(m.author.name, m.guild.name, city_user_input))

                    
                elif count == 2:
                    city_user_input = m.content.split(" ")[1]
                    weather_time_user_input = m.content.split(" ")[2]
                    server_id_from_m = m.guild.id                    
                    await rate_limit3(m, server_id_from_m, city_user_input, weather_time_user_input)                    
                    print("User {} in server {} entered start command: !weer {} morgen".format(m.author.name, m.guild.name, city_user_input))
            
            else:
                await m.channel.send("Er ging iets mis! Foutcode: Te_veel_argumenten!")
     
     

     
async def default_city_users(m, user_id, user_city):
    global cursor
    global db
    cursor.execute("SELECT * FROM weerbot_default_city WHERE city_set_author_id='" + str (user_id) + str ("'"))
    db.commit()
    result = cursor.fetchall()
    print(result)
    if len(result) == 0:
        print("nieuwe server")
        cursor.execute("INSERT INTO `weerbot_default_city` (`city_set_author_id`, `city_set`) VALUES ('{}', '{}')".format(user_id, user_city))
        db.commit()

    else:
        cursor.execute("UPDATE weerbot_default_city set city_set = '{0}' WHERE city_set_author_id = '{1}'".format(user_city, user_id))
        db.commit()
        
    await m.channel.send("Je hebt je standaard stad succesvol gewijzigd naar: {}. Gebruik !weer om er gebruik van te maken.".format(user_city))
    
bot.run('TOKENHERE')
