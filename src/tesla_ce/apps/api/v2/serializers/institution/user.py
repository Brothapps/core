#  Copyright (c) 2020 Xavier Baró
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""User api serialize module."""
from django.contrib.auth.models import make_password

from rest_framework import serializers
from rest_framework import validators

from tesla_ce.models import InstitutionUser
from tesla_ce.models import User


class InstitutionUserSerializer(serializers.ModelSerializer):
    """Institution User serialize model module."""

    username = serializers.CharField(allow_null=False,
                                     allow_blank=False,
                                     validators=[
                                         validators.UniqueValidator(queryset=User.objects.all())
                                     ]
                                     )
    password = serializers.CharField(write_only=True, default=None, allow_null=True)
    password2 = serializers.CharField(write_only=True, default=None, allow_null=True)
    last_login = serializers.DateTimeField(read_only=True)
    first_name = serializers.CharField(required=False, default=None)
    last_name = serializers.CharField(required=False, default=None)
    uid = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    email = serializers.EmailField(required=False, default=None,
                                   validators=[
                                       validators.UniqueValidator(queryset=User.objects.all())
                                   ]
                                   )
    institution_id = serializers.HiddenField(default=None)
    login_allowed = serializers.BooleanField(required=False, allow_null=True, default=False, write_only=True)
    inst_admin = serializers.BooleanField(required=False, allow_null=False, default=False)
    legal_admin = serializers.BooleanField(required=False, allow_null=False, default=False)
    send_admin = serializers.BooleanField(required=False, allow_null=False, default=False)
    data_admin = serializers.BooleanField(required=False, allow_null=False, default=False)

    class Meta:
        model = InstitutionUser
        exclude = ["is_superuser", "is_staff", "is_active", "date_joined", "groups",
                   "user_permissions", "institution"]
        validators = [serializers.UniqueTogetherValidator(
            queryset=InstitutionUser.objects.all(),
            fields=['institution_id', 'uid']
        ), ]

    def validate(self, attrs):
        """
            Validate the given attributes
            :param attrs: Attributes parsed from request
            :type attrs: dict
            :return: Validated attributes
            :rtype: dict
        """
        # Add predefined fields
        attrs['institution_id'] = self.context['view'].kwargs['parent_lookup_institution_id']

        # Check passwords
        if attrs.get('login_allowed', True):
            if 'password' in attrs and attrs.get('password') != attrs.get('password2'):
                raise serializers.ValidationError('Passwords does not match')
            if 'password2' in attrs:
                del attrs['password2']
            if 'password' in attrs:
                attrs['password'] = make_password(attrs['password'])
        else:
            attrs['login_allowed'] = False

        # Apply validators
        for validator in self.get_validators():
            validator(attrs, self)
        return super().validate(attrs)
