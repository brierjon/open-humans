import sys


class InvalidString(str):
    """
    Raise an exception if an invalid template string is encountered.
    """

    allowed_undefined_variables = [
        'css_classes.label',
        'css_classes.wrap',
        'form.email.value',
        'form.name.value',
        'form.password.value',
        'form.password_confirm.value',
        'form.username.value',
        'form_submit_value',
        'panel_offset',
        'panel_width',
        'source.href_next',
        'user_data.href_next',
    ]

    def __mod__(self, other):
        if other.var in self.allowed_undefined_variables:
            return super(InvalidString, self).__mod__(other)

        from django.template.base import TemplateSyntaxError

        raise TemplateSyntaxError(
            'Undefined variable or unknown value for "{}"'.format(other))


def has_migration(app, migration):
    if 'migrate' in sys.argv:
        return False

    if 'test' not in sys.argv:
        return True

    from django.db.migrations.recorder import MigrationRecorder

    try:
        MigrationRecorder.Migration.objects.get(app=app, name=migration)
    except MigrationRecorder.Migration.DoesNotExist:
        return False

    return True
