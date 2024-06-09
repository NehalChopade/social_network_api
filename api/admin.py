from django.contrib import admin
from api.models import (
    User,
    FriendRequest
)


models_tuple = (
    User,
    FriendRequest
)
admin.site.register(models_tuple)
