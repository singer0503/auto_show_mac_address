## 背景介绍
網路工程在日常工作中仍然少不了大量登入交換機，因此寫一個 python 腳本，可以自動化登錄設備，然後顯示命令結果，從而減少人力成本，增加下午茶時間。

## 設計思路
onecollect.py 是簡單的批次多執行緒 ssh 登入。使用方法很簡單，在 config.py 文件裡面填入設備帳號密碼IP和命令，最多五個執行緒。抓取完設備會放在設備名產生的資料夾下，加上日期。如果進行大量設備資訊收集可以使用，效率還不錯。 

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
- paramiko：python 的一種模組，支援 Linux, Solaris, BSD, MacOS X, Windows 等平台透過 SSH從一個平台連接到另外一個平台。利用該模組，可以方便的進行 ssh 連接和 sftp 協議進行 sftp文件傳輸。

安裝順序：

brew → pyenv → Python → pip → paramiko

以下教學均使用 Mac 進行開發教學（Mac 開發程式就是好用）

# 都還沒開始裝 Python，電腦裡面怎麼已經有了？

Mac 系統其實已經內建了 Python，所以平常沒事不要去亂動比較好！

所以我們要用 pyenv 來安裝平常可以使（亂）用（搞）的 Python。

pyenv：可以把他想像成一套虛擬環境

# 安裝 brew 吧 [https://brew.sh/](https://brew.sh/)

```go
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

# 接下來安裝 pyenv

我們使用 brew 直接下指令安裝 pyenv，如果有需要，也可以下 upgrade 來更新版本

```go
brew update
brew install pyenv
brew upgrade pyenv
```

### **pyenv 設定**

安裝 pyenv 完成之後，請執行以下指令，以進行後續的設定：

```
pyenv init
```

執行成功之後，會出現以下的提示，告訴我們必須在 `~/.zshrc` 中加入 1 行 `eval "$(pyenv init -)"`：

```
# Load pyenv automatically by appending
# the following to ~/.zshrc:

eval "$(pyenv init -)"
```

上述設定是登入系統後就自動啟用 pyenv 

### p.s. 如果是習慣使用 bash 的使用者，需修改 `.bash_profile` 而不是 `.zshrc`

設定完成後，執行以下指令讓 SHELL 重新啟動，讓 pyenv 的設定生效：

```
exec "$SHELL"
```

以上就完成設定囉！

如果你從來沒使用過 terminal 而且系統告訴你

> The file /Users/xxx/.bashrc does not exist.

那就在 terminal 輸入以下指令後，複製貼上剛剛提到的那幾行

```
touch ~/.bashrc && open ~/.bashrc
```

接著**重開 terminal**！就準備好安裝 python

# **安裝 Python**

使用 pyenv 輸入以下指令安裝

```
pyenv install 3.9.0
```

裝好之後我們可以看看我們總共有哪些版本

```
pyenv versions
```

![https://i2.wp.com/stringpiggy.hpd.io/wp-content/uploads/2019/10/carbon.png?fit=720%2C281&ssl=1](https://i2.wp.com/stringpiggy.hpd.io/wp-content/uploads/2019/10/carbon.png?fit=720%2C281&ssl=1)

有``的為目前的版本，代表我們還在使用系統版本，所以要整個切過去

```
pyenv global 3.9.0
```

在跑一次

```
pyenv versions
```

![https://i0.wp.com/stringpiggy.hpd.io/wp-content/uploads/2019/10/carbon-1.png?fit=720%2C281&ssl=1](https://i0.wp.com/stringpiggy.hpd.io/wp-content/uploads/2019/10/carbon-1.png?fit=720%2C281&ssl=1)

**完成囉，確認安裝結果**

來看看我們的 python 出自於哪裡！

```
which python
```

> /Users/<user-name>/.pyenv/shims/python

確認是不是已經是 3.9.0 了

```
python --version
```

> Python 3.9.0

安裝 python 的動作大功告成！

# 安裝 pip

```go
sudo easy_install pip
```

# 使用 pip 安裝 paramiko 套件

```go
pip install paramiko
```

以上都安裝完成了，就可以開始用該程式碼



