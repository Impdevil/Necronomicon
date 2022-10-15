import app.GetData
import app.RetrieveDayData
import datetime as dt


daysforecast = GetData.GetForecast()
print(RetrieveDayData.WillItRain(RetrieveDayData.GetDayWeatherFromData(daysforecast)))



