import Ghroth.app
import c2
import asyncio



def __main__():

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        print("Error No Loop, Starting Loop.")
        loop = asyncio.get_event_loop()

    #if loop and loop.is_running():
    #    print("reached?")
    #    loop = asyncio.new_event_loop()

    loop.create_task(Ghroth.app.start_bot())
    loop.create_task(c2.LoadConfig())

    loop.run_forever()


def run_Ghorth():
    Ghroth.app.start_bot()

__main__()


