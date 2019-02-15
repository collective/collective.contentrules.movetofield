# -*- coding: utf-8 -*-
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from zope.schema import Choice
from zope.schema import List
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def get_fields(portal_type):
    """List all fields from portal_type and behaviors
    https://stackoverflow.com/q/12178669/2116850
    """
    fti = getUtility(IDexterityFTI, name=portal_type)
    schema = fti.lookupSchema()
    fields = schema.names()
    for bname in fti.behaviors:
        factory = getUtility(IBehavior, bname)
        behavior = factory.interface
        fields += behavior.names()
    return [(schema.get(field).title, field,) for field in fields if
            type(schema.get(field)) in [RelationChoice,
                                        RelationList,
                                        Choice,
                                        List]]


def relationfields(context):
    """Vocabulary factory for relationfields in content types."""
    factory = getUtility(
        IVocabularyFactory, 'plone.app.vocabularies.ReallyUserFriendlyTypes')
    vocabulary = factory(None)
    fields = []
    for term in vocabulary:
        portal_type = term.value
        try:
            fields += get_fields(portal_type)
        except ComponentLookupError:
            pass
    return SimpleVocabulary(
        [SimpleTerm(title='Select...', value=None)] +
        [SimpleTerm(title=field[0], value=field[1]) for field in set(fields)
    ])
