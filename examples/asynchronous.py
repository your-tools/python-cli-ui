import asyncio

import cli_ui


async def long_computation():
    # Simulates a long computation
    await asyncio.sleep(0.6)


async def count_down(lock, start):
    x = start
    while x >= 0:
        async with lock:
            # Note: the sleeps are here so that we are more likely to
            # see mangled output
            #
            # In reality, if you only call `ui.info()` once you don't
            # need locks at all thanks to the GIL
            cli_ui.info("down", end=" ")
            await asyncio.sleep(0.2)
            cli_ui.info(x)
            await asyncio.sleep(0.2)
        await long_computation()
        x -= 1


async def count_up(lock, stop):
    x = 0
    while x <= stop:
        async with lock:
            cli_ui.info("up", end=" ")
            await asyncio.sleep(0.2)
            cli_ui.info(x)
            await asyncio.sleep(0.2)
        await long_computation()
        x += 1


async def main():
    lock = asyncio.Lock()
    await asyncio.gather(count_down(lock, 4), count_up(lock, 4))


if __name__ == "__main__":
    asyncio.run(main())
