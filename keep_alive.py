from flask import Flask
from threading import Thread
# keeps the bot alive in replit
app = Flask('')

@app.route('/')
def home():
    return "Hello. Fuck you"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()