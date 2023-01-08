import Ghroth.app
import c2
import WeatherChecker
import asyncio
import logging
import os


loggingmode = os.getenv("LOGGING_MODE")
def __main__():

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        print("Error No Loop, Starting Loop.")
        loop = asyncio.get_event_loop()

    logging.info("starting loop")
    print("starting loop")
    loop.create_task(Ghroth.app.start_bot())
    loop.create_task(c2.Start_bot())
    loop.create_task(WeatherChecker.periodic_check())

    loop.run_forever()


def run_Ghorth():
    Ghroth.app.start_bot()



logging.basicConfig(filename="necronomicon.log", filemode=loggingmode, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S')
__main__()


