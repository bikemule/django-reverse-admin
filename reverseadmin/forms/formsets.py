
from django.forms.models import BaseModelFormSet, modelformset_factory
from django.forms import ModelForm


class ReverseInlineFormSet(BaseModelFormSet):
    '''
    A formset with either a single object or a single empty
    form. Since the formset is used to render a required OneToOne
    relation, the forms must not be empty.
    '''
    model = None
    parent_fk_name = ''

    def __init__(self,
                 data=None,
                 files=None,
                 instance=None,
                 prefix=None,
                 queryset=None,
                 save_as_new=False):
        object = getattr(instance, self.parent_fk_name)
        if object:
            qs = self.model.objects.filter(pk=object.id)
        else:
            qs = self.model.objects.filter(pk=-1)
            self.extra = 1
        super(ReverseInlineFormSet, self).__init__(data, files,
                                                   prefix=prefix,
                                                   queryset=qs)
        for form in self.forms:
            form.empty_permitted = False


def reverse_inlineformset_factory(parent_model,
                                  model,
                                  parent_fk_name,
                                  form=ModelForm,
                                  fields=None,
                                  exclude=None,
                                  formfield_callback=lambda f: f.formfield()):
    kwargs = {
        'form': form,
        'formfield_callback': formfield_callback,
        'formset': ReverseInlineFormSet,
        'extra': 0,
        'can_delete': False,
        'can_order': False,
        'fields': fields,
        'exclude': exclude,
        'max_num': 1,
    }
    FormSet = modelformset_factory(model, **kwargs)
    FormSet.parent_fk_name = parent_fk_name
    return FormSet
