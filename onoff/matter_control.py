import sys
import os
import subprocess
import time

contorl_success = "status = 0x00 (SUCCESS)"
commission_success="Device commissioning completed with success"
class Logger(object):
    def __init__(self, filename='default.log', add_flag=True, stream=sys.stdout):
        self.terminal = stream
        print("filename:", filename)
        self.filename = filename
        self.add_flag = add_flag


    def write(self, message):
        if self.add_flag:
            with open(self.filename, 'a+') as log:
                self.terminal.write(message)
                log.write(message)
        else:
            with open(self.filename, 'w') as log:
                self.terminal.write(message)
                log.write(message)

    def flush(self):
        pass

def main():
    contorl_success_num=0;
    contorl_num=0;
    sys.stdout = Logger("matter.log", sys.stdout)
    result = subprocess.run(['python','commission.py'], stdout=subprocess.PIPE)
    print(result.stdout.decode('utf-8'))
    if result.stdout.decode('utf-8').find(commission_success) > 0:
        print("commission ok\r\n")
    
    while True:
        try:
            result = subprocess.run(['python','onoff.py'], stdout=subprocess.PIPE)
            print(result.stdout.decode('utf-8'))
            if result.stdout.decode('utf-8').find(contorl_success) > 0:
                contorl_success_num+=1
                print("contorl_success_num =",contorl_success_num);
        except subprocess.TimeoutExpired:
            result.kill()  
        contorl_num+=1;
        print("contorl_num =",contorl_num);  

if __name__ == '__main__':
    main()