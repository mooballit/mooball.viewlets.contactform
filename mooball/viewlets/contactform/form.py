# coding=utf-8
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from five import grok
import plone.app.layout.viewlets.interfaces
import plone.directives.form
import z3c.form.button
import z3c.form.field
import zope.interface


class ContactFormViewlet(grok.Viewlet):
    grok.name('mooball.contact_form')
    grok.context(zope.interface.Interface)
    grok.viewletmanager(plone.app.layout.viewlets.interfaces.IPortalFooter)

    def update(self):
        self.form = ContactForm(aq_inner(self.context), self.request)
        self.form.update()

    def has_email_from(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        return bool(portal.email_from_address)


class IContactForm(plone.directives.form.Schema):

    name = zope.schema.TextLine(
        title=u'Your Name'
    )

    email = zope.schema.TextLine(
        title=u'Your Email'
    )

    msg = zope.schema.Text(
        title=u'Your Message'
    )


class ContactForm(plone.directives.form.Form):
    description = u'Note: ■ are required fields.'
    grok.name('contactus.html')
    grok.require('zope2.View')
    grok.context(zope.interface.Interface)
    fields = z3c.form.field.Fields(IContactForm)
    ignoreContext = True
    plone.directives.form.wrap(False)

    @z3c.form.button.buttonAndHandler(u'Submit', name='submit')
    def submit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.nextURL()

    def nextURL(self):
        IStatusMessage(self.request).addStatusMessage(
            u'Thank you for your enquiry', 'info'
        )
        self.request.response.redirect(self.context.absolute_url())
