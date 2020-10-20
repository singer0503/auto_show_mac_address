# Mac 開發環境安裝

### Mac 安裝順序：
brew → pyenv → Python → pip → paramiko

以下教學均使用 Mac 進行開發環境設定教學（Mac 開發程式就是好用）

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

有 ＊ 的為目前的版本，代表我們還在使用系統版本，所以要整個切過去

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
開發Python應用程式時，需要使用到許多第三方開發的Python套件(package)。建議使用pip套件管理工具來從PyPI下載所需的套件。

# 使用 pip 安裝 paramiko 套件

```go
pip install paramiko
```

以上都安裝完成了，就可以開始用該程式碼


## 連結

- [目錄](directory.md)
- 下一章：[開發 ssh 功能](./Document/01.1.md)