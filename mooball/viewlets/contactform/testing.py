from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from zope.configuration import xmlconfig
import mooball.viewlets.contactform


class ContactFormTestBase(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file('configure.zcml', mooball.viewlets.contactform,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'mooball.viewlets.contactform:default')


CONTACTFORM_FIXTURE = ContactFormTestBase()
CONTACTFORM_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CONTACTFORM_FIXTURE,),
    name="ContactForm:Integration")
CONTACTFORM_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CONTACTFORM_FIXTURE,),
    name="ContactForm:Functional")
