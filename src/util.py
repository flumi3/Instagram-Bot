import os

from selenium import webdriver


def check_webdriver():
    for root, dirs, files in os.walk(r"C:\Users"):
        for file in files:
            if "geckodriver" in file:
                geckodriver_path = os.path.join(root, file)

    if not geckodriver_path:
        print("Could not find path of geckodriver executable.")
        return

    browser = webdriver.Firefox(executable_path=geckodriver_path)
    browser.get("https://google.com")
    print(browser.title)
    browser.quit()


if __name__ == "__main__":
    check_webdriver()
