#!/usr/bin/env python
import time
import os
import signal
import logging
import datetime as dt
import argparse

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d  %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger.setLevel(logging.DEBUG)

# globals
exit_flag = False


# def signal_handler(sig_num, frame):
#     """
#     This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
#     Basically it just sets a global flag, and main() will exit it's loop if the signal is trapped.
#     :param sig_num: The integer signal number that was trapped from the OS.
#     :param frame: Not used
#     :return None
#     """
#     logger.info('Received ' + signal.Signals(sig_num).name)
#     global exit_flag
#     exit_flag = True


def watch_directory():
    while True:
        try:
            logger.info('Inside Watch Loop')
            time.sleep(1)
        except KeyboardInterrupt:
            # logger.error('Hey DONT INTERRUPT ME!!')
            break


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('e', '--ext', type=str, default='.txt',
                        help='Text file extension to watch')
    parser.add_argument('-i', '--interval', type=float,
                        default=1.0, help='Number of seconds between polling')
    parser.add_argument('path', help='Directory path to watch')
    parser.add_argument('magic', help='String to watch for')
    return parser


def main():
    app_start_time = dt.datetime.now()

    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '   Running {}\n'
        '   Started on {}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, app_start_time.isoformat())
    )

    # # Hook these two signals from the OS ..
    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)
    # # Now my signal_handler will get called if OS sends either of these to my process.

    parser = create_parser()
    ns = parser.parse_args()

    watch_directory()

    uptime = dt.datetime.now() - app_start_time
    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '   Stopped {}\n'
        '   Uptime was {}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, str(uptime))

    )
    logging.shutdown()

    # EX. if ns.loglevel == info:
    # logger.setLevel(logging.INFO)


if __name__ == '__main__':
    main()
