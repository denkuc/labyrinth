import sys


class Logger:
    @staticmethod
    def log(something):
        print(str(something), file=sys.stderr, flush=True)
