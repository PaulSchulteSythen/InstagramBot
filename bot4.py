# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:28:48 2020

@author: Paul Schulte

bot for linking and saving every post at a persons tagged
"""

from bot_general import bot_general
import logging
import time
import random

class bot4(bot_general):
    
    
    def __init__(self, minimize):
        # try to init bot
        if bot_general.__init__(self, minimize, "bot4") == -1:
            return
        
        
    def start(self, links_string, wait):
        # get post-links first
        self.obtainNormalLinks(links_string)
        self.obtainSocialLinks(links_string)


        # like and save all normal posts first
        self.logger.info(self.bot_name + ": liking and saving normal links first...")
        postCode = bot_general.start(self, wait)
        if postCode < 0:
            return postCode


        # add post code to social links post code
        num_liked_posts = postCode

        # social links liken
        self.logger.info(self.bot_name + ": liking and saving all social links...")

        # load already liked posts
        already_links = self.readFile(self.key + "." + self.bot_name)

        links_done = list()

        for number, link in enumerate(self.social_links):
            try:
                # extract link from account name
                link = self.getSocialLinks(link)

                if str(link).split("p/")[1].split("/")[0] not in already_links:
                    # like post
                    if self.likeAndSavePost(link) == 1:
                        self.logger.info(self.bot_name + ": successfully liked and saved post " + str(number + 1) + " / " + str(len(self.social_links)) + ": " + '"' + str(link) + '"') # "  + str(link))
                        num_liked_posts += 1
                        links_done.append(link)
                    else:
                        self.logger.error(self.bot_name + ": failed to like and save post") 

                    # wait time not to seem suspicious
                    twait = wait + random.random()
                    self.logger.info(self.bot_name + ": waiting " + str(twait) + " seconds...")
                    time.sleep(twait)
            except:# Exception as e:
                #print("liking routine failed")
                pass#self.logger.error(e)

        # save liked and saved links
        self.saveFile(self.key + "." + self.bot_name, links_done)    

        return num_liked_posts



        """
        # then like all social links

        # initialize pause-boolean
        self.stop = False

        # fetch for error codes
        if self.social_links == -1:
            return -1 # page not available
        elif self.social_links == -2:
            return -2 # obtaining links failed
            

        # for saving / not repeating
        links_done = list()
        
        # like and save posts
        try:
            for number, post in enumerate(self.social_links):
                try:
                    # bot got stopped per button
                    if self.stop:
                        return -3 # stop-code
                    else:
                        # like and save post
                        if InstagramBot.likeAndSavePost(self, post) == 1:
                            self.logger.info(self.bot_name + ": successfully liked and saved post " + str(number + 1) + " / " + str(len(self.social_links)) + ": " + '"' + str(post) + '"')
                            links_done.append(post)
                        else:
                            self.logger.error(self.bot_name + ": failed to like and save post " + str(post)) 
                    
                        # wait time not to seem suspicious
                        twait = wait + random.random()
                        self.logger.info(self.bot_name + ": waiting " + str(twait) + " seconds...")
                        time.sleep(twait)
                except:
                        self.logger.error("FAIL")

        except Exception as e:
            #print("liking routine failed")
            self.logger.error(e)
            return -5
        return len(links_done)"""

        

        
        
    """ 
    def obtainLinks(self, links_string):
        try:
            self.key = "links"
            # formating links
            links_raw = links_string.split("\n")
        
        
            # dump dump
            http_links = list()
            instagram_links = list()
            for link in links_raw:
                try:
                    if "https" in link:
                        http_links.append("https" + link.split("https")[1])
                    elif "instagram://user?username=" in link:
                        instagram_links.append("instagram://user?username=" + link.split("instagram://user?username=")[1])
                except:
                    pass
            
            # remove posts from list that already are liked
            already_links = self.readFile(self.key + "." + self.bot_name)
            
            # remove already liked links
            links = list()
            for link in http_links:
                try:
                    if link.split("p/")[1].split("/")[0] not in already_links:
                        links.append(link)
                except:
                    pass
        
            #links = [link for link in links if link.split("p/")[1].split("/")[0] not in already_links]
            self.links = links
            
            # instagram-links
            raw_links = list()
            for link in instagram_links:
                try:
                    if link.split("instagram://user?username=")[1] not in already_links:
                        raw_links.append(link)
        except:
            # obtaining links failed
            self.links = -2
    
    
    
    """
    
    def obtainSocialLinks(self, links_string):
        try:
            # formating links
            links_list = links_string.split("\n")
        
            # remove spaces and , at the end of the lines
            links_raw = list()
            for line in links_list:
                links_raw.append(line.rstrip(" ,"))
        
            # dump dump
            links = list()
            for link in links_raw:
                try:
                    if "instagram://user?username=" in link:
                        # check if line begins with instagram://user?username=
                        if line.startswith("instagram://user?username="):
                            links.append(link)
                        else:
                            # remove dump from beginning
                            links.append(link.split("instagram://user?username=")[1])
                except:
                    pass
            
            #links = [link for link in links if link.split("p/")[1].split("/")[0] not in already_links]
            self.social_links = links
        except:
            self.social_links = -2




    def obtainNormalLinks(self, links_string):
        try:
            self.key = "links"
            # formating links
            links_list = links_string.split("\n")
        
            # remove spaces and , at the end of the lines
            links_raw = list()
            for line in links_list:
                links_raw.append(line.rstrip(" ,"))
        
            # dump dump
            links = list()
            for link in links_raw:
                try:
                    if "https" in link:
                        # check if line begins with https
                        if line.startswith("https"):
                            links.append(link)
                        else:
                            # remove dump from beginning
                            links.append("https" + link.split("https")[1])
                except:
                    pass
            
            # remove posts from list that already are liked
            already_links = self.readFile(self.key + "." + self.bot_name)
            
            # remove already liked links
            links_raw = links.copy()
            links = list()
            for link in links_raw:
                try:
                    if link.split("p/")[1].split("/")[0] not in already_links:
                        links.append(link)
                except:
                    pass
        
            #links = [link for link in links if link.split("p/")[1].split("/")[0] not in already_links]
            self.links = links
        except:
            # obtaining links failed
            self.links = -2
      
        



if __name__ == "__main__":
    bot = bot4(False)
    bot.login("bottest371", "BotTestAccount1")

    datei= open("bot4/TEST1.links", "r", encoding="utf8").read()
    print(datei)
    print()
    print("wird zu")
    print()
    print(bot.links)
    bot.start(links_string=datei, wait=3)