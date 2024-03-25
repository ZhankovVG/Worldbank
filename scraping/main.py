import json
import csv
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def gather_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://projects.worldbank.org/en/projects-operations/projects-list?os=180")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".project-list-link")))

    html = driver.page_source

    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    project_titles = soup.find_all("a", class_="project-list-link")

    bank_data = [{"title": title.text.strip()} for title in project_titles]

    return bank_data

def main():
    bank_data = gather_data()
    
    if bank_data:
        cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
        with open(f"bank_{cur_time}_async.json", "w", encoding="utf-8") as file:
            json.dump(bank_data, file, indent=4, ensure_ascii=False)

        with open(f"bank_{cur_time}_async.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(("title",))
            for item in bank_data:
                writer.writerow((item["title"],))
    else:
        print("Данные не найдены.")


if __name__ == "__main__":
    main()