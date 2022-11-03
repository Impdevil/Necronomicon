import GetData
import RetrieveDayData
import datetime as dt
import asyncio
import discord_webhook
import os


daysforecast = GetData.GetForecast()
print(RetrieveDayData.WillItRain(RetrieveDayData.GetDayWeatherFromData(daysforecast)))

DISCORD_TOKEN = os.getenv("discord_webhook")
#this as a loop needs to act once every day at 22:00 everyday, send the notifcation
#to discord through a webhook.

async def wait_till_ten():
    await asyncio.sleep (15)#*60)
    now = dt.datetime.now()
    if now.hour == 22:
        print("sending discord notifcation")
        send_discord_notifcation()
    else:
        print("to early " + now.hour+":"+now.minute)


def send_discord_notifcation(): 
    if RetrieveDayData.WillItRain(RetrieveDayData.GetDayWeatherFromData(GetData.GetForecast())):
        #fuck this part specifically /\
        hook = discord_webhook.DiscordWebhook(DISCORD_TOKEN, rate_limit_retry=True, content="@all tomorrow it is raining, so dont put on a washing")
    else: hook = discord_webhook.DiscordWebhook(DISCORD_TOKEN,rate_limit_retry=True,content="@all put a washing on now as tomorrow will be a nice enough day to dry washing.")
    respo = hook.execute()
    print(respo)

if __name__ == "main":
    wait_till_ten();