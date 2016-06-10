from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import unittest


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        pass

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Stefan heard about a cool new online to-do app. He goes to check out its homepage
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # He types "Go to the store" into a text box
        inputbox.send_keys('Go to the store')

        # When he hits enter, he is taken to a new URL, and now the page lists
        # "1: Go to the store" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        stefan_list_url = self.browser.current_url
        self.assertRegex(stefan_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Go to the store')

        # There is still a text box inviting him to add another item. He enters "Buy apples"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy apples')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Go to the store')
        self.check_for_row_in_list_table('2: Buy apples')

        # Now a new user, Bob, comes along to the site

        # We use a new browser session to make sure that no information
        # of Stefan's is coming through from cookies, etc.

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Bob visits the home page.  There is no sign of Stefan's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Go the the store', page_text)
        self.assertNotIn('But apples', page_text)

        # Bob starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Bob gets his own unique URL
        bob_list_url = self.browser.current_url
        self.assertRegex(bob_list_url, '/lists/.+')
        self.assertNotEqual(bob_list_url, stefan_list_url)

        # Again, no trace of Stefan's list
        bob_page_text = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Go to the store', bob_page_text)
        self.assertNotIn('Buy apples', bob_page_text)
        self.assertIn('Buy milk', bob_page_text)
