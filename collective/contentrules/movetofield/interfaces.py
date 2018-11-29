from collective.contentrules.movetofield import MoveToFieldMessageFactory as _
from zope import schema
from zope.interface import Interface


class IMoveToFieldAction(Interface):

    field = schema.Choice(
        title=_(u"Field"),
        description=_(u"Pick a field which contains the location you wish to"
                      u"move the object to."),
        required=True,
        vocabulary=u'collective.contentrules.movetofield.relationfields ',)
