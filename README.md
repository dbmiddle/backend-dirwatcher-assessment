DIRWATCHER!

This is a long running program that monitors a directory 
for text files and magic words provided through the command line.
As the program is long running, it will continue to run despite
despite exceptions (which will be logged with timestamps) until 
it is sent a terminaltion signal.

To run the program type the following in your command line:

'python dirwatcher.py --ext .txt --interval (float number 
for sleep intervals) (directory to watch) (magic text)'