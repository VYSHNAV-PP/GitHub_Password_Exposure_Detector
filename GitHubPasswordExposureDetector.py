
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import  ChromeDriverManager
from telnetlib import EC
from selenium.webdriver.support import expected_conditions as EC
import time


def is_valid_url(url): #To check whether the url is valid
    return url.startswith("http://") or url.startswith("https://")

def going_for_raw(browser, second_page):#To click the raw button of github
    try:
        browser.get(second_page)
        time.sleep(5)

        try:
            raw = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-testid='raw-button']")))

            raw.click()
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "pre"))
            )
        except Exception as a:
            print(f"Error finding raw button : {a}")

        html=browser.page_source
        time.sleep(2)
        if "password" in html.lower(): #To check for the specific word "password"
            time.sleep(3)
            lines = html.split('\n')
            for line in lines:
                if 'password' in line.lower(): #All the code inside the if statement is for finding and printing the words near to the word "password"
                    start_index = line.lower().find('password')
                    before = line[max(0, start_index - 10):start_index]
                    after = line[start_index + len('password'):start_index + len('password') + 10]
                    snippet = before + '[password]' + after
                    print(f"Found 'password' in {second_page}:.....{snippet}")
            time.sleep(2)
            browser.quit()
        else:
            print(f"No 'password' found in {second_page}")
    except Exception as e:
        print(f"ERROR ACCESSING {second_page}: {e}")


def loop(browser, page):
    try:
        browser.get(page)
        time.sleep(3)
        resource2 = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "Link--primary")) #To locate repository
        )
        print(resource2)
        for extension in resource2:
            print(extension.text)
            if "py" in extension.text:
                second_page = f"{page}/blob/main/{extension.text}"
                print(second_page)
                print(".py file found")
                going_for_raw(browser, second_page)

            elif "json" in extension.text:
                second_page = f"{page}/blob/main/{extension.text}"
                print(".json file found")
                going_for_raw(browser, second_page)

            elif "php" in extension.text:
                second_page = f"{page}/blob/main/{extension.text}"
                print(".php file found")
                going_for_raw(browser, second_page)

            elif "xml" in extension.text:
                second_page = f"{page}/blob/main/{extension.text}"
                print(".xml file found")
                going_for_raw(browser, second_page)
            elif "html" in extension.text:
                second_page = f"{page}/blob/main/{extension.text}"
                print(".html file found")
                going_for_raw(browser, second_page)
            else :
                pass
    except Exception as e:
        print(f"Error processing {page}: {e}")

def main():

    target_url=input("Enter you target url (NOTE: THIS BOT ONLY WORKS FOR GITHUB TARGETS): ").strip()

    if is_valid_url(target_url):
        s=Service(ChromeDriverManager().install())

        browser=webdriver.Chrome(service=s)
        try:
            browser.get(target_url)
            time.sleep(3)
            resource = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "repo"))
            )

            links =[]
            flink=[]

            for i in resource:
                links.append(i.text)
            print(links)

            for j in links:
                next_page=f"{target_url}/{j}"
                flink.append(next_page)
                print(next_page)
                loop(browser, next_page)
        except Exception as e:
            print(f"An error occurred : {e}")

        finally:
            browser.quit()
    else:
        print("INVALID URL!")

if __name__ == '__main__':
    while True:
        main()
        user=input("DO YOU WANT TO RUN ANOTHER URL? (YES/NO)").strip()
        if user.lower()=="no":
            print("EXITING PROGRAM...")
            break
        elif user.lower()=="yes":
            main()
        else:
            print("Invalid Input!..")





