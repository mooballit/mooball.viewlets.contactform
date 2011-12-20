import unittest
from mooball.viewlets.contactform.testing import CONTACTFORM_FUNCTIONAL_TESTING
from plone.testing.z2 import Browser


class TestContactFormViewlet(unittest.TestCase):

    layer = CONTACTFORM_FUNCTIONAL_TESTING

    def test_render(self):
        portal = self.layer['portal']
        browser = Browser(self.layer['app'])
        browser.handleErrors = False
        browser.open(portal.absolute_url())
        self.assertTrue(browser.getControl('Your Name'))
