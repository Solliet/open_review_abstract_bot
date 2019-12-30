import praw
import requests
import bs4
import html2text
import time

import attr
import argparse
import toml
import itertools

import functools

import operator

@attr.s
class Bot:
    username = attr.ib()
    password = attr.ib()
    subreddit = attr.ib()
    client_id = attr.ib()
    client_secret = attr.ib()
    limit = attr.ib(default=400)
    disclaimer_comment = attr.ib(default="*ps: I am a bot and this action was done automatically. If there's a bug, please send a pm.*\n")

    done = attr.ib(init=False, factory=set)

    def __attrs_post_init__(self):
        self.reddit = praw.Reddit(
            username=self.username,
            password=self.password,
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent='linux:openreview_abstract_bot:0.1 (by /u/ada_td)'
        )
        setattr(self, 'subreddit', self.reddit.subreddit(self.subreddit))
    

    
    def parse_openreview(self, post):
        try:
            url = post.url
            
            #https://openreview.net/forum?id=<id>
            orid = url.split("=")[1]

            #ensure we are downloading a proper page and not a pdf
            url = f'https://openreview.net/forum?id={orid}'

            r = requests.get(url)
            soup = bs4.BeautifulSoup(r.text, features="lxml")
            soup = soup.select_one(f'div#note_{orid}')
            keys = map(operator.attrgetter("text"), soup.select(".note-content-field"))
            values = map(operator.attrgetter("text"), soup.select(".note-content-value"))
            kv = filter(lambda x: x[0] not in {"Original Pdf:", "Keywords:"} ,zip(keys, values))
            content = "\n\n___\n".join(itertools.starmap("__{}__ {}".format, kv))
            content = "\n\n___\n".join([
                content,
                f'__[Discussion](https://openreview.net/forum?id={orid})__ __[PDF](https://openreview.net/pdf?id={orid})__',
                self.disclaimer_comment
            ])
            return content
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def filterOpenReviewUrls(posts):
        return (x for x in posts if "openreview.net" in x.url)

    def filterVisited(self, posts):
        return (x for x in posts if x.id not in self.done)
    
    def filterCommented(self, posts):
        return (x for x in posts if not any(map(self.username.__eq__, map(operator.attrgetter('author'), x.comments))))

    def addVisited(self, posts):
        return ((x,self.done.add(x.id))[0]  for x in posts)

    
    def makeReplies(self, posts):
        return ((x, self.parse_openreview(x)) for x in posts)

    def postReplies(self, posts):
        posts = list(posts)
        success = []
        for post, message in posts:
            if message=="" or message is None:
                continue
            try:
                post.reply(message)
                success.append(post)
            except Exception as e:
                print(e)
                pass
        
        return success
        
    def get_posts(self):
        return functools.reduce((lambda items,fn: fn(items)),  [
            self.filterOpenReviewUrls,
            self.filterVisited,
            self.filterCommented,
            self.makeReplies,
            self.postReplies,
            self.addVisited,
            list
        ], self.subreddit.new(limit=self.limit))
        

    def run(self):
        while True:
            posts = self.get_posts()
            time.sleep(10)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=toml.load)
    config = parser.parse_args().config
    bot = Bot(**config)
    bot.run()