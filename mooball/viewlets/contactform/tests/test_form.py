from Products.CMFCore.utils import getToolByName
from mooball.viewlets.contactform.form import ContactFormViewlet
from mooball.viewlets.contactform.testing import CONTACTFORM_INTEGRATION_TESTING
from plone.testing.z2 import Browser
import plone.app.z3cform.interfaces
import transaction
import unittest
import zope.component
import zope.interface


class TestContactFormViewletIntegration(unittest.TestCase):

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
        self.assertEquals(1, len(self.portal.MailHost.messages))


class TestContactFormViewlet(unittest.TestCase):

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


class TestContactFormViewlet(unittest.TestCase):

    layer = CONTACTFORM_INTEGRATION_TESTING

    def setUp(self):
        zope.interface.alsoProvides(self.layer['request'],
                                    plone.app.z3cform.interfaces.IPloneFormLayer)
        self.form = zope.component.getMultiAdapter(
            (self.layer['portal'], self.layer['request']), name='contactus.html')
        self.form.updateWidgets()

    def test_widgets_default(self):
        self.assertFalse(self.form.widgets['name'].title)

    def test_widgets_inline_titles(self):
        ptool = getToolByName(self.layer['portal'], 'portal_properties')
        ptool.contactform_properties.inline_titles = True
        self.form.updateWidgets()
        self.assertTrue(self.form.widgets['name'].title)
