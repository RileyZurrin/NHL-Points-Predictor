from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from clean_data import clean
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.quanthockey.com/nhl/seasons/nhl-players-stats.html"

# Function to click on a specific page number
def click_page_number(page_number, driver):
    
    # Scroll to page number links so that they're not obstructed
    pagination_element = driver.find_element(By.CLASS_NAME, "pagination")
    driver.execute_script("arguments[0].scrollIntoView();", pagination_element)
    
    try:
        
        # Find the element by link text (the page number)
        page_link = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.LINK_TEXT, str(page_number)))
        )
        page_link.click()
        
        # Wait for the new content to load (if needed)
        WebDriverWait(driver, 1).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'loading-spinner'))
        )

        print("page " + str(page_number))
        
        return True
    except Exception as e:
        print("All Pages Extracted")
        return False
    
# Function that grabs data off given page number
def extract_page(html):
    soup = BeautifulSoup(html, "html.parser")
    stats = []

    rows = soup.find_all('tr')[2:]  # Skip the first two rows
    for row in rows:
        columns = row.find_all(['th', 'td'])

        rank = columns[0].text
        player_name = columns[2].text

        values = [column.text for column in columns[3:]]  # Skip the first three columns
        values.insert(0, player_name)
        values.insert(0, rank)

        stats.append(values)

    return stats


def extract(url):
    # Extraction
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    homepage = driver.get(url)

    # Initial extraction for the first set of rows
    html = driver.page_source

    # Extract column header
    soup = BeautifulSoup(html, "html.parser")
    row = soup.find('tr', {'role': 'row', 'class': 'orange'})
    header = [th.get_text(strip=True) for th in row.find_all('th', {'role': 'columnheader'}) if th.get_text(strip=True)]

    # Get Data
    stats_total = extract_page(html)

    print("page 1")
    page_number = 2


    # Loop to load and extract additional rows
    while click_page_number(page_number, driver):
        page_number += 1
        html = driver.page_source
        stats_total += extract_page(html)
        
    driver.quit()

    return stats_total, header


# extract data
stats, header = extract(url)
df = pd.DataFrame(stats, columns=header)
df = clean(df)

# Write DataFrame to CSV file
df.to_csv('data.csv', index=False)
