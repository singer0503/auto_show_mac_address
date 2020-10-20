import time,multiprocessing,os
import paramiko     #Note: 提供 ssh 功能模組
import re           #Noet: 正則表達式模組

import sys          #Noet: 檢測錯誤模組
import traceback    #Noet: 檢測錯誤模組

try:
    from config import * #Note: 把 config.py 讀進來
except:
    hosts = ''
    username = '' 
    password = ''
    cmds = ''

stdmore = re.compile(r"-[\S\s]*[Mm]ore[\S\s]*-")
hostname_endcondition = re.compile(r"\S+[#>\]]\s*$")

class ssh_comm(object):
    def __init__(self,address,username,password,port=22):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Note: 自動添加主機名及密鑰到本地並保存，不依賴load_system_host_keys()配置，即如果known_hosts裡沒有遠程主機的公鑰時，默認連接會提示yes/no，自動yes
        print('ssh_comm connection...')
        self.client.connect(address, port=port, username=username, password=password, timeout=10, look_for_keys=True,allow_agent=False)
        self.shell = self.client.invoke_shell()
        while True:
            time.sleep(0.5)
            if self.shell.recv_ready() or self.shell.recv_stderr_ready():
                break
        self.shell.recv(4096).decode('utf-8')
        self.shell.send('\n')
        output = self.shell.recv(4096).decode('utf-8')
        output = output
        while True:
            if hostname_endcondition.findall(output):
                self.hostname = hostname_endcondition.findall(output)[0].strip().strip('<>[]#')
                break
            while True:
                time.sleep(0.1)
                if self.shell.recv_ready() or self.shell.recv_stderr_ready():
                    break
            output += self.shell.recv(4096).decode('utf-8')
    def recv_all(self,interval,stdjudge,stdconfirm):
        endcondition = re.compile(r"%s\S*[#>\]]\s*$"%self.hostname)
        while True:
            time.sleep(interval)
            if self.shell.recv_ready() or self.shell.recv_stderr_ready():
                break
        output = self.shell.recv(99999).decode('utf-8')
        if (stdjudge != '') and (stdjudge in output):
            self.shell.send(stdconfirm+'\n')
        while True:
            if stdmore.findall(output.split('\n')[-1]):
                break
            elif endcondition.findall(output):
                break
            while True:
                time.sleep(interval)
                if self.shell.recv_ready() or self.shell.recv_stderr_ready():
                    break
            output += self.shell.recv(99999).decode('utf-8')
        return output
    def send_command(self,command_interval,command,stdjudge,stdconfirm):
        command += "\n"
        self.shell.send(command)
        if ('hostname' in command) or ('sysname' in command):
            while True:
                time.sleep(0.5)
                if self.shell.recv_ready() or self.shell.recv_stderr_ready():
                    break
            stdout = self.shell.recv(4096).decode('utf-8')
            self.hostname = hostname_endcondition.findall(stdout)[-1].strip().strip('<>[]#')
        else:
            stdout = self.recv_all(interval=command_interval,stdjudge=stdjudge,stdconfirm=stdconfirm)
        data = stdout.split('\n')
        while stdmore.findall(data[-1]):
            self.shell.send(" ")
            tmp = self.recv_all(interval=command_interval,stdjudge=stdjudge,stdconfirm=stdconfirm)
            data = tmp.split('\n')
            stdout += tmp
        return stdout
    def close(self):
        if self.client is not None:
            self.client.close()
    def run(self,cmds,command_interval,stdjudge,stdconfirm):
        stdout = ''
        rc = 'success'
        for cmd in cmds.split('\n'):
            if cmd.strip():
                stdout += self.send_command(command=cmd,command_interval=command_interval,stdjudge=stdjudge,stdconfirm=stdconfirm)
        return rc, stdout

def writeoutput(address,username,password,cmds):
    try:
        connection = ssh_comm(address=address, username=username, password=password, port=22)
    except Exception as e:
        error_class = e.__class__.__name__ #取得錯誤類型
        detail = e.args[0] #取得詳細內容
        cl, exc, tb = sys.exc_info() #取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        print(errMsg)
        rc = 'connection failed'
        return address,rc
    stdjudge = 'Y/N'
    stdconfirm = 'Y'
    rc,stdout = connection.run(cmds=cmds,command_interval=0.1,stdjudge=stdjudge,stdconfirm=stdconfirm)
    connection.close()
    hostname = connection.hostname.split('/')[-1].split(':')[-1]
    #Note: 若有需要可以使用 SNMP v2c 做事情 
    #hostname = os.popen('/usr/local/net-snmp/bin/snmpwalk -v 2c -c tcnw %s sysname -Oqv'%address).read().strip()

    #Note: 根據各機器名稱產生目錄
    if not os.path.exists(hostname):
        os.makedirs(hostname)
    filename = hostname+'-'+time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

    #Note: 產生 txt 檔保存資料
    with open ('%s/%s.txt'%(hostname,filename),'w') as f:
        f.write(stdout)
    return address,rc
    
#Note: 主程式呼叫 main
def main(username,password,hosts,cmds):
    print('main('+username+','+password+','+hosts+','+cmds+')')
    #Note: 檢查欄位是否有問題
    if username == '':
        username = raw_input('請輸入使用者名稱：')
    if password == '':
        password = raw_input('請輸入密碼： ')
    if hosts == '':
        hosts = raw_input('請輸入主機地址： ')
    if cmds == '':
        cmds = raw_input('請輸入採集命令： ')
    
    host_list = hosts.split('\n')
    if len(host_list) < 5:
        processnum = len(host_list)
    else:
        processnum = 5
    #Note: 可以調整多執行緒的地方，預設最高是 5 個 thread 再跑
    pool = multiprocessing.Pool(processes=processnum )
    process = []
    for host in host_list:
        if host:
            process.append(pool.apply_async(writeoutput, (host.strip(),username,password,cmds)))
    pool.close()
    pool.join()
    outs = ''
    for o in process:
        rc,ip = o.get()
        print('[ '+ip+' : '+rc+' ]')

#Note: 主程式入口
if __name__== '__main__':
    main(username,password,hosts,cmds)
