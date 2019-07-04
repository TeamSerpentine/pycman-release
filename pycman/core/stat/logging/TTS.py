import logging
import sys


def configure_logging():
    h = TTSHandler()
    root = logging.getLogger()
    root.addHandler(h)
    # the default formatter just returns the message
    root.setLevel(logging.DEBUG)


def main():
    logging.info('info Hello')
    logging.debug('debug, goodbye')


if __name__ == '__main__':
    configure_logging()
    sys.exit(main())
