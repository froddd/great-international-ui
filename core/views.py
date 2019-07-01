import random

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.functional import cached_property
from django.utils import translation

from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import handle_cms_response

from directory_constants.choices import COUNTRY_CHOICES
from directory_constants import urls
from directory_components.helpers import get_user_country, SocialLinkBuilder
from directory_components.mixins import (
    CMSLanguageSwitcherMixin,
    GA360Mixin, CountryDisplayMixin)

from core import forms, helpers
from core.context_modifiers import (
    register_context_modifier,
    registry as context_modifier_registry
)
from core.helpers import get_ga_data_for_page, filter_opportunities, \
    SectorFilter, RegionFilter, ScaleFilter, SortFilter, sort_opportunities
from core.mixins import (
    TEMPLATE_MAPPING, NotFoundOnDisabledFeature, RegionalContentMixin)


class CMSPageFromPathView(
    RegionalContentMixin,
    CMSLanguageSwitcherMixin,
    NotFoundOnDisabledFeature,
    GA360Mixin,
    TemplateView
):
    cms_site_id = settings.DIRECTORY_CMS_SITE_ID

    def dispatch(self, request, *args, **kwargs):
        dispatch_result = super().dispatch(request, *args, **kwargs)

        page_type = self.page['page_type']
        ga360_data = get_ga_data_for_page(page_type)
        self.set_ga360_payload(
            page_id=page_type,
            business_unit=ga360_data['business_unit'],
            site_section=ga360_data['site_section'],
            site_subsection=ga360_data['site_subsection']
        )
        return dispatch_result

    @property
    def template_name(self):
        return TEMPLATE_MAPPING[self.page['page_type']]

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_path(
            site_id=self.cms_site_id,
            path=self.kwargs['path'],
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(page=self.page, **kwargs)

        flag_map = {
            'CapitalInvestRegionPage':
                'CAPITAL_INVEST_REGION_PAGE_ON',
            'CapitalInvestOpportunityPage':
                'CAPITAL_INVEST_OPPORTUNITY_PAGE_ON',
            'InternationalCapitalInvestLandingPage':
                'CAPITAL_INVEST_LANDING_PAGE_ON',
            'CapitalInvestOpportunityListingPage':
                'CAPITAL_INVEST_OPPORTUNITY_LISTING_PAGE_ON'
        }

        flag_name = flag_map.get(self.page['page_type'])

        if flag_name and not settings.FEATURE_FLAGS[flag_name]:
            raise Http404

        for modifier in context_modifier_registry.get_for_page_type(
            self.page['page_type']
        ):
            context.update(modifier(context, request=self.request))

        return context


@register_context_modifier('InternationalArticlePage')
def article_page_context_modifier(context, request):

    page_title = context['page'].get('article_title', '')

    social_links_builder = SocialLinkBuilder(
        request.build_absolute_uri(),
        page_title,
        'great.gov.uk')

    return {
        'social_links': social_links_builder.links
    }


@register_context_modifier('InternationalHomePage')
def home_page_context_modifier(context, request):

    country_code = get_user_country(request)
    country_name = dict(COUNTRY_CHOICES).get(country_code, '')

    return {
        'tariffs_country': {
            # used for flag icon css class. must be lowercase
            'code': country_code.lower(),
            'name': country_name,
        },
        'tariffs_country_selector_form': forms.TariffsCountryForm(
            initial={'tariffs_country': country_code}
        ),
    }


@register_context_modifier('InternationalTopicLandingPage')
def sector_landing_page_context_modifier(context, request):

    def rename_heading_field(page):
        page['landing_page_title'] = page['heading']
        return page

    context['page']['child_pages'] = [
        rename_heading_field(child_page)
        for child_page in context['page']['child_pages']]

    return context


@register_context_modifier('InternationalSectorPage')
def sector_page_context_modifier(context, request):

    def count_data_with_field(list_of_data, field):
        filtered_list = [item for item in list_of_data if item[field]]
        return len(filtered_list)

    page = context['page']

    random.shuffle(page['related_opportunities'])
    random_opportunities = page['related_opportunities'][0:3]

    return {
        'invest_contact_us_url': urls.build_invest_url('contact/'),
        'num_of_statistics': count_data_with_field(
            page['statistics'], 'number'),
        'section_three_num_of_subsections': count_data_with_field(
            page['section_three_subsections'], 'heading'),
        'random_opportunities': random_opportunities
        }


@register_context_modifier('CapitalInvestRegionPage')
def capital_invest_region_page_context_modifier(context, request):

    def count_data_with_field(list_of_data, field):
        filtered_list = [item for item in list_of_data if item[field]]
        return len(filtered_list)

    page = context['page']
    return {
        'num_of_economics_statistics': count_data_with_field(
            page['economics_stats'], 'number'),
        'num_of_location_statistics': count_data_with_field(
            page['location_stats'], 'number'),
        'invest_cta_link': urls.SERVICES_INVEST,
        'buy_cta_link': urls.SERVICES_FAS,
    }


@register_context_modifier('CapitalInvestOpportunityPage')
def capital_invest_opportunity_page_context_modifier(context, request):

    return {
        'invest_cta_link': urls.SERVICES_INVEST,
        'buy_cta_link': urls.SERVICES_FAS,
    }


<<<<<<< HEAD
class OpportunitySearchView(
    CountryDisplayMixin,
    GA360Mixin,
    TemplateView
):
    template_name = 'core/capital_invest/capital_invest_opportunity_listing_page.html'  # NOQA
    page_size = 10

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='GreatInternationalCapitalInvestmentOpportunitySearch',
            business_unit='CapitalInvestment',
            site_section='Opportunities',
            site_subsection='Search'
        )

    def get(self, request, *args, **kwargs):
        try:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        except (EmptyPage, PageNotAnInteger):
            url = helpers.get_paginator_url(self.request.GET, 'opportunities') + "&page=1"  # NOQA
            return redirect(url)

    @property
    def page_number(self):
        return self.request.GET.get('page', '1')

    @property
    def sector(self):
        return SectorFilter(self.request.GET.getlist('sector', []))

    @property
    def scale(self):
        return ScaleFilter(self.request.GET.getlist('scale', []))

    @property
    def region(self):
        return RegionFilter(self.request.GET.getlist('region', ''))

    @property
    def sort_filter(self):
        return SortFilter(self.request.GET.get('sort_by', ''))

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_path(
            site_id=settings.DIRECTORY_CMS_SITE_ID,
            path=self.kwargs['path'],
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    @property
    def opportunities(self):
        return self.page['opportunity_list']

    @property
    def all_sectors(self):
        sectors = set()

        for opp in self.opportunities:
            for sector in opp['related_sectors']:
                if sector['related_sector'] \
                        and sector['related_sector']['title']:
                    sectors.add(sector['related_sector']['title'])

        return [
            (sector, sector) for sector in sectors
        ]

    @property
    def all_scales(self):
        return [
            (scale.title, scale.title)
            for scale in ScaleFilter.scales_with_values
        ]

    @property
    def all_regions(self):
        regions = set()
        for opp in self.opportunities:
            if opp['related_region'] and opp['related_region']['title']:
                regions.add(opp['related_region']['title'])

        return [
            (region, region) for region in regions
        ]

    @property
    def all_sort_filters(self):
        sort_filters_with_selected_status = [
            (sort_filter.title, sort_filter.title)
            for sort_filter in SortFilter.sort_by_with_values
        ]

        return sort_filters_with_selected_status

    @property
    def filtered_opportunities(self):

        filtered_opportunities = [opp for opp in self.opportunities]

        if self.sector.sectors:
            filtered_opportunities = filter_opportunities(
                filtered_opportunities,
                self.sector
            )

        if self.region.regions:
            filtered_opportunities = filter_opportunities(
                filtered_opportunities,
                self.region
            )

        if self.scale.selected_scales:
            filtered_opportunities = filter_opportunities(
                filtered_opportunities,
                self.scale
            )

        if self.sort_filter.sort_by_filter_chosen:
            filtered_opportunities = sort_opportunities(
                filtered_opportunities,
                self.sort_filter
            )

        return filtered_opportunities

    @property
    def num_of_opportunities(self):
        return len(self.filtered_opportunities)

    @property
    def pagination(self):
        paginator = Paginator(self.filtered_opportunities, self.page_size)
        return paginator.page(self.page_number or 1)

    @property
    def filters_chosen(self):
        filters = []
        for sector in self.sector.sectors:
            filters.append(sector)
        for scale in self.scale.selected_scales:
            filters.append(scale.title)
        for region in self.region.regions:
            filters.append(region)
        return filters

    @property
    def sorting_chosen(self):
        return self.sort_filter.sort_by_filter_chosen.title

    @property
    def opportunity_search_form(self):
        return forms.OpportunitySearchForm(
            sectors=self.all_sectors,
            scales=self.all_scales,
            regions=self.all_regions,
            sort_by_options=self.all_sort_filters,
            initial={
                'sector': self.filters_chosen,
                'scale': self.filters_chosen,
                'region': self.filters_chosen,
                'sort_by': self.sorting_chosen,
            },
=======
class InternationalContactPageView(
    CountryDisplayMixin, GA360Mixin, TemplateView
):
    template_name = 'core/contact_page.html'

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='InternationalContactPage',
            business_unit='GreatInternational',
            site_section='Contact',
            site_subsection='ContactForm'
>>>>>>> Add invest homepage
        )

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
<<<<<<< HEAD
            page=self.page,
            invest_url=urls.SERVICES_INVEST,
            num_of_opportunities=self.num_of_opportunities,
            sectors=self.all_sectors,
            scales=self.all_scales,
            regions=self.all_regions,
            sorting_filters=self.all_sort_filters,
            pagination=self.pagination,
            sorting_chosen=self.sorting_chosen,
            filters=self.filters_chosen,
            current_page_num=self.page_number,
            form=self.opportunity_search_form,
            *args, **kwargs,
=======
            hide_language_selector=True,
            invest_contact_us_url=urls.build_invest_url('contact/'),
            *args, **kwargs
>>>>>>> Add invest homepage
        )
