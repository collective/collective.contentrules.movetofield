from collective.contentrules.movetofield import MoveToFieldMessageFactory as _
from zope import schema
from zope.interface import Interface


class IMoveToFieldAction(Interface):

    field = schema.Choice(
        title=_(u"Field"),
        description=_(u"Pick a field which contains the location you wish to"
                      u"move the object to."),
        required=True,
        vocabulary=u'collective.contentrules.movetofield.relationfields',)

    bypasspermissions = schema.Bool(
        title=_(u"Bypass User Permissions"),
        description=_(u"When selected, permissions will be bypassed and the "
                      u"object will be moved regardless of whether or not the"
                      u"user has permission to move it."),
        default=False,
        required=False
    )
