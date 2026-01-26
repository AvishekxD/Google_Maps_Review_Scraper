import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_lakshya_library_reviews(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en")
    # Using a mobile user-agent because your HTML snippet is from the mobile view
    options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 40) #increase the time for more scrolling and scraping

        
        print("Checking for 'Google Maps is better on the app' popup...")
        try:
            # This targets the "Go back to web" button specifically
            back_to_web_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Go back to web')]")))
            back_to_web_btn.click()
            print("Successfully clicked 'Go back to web'.")
            time.sleep(2)
        except Exception:
            print("Popup didn't appear or already dismissed.")
        

        # 1. Wait for the review items to appear
        print("Waiting for reviews to load...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'hjmQqc')))

        # 2. Scrolling logic for the mobile review pane
        print("Starting scroll...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(10):  # Scans more reviews
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            print(f"Scroll {i+1} complete...")

        # 3. Extract Data using your specific classes
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        reviews_data = []
        # Each 'hjmQqc' is a review block in your HTML
        review_containers = soup.select('.hjmQqc')

        for container in review_containers:
            try:
                # Extracting Star Rating from aria-label (e.g., "Rating of 5")
                rating_tag = container.select_one('.HeTgld')
                rating_text = rating_tag['aria-label'] if rating_tag else "0"
                stars = int(''.join(filter(str.isdigit, rating_text)))

                # Only keep high-quality reviews
                if stars >= 4:
                    reviews_data.append({
                        "name": container.select_one('.IaK8zc').text.strip(),
                        "profile_pic": container.select_one('.AqC5qd')['src'] if container.select_one('.AqC5qd') else "",
                        "time": container.select_one('.bHyEBc').text.strip(),
                        "content": container.select_one('.d5K5Pd').text.strip() if container.select_one('.d5K5Pd') else "No text",
                        "stars": stars
                    })
            except Exception as e:
                continue

        # 4. Save to JSON
        output_path = 'polished_reviews.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(reviews_data, f, indent=4, ensure_ascii=False)
        
        print(f"Success! Captured {len(reviews_data)} high-quality reviews.")

    except Exception as e:
        print(f"Error encountered: {e}")
    finally:
        driver.quit()

# Use the URL of the review page specifically
target_url = "https://www.google.com/maps/place/Zudio+-+Mansarovar,+Jaipur/@26.8400185,75.4559624,11z/data=!4m12!1m2!2m1!1szudio!3m8!1s0x396db5ab4004fb9d:0xa0380e7e79288cc8!8m2!3d26.8400185!4d75.760833!9m1!1b1!15sCgV6dWRpb1oHIgV6dWRpb5IBDmNsb3RoaW5nX3N0b3Jl4AEA!16s%2Fg%2F11vcbqt830?entry=ttu&g_ep=EgoyMDI2MDEyOC4wIKXMDSoKLDEwMDc5MjA2N0gBUAM%3D" 
scrape_lakshya_library_reviews(target_url)