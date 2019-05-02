from django.conf import settings
from django.views.generic import TemplateView
from django.utils.functional import cached_property
from django.utils import translation

from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import handle_cms_response

from directory_constants import slugs, urls
from directory_constants.choices import COUNTRY_CHOICES
from directory_components.mixins import (
    CMSLanguageSwitcherMixin,
    CountryDisplayMixin,
)
from directory_components.helpers import get_user_country

from core.mixins import (
    TEMPLATE_MAPPING,
    RegionalContentMixin,
)
from core import forms
from core.context_modifier_registry import (
    context_modifier_registry,
    register_context_modifier,
)


class CMSPageFromPathView(
    CMSLanguageSwitcherMixin, RegionalContentMixin, CountryDisplayMixin,
    TemplateView
):

    # Allow subclasses to override these (will be useful when UIs are merged)
    site_id = settings.DIRECTORY_CMS_SITE_ID
    template_mapping = TEMPLATE_MAPPING

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_path(
            site_id=self.site_id,
            path=self.kwargs['path'],
            language_code=translation.get_language(),
            region=self.region,
            draft_token=self.request.GET.get('draft_token'),
        )
        return self.handle_cms_response(response)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        for fn in context_modifier_registry.get_for_page_type(
            self.page['page_type']
        ):
            # context modifiers are applied here rather than in
            # get_context_data() to allow them to interrupt the
            # process by returning a HttpResponse
            result = fn(context, request, self)
            if hasattr(result, 'status_code'):
                # This looks like a HttpResponse, so return immediately to
                # avoid further unnecessary processing
                return result
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context_data = dict(
            page=self.page,
            page_path=self.kwargs['path'],
        )
        # allows subclasses to override the above values, and
        # also prevents super() being called with duplicate args
        context_data.update(kwargs)
        return super().get_context_data(*args, **context_data)

    def handle_cms_response(self, response):
        return handle_cms_response(response)

    @property
    def template_name(self):
        return self.template_mapping[self.page['page_type']]


@register_context_modifier('InternationalHomePage')
def home_page_context_modifier(context, request=None, view=None):

    country_code = get_user_country(request)
    country_name = dict(COUNTRY_CHOICES).get(country_code, '')
    context.update({
        'tariffs_country': {
            # used for flag icon css class. must be lowercase
            'code': country_code.lower(),
            'name': country_name,
        },
        'tariffs_country_selector_form': forms.TariffsCountryForm(
            initial={'tariffs_country': country_code}
        ),
        'invest_contact_us_link': urls.INVEST_CONTACT_US,
    })


@register_context_modifier('InternationalTopicLandingPage')
def topic_landing_context_modifier(context, request=None, view=None):

    def rename_heading_field(page):
        page['landing_page_title'] = page['heading']
        return page

    context['page']['child_pages'] = [
        rename_heading_field(child_page)
        for child_page in context['page']['child_pages']
    ]

    return context


@register_context_modifier('InternationalSectorPage')
def sector_page_context_modifier(context, request=None, view=None):

    def count_data_with_field(list_of_data, field):
        filtered_list = [item for item in list_of_data if item[field]]
        return len(filtered_list)

    context['num_of_statistics'] = count_data_with_field(
        context['page']['statistics'], 'number')

    context['section_three_num_of_subsections'] = count_data_with_field(
        context['page']['section_three_subsections'], 'heading')

    return context
