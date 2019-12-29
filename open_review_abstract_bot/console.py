import argparse
import toml

from open_review_abstract_bot import Bot

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=toml.load)
    config = parser.parse_args().config
    bot = Bot(**config)
    bot.run()