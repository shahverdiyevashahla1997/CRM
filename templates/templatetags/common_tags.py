from django import template

register = template.Library()

@register.filter
def get_fields(obj):
    """Return human-readable model fields and values for detail pages."""
    result = []
    for field in obj._meta.fields:
        value = field.value_from_object(obj)
        if field.is_relation and value is not None:
            try:
                value = getattr(obj, field.name)
            except (AttributeError, ValueError):
                pass
        if field.name == "document" and value:
            try:
                value = value.url
            except ValueError:
                value = "—"
        result.append((field.verbose_name.capitalize(), value))
    return result
