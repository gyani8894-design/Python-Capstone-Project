import os
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 🎯 URLs categorized by movie genres
MOVIE_GENRES = {
    "action": "https://www.rottentomatoes.com/browse/movies_at_home/genres:action",
    "comedy": "https://www.rottentomatoes.com/browse/movies_at_home/genres:comedy",
    "drama": "https://www.rottentomatoes.com/browse/movies_at_home/genres:drama",
    "horror": "https://www.rottentomatoes.com/browse/movies_at_home/genres:horror",
    "romance": "https://www.rottentomatoes.com/browse/movies_at_home/genres:romance",
    "sci-fi": "https://www.rottentomatoes.com/browse/movies_at_home/genres:sci_fi",
    "documentary": "https://www.rottentomatoes.com/browse/movies_at_home/genres:documentary",
    "animation": "https://www.rottentomatoes.com/browse/movies_at_home/genres:animation"
}

def collect_movies(genre: str, limit: int = 5):
    """
    Extracts movie titles from Rotten Tomatoes based on the given genre.
    Stores them in a CSV file.
    """

    # validate genre
    if genre not in MOVIE_GENRES:
        print(f"⚠️ Genre '{genre}' is not supported. Try one of: {', '.join(MOVIE_GENRES.keys())}")
        return
    
    # initialize chrome driver in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        url = MOVIE_GENRES[genre]
        print(f"\n🔗 Opening page for {genre.title()} movies...\n")
        driver.get(url)

        # random wait to simulate natural browsing
        time.sleep(random.uniform(4, 7))

        # locate all movie cards
        cards = driver.find_elements(By.CSS_SELECTOR, "a.js-tile-link")[:limit]
        scraped_list = []

        for idx, card in enumerate(cards, start=1):
            try:
                title = card.find_element(By.CSS_SELECTOR, "span.p--small").text.strip()
            except Exception:
                title = "Unknown Title"
            
            print(f"{idx}) 🎬 {title}")
            scraped_list.append({"Movie Title": title, "Category": genre.title()})

        # Save to CSV
        if scraped_list:
            df = pd.DataFrame(scraped_list)
            save_to_csv(df)

    except Exception as err:
        print(f"🚨 Unexpected error: {err}")
    finally:
        driver.quit()


def save_to_csv(dataframe: pd.DataFrame, filename: str = "movies_dataset.csv"):
    """
    Appends the scraped movie data into a CSV file.
    Creates the file if it doesn't already exist.
    """
    try:
        file_path = os.path.join(os.getcwd(), filename)
        dataframe.to_csv(file_path, mode="a", header=not os.path.exists(file_path), index=False)
        print(f"\n✅ Data saved successfully to '{filename}'")
    except PermissionError:
        print("❌ ERROR: Unable to write to file. Please close it if it's already open.")
    except Exception as e:
        print(f"⚠️ Could not save file: {e}")


if __name__ == "__main__":
    # Example usage
    collect_movies("comedy", limit=7)
    collect_movies("drama", limit=5)