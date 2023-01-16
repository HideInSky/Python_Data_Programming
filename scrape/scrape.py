
import time
import os
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

url = 'https://www.bzjar.com/tag/%e5%be%a1%e5%a7%90jok'
base_url = 'https://www.bzjar.com/'
download_dest = f'F:/media/asmr/jok/'
# driver.get(url)
# time.sleep(20)
# post_infos = driver.find_elements(by="class name", value="post-info")
# time.sleep(20)
# links = []
# for post_info in post_infos:
#     time.sleep(2)
#     tag_a = driver.find_element(by="tag name", value="a")
#     link = tag_a.get_attribute('href')
#     links.append(link)
    
driver.get(url)
time.sleep(2)
lists = driver.find_elements(by="tag name", value="li")
ids = []
links = []
srcs = []
for list in lists:
    id = list.get_attribute('id')
    ids.append(id)
for id in ids:
    if len(id)>0 and id[0]=='i':
        temp = base_url + id[5:] + ".html"
        links.append(temp)
for link in links:
    driver.get(link)
    audio = driver.find_element(by="tag name", value="audio")
    source = audio.find_element(by="tag name", value="source")
    src = source.get_attribute('src')
    srcs.append(src)
driver.quit()

print(links)
print(src)
with open(download_dest+"from.txt", "w")
print(len(src))
