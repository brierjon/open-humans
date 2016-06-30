from itertools import groupby
from operator import attrgetter

from django.db import models

from activities.data_selfie.models import DataSelfieDataFile
from common.fields import AutoOneToOneField
from data_import.models import DataRetrievalTask, is_public
from open_humans.models import Member
from private_sharing.models import ProjectDataFile


class Participant(models.Model):
    """
    Represents a participant in the Public Data Sharing study.
    """
    member = AutoOneToOneField(Member,
                               related_name='public_data_participant')
    enrolled = models.BooleanField(default=False)
    signature = models.CharField(max_length=70)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    @property
    def public_sources(self):
        return [data_access.data_source
                for data_access in self.publicdataaccess_set.all()
                if data_access.is_public]

    @property
    def public_data_tasks(self):
        """
        Return most recent tasks for public sources.

        This is a tuple of (source, DataRetrievalTask) as produced by
        DataRetrievalTask's custom queryset method, "grouped_recent".
        """
        if not self.enrolled:
            return []

        tasks = (DataRetrievalTask.objects.for_user(self.member.user)
                 .grouped_recent())

        # filter this way to maintain ordering of OrderedDict from
        # grouped_recent()
        for source in tasks.keys():
            if source not in self.public_sources:
                del tasks[source]

        return tasks

    @property
    def public_direct_sharing_project_files(self):
        files = []

        project_memberships = (self.member.datarequestprojectmember_set.
                               filter(joined=True, authorized=True,
                                      revoked=False))

        for membership in project_memberships:
            if is_public(self.member,
                         'direct-sharing-{}'.format(membership.project_id)):
                files += list(ProjectDataFile.objects.filter(
                    user=membership.member.user,
                    direct_sharing_project=membership.project))

        return list(groupby(sorted(
            files, key=attrgetter('direct_sharing_project')),
            key=attrgetter('direct_sharing_project')))

    @property
    def public_selfie_files(self):
        if is_public(self.member, 'data_selfie'):
            return DataSelfieDataFile.objects.filter(user=self.member.user)

    def __unicode__(self):
        status = 'Enrolled' if self.enrolled else 'Not enrolled'

        return '%s:%s' % (self.member, status)


class PublicDataAccess(models.Model):
    """
    Keep track of public sharing for a data source.

    Sources are currently expected to match a study or activity app_label.
    """

    participant = models.ForeignKey(Participant)
    # Max length matches that used for ContentTypes' 'app_label' field.
    data_source = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)

    def __unicode__(self):
        status = 'Private'

        if self.is_public:
            status = 'Public'

        return '%s:%s:%s' % (self.participant.member.user.username,
                             self.data_source, status)


class WithdrawalFeedback(models.Model):
    """
    Keep track of any feedback a study participant gives when they withdraw
    from the study.
    """
    member = models.ForeignKey(Member)
    feedback = models.TextField(blank=True)
    withdrawal_date = models.DateTimeField(auto_now_add=True)
