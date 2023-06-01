from utils.libs import *
from utils.init import *
from utils.interaction import * 
from utils.tasks import * 




if __name__ == '__main__':

    logging.info("Hallo\n\nComments, ideas - telegram - @Straus_fm")

    
    with open('wallets.txt') as f:
        wallets = f.readlines()

    for i in range(len(wallets)):
        try:
            wallets[i] = wallets[i].split('\n')[0]

            if wallets[i][0] == '0' and wallets[i][1] == 'x':
                wallets[i] = wallets[i].split('0x')[1]
        except:
            pass
    
    
    
    try:
        with open('proxy.txt') as f:
            proxies = f.readlines()

        for i in range(len(proxies)):
            proxies[i] = proxies[i].split('\n')[0]
        logging.info(f"Proxies num - {len(proxies)}") 

        i=0
        proxies_base_len = len(proxies)
        while len(proxies) < len(wallets):
            proxies.append(proxies[i])
            i+=1
            if i >= proxies_base_len:
                i=0

        logging.info(f"Proxies num extendent - {len(proxies)}") 
    except:
        proxies = None
        logging.info("No proxies found")


    logging.info(f"Wallets num - {len(wallets)}") 

    for key, value in TASKS_list.items():
        logging.info(f"{key}) {value}")


    task_todo = int(input("Your choise: "))

    if task_todo == 1:
        task_option = int(input("Choose:\n1)Manually entered addresses\n2)Random 5 wallets\nYour choise: "))
        if task_option == 1:
            with open('follow_to.txt') as f:
                follow_to = f.readlines()
            for i in range(len(follow_to)):
                try:
                    follow_to[i] = follow_to[i].split('\n')[0].lower()
                except:
                    pass
                                    
        elif task_option == 2:
            with open('popular_wallets.txt') as f:
                filename = f.readlines()
            follow_to = random.choices(filename, k=5)
            for i in range(len(follow_to)):
                try:
                    follow_to[i] = follow_to[i].split('\n')[0].lower()
                except:
                    pass

            
        logging.info(f"Entered {len(follow_to)} addresses")

    
        if len(follow_to) == 0:
            Report_message("List to follow addresses is empty")
        
    
        if proxies is not None:
            for i in range(len(wallets)):
                try:
                    lol = Tasks(wallets[i],proxy=proxies[i])
                    lol.follow_on_list(follow_to)
                    
                except Exception as er:
                    logging.error(f"Error - {er}")
                logging.info(f"Sleeping")
                sleep(10)
        else:
            for i in range(len(wallets)):
                try:
                    lol = Tasks(wallets[i])
                    lol.follow_on_list(follow_to)           
                except Exception as er:
                    logging.error(f"Error - {er}")
                logging.info(f"Sleeping")
                sleep(10)

    input("Done, Press any button to close")


    

    