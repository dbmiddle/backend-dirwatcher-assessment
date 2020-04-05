#!/usr/bin/env python

__author__ = 'dbmiddle'

import time
import os
import signal
import logging
import datetime as dt
import argparse

# globals
exit_flag = False
track_files = {}
file_logger = []

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d  %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger.setLevel(logging.DEBUG)

current_dir = os.getcwd()


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically it just sets a global flag, and main() will exit it's loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    logger.info('Received ' + signal.Signals(sig_num).name)
    global exit_flag
    exit_flag = True


def watch_directory(args):
    logger.info('Watching directory: {}, File Extension: {}, Polling Interval: {}, Magic Text: {}'
                .format(args.path, args.ext, args.interval, args.magic
                        ))
    # Keys are the actual filename and the values are where to begin searching
    # Look at directory and get a list of files from it;
    # Add those to dictionary if not already present and log it as a new file;
    # Look through 'track_files' dict and compare that to a list of files
    #   that is in the dictionary
    # If file is not in your list anymore you have to log the
    #   file and remove it from your dictionary
    # Iterate through dictionary, open each file at the last line that you read
    #   from
    # Start reading from that point looking for any 'magic' text
    # Update the last position that you read from in the dictionary

    while not exit_flag:
        try:
            # logger.info('Inside Watch Loop')
            find_magic(args)
            # detect_removed_files(args)
            time.sleep(args.interval)
        except RuntimeError:
            pass
        except KeyboardInterrupt:
            break


def find_magic(args):
    try:
        watched_dir_path = os.path.join(current_dir, args.path)
        file_list = os.listdir(watched_dir_path)
        full_file_path_list = [os.path.join(current_dir, args.path, f)
                               for f in file_list if f.endswith('.txt')]
    except FileNotFoundError:
        logger.exception('*** Directory {} not found ***'.format(args.path))
    else:
        for target_file in full_file_path_list:
            if target_file not in file_logger:
                logger.info('*** New file {} added to track_files dictionary ***'
                            .format(target_file
                                    ))
                file_logger.append(target_file)
            full_file_path = os.path.join(watched_dir_path, target_file)
            if search_file(args, full_file_path):
                break
        detect_removed_files(args)


def search_file(args, full_file_path):
    with open(full_file_path, 'r') as f:
        lines = f.readlines()
        for line_number, line in enumerate(lines):
            detect_added_files(args, line_number)
            if args.magic in line:
                if line_number >= track_files[full_file_path] and full_file_path in track_files.keys():
                    logger.info('*** Magic text {} found in {} on Line {} ***'
                                .format(args.magic, full_file_path, line_number + 1
                                        ))
                    track_files[full_file_path] += 1


def detect_added_files(args, line_number):
    watched_dir_path = os.path.join(current_dir, args.path)
    file_list = os.listdir(watched_dir_path)
    full_file_path_list = [os.path.join(current_dir, args.path, f)
                           for f in file_list if f.endswith('.txt')]
    for target_file in full_file_path_list:
        if target_file not in track_files.keys():
            track_files[target_file] = line_number


def detect_removed_files(args):
    watched_dir_path = os.path.join(current_dir, args.path)
    file_list = os.listdir(watched_dir_path)
    full_file_path_list = [os.path.join(current_dir, args.path, f)
                           for f in file_list if f.endswith('.txt')]
    for target_file in file_logger:
        if target_file not in full_file_path_list:
            del track_files[target_file]
            logger.info('*** File {} deleted from track_files dictionary ***'
                        .format(target_file
                                ))
            file_logger.remove(target_file)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--ext', type=str, default='.txt',
                        help='Text file extension to watch')
    parser.add_argument('-i', '--interval', type=float,
                        default=1.0, help='Number of seconds between polling')
    parser.add_argument('path', help='Directory path to watch')
    parser.add_argument('magic', help='String to watch for')
    return parser


def main():
    # Hook these two signals from the OS ..
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

    app_start_time = dt.datetime.now()

    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '   Running {}\n'
        '   Started on {}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, app_start_time.isoformat())
    )

    parser = create_parser()
    args = parser.parse_args()

    watch_directory(args)
    # find_magic(args)
    # detect_added_files(args)
    # detect_removed_files(args)

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
