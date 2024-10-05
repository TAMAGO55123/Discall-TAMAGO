from flask import Flask
from threading import Thread
from dotenv import load_dotenv
from os import getenv

load_dotenv()


app = Flask("")

@app.route("/")
def main():
  return "Discall-Nofication is alive!"

def run():
  app.run("0.0.0.0", port=getenv("Flask_port"))

def keep_alive():
  t = Thread(target=run)
  t.start()

