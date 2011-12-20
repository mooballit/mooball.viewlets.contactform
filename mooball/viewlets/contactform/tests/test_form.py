from mooball.viewlets.contactform.form import ContactFormViewlet
from mooball.viewlets.contactform.testing import CONTACTFORM_INTEGRATION_TESTING
from plone.testing.z2 import Browser
import transaction
import unittest


class TestContactFormViewlet(unittest.TestCase):

    layer = CONTACTFORM_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal.manage_changeProperties(email_from_address='admin@mooball.net')
        transaction.commit()

        self.browser = Browser(self.layer['app'])
        self.browser.open(self.portal.absolute_url())

    def test_render(self):
        self.assertTrue(self.browser.getControl('Your Name'))

    def test_error_in_form(self):
        self.browser.getControl('Your Name').value = 'Roman'
        self.browser.getControl('Submit').click()
        self.assertTrue('Error' in self.browser.contents)

    def test_mailout(self):
        self.browser.getControl('Your Name').value = 'Roman'
        self.browser.getControl('Your Email').value = 'roman@mooball.com'
        self.browser.getControl('Your Message').value = 'Good stuff'
        self.browser.getControl('Submit').click()
        self.assertTrue('Thank you' in self.browser.contents)


class TestContactForm(unittest.TestCase):

    layer = CONTACTFORM_INTEGRATION_TESTING

    def test_has_email_from(self):
        viewlet = ContactFormViewlet(self.layer['portal'],
                                     self.layer['request'],
                                     None,
                                     None)
        self.assertFalse(viewlet.has_email_from())

        browser = Browser(self.layer['app'])
        browser.open(self.layer['portal'].absolute_url())
        self.assertRaises(LookupError, browser.getControl, 'Your Name')
