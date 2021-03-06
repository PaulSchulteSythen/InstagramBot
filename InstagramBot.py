# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 21:43:47 2020

@author: Paul Schulte
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import time
from datetime import datetime

import os


class InstagramBot:
    
    def __init__(self, minimize):
        # options for minimization
        firefox_options = Options()
        firefox_options.headless = minimize
        
        # load Firefox-driver
        self.driver = webdriver.Firefox(options=firefox_options)

        # check if config-file exists and get xpaths
        if self.get_xpaths() == -1:
            return -1
        
        # create posts-file if not existing yet
        try:
            # fails if already existing
            os.makedirs("posts/" + str(datetime.now().strftime('%m-%d-%Y')))
        except FileExistsError:
            # directory already exists
            pass
        
        # load instagram-page
        self.driver.get("https://instagram.com")
        
        # wait for loading
        time.sleep(2)
        
        
    def get_xpaths(self):
        # get xpaths from config file
        try:
            with open("config/xpaths.conf", "r") as file:
                for line in file:
                    xpath = line.split("{")[1].split("}")[0]
                    configuration = line.split("=")[0]
                    if configuration == "like_mainpage":
                        self.like_mainpage_xpath = xpath
                    elif configuration == "like":
                        self.like_xpath = xpath
                    elif configuration == "save":
                        self.save_xpath = xpath
                    elif configuration == "hashtag_amount":
                        self.hashtag_amount_xpath = xpath
        except: 
            # config/xpaths.conf not existing
            return -1
        
        
        # get all save and like xpaths
        try:
            self.like_xpaths = list()
            with open("config/like_xpaths.conf", "r") as file:
                for line in file:
                    if line.endswith("\n"):
                        self.like_xpaths.append(line[:-1])
                    else:
                        self.like_xpaths.append(line)
        except:
            # list of all xpaths for like-buttons
            pass
                    
        # get all save and save xpaths
        try:
            self.save_xpaths = list()
            with open("config/save_xpaths.conf", "r") as file:
                for line in file:
                    if line.endswith("\n"):
                        self.save_xpaths.append(line[:-1])
                    else:
                        self.save_xpaths.append(line)
        except:
            # list of all xpaths for like-buttons
            pass

        # get all save and likeMainpage xpaths
        try:
            self.like_mainpage_xpaths = list()
            with open("config/like_mainpage_xpaths.conf", "r") as file:
                for line in file:
                    if line.endswith("\n"):
                        self.save_xpaths.append(line[:-1])
                    else:
                        self.save_xpaths.append(line)
        except:
            # list of all xpaths for like-buttons
            pass
            
        
        
        
    def login(self, username, pw):
        # save username and password for inner class
        self.username = username
        self.pw = pw
        
        # login-process
        try:
            # locating input form and sending keys
            self.driver.find_element_by_xpath('//input[@name="username"]').send_keys(username)
            self.driver.find_element_by_xpath('//input[@name="password"]').send_keys(pw)
            time.sleep(3)
            
            # click login-button    
            self.driver.find_element_by_xpath('//button[@type="submit"]').click()
            time.sleep(4) # wait for load    
        except:
            #print("Login failed")
            return -1
        
        # ----------------------logged in successfully---------------------------
        
        # bypass popups
        # "Login-Informationen nicht behalten und Beitragsbenachrichtigungen ausschalten"
        popups_deleted = False
        while not popups_deleted:
            try:
            	try:
		            # check if loaded
		            self.driver.find_element_by_xpath(self.like_mainpage_xpath) # like button on main page
		            popups_deleted = True
            	except:
                	pass

            	try:
	                for xpath in like_mainpage_xpaths:
	                	self.driver.find_element_by_xpath(xpath)
            	except:
	            	pass

            except:
                pass
            
            try: # click on buttons
                self.driver.find_element_by_xpath('//button[contains(text(), "Jetzt nicht")]').click()
                time.sleep(4)
                self.driver.find_element_by_xpath('//button[contains(text(), "Jetzt nicht")]').click()
                time.sleep(4)
            except:
                # failed to bypass -> retry
                continue
            
        
        # successfully bypassed popups
        return 1
    
    
    def getHashtagPostLinks(self, hashtag, howMany):
        '''
        Returns
        -------
        -1 : failed to load hashtag / hashtag not available.
        -2 : error while finding links.
        posts : if successful.
        '''
        
        # load hashtag-page / check if it is available
        self.driver.get("https://www.instagram.com/explore/tags/" + hashtag)
        time.sleep(1) # wait for finish
        
        # check if hashtag exists
        try:
            self.driver.find_element_by_xpath('//h2[contains(text(), "Diese Seite ist leider nicht verfügbar")]')
            # page not available
            return -1
        except:
            # page available
            pass
        
        
        # get all the post-links
        try:
            # if all posts: get amount
            try:
                if howMany == -1:
                    howMany = int(self.driver.find_element_by_xpath(self.hashtag_amount_xpath).get_attribute("innerHTML"))      
            except:
                howMany = 10
              
            # create lists
            posts = list()
            last_appended = time.time() # for initialization
              
            # continue as long as not all posts found
            while len(posts) < howMany:
                # save posts in list
                href_found = self.driver.find_elements_by_tag_name("a")
                links = [element.get_attribute('href') for element in href_found if '.com/p' in element.get_attribute('href')]
                for element in links:
                    if not element in posts:
                        posts.append(element)
                        # count appended elements
                        last_appended = time.time()
                        
                # end reached? -> no more elements to append
                if time.time() - last_appended > 5.0:  # last appending was 5 seconds ago
                    return posts
                
                # scroll down
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.8)
        
            # return post-links
            return posts[:howMany]
        except:
            # finding links failed
            return -2 

    def getSocialLinks(self, account):
    	'''
        Returns
        -------
        -1 : failed to load page not available.
        -2 : error while finding links.
        posts : if successful.
        '''

    	# load page
    	self.driver.get("https://www.instagram.com/" + account)

    	# check if page exists
    	try:
            self.driver.find_element_by_xpath('//h2[contains(text(), "Diese Seite ist leider nicht verfügbar")]')
            # page not available
            return -1
    	except:
            # page available
            pass


    	try:
        	href_found = self.driver.find_elements_by_tag_name("a")
        	links = [element.get_attribute('href') for element in href_found if '.com/p' in element.get_attribute('href')]
        	return links[0]
    	except:
        	return -2



        
    def getTaggingLinks(self, account, howMany):
        '''
        Returns
        -------
        -1 : failed to load page not available.
        -2 : error while finding links.
        posts : if successful.
        '''
        
        # load tagged page
        self.driver.get("https://www.instagram.com/" + account + "/tagged/")
        
        # check if page exists
        try:
            self.driver.find_element_by_xpath('//h2[contains(text(), "Diese Seite ist leider nicht verfügbar")]')
            # page not available
            return -1
        except:
            # page available
            pass
        
        
        # get all the post-links
        try:
            # create lists
            posts = list()
            last_appended = time.time() # for initialization
            
            # continue as long as not all posts found
            while True:
                # save posts in list
                href_found = self.driver.find_elements_by_tag_name("a")
                links = [element.get_attribute('href') for element in href_found if '.com/p' in element.get_attribute('href')]
                for element in links:
                    if not element in posts:
                        posts.append(element)
                        # count appended elements
                        last_appended = time.time()
                        
                # enough items
                if len(posts) > howMany and howMany != -1:
                    break
                
                # no more loading -> also end reached
                if time.time() - last_appended > 5.0:  # last appending was 5 seconds ago
                    howMany = len(posts)
                    break
                
                # scroll down
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.8)
        
            # return post-links
            return posts[:howMany]
        except:
            # finding links failed
            return -2 
        
        
    # MECHANIC FUNCTIONS------------------------------------------------------------------------------------------------------------
    
    def likePost(self, link, loaded=False):
        '''
        Parameters
        ----------
        link : link of the post that will be liked.
        loaded : if page ist already loaded

        Returns
        -------
        -1 if failed, 1 when successfull.
        '''

        try:
            # get page if not already done
            if not loaded:
                self.driver.get(link)
                time.sleep(1) 
                
            #check if post is already liked      
            if not "#ed4956" in self.driver.find_element_by_xpath(self.like_xpath).get_attribute("innerHTML"):
                like = self.driver.find_element_by_xpath(self.like_xpath)
                like.click()
            else:
                print("post already liked")
        except:
            # backup xpaths if normal xpath is not working
            for xpath in self.like_xpaths:
                try:
                    #check if post is already liked     
                    if not "#ed4956" in self.driver.find_element_by_xpath(xpath).get_attribute("innerHTML"):
                        like = self.driver.find_element_by_xpath(xpath)
                        like.click()                    
                    else:
                        print("post already liked")
                    return 1 # successful
                except:
                    pass
            return -1
        return 1
    
    def savePost(self, link, loaded=False):
        '''
        Parameters
        ----------
        link : link of the post that will be saved.
        loaded : if page ist already loaded

        Returns
        -------
        -1 if failed, 
         1 when successfull.
        '''

        try:
            # check if site already is loaded
            if not loaded:
                self.driver.get(link)
                time.sleep(1) 
                
            # check if post is already saved     
            if not "Entfernen" in self.driver.find_element_by_xpath(self.save_xpath).get_attribute("innerHTML"):
                save = self.driver.find_element_by_xpath(self.save_xpath)
                save.click()                    
            else:
                print("post already saved")
        except:
            # backup xpaths if normal xpath is not working
            for xpath in self.save_xpaths:
                try:
                    #check if post is already saved     
                    if not "Entfernen" in self.driver.find_element_by_xpath(xpath).get_attribute("innerHTML"):
                        save = self.driver.find_element_by_xpath(xpath)
                        save.click()                    
                    else:
                        print("post already saved")
                    return 1 # successful
                except:
                    pass
            return -1
        return 1
    
    def likeAndSavePost(self, link):
        """
        Parameters
        ----------
        link : post link.

        Returns
        -------
        1 : successful.
        -1 : failed

        """
        try:
            # get/open page
            self.driver.get(link)
            time.sleep(1)
            
            #check if post is already liked
            if self.likePost(link, loaded=True) == -1:
                return -1
            #check if post is already saved
            if self.savePost(link, loaded=True) == -1:
                return -1
        except BaseException as e:
            #print(e)
            return -1
        return 1
    
    
    
    #---------------------file handle-----------------------------------
    
    def saveFile(self, filename, links):
        # given links to write into file
        already_links = self.readFile(filename)
        
        # get date for folder to save file in
        current_time = datetime.now()
        time = current_time.strftime('%m-%d-%Y')
        
        # append all links to file and close it
        with open("posts/" + str(time) + "/" + filename, "a+") as file:
            for link in links:
                link = str(link.split("p/")[1].split("/")[0])
                if link not in already_links:
                    file.write(link + ",\n")
            file.close()
            
    
    def readFile(self, filename):
        # get folder to read from by date
        current_time = datetime.now()
        time = current_time.strftime('%m-%d-%Y')
        
        # read all links from file and return them
        try:
            with open("posts/" + str(time) + "/" + filename, "r") as file:
                links = file.readlines()
                for index, link in enumerate(links):
                    links[index] = link[:-2]
                file.close()
                return links
        except:
            # file not found
            return[]
         
#Main-------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    bot = InstagramBot(minimize=False)
    bot.login("bottest371", "BotTestAccount1")
    links = bot.getTaggingLinks("instagram", 10)
    print(links)
    for link in links:
        print(bot.likeAndSavePost(link))
    #bot.saveFile("test2.bot2", links)
    #print(bot.readFile("test2.bot2"))
    #if bot != -1:
    #    links = bot.getHashtagPostLinks("blacklivesmatter", 30)
    #    bot.likeAndSavePost(links[0])
    #if bot.postStory("C:\\Users\\Anwender\\Pictures\\Saved Pictures\\quad_damage-1920x1200.jpg") == 1:
    #    print("successfull")
    
    #postLinks = bot.getHashtagPostLinks("blacklivesmatter", 30)
    #postLinks = bot.getTaggingLinks("montanablack")
    #print(len(postLinks))
    #print(postLinks[0])
    #bot.likeAndSavePost(postLinks[0])


















