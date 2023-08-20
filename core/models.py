from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


class TimeStampedModel(models.Model):
    """
    Abstract model for keeping track of
    create, update, and delete dates.
    """

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    datetime_deleted = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class DoerOfActionModel(models.Model):
    """
    Abstract model that keeps track of the users
    responsible for the creation, modification,
    or deletion of a database item.
    """

    created_by = models.ForeignKey(
        User,
        null=True,
        related_name="%(app_label)s_%(class)s_created_set",
        on_delete=models.SET_NULL
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated_set",
        on_delete=models.SET_NULL
    )
    deleted_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_deleted_set",
        on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True


class ObjectStatusCheckModel(models.Model):
    """
    Abstract model for determining the current state
    of an object.
    """

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel, DoerOfActionModel, ObjectStatusCheckModel):
    """
    A base model containing all fields dedicated for
    tracking data updates. All significant models are
    recommended to inherit this.
    """

    class Meta:
        abstract = True

    def soft_delete(self, user):
        """
        Set object as inactive.

        Inactive objects are treated as deleted.
        """
        self.datetime_deleted = timezone.now()
        self.deleted_by = user
        self.is_active = False
        self.save(
            update_fields=[
                'datetime_deleted',
                'deleted_by',
                'is_active'
            ]
        )

