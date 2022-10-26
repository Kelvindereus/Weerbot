from unicodedata import name
import disnake
from disnake.ext import commands
import mysql.connector
#mijn modules
import default_plan_pwa
import premium_plan_pwa
import time 
from threading import Thread 
import secrets
from secrets import secure


list_premium_servers = [1002208148930691172, 444581384745648146]
bot = commands.Bot("!") 
from threading import Thread 
import time 
 
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
t = EverySoOften(30) 
t.start() 
    
         

@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.listening , name="/weer"))
    global cursor
    global db
    db = mysql.connector.connect(
    host="172.17.0.1",
    user=secure.dadatabase_username,
    password=secure.database_password,
    database="weerbot",
    auth_plugin="mysql_native_password"
    )
    cursor = db.cursor(buffered=True)
    print("The bot is ready!")

@bot.event
async def member_count_channel():
    welchannel = bot.get_channel("1002208417458442350")
    server_count = str(len(bot.guilds))    
    await bot.edit_channel(welchannel, f"members: " + str(server_count))
    

@bot.slash_command(description="Alle commands voor de Weerbot!")
@commands.cooldown(1, 3, commands.BucketType.user)
async def weer_help(inter):
        server_id_from_m = inter.guild.id
        if server_id_from_m in list_premium_servers:
            await premium_plan_pwa.send_help_embed(inter)
        else:
            await default_plan_pwa.send_help_embed(inter)

@bot.slash_command(description="Weer")
@commands.cooldown(1, 3, commands.BucketType.user)
async def weer(inter):
        server_id_from_m = inter.guild.id
        author_id_from_m = inter.author.id
        await get_default_city_db(inter, author_id_from_m, server_id_from_m)
            
@bot.slash_command(description="Weer stel je default stad in!")
@commands.cooldown(1, 3, commands.BucketType.user)
async def weer_set_standaard_stad(inter, stad: str):
        user_id = inter.author.id
        user_city =  stad
        await default_city_users(inter, user_id, user_city)   

@bot.slash_command(description="Het weer voor nu!")
@commands.cooldown(1, 3, commands.BucketType.user)
async def weer_nu(inter, stadnaam: str):
        server_id_from_m = inter.guild.id
        if server_id_from_m in list_premium_servers:
            await premium_plan_pwa.weather_NL_city(inter, stadnaam)
        else:
            await default_plan_pwa.weather_NL_city(inter, stadnaam)

@bot.slash_command(description="Het weer voor morgen!")
@commands.cooldown(1, 3, commands.BucketType.user)
async def weer_morgen(inter, stadnaam: str):
        server_id_from_m = inter.guild.id
        if server_id_from_m in list_premium_servers:
            await premium_plan_pwa.weather_NL_city_tomorrow(inter, stadnaam)
        else:
            await default_plan_pwa.weather_NL_city_tomorrow(inter, stadnaam)

@bot.slash_command(description="De weersvoorspelling voor de komende uren!!")
@commands.cooldown(1, 3, commands.BucketType.user)
async def weer_voorspelling(inter, stadnaam: str):
        server_id_from_m = inter.guild.id
        if server_id_from_m in list_premium_servers:
            await premium_plan_pwa.weather_NL_city_voorspelling(inter, stadnaam)
        else:
            await default_plan_pwa.weather_NL_city_voorspelling(inter, stadnaam)







# Database stuff, defining enzo
async def get_default_city_db(inter, author_id_from_m, server_id_from_m):
        cursor.execute("SELECT city_set FROM weerbot_default_city WHERE city_set_author_id='" + str (author_id_from_m) + str ("'"))
        db.commit()
        result_city = cursor.fetchall()
        result_city = result_city[0][0]
        print(result_city)
        if server_id_from_m in list_premium_servers:
            await premium_plan_pwa.weather_NL_general(inter, result_city)
        else:
            await default_plan_pwa.weather_NL_general(inter, result_city)

           
async def default_city_users(inter, user_id, user_city):
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
        
    await inter.response.send_message("Je hebt je standaard stad succesvol gewijzigd naar: {}. Gebruik /weer om er gebruik van te maken.".format(user_city))
    
            
bot.run(secure.bot_token)

