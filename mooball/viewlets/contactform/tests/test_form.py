import unittest
from mooball.viewlets.contactform.testing import CONTACTFORM_INTEGRATION_TESTING
from plone.testing.z2 import Browser


class TestContactFormViewlet(unittest.TestCase):

    layer = CONTACTFORM_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser(self.layer['app'])
        self.browser.open(self.portal.absolute_url())

    def test_render(self):
        self.assertTrue(self.browser.getControl('Your Name'))

    def test_error_in_form(self):
        self.browser.getControl('Your Name').value = 'Roman'
        self.browser.getControl('Submit').click()
        self.assertTrue('Error' in self.browser.contents)
