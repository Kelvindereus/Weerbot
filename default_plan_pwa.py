import disnake
import requests
from re import M
from datetime import date
from datetime import datetime
from statistics import mode
from threading import Timer
import matplotlib.pyplot as plt
import os

version_nummer =  ("2.0")


              
# Weerbot NL General
async def weather_NL_general(inter, result_city):
        api_key = "a8a15ef8a0ee24d6782ee2cddea5afae"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        units = ("&units=metric")
        complete_url = base_url + "appid=" + api_key + "&q=" + str(result_city) + units
        response = requests.get(complete_url)
        response_api_json = response.json()        
        if response_api_json['cod'] == "404":
            await inter.response.send_message("Er ging iets mis! Foutcode: Stad_niet_gevonden!")
        else:
            y = response_api_json["main"]
            current_temp = y["temp"]
            feeling_temp = y["feels_like"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            regenofdroog = response_api_json["weather"]
            z = response_api_json["weather"]
            weather_description = z[0]["description"]
            cloud_icon = z[0]["icon"]
            u = response_api_json["wind"]
            windspeed = u["speed"] 
            sunrise_get_data = response_api_json["sys"]["sunrise"]
            sunset_get_data = response_api_json["sys"]["sunset"]


            if '10d' == cloud_icon:   
                rain_or_dry = (":cloud_rain:  Zorg ervoor dat je een paraplu meeneemt!")
            else:
                rain_or_dry = (":cloud: Je blijft mooi droog!")

            if current_pressure > 1025: 
                h = (":compression: Dit is momenteel een hoge drukgebied!")
            else:
                h = (":compression: Dit is momenteel een lage drukgebied!")       

            if current_humidity > 70:
                d = (":sweat_drops: Het is behoorlijk vochtig in de lucht!")
            else:
                d = (":droplet: Het is best wel droog in de lucht!")
            if '01d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/sunedited.png")
            elif '01n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/01n@2x.png")
            elif '02d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/02d@2x.png")
            elif '02n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/02n@2x.png")
            elif '03d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/03d@2x.png")
            elif '03n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/03n@2x.png")      
            elif '04d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/04d@2x.png")
            elif '04n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/04n@2x.png")
            elif '09d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/09d@2x.png")
            elif '09n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/09n@2x.png")                            
            elif '10d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/10d@2x.png")
            elif '10n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/10n@2x.png")      
            elif '11d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/11d@2x.png")
            elif '11n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/11n@2x.png")
            elif '13d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/13d@2x.png")
            elif '13n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/13n@2x.png")                   
            elif '50d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/50d@2x.png")
            elif '50n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/50n@2x.png")          

                
            if current_temp < 0:
                color = 0x4793FF                    
                x = ("Het vriest!")
            elif ((current_temp>= 0) and (current_temp < 18)):
                color = 0x4793FF                    
                x = (":cold_face: Ik zou een lange broek aantrekken! ")
            elif ((current_temp>= 18) and (current_temp< 30)):
                color = 0xff0000
                x = (":hot_face: Trek je korte broek maar aan! ")  
            elif current_temp >= 30:
                color = 0xff0000                    
                x = (":fire: Het is snikheet! Pak lekker een koel ijsje! ")  
                
            ts = int(sunrise_get_data)
            ts = ts + 7200
            sunrise_normal = (datetime.utcfromtimestamp(ts).strftime(' %H:%M:%S'))
            ts = int(sunset_get_data)
            ts = ts + 7200
            sunset_normal = (datetime.utcfromtimestamp(ts).strftime(' %H:%M:%S'))

            if ((windspeed>= 0) and (windspeed< 2)):
                windspeed_sentence = (":leaves: Windstil: Rook stijgt recht op uit schoorstenen. ")
            elif ((windspeed>= 2) and (windspeed< 5)):
                windspeed_sentence = (":leaves: Zwakke wind, flauw en stil: Windrichting af te leiden uit rookpluimen. ")
            elif ((windspeed>= 5) and (windspeed< 11)):
                windspeed_sentence = (":leaves: Zwak, flauwe koelte: Wind voelbaar in gezicht, bladeren bewegen licht. ")    
            elif ((windspeed>= 11) and (windspeed< 20)):
                windspeed_sentence = (":leaves: Matige wind, lichte koelte: Bladeren bewegen steeds, vlaggen wapperen. ")
            elif ((windspeed>= 20) and (windspeed< 29)):
                windspeed_sentence = (":leaves: Matige wind, matige koelte: Takken bewegen, kleding flappert. ")    
            elif ((windspeed>= 29) and (windspeed< 39)):
                windspeed_sentence = (":wind_blowing_face: Vrij krachtige, frisse bries: Matige langere golven, kleine bomen bewegen. ")
            elif ((windspeed>= 39) and (windspeed< 50)):
                windspeed_sentence = (":wind_blowing_face: Krachtige, stijve bries: Bomen bewegen, vlaggen staan strak. ")    
            elif ((windspeed>= 50) and (windspeed< 62)):
                windspeed_sentence = (":wind_blowing_face: Hard, harde wind: Matig grote golven, latig tegen wind inlopen. ")
            elif ((windspeed>= 62) and (windspeed< 75)):
                windspeed_sentence = (":wind_blowing_face: Stormachtig: Grote golven, kammen beginnen te breken, kleine takken breken af. ")             
            elif ((windspeed>= 75) and (windspeed< 89)):
                windspeed_sentence = (":cloud_tornado: Storm: Hoge golven, golven rollen en kammen breken, veel stuifwater, takken breken. ")
            elif ((windspeed>= 89) and (windspeed< 103)):
                windspeed_sentence = (":cloud_tornado: Zware storm: Zeer hoge golven, hele oppervlak is wit van stuifwater, bomen worden ontworteld. ")    
            elif ((windspeed>= 103) and (windspeed< 118)):
                windspeed_sentence = (":cloud_tornado: Zeer zware storm, orkaanachtig: Buitengewoon hoge golven, grote schade aan bossen/gebouwen. ")
            elif windspeed >= 118: 
                windspeed_sentence = (":cloud_tornado: AAAH! RUN BITCH< RUUUUN. Orkaan: Lucht gevuld met schuim en water, verwoestingen aan gebouwen en bossen, extreem hoge golven. ")   
            
            
            embed = disnake.Embed(
                title="Weer-info voor de stad: " +str (result_city),
                description="Info geleverd door Openweathermap. Default plan!",
                color=color,
            )

            embed.set_footer(
                text="By </Kelvin>. Versie: " + str(version_nummer),
                icon_url="https://kelvindereus.nl/CustomCPULOGO.png",
            )
            embed.add_field(name="Temperatuur", value=x + str (" ") + str (round(current_temp,1)) + str ("℃"), inline=False)    
            embed.add_field(name="Windsnelheid", value=windspeed_sentence + str (round(windspeed, 2)) + str ("Km/u"), inline=False)   
            embed.add_field(name="Druk", value=h + str (" ") + str (current_pressure) + str ("mbar"), inline=False)
            embed.add_field(name="Vocht", value=d + str (" ") + str (current_humidity) + str ("%"), inline=False)
            embed.set_image(url=ci)
            embed.add_field(name="Regen", value=rain_or_dry, inline=False) 
            
            await inter.response.send_message(embed=embed)


#DEFINING
async def weather_NL_city(inter, stadnaam):
        api_key = "a8a15ef8a0ee24d6782ee2cddea5afae"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        units = ("&units=metric")
        complete_url = base_url + "appid=" + api_key + "&q=" + stadnaam + units
        response = requests.get(complete_url)
        response_api_json = response.json()   
        if response_api_json['cod'] == "404":
            await inter.response.send_message("Er ging iets mis! Foutcode: Stad_niet_gevonden!")
        else:
            y = response_api_json["main"]
            current_temp = y["temp"]
            feeling_temp = y["feels_like"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            regenofdroog = response_api_json["weather"]
            z = response_api_json["weather"]
            weather_description = z[0]["description"]
            cloud_icon = z[0]["icon"]
            u = response_api_json["wind"]
            windspeed = u["speed"] 
            sunrise_get_data = response_api_json["sys"]["sunrise"]
            sunset_get_data = response_api_json["sys"]["sunset"]


            if '10d' == cloud_icon:   
                rain_or_dry = (":cloud_rain:  Zorg ervoor dat je een paraplu meeneemt!")
            else:
                rain_or_dry = (":cloud: Je blijft mooi droog!")

            if current_pressure > 1025: 
                h = (":compression: Dit is momenteel een hoge drukgebied!")
            else:
                h = (":compression: Dit is momenteel een lage drukgebied!")       

            if current_humidity > 70:
                d = (":sweat_drops: Het is behoorlijk vochtig in de lucht!")
            else:
                d = (":droplet: Het is best wel droog in de lucht!")
            if '01d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/sunedited.png")
            elif '01n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/01n@2x.png")
            elif '02d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/02d@2x.png")
            elif '02n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/02n@2x.png")
            elif '03d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/03d@2x.png")
            elif '03n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/03n@2x.png")      
            elif '04d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/04d@2x.png")
            elif '04n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/04n@2x.png")
            elif '09d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/09d@2x.png")
            elif '09n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/09n@2x.png")                            
            elif '10d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/10d@2x.png")
            elif '10n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/10n@2x.png")      
            elif '11d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/11d@2x.png")
            elif '11n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/11n@2x.png")
            elif '13d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/13d@2x.png")
            elif '13n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/13n@2x.png")                   
            elif '50d' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/50d@2x.png")
            elif '50n' == cloud_icon:
                ci = ("https://kelvindereus.nl/images/weer/50n@2x.png")          

                
            if current_temp < 0:
                color = 0x0096FF                    
                x = ("Het vriest! ")
            elif ((current_temp>= 0) and (current_temp < 18)):
                color = 0x0096FF                    
                x = (":cold_face: Ik zou een lange broek aantrekken! ")
            elif ((current_temp>= 18) and (current_temp< 30)):
                color = 0xff0000
                x = (":hot_face: Trek je korte broek maar aan! ")  
            elif current_temp >= 30:
                color = 0xff0000                     
                x = (":fire: Het is snikheet! Pak lekker een koel ijsje! ")  
                
            ts = int(sunrise_get_data)
            ts = ts + 7200
            sunrise_normal = (datetime.utcfromtimestamp(ts).strftime(' %H:%M:%S'))
            ts = int(sunset_get_data)
            ts = ts + 7200
            sunset_normal = (datetime.utcfromtimestamp(ts).strftime(' %H:%M:%S'))

            if ((windspeed>= 0) and (windspeed< 2)):
                windspeed_sentence = (":leaves: Windstil: Rook stijgt recht op uit schoorstenen. ")
            elif ((windspeed>= 2) and (windspeed< 5)):
                windspeed_sentence = (":leaves: Zwakke wind, flauw en stil: Windrichting af te leiden uit rookpluimen. ")
            elif ((windspeed>= 5) and (windspeed< 11)):
                windspeed_sentence = (":leaves: Zwak, flauwe koelte: Wind voelbaar in gezicht, bladeren bewegen licht. ")    
            elif ((windspeed>= 11) and (windspeed< 20)):
                windspeed_sentence = (":leaves: Matige wind, lichte koelte: Bladeren bewegen steeds, vlaggen wapperen. ")
            elif ((windspeed>= 20) and (windspeed< 29)):
                windspeed_sentence = (":leaves: Matige wind, matige koelte: Takken bewegen, kleding flappert. ")    
            elif ((windspeed>= 29) and (windspeed< 39)):
                windspeed_sentence = (":wind_blowing_face: Vrij krachtige, frisse bries: Matige langere golven, kleine bomen bewegen. ")
            elif ((windspeed>= 39) and (windspeed< 50)):
                windspeed_sentence = (":wind_blowing_face: Krachtige, stijve bries: Bomen bewegen, vlaggen staan strak. ")    
            elif ((windspeed>= 50) and (windspeed< 62)):
                windspeed_sentence = (":wind_blowing_face: Hard, harde wind: Matig grote golven, latig tegen wind inlopen. ")
            elif ((windspeed>= 62) and (windspeed< 75)):
                windspeed_sentence = (":wind_blowing_face: Stormachtig: Grote golven, kammen beginnen te breken, kleine takken breken af. ")             
            elif ((windspeed>= 75) and (windspeed< 89)):
                windspeed_sentence = (":cloud_tornado: Storm: Hoge golven, golven rollen en kammen breken, veel stuifwater, takken breken. ")
            elif ((windspeed>= 89) and (windspeed< 103)):
                windspeed_sentence = (":cloud_tornado: Zware storm: Zeer hoge golven, hele oppervlak is wit van stuifwater, bomen worden ontworteld. ")    
            elif ((windspeed>= 103) and (windspeed< 118)):
                windspeed_sentence = (":cloud_tornado: Zeer zware storm, orkaanachtig: Buitengewoon hoge golven, grote schade aan bossen/gebouwen. ")
            elif windspeed >= 118: 
                windspeed_sentence = (":cloud_tornado: AAAH! RUN BITCH< RUUUUN. Orkaan: Lucht gevuld met schuim en water, verwoestingen aan gebouwen en bossen, extreem hoge golven. ")   
                

                                    
   
#            embedVar = discord.Embed(title="Weer-info voor de stad: " +str (stadnaam), description="Info geleverd door Openweathermap. Default plan!", color=color)
#            embedVar.add_field(name="Temperatuur", value=x + str (" ") + str (round(current_temp,1)) + str ("℃"), inline=False)     
#            embedVar.add_field(name="Windsnelheid", value=windspeed_sentence + str (round(windspeed, 2)) + str ("Km/u"), inline=False)     
#            
#           embedVar.add_field(name="Druk", value=h + str (" ") + str (current_pressure) + str ("mbar"), inline=False)
#           embedVar.add_field(name="Vocht", value=d + str (" ") + str (current_humidity) + str ("%"), inline=False)
#            embedVar.set_image(url=ci)
#            embedVar.add_field(name="Regen", value=rain_or_dry, inline=False) 
#            
#           embedVar.set_footer(text="By </Kelvin>. Versie: " + str(version_nummer),icon_url="https://kelvindereus.nl/CustomCPULOGO.png")

#            await inter.response.send_message(embed=embedVar)
#            print("AllDayWeer succesvol uitgevoerd.")

# Inside a command, event listener, etc.
            embed = disnake.Embed(
                title="Weer-info voor de stad: " +str (stadnaam),
                description="Info geleverd door Openweathermap. Default plan!",
                color=color,
            )

            embed.set_footer(
                text="By </Kelvin>. Versie: " + str(version_nummer),
                icon_url="https://kelvindereus.nl/CustomCPULOGO.png",
            )

            embed.add_field(name="Temperatuur", value=x + str (" ") + str (round(current_temp,1)) + str ("℃"), inline=False)    
            embed.add_field(name="Windsnelheid", value=windspeed_sentence + str (round(windspeed, 2)) + str ("Km/u"), inline=False)    
            embed.add_field(name="Druk", value=h + str (" ") + str (current_pressure) + str ("mbar"), inline=False)
            embed.add_field(name="Vocht", value=d + str (" ") + str (current_humidity) + str ("%"), inline=False)
            embed.add_field(name="Regen", value=rain_or_dry, inline=False) 
            embed.set_image(url=ci)
            await inter.response.send_message(embed=embed)




async def weather_NL_city_tomorrow(inter, stadnaam):
                api_key = "a8a15ef8a0ee24d6782ee2cddea5afae"
                base_url = "http://api.openweathermap.org/data/2.5/forecast?"
                complete_url = base_url + "appid=" + api_key + "&q=" + stadnaam
                response = requests.get(complete_url)
                data = response.json()
                
                if data['cod'] == "404":
                    await inter.response.send_message("Er ging iets mis! Foutcode: Stad_niet_gevonden!")
                
                else:
                    tempdag0tijd0 = data['list'][2]['main']['temp'] - 273.15
                    tempdag1tijd1 = data['list'][3]['main']['temp'] - 273.15
                    tempdag2tijd2 = data['list'][4]['main']['temp'] - 273.15
                    tempdag3tijd3 = data['list'][5]['main']['temp'] - 273.15
                    tempdag4tijd4 = data['list'][6]['main']['temp'] - 273.15
                    tempdag5tijd5 = data['list'][7]['main']['temp'] - 273.15
                    tempdag6tijd6 = data['list'][8]['main']['temp'] - 273.15
                    tempdag7tijd7 = data['list'][9]['main']['temp'] - 273.15
                    tempdag6tijd8 = data['list'][10]['main']['temp'] - 273.15
                
                    
                    listtempsmin = [tempdag0tijd0, tempdag1tijd1, tempdag2tijd2, tempdag3tijd3, tempdag4tijd4, tempdag5tijd5, tempdag6tijd6, tempdag6tijd8]
                    mintemp = (round(min(listtempsmin), 2))
                    maxtemp = (round(max(listtempsmin), 2))

                    feels_likedag0tijd0 = data['list'][0]['main']['feels_like'] - 273.15
                    feels_likedag1tijd1 = data['list'][1]['main']['feels_like'] - 273.15
                    feels_likedag2tijd2 = data['list'][2]['main']['feels_like'] - 273.15
                    feels_likedag3tijd3 = data['list'][3]['main']['feels_like'] - 273.15
                    feels_likeag4tijd4 = data['list'][4]['main']['feels_like'] - 273.15
                    feels_likedag5tijd5 = data['list'][5]['main']['feels_like'] - 273.15
                    feels_likedag6tijd6 = data['list'][6]['main']['feels_like'] - 273.15
                    feels_likedag7tijd7 = data['list'][7]['main']['feels_like'] - 273.15
                
                    winddag1tijd0 = data['list'][0]['wind']['speed'] * 3.6
                    winddag1tijd1 = data['list'][1]['wind']['speed'] * 3.6
                    winddag1tijd2 = data['list'][2]['wind']['speed'] * 3.6
                    winddag1tijd3 = data['list'][3]['wind']['speed'] * 3.6
                    winddag1tijd4 = data['list'][4]['wind']['speed'] * 3.6
                    winddag1tijd5 = data['list'][5]['wind']['speed'] * 3.6
                    winddag1tijd6 = data['list'][6]['wind']['speed'] * 3.6
                    winddag1tijd7 = data['list'][7]['wind']['speed'] * 3.6

                    weatherdag1tijd0 = data['list'][0]['weather'][0]['main']
                    weatherdag1tijd1 = data['list'][1]['weather'][0]['main']
                    weatherdag1tijd2 = data['list'][2]['weather'][0]['main']
                    weatherdag1tijd3 = data['list'][3]['weather'][0]['main']
                    weatherdag1tijd4 = data['list'][4]['weather'][0]['main']
                    weatherdag1tijd5 = data['list'][5]['weather'][0]['main']
                    weatherdag1tijd6 = data['list'][6]['weather'][0]['main']
                    weatherdag1tijd7 = data['list'][7]['weather'][0]['main']

                    icondag1tijd0 = data['list'][0]['weather'][0]['icon']
                    icondag1tijd1 = data['list'][1]['weather'][0]['icon']
                    icondag1tijd2 = data['list'][2]['weather'][0]['icon']
                    icondag1tijd3 = data['list'][3]['weather'][0]['icon']
                    icondag1tijd4 = data['list'][4]['weather'][0]['icon']
                    icondag1tijd5 = data['list'][5]['weather'][0]['icon']
                    icondag1tijd6 = data['list'][6]['weather'][0]['icon']
                    icondag1tijd7 = data['list'][7]['weather'][0]['icon']
                        
            ##sunrise + sunset
                    sunrise = data['city']['sunrise']
                    sunset = data['city']['sunset']
                    
                    ts = int(sunrise)
                    ts = ts + 7200
                    sunrisenormal = (datetime.utcfromtimestamp(ts).strftime(' %H:%M:%S'))

                    ts = int(sunset)
                    ts = ts + 7200
                    sunsetnormal = (datetime.utcfromtimestamp(ts).strftime(' %H:%M:%S'))


            ### gemiddelde uitrekenen
                    def Average(l): 
                        avg = sum(l) / len(l) 
                        return avg
                    temp = [tempdag0tijd0, tempdag1tijd1, tempdag2tijd2, tempdag3tijd3,
                tempdag4tijd4, tempdag5tijd5, tempdag6tijd6, tempdag7tijd7] 
                    averagetempdag1 = Average(temp) 

                    def Average(l): 
                        avg = sum(l) / len(l) 
                        return avg
                    feels_like = [feels_likedag0tijd0, feels_likedag1tijd1, feels_likedag2tijd2, feels_likedag3tijd3,
                feels_likeag4tijd4, feels_likedag5tijd5, feels_likedag6tijd6, feels_likedag7tijd7] 
                    averagefeeltempdag1 = Average(feels_like) 

                    def Average(l): 
                        avg = sum(l) / len(l) 
                        return avg
                    wind = [winddag1tijd0, winddag1tijd1, winddag1tijd2, winddag1tijd3,
                winddag1tijd4, winddag1tijd5, winddag1tijd6, winddag1tijd7] 
                    averagewindspeeddag1 = Average(wind) 

                    test_list = [weatherdag1tijd0, weatherdag1tijd1, weatherdag1tijd2, weatherdag1tijd3, 
                    weatherdag1tijd4, weatherdag1tijd5, weatherdag1tijd6, weatherdag1tijd7]
                    temp = [wrd for sub in test_list for wrd in sub.split()]
                    averagemain = mode(temp)
                    
                    test_list = [icondag1tijd0, icondag1tijd1, icondag1tijd2, icondag1tijd3,
                icondag1tijd4, icondag1tijd5, icondag1tijd6, icondag1tijd7]
                    temp = [wrd for sub in test_list for wrd in sub.split()]
                    averageicon = mode(temp)

            ### vertalen engels = > nederlands

                    if "Clouds" == averagemain:
                        AM = (":cloud: Bewolking verwacht!")
                        ci =("https://kelvindereus.nl/images/weer/03d@2x.png")
                    elif "Clear" == averagemain:
                        AM = (":white_sun_small_cloud:  Er komt geen wolkje aan de lucht")
                        ci = ("https://kelvindereus.nl/images/weer/sunedited.png")
                    elif "Rain" == averagemain:
                        AM = (":cloud_rain: Regen verwacht!")
                        ci = ("https://kelvindereus.nl/images/weer/09d@2x.png")
                    elif "Thunderstorm" == averagemain:
                        AM = (":cloud_lightning: Onweer verwacht!")
                        ci = ("https://kelvindereus.nl/images/weer/11d@2x.png")


                    if mintemp < 0:
                        mint = (":cold_face: ")
                        warning_weather_max = ("Het is beneden het vriespunt, zorg ervoor dat je je goed aankleed! ")                                
                    if ((mintemp>= 0) and (mintemp< 18)):
                        mint = (":cold_face: ")
                    if ((mintemp>= 18) and (mintemp< 30)):
                        mint = (":hot_face: ")
                    if mintemp >= 30:
                        mint = (":hot_face: ")
                        warning_weather_max = ("Vergeet niet voldoende water te drinken in dit warme weer! Ga je naar buiten? Let er dan op dat je je insmeert! (Tevens smeer dan regelmatig!) ")                
                    else:
                        warning_weather_max = ("Geen waarschuwingen momenteel! ")
                        
                    if maxtemp < 0:
                        maxt = (":cold_face: ")
                        warning_weather_max = ("Het is beneden het vriespunt, zorg ervoor dat je je goed aankleed! ")                
                    if ((maxtemp>= 0) and (maxtemp< 18)):
                        maxt = (":cold_face: ")
                    if ((maxtemp>= 18) and (maxtemp< 30)):
                        maxt = (":hot_face: ")
                    if maxtemp >= 30:
                        maxt = (":hot_face: ")
                        warning_weather_max = ("Vergeet niet voldoende water te drinken in dit warme weer! Ga je naar buiten? Let er dan op dat je je insmeert! (Tevens smeer dan regelmatig!)")                
                    else:
                        warning_weather_max = ("Geen waarschuwingen momenteel!")


                    if averagetempdag1 > 18:
                        color = 0xff0000
                        at = (":hot_face: Trek je korte broek maar aan! ")
                    else:
                        color = 0x0096FF
                        at = (":cold_face: Trek je lange broek maar aan! ")
                    if averagefeeltempdag1 > 18:
                        aft = (":hot_face: Trek je korte broek maar aan! ")
                    else:
                        aft = (":cold_face: Trek je lange broek maar aan! ")    

                    if ((averagewindspeeddag1>= 0) and (averagewindspeeddag1< 2)):
                        windspeed_sentence = (":leaves: Windstil: Rook stijgt recht op uit schoorstenen. ")
                    elif ((averagewindspeeddag1>= 2) and (averagewindspeeddag1< 5)):
                        windspeed_sentence = (":leaves: Zwakke wind, flauw en stil: Windrichting af te leiden uit rookpluimen. ")
                    elif ((averagewindspeeddag1>= 5) and (averagewindspeeddag1< 11)):
                        windspeed_sentence = (":leaves: Zwak, flauwe koelte: Wind voelbaar in gezicht, bladeren bewegen licht. ")    
                    elif ((averagewindspeeddag1>= 11) and (averagewindspeeddag1< 20)):
                        windspeed_sentence = (":leaves: Matige wind, lichte koelte: Bladeren bewegen steeds, vlaggen wapperen. ")
                    elif ((averagewindspeeddag1>= 20) and (averagewindspeeddag1< 29)):
                        windspeed_sentence = (":leaves: Matige wind, matige koelte: Takken bewegen, kleding flappert. ")    
                    elif ((averagewindspeeddag1>= 29) and (averagewindspeeddag1< 39)):
                        windspeed_sentence = (":wind_blowing_face: Vrij krachtige, frisse bries: Matige langere golven, kleine bomen bewegen. ")
                    elif ((averagewindspeeddag1>= 39) and (averagewindspeeddag1< 50)):
                        windspeed_sentence = (":wind_blowing_face: Krachtige, stijve bries: Bomen bewegen, vlaggen staan strak. ")    
                    elif ((averagewindspeeddag1>= 50) and (averagewindspeeddag1< 62)):
                        windspeed_sentence = (":wind_blowing_face: Hard, harde wind: Matig grote golven, latig tegen wind inlopen. ")
                    elif ((averagewindspeeddag1>= 62) and (averagewindspeeddag1< 75)):
                        windspeed_sentence = (":wind_blowing_face: Stormachtig: Grote golven, kammen beginnen te breken, kleine takken breken af.")             
                    elif ((averagewindspeeddag1>= 75) and (averagewindspeeddag1< 89)):
                        windspeed_sentence = (":cloud_tornado: Storm: Hoge golven, golven rollen en kammen breken, veel stuifwater, takken breken. ")
                    elif ((averagewindspeeddag1>= 89) and (averagewindspeeddag1< 103)):
                        windspeed_sentence = (":cloud_tornado: Zware storm: Zeer hoge golven, hele oppervlak is wit van stuifwater, bomen worden ontworteld. ")    
                    elif ((averagewindspeeddag1>= 103) and (averagewindspeeddag1< 118)):
                        windspeed_sentence = (":cloud_tornado: Zeer zware storm, orkaanachtig: Buitengewoon hoge golven, grote schade aan bossen/gebouwen. ")
                    elif averagewindspeeddag1 >= 118: 
                        windspeed_sentence = (":cloud_tornado: AAAH! RUN BITCH< RUUUUN. Orkaan: Lucht gevuld met schuim en water, verwoestingen aan gebouwen en bossen, extreem hoge golven. ")   
                        
                                        
                    embed = disnake.Embed(title="Weer-info voor morgen voor de stad: " +str (stadnaam), description="Je maakt gebruik van het default plan!", color=color)
                    embed.add_field(name="LET OP!", value=warning_weather_max, inline=False)            
                    embed.add_field(name="Temperatuur min", value=mint + str (mintemp) + str ("℃"), inline=True) 
                    embed.add_field(name="Temperatuur max", value=maxt + str (maxtemp) + str ("℃"), inline=True) 
                    embed.add_field(name="Gemiddelde temperatuur ", value=at + str (round(averagetempdag1,1)) + str ("℃"), inline=False)
                    embed.add_field(name="Gemiddelde gevoelstemperatuur ", value=aft + str (round(averagefeeltempdag1,1)) + str ("℃"), inline=False)
                    embed.add_field(name="Gemiddelde wind", value=windspeed_sentence + str (round(averagewindspeeddag1,1)) + str ("Km/u"), inline=False)
                    embed.set_image(url=ci)
                    embed.add_field(name="Gemiddelde wolken:", value=AM, inline=False) 
                    embed.set_footer(text="By </Kelvin>. Versie: " + str(version_nummer),icon_url="https://kelvindereus.nl/CustomCPULOGO.png")
                    await inter.response.send_message(embed=embed)
                    




                    
async def weather_NL_city_voorspelling(inter, stadnaam):
                    units = ("&units=metric")
                    api_key = "a8a15ef8a0ee24d6782ee2cddea5afae"
                    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
                    complete_url = base_url + "appid=" + api_key + "&q=" + stadnaam + units
                    response = requests.get(complete_url)
                    data = response.json()        

                    #datums
                    datums0 = data['list'][0]['dt_txt']
                    datums1 = data['list'][1]['dt_txt']
                    datums2 = data['list'][2]['dt_txt']
                    datums3 = data['list'][3]['dt_txt']
                    datums4 = data['list'][4]['dt_txt']
                    datums5 = data['list'][5]['dt_txt']
                    datums6 = data['list'][6]['dt_txt']
                    datums7 = data['list'][7]['dt_txt']
                    #temp
                    temp0 = data['list'][0]['main']['temp']
                    temp1 = data['list'][1]['main']['temp']
                    temp2 = data['list'][2]['main']['temp']
                    temp3 = data['list'][3]['main']['temp']
                    temp4 = data['list'][4]['main']['temp']
                    temp5 = data['list'][5]['main']['temp']
                    temp6 = data['list'][6]['main']['temp']
                    temp7 = data['list'][7]['main']['temp']
                    #feel_temp
                    feels_temp0 = data['list'][0]['main']['feels_like']
                    feels_temp1 = data['list'][1]['main']['feels_like']
                    feels_temp2 = data['list'][2]['main']['feels_like']
                    feels_temp3 = data['list'][3]['main']['feels_like']
                    feels_temp4 = data['list'][4]['main']['feels_like']
                    feels_temp5 = data['list'][5]['main']['feels_like']
                    feels_temp6 = data['list'][6]['main']['feels_like']
                    feels_temp7 = data['list'][7]['main']['feels_like']
                    
                    #Windsnelheid
                    wind0 = data['list'][0]['wind']['speed']
                    wind1 = data['list'][1]['wind']['speed'] 
                    wind2 = data['list'][2]['wind']['speed'] 
                    wind3 = data['list'][3]['wind']['speed']
                    wind4 = data['list'][4]['wind']['speed'] 
                    wind5 = data['list'][5]['wind']['speed'] 
                    wind6 = data['list'][6]['wind']['speed'] 
                    wind7 = data['list'][7]['wind']['speed'] 
                                        
                    #lucht-wolken enzo
                    sub_weather_condition0 = data['list'][0]['weather'][0]['main']
                    sub_weather_condition1 = data['list'][1]['weather'][0]['main']
                    sub_weather_condition2 = data['list'][2]['weather'][0]['main']
                    sub_weather_condition3 = data['list'][3]['weather'][0]['main']
                    sub_weather_condition4 = data['list'][4]['weather'][0]['main']
                    sub_weather_condition5 = data['list'][5]['weather'][0]['main']
                    sub_weather_condition6 = data['list'][6]['weather'][0]['main']
                    sub_weather_condition7 = data['list'][7]['weather'][0]['main']

                    #icoon
                    icon0 = data['list'][0]['weather'][0]['icon']
                    icon1 = data['list'][1]['weather'][0]['icon']
                    icon2 = data['list'][2]['weather'][0]['icon']
                    icon3 = data['list'][3]['weather'][0]['icon']
                    icon4 = data['list'][4]['weather'][0]['icon']
                    icon5 = data['list'][5]['weather'][0]['icon']
                    icon6 = data['list'][6]['weather'][0]['icon']
                    icon7 = data['list'][7]['weather'][0]['icon']
                    
                    
                    datums0_formatted = datums0.split(" ")[1][0:5] #[0:5] pakt de 1e 5 karakters
                    datums1_formatted = datums1.split(" ")[1][0:5]
                    datums2_formatted = datums2.split(" ")[1][0:5]
                    datums3_formatted = datums3.split(" ")[1][0:5]
                    datums4_formatted = datums4.split(" ")[1][0:5]
                    datums5_formatted = datums5.split(" ")[1][0:5]
                    datums6_formatted = datums6.split(" ")[1][0:5]
                    datums7_formatted = datums7.split(" ")[1][0:5]
                    
                   
                
                    y_temp = [temp0, temp1, temp2, temp3, temp4, temp5, temp6, temp7]
                    x_time = [datums0_formatted, datums1_formatted, datums2_formatted, datums3_formatted, datums4_formatted, datums5_formatted, datums6_formatted, datums7_formatted]
                    axis_y_wind= [wind0, wind1, wind2, wind3, wind4, wind5, wind6, wind7]
                    



                    x = x_time
                    y1 = y_temp
                    y2 = axis_y_wind
                    ax = plt.axes()
                    ax.set_facecolor("#282828")
                    plt.figure(facecolor='#282828')
                    ax = plt.axes()
                    ax.set_facecolor("#282828")
  
                    plt.plot(x, y1, label="Temperatuur", color="Orange" )
                    plt.plot(x, y2, label="Wind-snelheid", color="deepskyblue")
                    plt.legend(loc="upper right")
                    plt.xlabel("Tijd", color="Black")
                    plt.ylabel("Wind-snelheid & temperatuur", color="Black")
                    plt.savefig('./defaulttemp_char.png')

                    
                    
                    embed = disnake.Embed(title="Temperatuur en windsnelheid", description="Info geleverd door OpenWeatherAPI. Default versie!", color=0x4793FF)
                    file = disnake.File("./defaulttemp_char.png", filename="image2.png")
                    embed.set_image(url="attachment://image2.png")
                    embed.set_footer(text="By </Kelvin>. Versie: " + str(version_nummer),icon_url="https://kelvindereus.nl/CustomCPULOGO.png")        
                    await inter.response.send_message(file=file, embed=embed)     
                    os.remove("./defaulttemp_char.png")


                    


async def send_help_embed(inter):
    embed = disnake.Embed(title="WeerBot help menu! (Standaard versie.)", description="Voor de community, door de community!", color=0x4793FF)
    embed.add_field(name="/weer_help", value="Dit laat dit bericht zien.", inline=False)   
    embed.add_field(name="/weer_set_standaard_stad", value="Stel hiermee je standaard stad in voor het command !weer.", inline=False)   
    embed.add_field(name="/weer", value="Dit laat je vooraf ingestelde weer zien.", inline=False)   
    embed.add_field(name="/weer_nu", value="Dit laat het weer in de opgegeven stad zien.", inline=False)            
    embed.add_field(name="/weer_morgen", value="Dit laat het weer voor morgen in de opgegeven stad zien.", inline=False)            
    embed.add_field(name="/weer_voorspelling", value="Dit laat een grafiek zien met de weersvoorspelling!", inline=False)   

    embed.set_footer(text="By </Kelvin>. Versie: " + str(version_nummer),icon_url="https://kelvindereus.nl/CustomCPULOGO.png")
    await inter.response.send_message(embed=embed)
