from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

@register_setting
class SocialMediaSettings(BaseSetting):
	"""Social media settings for the website"""
	
	linkedin = models.URLField(blank=True, null=True, help_text="LinkedIn URL")
	github = models.URLField(blank=True, null=True, help_text="Github URL")
	twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")

	panels = [
		MultiFieldPanel([			
			FieldPanel("linkedin"),
			FieldPanel("github"),
			FieldPanel("twitter"),
			], heading="Social Media Settings"),
	]