## 背景介绍
網路工程在日常工作中仍然少不了大量登入交換機，因此寫一個 python 腳本，可以自動化登入設備，然後顯示命令結果，從而減少人力成本，增加下午茶時間。

## 設計思路
onecollect.py 是簡單的批次多執行緒 ssh 登入。使用方法很簡單，在 config.py 文件裡面填入設備帳號、密碼、IP 和命令，最多五個執行緒。抓取完設備會放在設備名產生的資料夾下，加上日期。如果進行大量設備資訊收集可以使用，效率還不錯。 

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
```

執行主程式
``` python
python onecollect.py
```

# 開發環境設定
首先確認需求目標

- 使用 Python 開發
- 能夠登入 Cisco 設備並且下指令後把顯示資料做保存

接下來會用到的名詞解釋

- brew：Mac 電腦好用的開發套件管理器，我的 Java、tomcat...等等都是透過這個套件來安裝管理
- pyenv：因為 Python 的版本有 2~3，現在快要到 v4 版本了，這套件可以讓你電腦安裝多種版本
- Python：今日主角，就是個程式語言
- pip：Python 有很多套件預設是沒有安裝的，若要下載其他套件，就要透過這個模組
- paramiko：python 的一種模組，支援 Linux, Solaris, BSD, MacOS X, Windows 等平台透過 ssh 從一個平台連接到另外一個平台。利用該模組，可以方便的進行 ssh 連接和 sftp 協議進行檔案傳輸。

- choco：若為 Windows 電腦則需改用這個開發套件管理器

### Mac 安裝順序：
brew → pyenv → Python → pip → paramiko

### Windows 安裝順序：
choco → pyenv-win → Python → pip → paramiko

## 文件連結
這個專案的說明文件都會放在 Document 資料夾下
- 想讀書的人～[目錄](./Document/directory.md)
- [Mac 開發環境安裝](./Document/00-Mac.md)
- [Windows 開發環境安裝](./Document/00-Windows.md)
