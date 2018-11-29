# -*- coding:utf-8 -*-
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from Products.CMFPlone import utils
from Products.statusmessages.interfaces import IStatusMessage
from collective.contentrules.movetofield import MoveToFieldMessageFactory as _
from collective.contentrules.movetofield.interfaces import IMoveToFieldAction
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements
from zope.interface import Interface


class MoveToFieldAction(SimpleItem):
    """The actual persistent implementation of the action element.
    """
    implements(IMoveToFieldAction, IRuleElementData)

    field = ''
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
        self.event = event

    def __call__(self):
        obj = self.event.object


        field = getattr(self.element, 'field', False)
        if field:
            value = getattr(obj, field, False)
            if not value:
                return False

        # TODO: Can we handle this more elegantly?
        try:
            api.content.move(source=obj, taget=value.to_object)
        except Exception as e:
            self.error(obj, e)
            return False

        return True

    def error(self, obj, error):
        request = getattr(self.context, 'REQUEST', None)
        if request is not None:
            title = utils.pretty_title_or_id(obj, obj)
            message = _(u"Unable to apply local roles on ${name}: ${error}",
                        mapping={'name': title, 'error': error})
            IStatusMessage(request).addStatusMessage(message, type="error")


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
