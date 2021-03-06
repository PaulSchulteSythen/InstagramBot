# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 15:44:37 2020

@author: Paul Schulte
"""


from datetime import datetime, timedelta
import logging
import time

from bot_general import bot_general

class bot_like(bot_general): 
    
    def __init__(self, minimize):
        # try to init bot
        if bot_general.__init__(self, minimize, "likeBot") == -1:
            return
        
    def start(self, hashtag, wait, amount):
        self.stop = False
        
        # like every hour until bot is stopped
        while not self.stop:
            try:
                # get post-links first
                self.obtainLinks(hashtag, amount)
                
                # like and save all posts afterwards
                post_code = bot_general.start(self, wait)
                
                if post_code > 0:
                    self.logger.warning("LikeBot: Liked all posts successfully.")
                else:
                    return post_code
            except:
                pass         
            # waiting an hour
            wait_time = 3600
            self.logger.warning("LikeBot: starting again at: " + str(datetime.now() + timedelta(seconds=wait_time)))
            time.sleep(wait_time)
        
    def obtainLinks(self, hashtag, amount):
        # get as many posts as needed
        try:
            amount = amount + len(self.readFile(hashtag + "." + self.bot_name))
        except:
            pass
        # get post-links
        self.links = self.getHashtagPostLinks(hashtag, amount)
        # saving key for later
        self.key = hashtag
    
        
if __name__ == "__main__":
    bot = bot_like(False)
    bot.login("bottest371", "BotTestAccount1")
    bot.start("python", amount=3, wait=3)
    