from django import template

register = template.Library()


@register.filter
def split_by(value: str, delimiter: str = ","):
	if not value:
		return []
	return [part.strip() for part in value.split(delimiter) if part.strip()]


