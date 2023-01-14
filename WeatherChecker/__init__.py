import logging
import datetime as dt
import asyncio
import discord_webhook
import os
import WeatherChecker.GetData
import WeatherChecker.RetrieveDayData


daysforecast = GetData.GetForecast()
print(RetrieveDayData.WillItRain(RetrieveDayData.GetDayWeatherFromData(daysforecast)))
SENTFORTODAY = False


#this as a loop needs to act once every day at 22:00 everyday, send the notifcation
#to discord through a webhook.

async def periodic_check():
    while True:
        await wait_till_ten()
        await asyncio.sleep(60*15)

async def wait_till_ten():
    global SENTFORTODAY
    now = dt.datetime.now()
    if now.hour == 22 and SENTFORTODAY == False:
        print("sending discord notifcation")
        send_discord_notifcation()
        logging.info('sent weather next day.')
        SENTFORTODAY = True
    elif now.hour != 22:
        print("to early " + str(now.hour)+":"+str(now.minute)+":"+str(now.second))
        SENTFORTODAY = False


def send_discord_notifcation():
    DISCORD_TOKEN = os.getenv("discord_token_nightGaunt")
    allowed_mentions = {'parse': ["everyone"],}
    if RetrieveDayData.WillItRain(RetrieveDayData.GetDayWeatherFromData(GetData.GetForecast())):
        hook = discord_webhook.DiscordWebhook(url=DISCORD_TOKEN, rate_limit_retry=True,allowed_mentions=allowed_mentions, content="@everyone tomorrow it is raining, so dont put on a washing")
    else:
        hook = discord_webhook.DiscordWebhook(DISCORD_TOKEN,rate_limit_retry=True,allowed_mentions=allowed_mentions,content="@everyone put a washing on now as tomorrow will be a nice enough day to dry washing.")
    respo = hook.execute()
    print(respo)

if __name__ == "main":
    wait_till_ten();