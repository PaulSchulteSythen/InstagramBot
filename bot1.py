# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:28:48 2020

@author: Paul Schulte

bot for linking and saving every post at a persons tagged
"""


from bot_general import bot_general

class bot1(bot_general):
    def __init__(self, minimize):
        # try to init bot
        if bot_general.__init__(self, minimize, "bot1") == -1:
            return
        
    def start(self, accountName, wait, amount):
        # get post-links first
        self.obtainLinks(accountName, amount)
        
        # like and save all posts afterwards
        return bot_general.start(self, wait)
        
    def obtainLinks(self, accountName, amount):
        # get post-links
        self.links = self.getTaggingLinks(accountName, amount)
        # saving key for later
        self.key = accountName
    
    
    
        
if __name__ == "__main__":
    bot = bot1(False)
    bot.login("bottest371", "BotTestAccount1")
    bot.start("montanablack",  wait=5, amount=3)