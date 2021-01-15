from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import lxml 
import time
import csv


#path to chromedriver // chromedriver is for emulate the browser
PATH = "/chromedriver"
#put the path in a variable
driver = webdriver.Chrome(PATH)

#for the driver to get the url of the site we want to scrape :
link = driver.get("https://old.reddit.com/r/bapcsalescanada/")
#print(driver.title)


#Function next_page with a stop parameter. The stop parameter will be a number.
def next_page(stop):
	i=0
	#empty array for the data
	data = []
	#while loop : while i is inferior to the paramater stop, the loop goes on
	while i < stop:
		#we prepare the webdriverwait, where the driver will wait for the page to load. If the page takes too long,
		#then the browser closes.
		element = WebDriverWait(driver, 15).until(
			#we locate the element we're trying to get. Here, we want the "a" where it has a "rel" attribute with the value "next"
			EC.presence_of_element_located((By.XPATH, '//a[contains(@rel, "next")]'))
		)
		#the number of seconds the loop will wait before continue
		time.sleep(2)
		#click on the element
		element.click()
		#iteration
		i = i + 1
		#loop to prepare the data to scrape and send them to a csv file
		for i in range (1, stop) :
			result = requests.get('https://old.reddit.com/r/bapcsalescanada/')
			src = result.content
			soup = BeautifulSoup(src, 'lxml')
			links = soup.find_all('div', class_ = "score unvoted")
			
			data.append(links)

			with open ('data.csv','w') as file:
				writer=csv.writer(file)
				for row in data:
					writer.writerow(row)

		#quit if the page takes too long to load
	driver.quit()

#Call the function. 
next_page(3)



