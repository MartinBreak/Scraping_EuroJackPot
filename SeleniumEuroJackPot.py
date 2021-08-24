from selenium import webdriver
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
driver.get('https://www.lotto.pl/eurojackpot/wyniki-i-wygrane')
print("Strona została uruchomiona.")

driver.implicitly_wait(10)
skip1 = driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[4]/div/div/div[3]/div[2]/div[3]/button')
skip1.click()
skip2 = driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[4]/div/div/div[1]/div/div/div/div/button/i')
skip2.click()
print("Okienka zostały wyłączone.")

# driver.implicitly_wait(30)
# accept3 = driver.find_element_by_xpath('//*[@id="onesignal-slidedown-cancel-button"]')
# accept3.click()

for scroll_site in range(20):
    time.sleep(2)
    scroll_site = driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[4]/div/div/div[2]/div[3]/div/button/span')
    scroll_site.click()
print("strona została przewinięta.")

numerylos = []
for i in driver.find_elements_by_class_name('result-item__number')[:420]:
    numerylos.append(i.text)
    numerylos[:] = [x for x in numerylos if x]  # usuwa puste elementy z listy

numerywin = []
for i in driver.find_elements_by_class_name('result-item__balls-box')[:200]:
    numerywin.append(i.text.split('\n'))

data = []
for i in driver.find_elements_by_class_name('sg__desc-title')[:200]:
    data.append(i.text.strip(', godz. 20:00').strip('Pt., '))

#zamiana list na numpy array
numerylos = np.array(numerylos)
numerylos.flatten()
numerylos = np.reshape(numerylos, (len(numerylos), 1))
numerywin =np.array(numerywin)
numerywin.flatten()
data = np.array(data)
data.flatten()
data = np.reshape(data, (len(data), 1))

dict_los_win = np.hstack((numerylos, numerywin, data))

unique, counts = np.unique(numerywin, return_counts=True)
dict_win = dict(zip(unique, counts))

dict_win = dict(sorted(dict_win.items(), key=lambda item: item[1]))


keys = dict_win.keys()
values = dict_win.values()

pd.DataFrame(dict_los_win).to_csv("win_numbers.csv", header=["Nr", "Numer losowania", "Wylosowane 7 liczb","Data losowania","","","","",""])
print("Liczby zostały zapisane w pliku win_numbers.csv")

plt.figure(figsize=(20, 10))
plt.xticks(fontsize = 10)
plt.yticks(fontsize = 20)
plt.title("Wykres ile razy wypadła dana liczba")
plt.xlabel("Wylosowana liczba")
plt.ylabel("Ile razy wypadła liczba")
plt.bar(keys, values, edgecolor='black')
for i, v in enumerate(values):
    plt.text(i, v+0.5, str(v), fontweight='bold')
plt.savefig('chart.png')
print("Wykres został utworzony.")
