import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import warnings
import time

warnings.filterwarnings('ignore')

genres = ['Comedy']

options = Options()
options.add_argument("--log-level=3")
options.add_argument("--disable-logging")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('useAutomationExtension', False)

def scrape_genre(driver, genre):
    url = f"https://www.imdb.com/search/title/?genres={genre}&sort=user_rating,desc&title_type=feature"
    driver.get(url)
    time.sleep(3)

    try:
        movie_list = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul'))
        )

        movies_data = movie_list.find_elements(By.TAG_NAME, "li")
        
        data = []
        for movie in movies_data[:50]:
            try:
                # Extract movie title
                title = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text
                if '. ' in title:
                    title = title.split('. ')[1]
                
                # Extract year (updated selector)
                year_element = movie.find_element(By.CSS_SELECTOR, "span.dli-title-metadata-item:nth-child(1)")
                year = year_element.text

                # Extract duration (updated selector)
                duration_element = movie.find_element(By.CSS_SELECTOR, "span.dli-title-metadata-item:nth-child(2)")
                duration = duration_element.text
                
                data.append({
                    'Movie': title,
                    'Year': year,
                    'Duration': duration
                })

            except Exception as e:
                print(f"Error processing movie: {e}")
                continue

        return data

    except Exception as e:
        print(f"Error finding movie list: {e}")
        return []

try:
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    all_data = []
    for genre in genres:
        print(f"\nScraping {genre} movies...")
        genre_data = scrape_genre(driver, genre)
        if genre_data:
            all_data.extend(genre_data)

    if all_data:
        df = pd.DataFrame(all_data)

        # Save to CSV
        csv_path = os.path.join(os.getcwd(), 'movie_data_by_genre.csv')
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"\nData successfully saved to: {csv_path}")
        
        print("\nFirst few rows of the scraped data:")
        print(df.head())
    else:
        print("No data was collected.")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()