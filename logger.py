import datetime
import os
from datetime import datetime


class TLogger:
    FileName = "application.log"
    FullPath = os.getcwd()
    LogLevel = ['Error', 'Info']

    def __init__(self, fname=None, fpath=None, loglevel=None):
        if fname != None: TLogger.FileName = fname
        if fpath != None: TLogger.FullPath = fpath
        if loglevel != None: TLogger.LogLevel = loglevel

    @staticmethod
    def WriteLog(msg_type, msg):
        if msg_type == "Info" or msg_type == "Error":
            print('{}'.format(datetime.now()) + ' ' + msg_type + ': ' + '{}'.format(msg))
        if msg_type in TLogger.LogLevel:
            f = open(os.path.join(TLogger.FullPath, TLogger.FileName), "a", encoding="utf8")
            str = '{}'.format(datetime.now()) + ' ' + msg_type + ': ' + '{}'.format(msg) + '\n'
            f.write(str)
            f.close()


if __name__ == '__main__':
    logger = TLogger(fname='test.log', loglevel=["Warning"]);
    print(TLogger.FullPath)
    i = 0
    while i < 10:
        logger.WriteLog('Warning', "Hello {}".format(i))
        i += 1
