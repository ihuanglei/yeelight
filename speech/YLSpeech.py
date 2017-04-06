import speech_recognition as sr
import sys
import socket

reload(sys)
sys.setdefaultencoding('utf8')


class YLSpeech:
    pass


if __name__ == '__main__':
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(
            index, name.encode('utf8')))
