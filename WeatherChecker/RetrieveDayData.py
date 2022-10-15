


def GetDayWeatherFromData(Data):
    days = list()

    #print(days)
    #print(len(Data))
    #print(Data)
    print()
    i=0
    for i in range(0,len(Data)):
        #print (i)
        days.append({"date"  : Data[i]["date"]})
        days[i]["day"] = Data[i]["day"]
        #print( Data[i]["date"])

    #print(days)
    return days


def WillItRain(DayInfo):
    print(DayInfo)
    return DayInfo[1]["day"].get("daily_will_it_rain")
