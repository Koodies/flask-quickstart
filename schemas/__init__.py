from marshmallow import pre_dump, pre_load
import typing


# feel free to extend it
class DefaultFormatting():
	@pre_load(pass_many=False)
	def _strip_whitespace(self, value, **kwargs):
		if isinstance(value, str):
			value = value.strip()
		elif isinstance(value, typing.Mapping):
			return {k: self._strip_whitespace(value[k]) for k in value}
		elif isinstance(value, (list, tuple)):
			return type(value)(map(self._strip_whitespace, value))
		return value
