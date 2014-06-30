## Repository exists for reference and is really not intended for use.

* The code probably will not work (define 'working'). The last commit was pushed due to a server panic, so I was commiting unfinished changes to all repos regardless of code state. If you want a 'working' version, refer to commit 34a8b5c935, the original snippet, or Ramusus's updated gist (links below).
* The original snippet is for django 1.1. Forms/Formsets have changed a lot since then, so I'm not sure if this code would even be compatible with modern versions of Django. This snippet was also created before django introduced generic relations.
* I think this project is an incorrect solution, along the lines of dajaxice. It solved a specific problem at a certain time, but there are probably more correct solutions.

#### What should you use/do?

* Not use this snippet. It only handles the admin case, and it would be ideal to have a solution that handles ModelForms generally. And again, this snippet is extremetly outdated.
* Use generic relations. This functionality is built into Django, however lacks a solution for the one:one case. You can only embed sets, ie, books with tags, not people with a named address.
* Use [django rest framework](http://www.django-rest-framework.org/). DRF can work as a replacement for Django's forms. It supports the concept of nested resources, however I'm unsure if this extends to object creation. Even if nested object creation works, the admin panel would be unsupported.
* Use [django-formfield](https://github.com/jsoa/django-formfield). It effectively embeds a standard form into a model, which provides some notion of hierarchy, but it's just a wrapper around a JSONField.
    * Rendering is meh, as it just coerces form rendering into a list. It doesn't allow for custom form rendering.
    * This does not create support for relations between models - it's just a form backed by a JSONField which is really a PickleField. 
* Wait or pretend your use case doesn't exist.

#### wow, such advice, many helpful 

The problem is that embedded/nested models and forms don't fit within the normal ModelForm use case. ModelForms are meant to handle single objects, not multiple hierarchical objects. I have yet to find a comprehensive forms solution for embedded ModelForms. The only way to currently handle this is by composing the forms in views. 

Since there's no package that solves this, the only solution is to write it yourself or wait for someone else to do so. I'm currently trying to create a possible solution, but it's a fairly difficult problem, so don't count on that.

django-reverse-admin
====================

Django package for handling 'embedded' models in the admin pages


## Credits


This module was originally developed by bjourne for Django 1.1.1 and can be found on [djangosnippets](http://djangosnippets.org/snippets/2032/).

Project updated by [ramusus](https://github.com/ramusus). Updated code can be found on [gist](https://gist.github.com/ramusus/4343464).


## Original Documentation

Module that makes django admin handle OneToOneFields in a better way.
 
A common use case for one-to-one relationships is to "embed" a model
inside another one. For example, a Person may have multiple foreign
keys pointing to an Address entity, one home address, one business
address and so on. Django admin displays those relations using select
boxes, letting the user choose which address entity to connect to a
person. A more natural way to handle the relationship is using
inlines. However, since the foreign key is placed on the owning
entity, django admins standard inline classes can't be used. Which is
why I created this module that implements "reverse inlines" for this
use case.
 
Example:
 
    from django.db import models
    class Address(models.Model):
        street = models.CharField(max_length = 255)
        zipcode = models.CharField(max_length = 10)
        city = models.CharField(max_length = 255)
    class Person(models.Model):
        name = models.CharField(max_length = 255)
        business_addr = models.ForeignKey(Address,
                                             related_name = 'business_addr')
        home_addr = models.OneToOneField(Address, related_name = 'home_addr')
        other_addr = models.OneToOneField(Address, related_name = 'other_addr')
 
This is how standard django admin renders it:
 
    http://img9.imageshack.us/i/beforetz.png/
 
Here is how it looks when using the reverseadmin module:
 
    http://img408.imageshack.us/i/afterw.png/
 
You use reverseadmin in the following way:
 
    from django.contrib import admin
    from django.db import models
    from models import Person
    from reverseadmin import ReverseModelAdmin
    class AddressForm(models.Form):
        pass
    class PersonAdmin(ReverseModelAdmin):
        inline_type = 'tabular'
        inline_reverse = ('business_addr', ('home_addr', AddressForm), ('other_addr' (
            'form': OtherForm
            'exclude': ()
        )))
    admin.site.register(Person, PersonAdmin)
 
inline_type can be either "tabular" or "stacked" for tabular and
stacked inlines respectively.
 
The module is designed to work with Django 1.1.1. Since it hooks into
the internals of the admin package, it may not work with later Django
versions.
