import csv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

URL = "https://www.bbcgoodfood.com/recipes/collection/easy-dinner-recipes"
user_search = input("What do you want to look for? ")
max_recipes = 30

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get(URL)
driver.implicitly_wait(10)
frame_id = "sp_message_iframe_1109708"
driver.switch_to.frame(frame_id)

try:
    accept_cookies = driver.find_element(By.XPATH, '//button[@title="Essential Cookies Only"]')
    accept_cookies.click()
except NoSuchElementException:
    print("Accept All button not found.")

try:
    search_field = driver.find_element(By.ID, value='branded-section-search-input')
    search_field.send_keys(user_search)
    search_field.send_keys(Keys.ENTER)
    # Find all article elements
    articles = driver.find_elements(By.CSS_SELECTOR, 'article.card')
    articles_list = articles[:max_recipes]

    # Create a CSV file and write header
    with open('recipes.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link', 'Cooking Time'])

    # Iterate over each article to extract information and save to CSV
    for article in articles_list:
        title = article.find_element(By.CSS_SELECTOR, 'h2').text
        link = article.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        cooking_time = article.find_element(By.XPATH, '//*[@id="__next"]/div[4]/main/div[2]/div/div[5]/div/div[1]/div[1]/div[1]/div[2]/article/div[3]/ul/li[1]/span').text
        # Append data to CSV file
        with open('recipes.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([title, link, cooking_time])

    print("Data extracted and saved to recipes.csv")

except NoSuchElementException:
    print("Error: Element not found or search failed.")

# Close the browser
driver.quit()
