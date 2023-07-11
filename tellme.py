import re
import unicodedata
import pyautogui
import speech_recognition as sr
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Inicializa o objeto Recognizer
r = sr.Recognizer()

# Retira acentuação e caracteres especiais ao capturar a fala
def remove_accent(text):
    # Remove os acentos do texto
    nfkd = unicodedata.normalize('NFKD', text)
    without_accent = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    # Substitui os caracteres especiais por um espaço em branco
    without_special_chars = re.sub('[^a-zA-Z0-9 \\\]', '', without_accent)
    return without_special_chars.lower()

while True:
    # Captura o áudio e converte em texto
    with sr.Microphone() as source:
        print("Diga alguma coisa!")
        audio = r.listen(source, timeout=5)

    try:
        text = r.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {text}")
        #sleep(3)
        text = remove_accent(text) # Remove acentuação e caracteres especiais
        print(f"Texto tratado: {text}")
        #sleep(3)

        # Verifica se o texto não está vazio
        if text.strip() != "":
            # Automatiza o processo de copiar o texto e colá-lo na caixa de texto da página atual
            pyautogui.moveTo(2500, 811, duration=1)
            pyautogui.click()
            pyautogui.typewrite(text)
            pyautogui.press('enter')
            pyautogui.hotkey('ctrl', 'c')
            pyautogui.moveRel(0, -200, duration=1)  # move o mouse 200 pixels para cima
            
            for i in range(10):  # loop para rolar a página por 10 segundos
                pyautogui.scroll(-100)  # rola a página para baixo
                time.sleep(1)  # espera 1 segundo antes de rolar novamente
            
            pyautogui.moveRel(0, 200, duration=1)  # move o mouse de volta
        else:
            print("O texto está vazio, nada será colado!")
    except sr.UnknownValueError:
        print("Não entendi o que você disse!")
    except sr.RequestError as e:
        print("Não foi possível conectar ao serviço de reconhecimento de fala; {0}".format(e))