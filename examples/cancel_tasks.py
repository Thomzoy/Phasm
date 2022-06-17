import asyncio


# This is just a tutorial script to cancel scripts.
# Program workers emulates our main and interupter emulates the callback behavior.
# The worker should be creating new tasks all the time with a given name and
# the interupter can stop them using this name

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
    for i in range(50):
        new_task = asyncio.create_task(dodo(idx=i, sleep=sleep),
                                       name="program")
        try:
            await new_task
        except asyncio.CancelledError:
            print('Stopped sleeping, ready for a new nap')


async def program_interrupter():
    """
    Simulates the callback interactions
    """
    while True:
        await asyncio.sleep(1)
        print('now its time to kill')
        all_tasks = asyncio.all_tasks()
        tasks_to_cancel = [task for task in all_tasks if task.get_name() == 'program']
        print(tasks_to_cancel)
        for task in tasks_to_cancel:
            task.cancel()


async def main():
    """
    Simulates the external loop that launches device communication and main
    """
    task1 = asyncio.create_task(program_worker(), name='program_loop')
    task2 = asyncio.create_task(program_interrupter(), name='message_loop')
    await task1
    await task2


if __name__ == "__main__":
    pass

    # loop = asyncio.get_event_loop()
    # cors = asyncio.wait([long(), short()])
    # loop.run_until_complete(cors)

    asyncio.run(main())
