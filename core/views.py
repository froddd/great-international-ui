from urllib.parse import urlencode

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
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
from core.helpers import get_ga_data_for_page
from core.mixins import (
    TEMPLATE_MAPPING, NotFoundOnDisabledFeature, RegionalContentMixin,
    SubmitFormOnGetMixin)
from django.views.generic.edit import FormView


class CMSPageFromPathView(
    RegionalContentMixin,
    CMSLanguageSwitcherMixin,
    NotFoundOnDisabledFeature,
    GA360Mixin,
    TemplateView
):

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
            site_id=settings.DIRECTORY_CMS_SITE_ID,
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

    prioritised_opportunities = []
    if 'related_opportunities' in page:
        all_opportunities = page['related_opportunities']
        prioritised_opportunities = [
            opportunity for opportunity in all_opportunities if opportunity[
                'prioritised_opportunity'
            ]
        ]

    return {
        'invest_contact_us_url': urls.build_invest_url('contact/'),
        'num_of_statistics': count_data_with_field(
            page['statistics'], 'number'),
        'section_three_num_of_subsections': count_data_with_field(
            page['section_three_subsections'], 'heading'),
        'prioritised_opportunities': prioritised_opportunities
        }


class InternationalContactPageView(CountryDisplayMixin,
                                   GA360Mixin,
                                   TemplateView):
    template_name = 'core/contact_page.html'

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='InternationalContactPage',
            business_unit='GreatInternational',
            site_section='Contact',
            site_subsection='ContactForm'
        )

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            hide_language_selector=True,
            invest_contact_us_url=urls.build_invest_url('contact/'),
            *args, **kwargs
        )


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


class OpportunitySearchView(
    CountryDisplayMixin,
    GA360Mixin,
    FormView,
    TemplateView
):
    form_class = forms.OpportunitySearchForm
    page_size = 5
    template_name = 'core/capital_invest/capital_invest_opportunity_listing_page.html'  # NOQA

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierISDCompanySearch',
            business_unit='FindASupplier',
            site_section='InvestmentSupportDirectory',
            site_subsection='CompanySearch'
        )

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
    def filtered_opportunities(self):
        filtered_opportunities = self.opportunities

        if 'sector' in self.kwargs:
            filtered_opportunities = [opportunity for opportunity in
                                      filtered_opportunities if
                                      opportunity.sector == self.kwargs[
                                          'sector']]

        if 'scale' in self.kwargs:
            filtered_opportunities = [opportunity for opportunity in
                                      filtered_opportunities if
                                      opportunity.scale == self.kwargs[
                                          'scale']]
        return filtered_opportunities

    @property
    def num_of_opportunities(self):
        return len(self.filtered_opportunities)

    @property
    def page_number(self):
        return self.request.GET.get('page', '1')

    @property
    def sector(self):
        return self.request.GET.get('sector', '')

    @property
    def scale(self):
        return self.request.GET.get('scale', '')

    @property
    def pagination(self):
        paginator = Paginator(range(self.num_of_opportunities), self.page_size)
        return paginator.page(self.page_number)

    @property
    def results_for_page(self):
        max_value = self.page_size*int(self.page_number)
        min_value = max_value - self.page_size
        return self.filtered_opportunities[min_value:max_value:1]

    def get_context_data(self, *args, **kwargs):

        sectors = []
        for opp in self.opportunities:
            if opp['sector'] not in sectors:
                sectors.append(opp['sector'])

        scales = []
        for opp in self.opportunities:
            if opp['scale'] not in scales:
                scales.append(opp['scale'])

        return super().get_context_data(
            show_search_guide='show-guide' in self.request.GET,
            page=self.page,
            invest_url=urls.SERVICES_INVEST,
            num_of_opportunities=self.num_of_opportunities,
            opportunities=self.opportunities,
            filtered_opportunities=self.filtered_opportunities,
            sectors=sectors,
            scales=scales,
            pagination=self.pagination,
            paginator_url=helpers.get_paginator_url(self.request.GET),
            results=self.results_for_page,
            *args, **kwargs,
        )
