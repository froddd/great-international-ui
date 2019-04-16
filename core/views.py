from django.views.generic import TemplateView

from directory_constants import slugs
from directory_constants.choices import COUNTRY_CHOICES
from directory_components.mixins import (
    CMSLanguageSwitcherMixin
)
from directory_components.helpers import get_user_country

from core.mixins import (
    GetSlugFromKwargsMixin,
    ArticleSocialLinksMixin,
    BreadcrumbsMixin,
    CMSPageMixin,
    RegionalContentMixin,
    HowToDoBusinessPageFeatureFlagMixin,
)
from core import forms


class BaseCMSPage(
    CMSLanguageSwitcherMixin, RegionalContentMixin, CMSPageMixin, TemplateView
):
    pass


class CampaignPageView(GetSlugFromKwargsMixin, BaseCMSPage):
    template_name = 'core/campaign.html'
    page_type = 'InternationalCampaignPage'


class ArticleTopicPageView(
    BreadcrumbsMixin, GetSlugFromKwargsMixin, BaseCMSPage,
):
    page_type = 'InternationalTopicLandingPage'


class ArticleListPageView(
    BreadcrumbsMixin, GetSlugFromKwargsMixin, BaseCMSPage,
):
    page_type = 'InternationalArticleListingPage'


class LandingPageCMSView(BaseCMSPage):
    active_view_name = 'index'
    template_name = 'core/landing_page.html'
    page_type = 'InternationalHomePage'
    slug = slugs.GREAT_HOME_INTERNATIONAL

    tariffs_form_class = forms.TariffsCountryForm

    def get_context_data(self, *args, **kwargs):
        country_code = get_user_country(self.request)

        country_name = dict(COUNTRY_CHOICES).get(country_code, '')

        tariffs_country = {
            # used for flag icon css class. must be lowercase
            'code': country_code.lower(),
            'name': country_name,
        }

        return super().get_context_data(
            tariffs_country=tariffs_country,
            tariffs_country_selector_form=self.tariffs_form_class(
                initial={'tariffs_country': country_code}),
            *args, **kwargs,
        )


class CuratedLandingPageCMSView(
    HowToDoBusinessPageFeatureFlagMixin, GetSlugFromKwargsMixin, BaseCMSPage
):
    active_view_name = 'curated-topic-landing'
    page_type = 'InternationalCuratedTopicLandingPage'


class GuideLandingPageCMSView(GetSlugFromKwargsMixin, BaseCMSPage):
    active_view_name = 'guide-landing'
    page_type = 'InternationalGuideLandingPage'


class ArticlePageView(
    ArticleSocialLinksMixin, BreadcrumbsMixin,
    GetSlugFromKwargsMixin, BaseCMSPage,
):
    active_view_name = 'article'
    page_type = 'InternationalArticlePage'


class IndustriesLandingPageCMSView(
    BreadcrumbsMixin, GetSlugFromKwargsMixin, BaseCMSPage,
):
    page_type = 'InternationalTopicLandingPage'
    template_name = 'core/industries_landing_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        def rename_heading_field(page):
            page['landing_page_title'] = page['heading']
            return page

        context['page']['child_pages'] = [
            rename_heading_field(child_page)
            for child_page in context['page']['child_pages']]

        return context


class SectorPageCMSView(GetSlugFromKwargsMixin, BaseCMSPage):
    page_type = 'InternationalSectorPage'
    num_of_statistics = 0
    section_three_num_of_subsections = 0

    def count_data_with_field(self, list_of_data, field):
        filtered_list = [item for item in list_of_data if item[field]]
        return len(filtered_list)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.num_of_statistics = self.count_data_with_field(
            context['page']['statistics'],
            'number'
        )
        self.section_three_num_of_subsections = self.count_data_with_field(
            context['page']['section_three_subsections'],
            'heading'
        )
        return context
