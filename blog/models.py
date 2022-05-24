from django.db import models
from django.shortcuts import render

from django_extensions.db.fields import AutoSlugField

from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail.images.edit_handlers import ImageChooserPanel


from streams import blocks

class BlogAuthorsOrderable(Orderable):
	"""This allows us to select one or more blog authors from snippets"""

	page = ParentalKey("blog.BlogDetailPage", related_name="blog_authors")
	author = models.ForeignKey(
		"blog.BlogAuthor",
		on_delete=models.CASCADE,
		)

	panels = [
		SnippetChooserPanel("author"),

	]

class BlogAuthor(models.Model):
	"""Blog author for snippets"""

	name = models.CharField(max_length=100)
	website = models.URLField(blank=True, null=True)
	image = models.ForeignKey(
		"wagtailimages.Image",
		on_delete=models.SET_NULL,
		null=True,
		blank=False,
		related_name ="+",
		)

	panels = [
		MultiFieldPanel(
				[
				FieldPanel("name"),
				ImageChooserPanel("image"),				
				], heading="Name and image",
			),
		MultiFieldPanel(
				[
				FieldPanel("website"),				
				], heading="Links",
			),
	]

	def __str__(self):
		"""String Wrapper of this class"""
		return self.name

	class Meta:
		verbose_name = "Blog Author"
		verbose_name_plural = "Blog Authors"

register_snippet(BlogAuthor)

class BlogCategory(models.Model):
	"""Blog category for a snippet"""
	name = models.CharField(max_length=255)
	slug = AutoSlugField(
		populate_from=["name"]
		, editable=True,
		help_text='A slug to identify posts by this category',

		)

	panels = [
		FieldPanel("name"),
		FieldPanel("slug"),		
	]

	class Meta:
		verbose_name="Blog Category"
		verbose_name_plural="Blog Categories"
		ordering=["name"]

	def __str__(self):
		"""String Wrapper of this class"""
		return self.name

register_snippet(BlogCategory)

class BlogListingPage(RoutablePageMixin, Page):
	"""Listing Page lists all the Blog Detail Pages"""
	template  = "blog/blog_listing_page.html"
	custom_title = models.CharField(
		max_length=100, 
		blank=False,
		null=False,
		help_text='Overwrites the default title',
		)

	content_panels = Page.content_panels + [
		FieldPanel("custom_title"),			

	]

	# @todo I have to intervene here to create a general listing page
	def get_context(self, request, *args, **kwargs):
		"""Adding custom elements to our context"""

		context = super().get_context(request, *args, **kwargs)

		if request.GET.get('category'):

			context['this_cat'] = BlogCategory.objects.get(slug=request.GET.get('tags'))

			if request.GET.get('tags'):
				context['this_cat'] = BlogCategory.objects.get(slug=request.GET.get('tags'))
				context["posts"] = BlogDetailPage.objects.live().public().filter(tags__slug__in=[request.GET.get('tags')])
			else:
				context["posts"] = BlogDetailPage.objects.live().public()

			context["categories"] = BlogCategory.objects.all()
			
			return context


	@route(r'^latest/$', name = "latest_posts")
	def latest_blog_posts(self, request, *args, **kwargs):
		context = self.get_context(request, *args, **kwargs)
		context["latest_posts"] = context["posts"][:1]

		return render(request, "blog/latest_posts.html", context)

	def get_sitemap_urls(self, request): 
		# Uncomment to have no sitemap for this page
		# return []
		sitemap = super().get_sitemap_urls(request)
		sitemap.append({
				"location": self.full_url + self.reverse_subpage("latest_posts"),
				"lastmod": (self.last_published_at or self.latest_revison_created_at),
				"priority": 0.9,
			})
		return sitemap



class BlogDetailPage(Page):
	"""Parental Blog Detail Page."""

	template  = "blog/blog_detail_page.html"
	
	custom_title = models.CharField(
		max_length=100, 
		blank=False,
		null=False,
		help_text='Overwrites the default title',
		)

	tags = ParentalManyToManyField("blog.BlogCategory", blank=True)

	heading_image = models.ForeignKey(
		"wagtailimages.Image",
		null=True,
		blank=False,
		related_name="+",
		on_delete=models.SET_NULL,
		)

	card_image = models.ForeignKey(
		"wagtailimages.Image",
		null=True,
		blank=False,
		related_name="+",
		on_delete=models.SET_NULL,
		)

	intro = RichTextField(
		blank=True, 
		null=True,
		help_text='Intro text for preview'
		)

	content = StreamField(
		[
			("title_and_text", blocks.TitleAndTextBlock()),
			("full_richtext", blocks.RichtextBlock()),
			("simple_richtext", blocks.SimpleRichtextBlock()),
			("cards", blocks.CardBlock()),
			("cta", blocks.CTABlock()),
			("image", blocks.ImageBlock()),
			("markdown", blocks.BodyBlock()),
			# graph data block
		],
		null=True,
		blank=True
	)

	content_panels = Page.content_panels + [
		MultiFieldPanel([
						FieldPanel("intro"),
						ImageChooserPanel("heading_image"),
						ImageChooserPanel("card_image"),
						FieldPanel("tags", widget=forms.CheckboxSelectMultiple),
			]),
		StreamFieldPanel("content"),

		MultiFieldPanel([
			InlinePanel("blog_authors", label = "Author", min_num=1, max_num=4),
			FieldPanel("custom_title"),
			], heading="Details"),		
	]

"""
class ArticleBlogPage(BlogDetailPage):

	template = "blog/article_blog_page.html"

	subtitle = models.CharField(
		max_length=100, 
		blank=True, 
		null=True
		)

	intro_image = models.ForeignKey(
		"wagtailimages.Image",
		blank=True,
		null=True,		
		on_delete = models.SET_NULL,
		help_text = 'Best size for this image will be 1400x400'
		)


	content_panels = Page.content_panels + [
		FieldPanel("custom_title"),
		FieldPanel("subtitle"),
		ImageChooserPanel("banner_image"),
		ImageChooserPanel("intro_image"),
		MultiFieldPanel([
			InlinePanel("blog_authors", label = "Author", min_num=1, max_num=4),
			], heading="Author(s)"),
		MultiFieldPanel([
			FieldPanel("tags", widget=forms.CheckboxSelectMultiple)			
			], heading="Tags"),
		StreamFieldPanel("content"),
	]
"""