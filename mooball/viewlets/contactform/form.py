# coding=utf-8
import logging
import email
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from five import grok
import plone.app.layout.viewlets.interfaces
import plone.directives.form
import z3c.form.button
import z3c.form.field
import zope.interface


class IContactFormViewletLayer(zope.interface.Interface):
    """ Viewlet only browserlayer."""


class ContactFormViewlet(grok.Viewlet):
    grok.name('mooball.contact_form')
    grok.context(zope.interface.Interface)
    grok.viewletmanager(plone.app.layout.viewlets.interfaces.IPortalFooter)
    grok.layer(IContactFormViewletLayer)

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
    grok.layer(IContactFormViewletLayer)
    fields = z3c.form.field.Fields(IContactForm)
    ignoreContext = True
    plone.directives.form.wrap(False)

    def updateWidgets(self):
        super(ContactForm, self).updateWidgets()
        ptool = getToolByName(self.context, 'portal_properties')
        use_inline_titles = ptool.contactform_properties.getProperty(
            'inline_titles')
        if use_inline_titles:
            for key in self.widgets:
                w = self.widgets[key]
                w.klass += ' inputLabel'
                w.title = w.field.title

    @z3c.form.button.buttonAndHandler(u'Submit', name='submit')
    def submit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.prepare_and_send(data)
        self.nextURL()

    def nextURL(self):
        IStatusMessage(self.request).addStatusMessage(
            u'Thank you for your enquiry', 'info'
        )
        self.request.response.redirect(self.context.absolute_url())

    def prepare_and_send(self, data):
        """ Sends an e-mail to the administrator."""
        mailhost = getToolByName(self.context, 'MailHost')
        portal = getToolByName(self.context,
                               'portal_url').getPortalObject()
        encoding = portal.getProperty('email_charset')
        subject = u'Feedback from {0}'.format(portal.Title())
        to_address = portal.getProperty('email_from_address')
        envelope_from = '{0} <{1}>'.format(data['name'], data['email'])

        mail = email.MIMEMultipart.MIMEMultipart()
        mail_template = self.context.restrictedTraverse('feedbackmail')
        mail_template = mail_template(self.context, **data)
        mail.attach(email.MIMEText.MIMEText(
            mail_template.encode(encoding), 'html', encoding))

        self.log(to_address, envelope_from, subject, data)
        mailhost.send(mail, to_address, envelope_from,
                      subject=subject, charset=encoding)

    def log(self, send_to_address, envelope_from, subject, data):
        logger = logging.getLogger('mooball.viewlets.contactform')
        msg = 'Sending email {0} from {1} - "{2}": {3}'.format(
            send_to_address, envelope_from, subject, data)
        logger.info(msg)
