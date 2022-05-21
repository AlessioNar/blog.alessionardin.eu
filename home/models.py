from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from streams import blocks

from blog.models import BlogDetailPage

class HomePageCarouselImages(Orderable):
    """Between 1 and 5 images for the home page carousel."""

    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        )
    panels = [
        ImageChooserPanel("carousel_image"),
    ]




class HomePage(RoutablePageMixin, Page): 
    """Home page model"""

    template = "home/home_page.html"
    max_count = 1
    banner_title = models.CharField(max_length=100, blank=False, null=True) 
    banner_subtitle = RichTextField(features=["bold", "italic"], blank=True, null=True)

    content = StreamField(
        [            
            
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock()),
            ("simple_richtext", blocks.SimpleRichtextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
            ("image", blocks.ImageBlock()),
            ("markdown", blocks.BodyBlock()),
        ],
        null=True,
        blank=True
    )


    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("banner_subtitle"),
            ], heading="Banner Options"),
        MultiFieldPanel([
            InlinePanel("carousel_images", max_num=5, min_num=1, label="Image"),
            ], heading="Carousel Images"),
        StreamFieldPanel("content"),
        

    ]

    def get_context(self, request, *args, **kwargs):
        """Adding the four latest posts"""
        context = super().get_context(request, *args, **kwargs)        
        context["posts"] = BlogDetailPage.objects.live().public()[:4]
        return context

    class Meta:

        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"



    @route(r'^subscribe/$')
    def the_subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)        
        return render(request, "home/subscribe.html", context)

