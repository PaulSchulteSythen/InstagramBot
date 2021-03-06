# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 10:51:49 2020

@author: Paul Schulte
"""

from InstagramBot import InstagramBot
import time
import random
import logging

class bot_general(InstagramBot):

    def __del__(self):
        self.stop = True
        self.driver.close()
    
    def __init__(self, minimize, bot_name):
        # initialize bot_name -> "bot1", "bot2", "bot4", "likeBot"
        self.bot_name = bot_name

        try:
            # initialize random-seed
            random.seed()
            
            # define logger 
            self.logger = logging.getLogger("__main__")
            logging.basicConfig(level=logging.DEBUG)
            
            # start InstagramBot and check for success
            if InstagramBot.__init__(self, minimize) == -1:
                self.logger.error(self.bot_name + ": \"config/xpaths.conf\" not existing")
                return -1
            
            # click "accept cookies"-button
            while True:
                # some delay
                time.sleep(2)
                try:
                    # click button
                    self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/button[1]').click()
                    break
                except:
                    continue
        except:
            # put error-record to console-UI
            self.logger.error("initializing instance of " + self.bot_name + " failed")
            return -1
    

    def start(self, wait):
        '''
        Returns
        -------
         number of liked posts
         
         OR
        
        -1 : page not available.
        -2 : obtaining links somehow failed.
        -3 : stopped.
        -4 : liking or saving post failed.
        -5 : unknown error.
        '''

        # initialize pause-boolean
        self.stop = False

        # fetch for error codes
        if self.links == -1:
            return -1 # page not available
        elif self.links == -2:
            return -2 # obtaining links failed
            
        # remove posts from list that already were liked/saved etc.
        already_links = self.readFile(self.key + "." + self.bot_name)
        self.links = [link for link in self.links if link.split("p/")[1].split("/")[0] not in already_links]
        

        # for saving / not repeating
        links_done = list()
        
        # like and save posts
        try:
            for number, post in enumerate(self.links):
                try:
                    # bot got stopped per button
                    if self.stop:
                        return -3 # stop-code
                    else:
                        # like and save post
                        if InstagramBot.likeAndSavePost(self, post) == 1:
                            self.logger.info(self.bot_name + ": successfully liked and saved post " + str(number + 1) + " / " + str(len(self.links)) + ": " + '"' + str(post) + '"')
                            links_done.append(post)
                        else:
                            self.logger.error(self.bot_name + ": failed to like and save post " + str(post)) 
                            
                            # write link to error-folder
                            try:
                                with open("config/error_links.txt", "a+") as file:
                                    file.write(post + ",\n")
                                    file.close()
                            except:
                                pass
                    
                        # wait time not to seem suspicious
                        twait = wait + random.random()
                        self.logger.info(self.bot_name + ": waiting " + str(twait) + " seconds...")
                        time.sleep(twait)
                except:
                        self.logger.error("FAIL")
                    
            # save liked and saved links
            self.saveFile(self.key + "." + self.bot_name, links_done)
        except Exception as e:
            #print("liking routine failed")
            self.logger.error(e)
            return -5
        return len(links_done)
    
    def pause(self):
        """
        stop the bot

        Returns
        -------
        None.

        """
        self.stop = True
        
"""
if __name__ == "__main__":
    bot = bot1(False)
    bot.login("bottest371", "BotTestAccount1")
    bot.start("montanablack",  wait=5, amount=3)"""