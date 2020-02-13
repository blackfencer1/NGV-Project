#블랙아이스 발견 시 경고 음성메세지주는 코드#

from django.templatetags.i18n import language
from gtts import gTTS
import os

text = "Danger! It's black ice!"
language = 'en'
speech = gTTS(text = text, lang = language, slow = False)
speech.save("text.mp3")
os.system("start text.mp3")