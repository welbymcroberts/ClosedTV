from django import template

register = template.Library()



from django.template.defaultfilters import stringfilter

@stringfilter
def tchar(value, arg):
    return value[0:int(arg)]


register.filter('tchar', tchar)
