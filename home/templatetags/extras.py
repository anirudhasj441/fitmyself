from django import template

register = template.Library()

@register.filter(name="addstr")
def addstr(str1,str2):
    print(str(str1)+str(str2))
    return str(str1)+str(str2)