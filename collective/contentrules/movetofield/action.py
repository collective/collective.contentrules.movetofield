# -*- coding:utf-8 -*-
from logging import getLogger

from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import UnrestrictedUser
from OFS.SimpleItem import SimpleItem
from Products.CMFPlone import utils
from Products.statusmessages.interfaces import IStatusMessage
from collective.contentrules.movetofield import MoveToFieldMessageFactory as _
from collective.contentrules.movetofield.interfaces import IMoveToFieldAction
from plone import api
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.app.uuid.utils import uuidToObject
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from zope.component import adapts
from zope.formlib import form
from zope.interface import Interface
from zope.interface import implements

logger = getLogger('collective.contentrules.movetofield')


class MoveToFieldAction(SimpleItem):
    """The actual persistent implementation of the action element.
    """
    implements(IMoveToFieldAction, IRuleElementData)

    field = ''
    bypasspermissions = False
    element = "collective.contentrules.movetofield.ApplyMoveToField"

    @property
    def summary(self):
        return _(u"Move content to ${field}",
                 mapping=dict(field=self.field))


class MoveToFieldActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IMoveToFieldAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.request = getattr(self.context, 'REQUEST', None)
        self.event = event

    def __call__(self):
        obj = self.event.object
        field = getattr(self.element, 'field', False)
        bypasspermissions = getattr(self.element, 'bypasspermissions', False)
        value = None
        if field:
            value = getattr(obj, field, False)
            if not value:
                return False

        # It is possible that the value is a list. In this case, we move it
        # to the first matching item.
        if type(value) == list and len(value) > 0:
            value = value[0]

        target = None
        if type(value) == str:
            target = uuidToObject(value)
        elif hasattr(value, 'to_object'):
            target = value.to_object

        sm = getSecurityManager()
        portal = api.portal.get()
        try:
            try:
                if bypasspermissions is True:
                    tmp_user = UnrestrictedUser(sm.getUser().getId(),
                                                '',
                                                ['Copy or Move'],
                                                '')
                    tmp_user = tmp_user.__of__(portal.acl_users)
                    newSecurityManager(self.request, tmp_user)
                api.content.move(source=obj, target=target)
            except Exception as e:
                # TODO: Handle exceptions more elegantly
                self.error(obj, e)
                return False
        finally:
            if bypasspermissions is True:
                setSecurityManager(sm)
        return True

    def error(self, obj, error):

        title = utils.pretty_title_or_id(obj, obj)
        message = _(u"Unable to apply local roles on %s: %s" % (title, error))
        logger.error(message)
        if self.request is not None:
            IStatusMessage(self.request).addStatusMessage(message, type="error")


class MoveToFieldAddForm(AddForm):
    """An add form for local roles action.
    """
    form_fields = form.FormFields(IMoveToFieldAction)
    label = _(u"Add a Move to Field Action")
    description = _(u"An action that moves content to a folder defined by a "
                    u"field.")
    schema = IMoveToFieldAction

    def create(self, data):
        a = MoveToFieldAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class MoveToFieldEditForm(EditForm):
    """An edit form for local roles action.
    """
    form_fields = form.FormFields(IMoveToFieldAction)
    label = _(u"Edit a Move to Field Action")
    description = _(u"An action that moves content to a folder defined by a "
                    u"field.")
    schema = IMoveToFieldAction
