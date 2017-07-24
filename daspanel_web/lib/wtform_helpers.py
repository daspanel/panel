from wtforms import (SelectField)

__all__ = ['NoPreValidationSelectField']

# https://stackoverflow.com/questions/39395125/wtforms-selectmultiplefield-disable-validation
class NoPreValidationSelectField(SelectField):
    def pre_validate(self, form):
        """per_validation is disabled"""
        return True
