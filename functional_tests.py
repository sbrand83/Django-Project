from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Stefan heard about a cool new online to-do app. He goes to check out its homepage
		self.browser.get('http://localhost:8000')

		# He notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the test!')

		# He is invited to enter a to-do item right away

		# He types "Go to the store" into a text box

		# When he hits enter, the page updates, and now the page lists "1: Go to the store" as an item in a to-do list

		# There is still a text box inviting him to add another item. He enters "Buy apples"

		# The page updates again, and now shows both items on her list

		# The site has generated a unique URL for him

		# He visits that URL - the to-do list is still there

		#The end

if __name__ == '__main__':
	unittest.main(warnings='ignore')
