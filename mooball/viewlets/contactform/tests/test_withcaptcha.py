# Copyright (c) 2012 Mooball IT
# See also LICENSE.txt
from Products.CMFCore.utils import getToolByName
from mooball.viewlets.contactform.testing import CONTACTFORM_INTEGRATION_TESTING
from plone.testing.z2 import Browser
import transaction
import unittest


class TestContactFormViewletIntegration(unittest.TestCase):

    layer = CONTACTFORM_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal.manage_changeProperties(email_from_address='admin@mooball.net')
        ptool = getToolByName(self.layer['portal'], 'portal_properties')
        if not ptool.contactform_properties.hasProperty('show_captcha'):
            ptool.contactform_properties._setProperty('show_captcha',
                                                      True,
                                                      type='boolean')
        transaction.commit()

    def test_captcha_prevents_send(self):
        browser = Browser(self.layer['app'])
        browser.handleErrors = False
        browser.open(self.portal.absolute_url())
        browser.getControl('Your Name').value = 'Roman'
        browser.getControl('Your Email').value = 'roman@mooball.com'
        browser.getControl('Your Message').value = 'Good stuff'
        browser.getControl('Captcha').value = 'ignored'
        browser.getControl('Submit').click()
        self.assertTrue('There were some errors' in browser.contents)
        self.assertTrue('The code you entered was wrong' in
                        browser.contents)
