Introduction
============

This package adds a new rule type to Plone content rules system
which moves content to a field defined in the content.

First, add collective.contentrules.movetofield package to the
'eggs' parameter of your buildout, or in the dependencies of your policy product,
and restart your buildout.

Usage
-----

 - Add a relationfield to your content type, or enable the IRelationField
   behavior.
 - Add a new content rule and select the 'Move to Field' action.
 - Select the field from the dropdown.


Compatibility
-------------

    Plone 4.3.x and above (http://plone.org/products/plone)
    Plone 5.x and above
