from webbrowser import get
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from sys import argv

def getLastChapterANDmangaName(url):
    if __name__ == "__main__":
        options = Options()
        options.add_argument("--headless")
        driver = uc.Chrome(options=options)
        driver.get(url)
        lastChapter = str(driver.find_element(By.CSS_SELECTOR, "html#site_type body div#main-page.page div.page__inner div.container.container_responsive div.media-container div.media-sidebar div.media-info-list.paper div.media-info-list__item div.media-info-list__value.text-capitalize").text)
        mangaName = driver.find_element(By.CLASS_NAME, "media-name__main").text
        print(f'{lastChapter}¿{mangaName}')
        driver.quit()
        #return lastChapter,mangaName

if __name__ == "__main__":
    getLastChapterANDmangaName(argv[1])
#getLastChapterANDmangaName('https://mangalib.me/promisecinderella?section=info')