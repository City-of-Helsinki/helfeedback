from django.db import models
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext
import requests


class Feedback(models.Model):
    RATING_CHOICES = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
    )
    user_agent = models.TextField(null=True, blank=True, max_length=400,
                                  verbose_name=_('The user agent string of the user\'s browser'))
    rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES,
                                 verbose_name=_('Rating'))
    body = models.TextField(blank=True, verbose_name=_('Body'))
    url = models.URLField(verbose_name=_('URL of page where feedback was sent from'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('Email'))
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO metadata fields, more contact info fields?
    # service = models.UUIDField() #??
    # ip = models.GenericIPAddressField()
    # screen_resolution = models.TextField()
    # redux_state_dump = models.TextField(blank=True) # could this be JSONField?
    # id = models.CharField(primary_key=True, max_length=100, unique=True, default=uuid.uuid4)

    class Meta:
        ordering = (('-created_at'),)

    def notify(self):
        print('Feedback.notify')
        if not Notifier.objects.exists():
            return

        notifier = Notifier.objects.first()
        notifier.notify(self)

    def __str__(self):
        return "{}".format(self.url)


# Copypasted from https://github.com/City-of-Helsinki/digihel/blob/master/feedback/models.py
class Notifier(models.Model):
    type = models.CharField(max_length=20, choices=(('slack', 'Slack'),))
    url_base = models.CharField(max_length=200)
    language = models.CharField(max_length=20)

    def notify(self, feedback):
        if self.type == 'slack':
            notifier = self.slacknotifier
        else:
            raise NotImplementedError(_('Unsupported notifier type: %s' % self.type))
        notifier.notify(feedback)


class SlackNotifier(Notifier):
    webhook_url = models.URLField()
    channel = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    icon_emoji = models.CharField(max_length=50, null=True, blank=True)
    icon_url = models.URLField(null=True, blank=True)

    def notify(self, feedback):
        """
        Send a Slack notification for the given feedback.
        :param feedback: Feedback object
        :type feedback: feedback.models.Feedback
        """
        data = self.build_slack_message(feedback)
        print('@ models.py, data={}'.format(data))
        resp = requests.post(self.webhook_url, json=data)
        if resp.status_code != 200:
            raise Exception('Slack notify failed with HTTP status %d' % resp.status_code)

    def build_slack_message(self, feedback):
        """
        Build a Slack message dict from the feedback object.
        :param feedback: Feedback object
        :type feedback: feedback.models.Feedback
        :return: Slack message dict
        :rtype: dict
        """
        with translation.override(self.language):
            message = gettext('New feedback received for {url}').format(url=feedback.url)
        data = {
            'text': message,
            'attachments': [self.build_slack_attachment_from_feedback(feedback)],
        }
        data.update(self._get_notifier_config_for_slack_message())
        return data

    def build_slack_attachment_from_feedback(self, feedback):
        """
        Build a Slack attachment entity from the given Feedback object.
        :param feedback: Feedback object
        :type feedback: feedback.models.Feedback
        :return: Slack attachment dictionary
        :rtype: dict
        """
        attachment = {
            'text': feedback.body,
            'ts': int(feedback.created_at.timestamp()),
        }
        attachment['fields'] = fields = []
        # If the feedback refers to a Wagtail Page, add some more
        # information to the Slack notification.
        # try:
        #     Page = apps.get_model('wagtailcore', 'Page')
        #     klass = feedback.content_type.model_class()
        #     if issubclass(klass, Page):
        #         page = Page.objects.get(id=feedback.object_id)
        #         attachment['title'] = page.title
        #         attachment['title_link'] = page.full_url
        # except (LookupError, ObjectDoesNotExist):
        #     pass
        with translation.override(self.language):
            # if feedback.name:
            #     fields.append({'title': gettext('Name'), 'value': feedback.name, 'short': False})
            if feedback.email:
                fields.append({'title': gettext('Email'), 'value': feedback.email, 'short': False})
            if feedback.user_agent:
                fields.append({'title': gettext('User agent'), 'value': feedback.user_agent, 'short': False})
        return attachment

    def _get_notifier_config_for_slack_message(self):
        """
        Convert the notifier's configuration into fields for a Slack message
        :return: Part of a Slack message, to be combined into other things
        :rtype: dict
        """
        data = {}

        if self.username:
            data['username'] = self.username

        if self.icon_url:
            data['icon_url'] = self.icon_url

        if self.icon_emoji:
            emoji = self.icon_emoji.strip(':')
            data['icon_emoji'] = ':' + emoji + ':'

        if self.channel:
            data['channel'] = self.channel

        return data
