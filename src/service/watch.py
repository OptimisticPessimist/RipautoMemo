import getpass
import glob
import time


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from src.domain import Friend

DIR_WATCH = f"C:\\Users\\{getpass.getuser()}\\AppData\\LocalLow\\VRChat\\VRChat\\"
PATTERNS = "output_log_??-??-??.txt"


class FriendLog:
    def __init__(self) -> None:
        self.files: list[str] = glob.glob(DIR_WATCH + PATTERNS)
        self.files = sorted(self.files)

    def analysis(self) -> list[Friend]:
        friends = list()
        for file in self.files:
            with open(file, "r", encoding="utf-8") as f:
                username = ""
                uid = ""
                world = ""
                date = ""
                for line in f:
                    if "Joining or Creating Room" in line:
                        world = line[72:].strip("\n")
                    elif "type: friendRequest" in line:
                        met = line[:10].split(".")
                        year, month, day = met
                        date = f"{year}-{month}-{day}"
                        username = line[34:].split(",")[0]
                        username = username.split("from username:")[1]
                        uid = line.split("user id:")[1][:40]

                if (username != "") or (uid != "") or (world != world) or (date != ""):
                    friend = Friend(username=username, uid=uid, world=world, date=date)
                    friends.append(friend)
        return friends


DRIVER = "chromedriver.exe"
VRC_HOME = "https://vrchat.com/home"
FRIENDS_LIST = "e176ivn28"
USERNAME_ID = "username_email"
PASSWORD_ID = "password"
SEND_BUTTON = "e7cdgnz1"


class Scraper:
    def __init__(self) -> None:
        options = Options()
        # options.add_argument("--headless")
        options.add_argument("log-level=3")
        self.driver = webdriver.Chrome(executable_path=DRIVER, options=options)
        self.denominator = ""

    def get(self, username, password) -> list[list[str]]:
        self.driver.get(VRC_HOME)
        input_username = self.driver.find_element(By.ID, USERNAME_ID)
        input_password = self.driver.find_element(By.ID, PASSWORD_ID)
        send_button = self.driver.find_element(By.CLASS_NAME, SEND_BUTTON)

        input_username.clear()
        input_password.clear()

        input_username.send_keys(username)
        input_password.send_keys(password)
        send_button.submit()
        print(f"[login] {self.driver.current_url}")
        time.sleep(10)
        self.denominator = self.driver.find_element(By.CLASS_NAME, "pl-1").get_attribute("textContent")
        self.find_friends()

        results = list()
        values = self.driver.find_elements(By.CLASS_NAME, FRIENDS_LIST)
        for value in values:
            results.append([value.get_attribute("textContent"), value.get_attribute("href").split("/")[-1]])
        self.driver.close()
        return results

    def find_friends(self, last: str = None) -> None:
        elements = self.driver.find_elements(By.CLASS_NAME, FRIENDS_LIST)
        uid = elements[-1].get_attribute("href").split("/")[-1]
        numerator = len(elements)
        print(f"[loading] {numerator} / {self.denominator}")
        if uid == last:
            print("[loading] end")
            return
        elements[-1].location_once_scrolled_into_view
        time.sleep(5)
        self.find_friends(uid)
