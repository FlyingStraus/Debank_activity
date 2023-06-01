from utils.libs import *
from utils.interaction import *
from utils.init import *

class Tasks():
    def __init__(self, private_key,proxy=None):
        self.private_key = private_key
        self.public_key = w3.eth.account.from_key(self.private_key).address.lower()
        self.proxy = proxy

    def follow_on_list(self, to_follow_arr):
        driver = Debank(private_key = self.private_key, proxy=self.proxy)
        logging.info(f"Working with wallet - {self.public_key} ")

        try:
            driver.login()
            
            for to_follow in to_follow_arr:
                try:
                    driver.follow(str(to_follow))
                except Exception as e:
                    logging.critical(f"Could not follow on wallet-  {self.public_key} - {e}")
                sleep(0.50)

        except Exception as e:
            logging.critical(f'Could not login to waller - {self.public_key} - {e}')

        logging.info(f"Done with wallet - {self.public_key} ")

    def vote(self, vote_id):
        driver = Debank(private_key = self.private_key, proxy=self.proxy)
        logging.info(f"Working with wallet - {self.public_key} ")

        try:
            driver.login()
            try:
                driver.vote(vote_id)
            except Exception as e:
                logging.critical(f"Could not vote on wallet-  {self.public_key} - {e}")

        except Exception as e:
            logging.critical(f'Could not login to waller - {self.public_key} - {e}')

        logging.info(f"Done with wallet - {self.public_key} ")

    
    