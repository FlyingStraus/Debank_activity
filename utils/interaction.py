from utils.libs import *
from utils.init import *

class Debank():
    def __init__(self,private_key, proxy = None, user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"):
        self.private_key = private_key
        self.public_address =w3.eth.account.from_key(self.private_key).address.lower()
        self.session_id = None
        self.id = str(self.public_address)
        if proxy is not None:
            proxy = proxy.split(':')
            session.proxies = {
            'https' : f'https://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}',
            'http': f'http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}',
            }
        self.user_agent = user_agent
        self.headers = {"Content-Type": "application/json",
        "referer":"https://debank.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "accept-language": "ru-RU,ru;q=0.9",
        "account": json.dumps({"random_at":1678494411,"random_id":"00149223f8e845e1b6404c46f26d6f4b","user_addr":""})
        }
        # session.headers.update({"Content-Type": "application/json",
        # "referer":"https://layer3.xyz/quests/",
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        # "accept-language": "ru-RU,ru;q=0.9",
        # # "cookie": "_cfuvid=3S5fabJ_P_TK9yw.nsrhxeDgMhVER0miEh39eTr30lE-1684010334723-0-604800000;layer3_access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjMyMjI0OSwiaWF0IjoxNjg0MDcwMjE0LCJleHAiOjE2ODQwNzM4MTR9.rqrUNzxVE_suvhJCsXuWD8sIkGvO0MGmvTSZKY4N8ig;",
        # })

    
    def login(self):
        
        data = {"id":str(self.public_address)}
        r = session.post("https://api.debank.com/user/sign_v2", json=data, headers=self.headers)
        data = (r.text).replace("null", "None").replace("false", "False").replace("true", "True")
        if int(r.status_code) != 200:
            raise WrongResponce(r)
        
        nonce = json.loads(json.dumps(eval(data)))
        self.id = nonce["data"]["id"]
        msg = nonce["data"]["text"]


        # Signing
        message = encode_defunct(text=msg)
        signed_message =  w3.eth.account.sign_message(message, private_key=self.private_key).signature.hex()
        
        # logging
        data = {"signature":signed_message,"id":self.id}
        r = session.post("https://api.debank.com/user/login_v2", json=data, headers=self.headers)

        if int(r.status_code) != 200:
            raise WrongResponce(r)
        
        data = json.loads(json.dumps(eval((r.text).replace("null", "None").replace("false", "False").replace("true", "True"))))
        self.session_id = data["data"]["session_id"]

        self.headers = {"Content-Type": "application/json",
        "referer":"https://debank.com/",
        "user-agent": self.user_agent,
        "accept-language": "ru-RU,ru;q=0.9",
        "account": json.dumps({"random_at":1678494411,"random_id":"00149223f8e845e1b6404c46f26d6f4b","session_id":self.session_id,"user_addr":self.id,"wallet_type":"metamask","is_verified":True})
        }
        
        # logging.info(self.session_id)

        return self.public_address
            
    def follow(self, address):
        r = session.get(f"https://api.debank.com/user/follow?addr={address}", headers = self.headers)

        if int(r.status_code) != 200:
            raise WrongResponce(r)

        data = json.loads(json.dumps(eval((r.text).replace("null", "None").replace("false", "False").replace("true", "True"))))
        # print(data["data"]["is_success"])
        # if data["data"]["is_success"]!= True:
        #     raise FollowProblems(r,self.public_address)

    def vote(self,vote_id):

        data = {"id":vote_id}

        r = session.post(f"https://api.debank.com/proposal/vote", json = data,headers = self.headers)
        if int(r.status_code) != 200:
            raise WrongResponce(r)

        # data = json.loads(json.dumps(eval((r.text).replace("null", "None").replace("false", "False").replace("true", "True"))))

