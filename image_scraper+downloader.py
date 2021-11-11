from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time
import os

##Enter path of webdriver. For firefox its geckodriver for chrome its chromedriver.
PATH = r" "

wd = webdriver.Firefox(executable_path=PATH)

inp=input("Enter image class : ")
num=int(input("Enter number of images you want : "))

def get_images_from_google(wd, delay, max_images):
	
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    
    
    uri1="https://www.google.com/search?q="
    uri2="&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiJ8O_iroj0AhWCyzgGHb_UAjwQ_AUoAXoECAEQAw&biw=1536&bih=778&dpr=1.25"
    url = inp
    wd.get(uri1+url+uri2)
    
    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips:max_images]:
            
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)} images")

    return image_urls

##Enter the path where you want to downoad the images
download_path = r" "
file_path = download_path+inp
os.mkdir(file_path)
def download_image(download_path, url, fname):
    
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        
        with open(file_path+"\\"+fname, "wb") as f:
            image.save(f, "JPEG")

        print(f"Image {i+1} downloaded successfully.")
    except Exception as e:
        print(f"Image {i+1} download FAILED -", e)

urls = get_images_from_google(wd, 1, num)
print(len(urls))
for i, url in enumerate(urls):
	download_image(download_path, url ,str(i)+".jpg")

wd.quit()