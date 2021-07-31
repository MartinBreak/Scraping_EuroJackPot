from selenium import webdriver
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
#test czy działa push

driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
driver.get('https://www.lotto.pl/eurojackpot/wyniki-i-wygrane')

driver.implicitly_wait(10)
skip1 = driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[4]/div/div/div[3]/div[2]/div[3]/button')
skip1.click()
skip2 = driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[4]/div/div/div[1]/div/div/div/div/button/i')
skip2.click()

# driver.implicitly_wait(30)
# accept3 = driver.find_element_by_xpath('//*[@id="onesignal-slidedown-cancel-button"]')
# accept3.click()

# for more_sites in range(3):
#     time.sleep(2)
#     more_sites = driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[4]/div/div/div[2]/div[3]/div/button/span')
#     more_sites.click()

numerylos = []
for i in driver.find_elements_by_class_name('result-item__number')[:10]:
    numerylos.append(i.text)
    numerylos[:] = [x for x in numerylos if x]  # usuwa puste elementy z listy

numerywin = []
for i in driver.find_elements_by_class_name('result-item__balls-box')[:5]:
    numerywin.append(i.text.split('\n'))

data = []
for i in driver.find_elements_by_class_name('sg__desc-title')[:5]:
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

#pd.DataFrame(dict_los_win).to_csv("file.csv")

plt.figure(figsize=(20, 10))
plt.xticks(fontsize = 10)
plt.yticks(fontsize = 20)
#plt.xticks(keys)
plt.bar(keys, values, edgecolor='black')
for i, v in enumerate(values):
    plt.text(i, v+0.5, str(v), fontweight='bold')
plt.savefig('chart.png')
