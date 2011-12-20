from plone.app.testing import PLONE_FIXTURE
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from zope.configuration import xmlconfig
import Acquisition
import mooball.viewlets.contactform
import zope.component


def debug_contents(contents):
    with open('/tmp/debug.html', 'w') as f:
        f.write(contents)


class ContactFormTestBase(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file('configure.zcml', mooball.viewlets.contactform,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'mooball.viewlets.contactform:default')

        # Set up a mock mailhost
        portal._original_MailHost = portal.MailHost
        portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = zope.component.getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

    def tearDownPloneSite(self, portal):
        portal.MailHost = portal._original_MailHost
        sm = zope.component.getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(
            Acquisition.aq_base(portal._original_MailHost),
            provided=IMailHost)


CONTACTFORM_FIXTURE = ContactFormTestBase()
CONTACTFORM_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CONTACTFORM_FIXTURE,),
    name="ContactForm:Integration")
CONTACTFORM_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CONTACTFORM_FIXTURE,),
    name="ContactForm:Functional")
