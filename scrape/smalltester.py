import time
import os
import wget
from pyrsistent import b
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
os.system("pkill -f -9 chromium")
options = Options()
options.headless = True
service = Service(
    executable_path=r'C:/4coding/chromedriver_win32/chromedriver.exe')
driver = webdriver.Chrome(options=options, service=service)

download_dest = f'F:/media/asmr/jok/1.mp3'
link = 'https://www.bzjar.com/11166.html'
driver.get(link)
time.sleep(0.1)
audio = driver.find_element(by="tag name", value="audio")
source = audio.find_element(by="tag name", value="source")
src = source.get_attribute('src')

# download for each src
content = requests.get(src).content
download_files = []
# for x in range(25):
#     temp = download_dest + str(x) + ".mp3"
# print(download_files)
# for y in download_files:
with open(download_dest, "w") as f:
    f.write(content)
print(src)
