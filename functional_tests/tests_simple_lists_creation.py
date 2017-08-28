from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user_and_retrieve_it_later(self):
        # Aiden heard about a new to-do app. 
        # He visits it's homepage
        self.browser.get(self.live_server_url)

        # he notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to to enter a to-do item straight-away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types 'Buy Watch Dogs 2 disk' into a textbox
        inputbox.send_keys('Buy Watch Dogs 2 disk')

        # When he hits enter, page updates, and now page lists:
        # '1: Buy Watch Dogs 2 disk' in the to-do table
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_the_list_table('1: Buy Watch Dogs 2 disk')

        # There is still a text body inviting him to enter a to-do item
        # and he enters 'Play Watch Dogs 2'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Play Watch Dogs 2')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now it shows both items on the list
        self.wait_for_row_in_the_list_table('1: Buy Watch Dogs 2 disk')
        self.wait_for_row_in_the_list_table('2: Play Watch Dogs 2')

        # Aiden wonders whether site will remember the list. then he sees
        # that site generated a unique URL for him -- there is some 
        # self-explanatory text to that effect.
        

        # He visits URL and list is still there.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Aiden starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy Watch Dogs 2 disk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_the_list_table('1: Buy Watch Dogs 2 disk')

        # he notices that his list has a unique url
        aiden_list_url = self.browser.current_url
        self.assertRegex(aiden_list_url, '/lists/.+')

        # Now a new user, Batman, comes along to the site

        ## We use a new browser session to make sure that no information
        ## of Aiden is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Batman visits the home page. There is nosign of Aiden's list

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Watch Dogs 2 disk', page_text)
        self.assertNotIn('Play Watch Dogs 2', page_text)

        # Batman starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_the_list_table('1: Buy milk')
        
        # Batman gets his own unique URL
        batman_list_url = self.browser.current_url
        self.assertRegex(batman_list_url, '/lists/.+')
        self.assertNotEqual(batman_list_url, aiden_list_url)

        # Again, there is no trace of Aiden's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Watch Dogs 2 disk', page_text)
        self.assertIn('Buy milk', page_text)
        # Satisfied, they both go to sleep
