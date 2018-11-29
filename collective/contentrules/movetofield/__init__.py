from zope.i18nmessageid import MessageFactory


MoveToFieldMessageFactory = \
    MessageFactory('collective.contentrules.movetofield')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
