import threading
import time
from threading import Thread

import cli_ui


def long_computation():
    # Simulates a long computation
    time.sleep(0.6)


def count_down(lock, start):
    x = start
    while x >= 0:
        with lock:
            # Note: the sleeps are here so that we are more likely to
            # see mangled output
            #
            # In reality, if you only call `ui.info()` once you don't
            # need locks at all thanks to the GIL
            cli_ui.info("down", end=" ")
            time.sleep(0.2)
            cli_ui.info(x)
            time.sleep(0.2)
        long_computation()
        x -= 1


def count_up(lock, stop):
    x = 0
    while x <= stop:
        with lock:
            cli_ui.info("up", end=" ")
            time.sleep(0.2)
            cli_ui.info(x)
            time.sleep(0.2)
        long_computation()
        x += 1


def main():
    lock = threading.Lock()
    t1 = Thread(target=count_down, args=(lock, 4))
    t2 = Thread(target=count_up, args=(lock, 4))

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
