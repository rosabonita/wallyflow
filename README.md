# wallyflow
WallyFlow for Hackster.io Contest

## Rasbperry Pi 3 B

### 5V LED White LED Strip

## Local MySQL Database

```
sudo apt-get install mysql-server python-mysqldb
```

```
sudo mysql
```

```
CREATE DATABASE wallyflowdb;
```

```
GRANT ALL PRIVILEGES ON wallyflowdb.* to 'wallflow'@'localhost' IDENTIFIED BY 'wallyflow';
```

```
QUIT;
```

## Desktop File

```
cd .config/autostart/
```

```
sudo vim wallyflow.desktop
```

```
[Destop Entry]
Encoding=UTF-8
Type=Application
Name=WallyFlow_Walabot
Exec=lxterminal -e python /home/hackster/wallyflow/wallyflow_walabot.py
StartupNotify=true
Terminal=true
Hidden=false
```

## Lambda Function

### Homebrew
These instructions are for Mac OS. It is recommended that you used Homebrew to install required packages, as it expedites the process. Instructions for installing [Homebrew](https://brew.sh/) can be found on their website.

### Node JS
```
brew install node
```

``` mkdir wallyflow ```

``` touch index.js ```

#### Yarn

```
brew install yarn
```

``` 
sudo yarn.init 
```

```
question name (wallyflow): WallyFlow 
```

``` 
question version (1.0.0): 
```

```
question description: Wally Flow, Mindfulness with Walabot and Amazon Alexa 
```

```
question entry point (index.js):
```

``` 
question repository url:
```

``` 
question author: ```

```
question license (MIT):
```

```
question private:
```

### Alexa SDK

```
sudo yarn add alexa-sdk
```

#### Deployment Zip File

*Note: If you're building your deployment package on Mac, Zip from directly from the terminal, not the context menu. Otherwise you will get an error in your file structure when you upload.*

```
zip -r ../wallyflow.zip *
```

##### Role

## Alexa Skill

## TP Link
