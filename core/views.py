from django.conf import settings
from django.views.generic import TemplateView
from django.utils.functional import cached_property
from django.utils import translation

from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import handle_cms_response
from directory_constants.constants import cms


from core.mixins import (
    TEMPLATE_MAPPING,
    GetSlugFromKwargsMixin,
    ArticleSocialLinksMixin,
    BreadcrumbsMixin,
    CMSPageMixin,
    RegionalContentMixin,
    TariffsCountryDisplayMixin)

from core.forms import TariffsCountryForm


class BaseCMSPage(RegionalContentMixin, CMSPageMixin, TemplateView):
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


class LandingPageCMSView(TariffsCountryDisplayMixin, BaseCMSPage):
    active_view_name = 'index'
    template_name = 'core/landing_page.html'
    page_type = 'InternationalHomePage'
    slug = cms.GREAT_HOME_INTERNATIONAL_SLUG

    tariffs_country_selector_form = TariffsCountryForm()


class CuratedLandingPageCMSView(GetSlugFromKwargsMixin, BaseCMSPage):
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

    def get_context_data(self, **kwargs):
        context = super(
            IndustriesLandingPageCMSView, self
        ).get_context_data(**kwargs)

        def rename_heading_field(page):
            page['landing_page_title'] = page['heading']
            return page

        context['page']['child_pages'] = [rename_heading_field(child_page)
                                          for child_page
                                          in context['page']['child_pages']]
        return context


class SectorPageCMSView(GetSlugFromKwargsMixin, BaseCMSPage):
    page_type = 'InternationalSectorPage'
    num_of_statistics = 0
    section_three_num_of_subsections = 0

    def count_data_with_field(self, list_of_data, field):
        filtered_list = [item for item in list_of_data if item[field]]
        return len(filtered_list)

    def get_context_data(self, **kwargs):
        context = super(SectorPageCMSView, self).get_context_data(**kwargs)
        self.num_of_statistics = self.count_data_with_field(
            context['page']['statistics'],
            'number'
        )
        self.section_three_num_of_subsections = self.count_data_with_field(
            context['page']['section_three_subsections'],
            'heading'
        )
        return context


class SetupGuideLandingPageCMSView(BaseCMSPage):
    active_view_name = 'setup-guide'
    template_name = 'core/setup_guide_landing_page.html'
    slug = 'setup-guide-landing-page'
    subpage_groups = ['children_setup_guides']


class SetupGuidePageCMSView(GetSlugFromKwargsMixin, BaseCMSPage):
    active_view_name = 'setup-guide'
    template_name = 'core/accordion_content_page.html'


class UKRegionPageCMSView(GetSlugFromKwargsMixin, BaseCMSPage):
    template_name = 'core/accordion_content_page_with_hero_image.html'


class CMSPageFromPathView(TemplateView):

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_path(
            site_id=settings.DIRECTORY_CMS_SITE_ID,
            path=self.kwargs['path'],
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return self.handle_cms_response(response)

    def get_context_data(self, **kwargs):
        data = {'page': self.page}
        data.update(kwargs)
        return super().get_context_data(**data)

    def handle_cms_response(self, response):
        return handle_cms_response(response)

    @property
    def template_name(self):
        return TEMPLATE_MAPPING[self.page['page_type']]
