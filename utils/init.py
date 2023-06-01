from utils.libs import *

session = requests.Session()

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s - %(message)s',
                    # datefmt="%Y-%m-%d %I:%M:%S",
)

def settings():
    with open("./config.json", "r", encoding="utf-8") as f:
        return dict(json.loads(f.read()))


CFG = settings()

TASKS_list = CFG.get("TASK", None)


class WrongResponce(Exception):
    def _init (self,r):
        self.r = r
        logging.error(f"Wrong response - {self.r.status_code} -{self.r.text}")
        pass

class FollowProblems(Exception):
    def _init (self,r, address):
        self.r = r
        logging.error(f"Following problem - {self.r.status_code} -{self.r.text} - on {address}")
        pass

class Report_message(Exception):
    def _init (self, message):
        self.message = message
        super().__init__(self.message)



