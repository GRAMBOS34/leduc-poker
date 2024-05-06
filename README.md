# Leduc Poker - For Practical Research 1

## Library used - RLCard

> Link: https://github.com/datamllab/rlcard/tree/master

> Citation: Zha, Daochen, et al. "RLCard: A Platform for Reinforcement Learning in Card Games." IJCAI. 2020.

# Steps to make this thing run

_I didnt make this easier to run because i dont know how to so here you go_
_I really wish i couldve made this easier but since i procrastinated for weeks on end couldnt_

### Step 1 - Make sure you have pip, python, and npm installed

Go to google if you don't have these installed

### Step 2 - Install Packages

First, open a terminal and cd it into the folder where you have installed the project

a) For the server (do before the running the react app)

```
cd server
pip install -r requirements.txt
```

b) For the React App

```
cd leduc-poker
npm install
```

### Step 3 - Running them - ***RUN THESE COMMANDS IN SEPERATE TERMINALS***

a) To run the python apps

```
python server.py
```

```
python bot.py
```

b) To run the react app

> (Don't forget to go into the parent folder first)

> (The parent folder and the folder for the react app have the same name so keep that in mind)

> (Run these also in seperate terminals)

```
cd leduc-poker
npm run dev
```

> Then copy the link in the console to a web browser

# Other things to keep in mind

### 1) Only clear the data.json for every new person otherwise don't

> Do this by running the resetJson.py script

### 2) This is God's worst code so don't expect it to be really good

### 3) This is just for a mini research paper so I kinda didn't care what I did here tbh
