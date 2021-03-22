from django import template

register = template.Library()

@register.filter(name="addstr")
def addstr(str1,str2):
    print(str(str1)+str(str2))
    return str(str1)+str(str2)

@register.filter(name="value")
def value(dict,key):
    try:
        return dict[key].display_picture
    except AttributeError:
        return dict[key]

