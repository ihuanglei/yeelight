import os
from pocketsphinx import LiveSpeech


class YLSpeech:
    pass


if __name__ == '__main__':

    for phrase in LiveSpeech():
        print(phrase)
