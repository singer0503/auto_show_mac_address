## 背景介绍
網路工程在日常工作中仍然少不了大量登入交換機，因此寫一個 python 腳本，可以自動化登錄設備，然後顯示命令結果，從而減少人力成本，增加下午茶時間。

## 設計思路
onecollect.py 是簡單的批次多執行緒 ssh 登入。使用方法很簡單，在 config.py 文件裡面填入設備帳號密碼IP和命令，最多五個執行緒。抓取完資訊會放在設備名產生的資料夾下，加上日期。如果進行大量設備資訊收集可以使用，效率還不錯。 

## 使用方式
config.py 文件主要是配置登入設備的相關參數
``` python
username = 'cisco'
password = 'cisco'
hosts = '''
10.64.1.254
10.1.1.12
'''
cmds = '''
terminal length 0
show mac address-table
'''

執行主程式
```
``` python
python onecollect.py
```



