# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 16:28:48 2020

@author: Paul Schulte

bot for linking and saving posts within a hashtag
"""

from bot_general import bot_general

class bot2(bot_general):
    def __init__(self, minimize):
        # try to init bot
        if bot_general.__init__(self, minimize, "bot2") == -1:
            return
        
    def start(self, hashtag, wait, amount):
        # get post-links first
        self.obtainLinks(hashtag, amount)
        
        # like and save all posts afterwards
        return bot_general.start(self, wait)
        
    def obtainLinks(self, hashtag, amount):
        # get post-links
        self.links = self.getHashtagPostLinks(hashtag, amount)
        # saving key for later
        self.key = hashtag
        
if __name__ == "__main__":
    bot = bot2(False)
    bot.login("bottest371", "BotTestAccount1")
    bot.start("handball", wait=3, amount=4)