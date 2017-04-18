import speech_recognition as sr
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class YLSpeecher:
    pass


if __name__ == '__main__':

    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Sphinx
    try:
        print('Sphinx thinks you said ' + r.recognize_sphinx(audio, 'zh-CN'))
    except sr.UnknownValueError:
        print('Sphinx could not understand audio')
    except sr.RequestError as e:
        print('Sphinx error; {0}'.format(e))
