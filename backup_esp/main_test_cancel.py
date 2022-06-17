import uasyncio as asyncio


# This is just a tutorial script to cancel scripts.
# Program workers emulates our main and interupter emulates the callback behavior.
# The worker should be creating new tasks all the time with a given name and
# the interupter can stop them using this name

CURRENT_TASK = None

async def dodo(idx, sleep):
    """
    Dummy program
    """
    print('Starting a new sleeping program')
    await asyncio.sleep(sleep)
    print(f'slept a bit{idx}')


async def program_worker(sleep=10):
    """
    Simulates the main loop, we execute new dummy program called dodo for 50 secs
    """
    global CURRENT_TASK

    for i in range(50):
        CURRENT_TASK = asyncio.create_task(dodo(idx=i, sleep=sleep))
        try:
            await CURRENT_TASK
        except asyncio.CancelledError:
            print('Stopped sleeping, ready for a new nap')


async def program_interrupter():
    """
    Simulates the callback interactions
    """
    global CURRENT_TASK
    while True:
        await asyncio.sleep(1)
        print('now its time to kill')
        CURRENT_TASK.cancel()


async def main():
    """
    Simulates the external loop that launches device communication and main
    """
    task1 = asyncio.create_task(program_worker())
    task2 = asyncio.create_task(program_interrupter())
    await task1
    await task2


if __name__ == "__main__":
    pass

    # loop = asyncio.get_event_loop()
    # cors = asyncio.wait([long(), short()])
    # loop.run_until_complete(cors)

    asyncio.run(main())