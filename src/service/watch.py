import getpass
import glob

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
