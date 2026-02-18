from django import template

register = template.Library()


@register.filter(name="dict_lookup")
def dict_lookup(value, key):
    """Return value[key] for dict-like or object.__getitem__ access."""
    if value is None:
        return ""
    try:
        return value.get(key, "")
    except AttributeError:
        try:
            return value[key]
        except Exception:
            return ""
