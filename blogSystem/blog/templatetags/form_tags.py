from django import template

register = template.Library()

@register.filter
def add_class(field, class_name):
    """
    Adds a CSS class to the given field widget.
    Usage:
    {{ form.field_name|add_class:"form-control" }}
    """
    return field.as_widget(attrs={'class': class_name})
