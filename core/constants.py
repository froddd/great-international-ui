from django.utils.translation import ugettext_lazy as _
from collections import namedtuple

from django.conf import settings
from core.header_config import tier_one_nav_items as tier_one, tier_two_nav_items as tier_two
from directory_constants import urls

TEMPLATE_MAPPING = {
    # Great international core
    'InternationalHomePage': 'core/landing_page.html',
    'InternationalTopicLandingPage': 'investment_atlas/topic_list.html',
    'InternationalArticleListingPage': 'core/article_list.html',
    'InternationalArticlePage': 'investment_atlas/article_detail.html',

    # InternationalSectorPage and InternationalSubSectorPage used to use
    # 'core/sector_page.html' but they have been deprecated in favour of
    # InternationalInvestmentSectorPage and InternationalInvestmentSubSectorPage
    'InternationalCuratedTopicLandingPage': 'core/how_to_do_business_landing_page.html',
    'InternationalGuideLandingPage': 'core/uk_setup_guide/guide_landing_page.html',

    # Brexit
    'InternationalEUExitFormPage': 'euexit/international-contact-form.html',
    'InternationalEUExitFormSuccessPage': 'euexit/international-contact-form-success.html',

    # Capital investment
    'InternationalCapitalInvestLandingPage': 'core/capital_invest/capital_invest_landing_page.html',
    'CapitalInvestRegionPage': 'core/capital_invest/capital_invest_region_page.html',
    'CapitalInvestOpportunityPage': 'core/capital_invest/capital_invest_opportunity_page.html',
    'CapitalInvestOpportunityListingPage': 'core/capital_invest/capital_invest_opportunity_listing_page.html',
    'CapitalInvestContactFormPage': 'core/capital_invest/capital_invest_contact_form.html',
    'CapitalInvestContactFormSuccessPage': 'core/capital_invest/capital_invest_contact_form_success.html',

    # About DIT
    'AboutDitLandingPage': 'core/about_dit/about_dit_landing_page.html',
    'AboutDitServicesPage': 'core/about_dit/services_page.html',
    'AboutUkLandingPage': 'core/about_uk/about_uk_landing_page.html',
    'AboutUkRegionListingPage': 'investment_atlas/region_listing_page.html',
    'AboutUkRegionPage': 'investment_atlas/region.html',
    'AboutUkWhyChooseTheUkPage': 'core/about_uk/why_choose_the_uk_page.html',

    # Invest
    'InvestInternationalHomePage': 'invest/landing_page.html',
    'InvestHighPotentialOpportunityDetailPage': 'invest/hpo/high_potential_opportunity_detail.html',
    'InvestRegionPage': 'invest/regions/region_detail.html',

    # Find a supplier
    'InternationalTradeHomePage': 'find_a_supplier/landing_page.html',
    'InternationalTradeIndustryContactPage': 'find_a_supplier/buy_from_the_uk_form.html',

    # Investment Atlas
    'InvestmentOpportunityPage': 'investment_atlas/opportunity.html',
    'InvestmentAtlasLandingPage': 'investment_atlas/investment.html',
    'InternationalInvestmentSectorPage': 'investment_atlas/sector.html',
    'InternationalInvestmentSubSectorPage': 'investment_atlas/sector.html',
    'InvestmentGeneralContentPage': 'investment_atlas/general_content_page.html',
    'WhyInvestInTheUKPage': 'investment_atlas/why_invest_in_the_uk_page.html',
}

FEATURE_FLAGGED_URLS_MAPPING = {
    '/international/content/how-to-do-business-with-the-uk/':
        'HOW_TO_DO_BUSINESS_ON',
}

FEATURE_FLAGGED_PAGE_TYPES_MAPPING = {
    'CapitalInvestRegionPage': 'CAPITAL_INVEST_REGION_PAGE_ON',
    'AboutUkRegionPage': 'ABOUT_UK_REGION_PAGE_ON',
    'AboutUkRegionListingPage': 'ABOUT_UK_REGION_LISTING_PAGE_ON',
    'CapitalInvestOpportunityPage': 'CAPITAL_INVEST_OPPORTUNITY_PAGE_ON',
    'InternationalCapitalInvestLandingPage': 'CAPITAL_INVEST_LANDING_PAGE_ON',
    'CapitalInvestOpportunityListingPage': 'CAPITAL_INVEST_OPPORTUNITY_LISTING_PAGE_ON',
    'InternationalSubSectorPage': 'CAPITAL_INVEST_SUB_SECTOR_PAGE_ON',
    'CapitalInvestContactFormPage': 'CAPITAL_INVEST_CONTACT_FORM_PAGE_ON',
    'CapitalInvestContactFormSuccessPage': 'CAPITAL_INVEST_CONTACT_FORM_PAGE_ON',
    'AboutUkLandingPage': 'ABOUT_UK_LANDING_PAGE_ON',
}

GA_DATA_MAPPING = {
    # Great international core
    'InternationalHomePage': {
        'business_unit': 'GreatInternational',
        'site_section': 'HomePage',
        'site_subsection': ''
    },
    'InternationalTopicLandingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'Topic',
        'site_subsection': 'ListingPage'
    },
    'InternationalArticleListingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'Article',
        'site_subsection': 'ListingPage'
    },
    'InternationalArticlePage': {
        'business_unit': 'GreatInternational',
        'site_section': 'Article',
        'site_subsection': 'DetailPage'
    },
    # InternationalSectorPage is deprecated
    'InternationalInvestmentSectorPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'Sector',
        'site_subsection': 'DetailPage'
    },
    # InternationalSubSectorPage
    'InternationalInvestmentSubSectorPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'SubSector',
        'site_subsection': 'DetailPage'
    },
    'InternationalCuratedTopicLandingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'CuratedTopic',
        'site_subsection': 'LandingPage'
    },
    'InternationalGuideLandingPage': {
        'business_unit': 'Invest',
        'site_section': 'Guide',
        'site_subsection': 'ListingPage'
    },

    # Brexit
    'InternationalEUExitFormPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'EUExit',
        'site_subsection': 'FormPage'
    },
    'InternationalEUExitFormSuccessPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'EUExit',
        'site_subsection': 'FormSuccessPage'
    },

    # Capital investment
    'InternationalCapitalInvestLandingPage': {
        'business_unit': 'CapitalInvestment',
        'site_section': 'LandingPage',
        'site_subsection': ''
    },
    'CapitalInvestRegionPage': {
        'business_unit': 'CapitalInvestment',
        'site_section': 'Region',
        'site_subsection': 'DetailPage'
    },
    'CapitalInvestOpportunityPage': {
        'business_unit': 'CapitalInvestment',
        'site_section': 'Opportunity',
        'site_subsection': 'DetailPage'
    },
    'CapitalInvestOpportunityListingPage': {
        'business_unit': 'CapitalInvestment',
        'site_section': 'Opportunity',
        'site_subsection': 'ListingPage'
    },
    'CapitalInvestContactFormPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'CapitalInvest',
        'site_subsection': 'Contact',
    },
    'CapitalInvestContactFormSuccessPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'CapitalInvest',
        'site_subsection': 'ContactSuccess'
    },

    # Invest
    'InvestInternationalHomePage': {
        'business_unit': 'Invest',
        'site_section': 'HomePage',
        'site_subsection': 'ListingPage'
    },
    'InvestHighPotentialOpportunityDetailPage': {
        'business_unit': 'Invest',
        'site_section': 'HighPotentialOpportunities',
        'site_subsection': 'DetailPage',
    },
    'ForeignDirectInvestmentFormPage': {
        'business_unit': 'Invest',
        'site_section': 'ForeignDirectInvestment',
        'site_subsection': 'FormPage',
    },
    'ForeignDirectInvestmentFormSuccessPage': {
        'business_unit': 'Invest',
        'site_section': 'ForeignDirectInvestment',
        'site_subsection': 'FormSuccessPage',
    },
    'InvestRegionPage': {
        'business_unit': 'Invest',
        'site_section': 'Regions',
        'site_subsection': 'DetailPage',
    },
    'WhyInvestInTheUKPage': {
        'business_unit': 'Invest',
        'site_section': 'WhyInvestInTheUKPage',
        'site_subsection': 'DetailPage',
    },

    # Perfect fit
    'PerfectFitFormPage': {
        'business_unit': 'Invest',
        'site_section': 'PerfectFit',
        'site_subsection': 'FormPage',
    },
    'PerfectFitFormSuccessPage': {
        'business_unit': 'Invest',
        'site_section': 'PerfectFit',
        'site_subsection': 'FormSuccessPage',
    },

    # About DIT
    'AboutDitLandingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'AboutDIT',
        'site_subsection': 'LandingPage'
    },
    'AboutDitServicesPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'AboutDIT',
        'site_subsection': 'ServicesPage'
    },
    'AboutUkLandingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'AboutUK',
        'site_subsection': 'LandingPage'
    },
    'AboutUkRegionListingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'AboutUK',
        'site_subsection': 'RegionListingPage'
    },
    'AboutUkRegionPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'AboutUK',
        'site_subsection': 'RegionPage'
    },
    'AboutUkWhyChooseTheUkPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'AboutUK',
        'site_subsection': 'WhyChooseTheUkPage'
    },

    # Find a supplier
    'InternationalTradeHomePage': {
        'business_unit': 'FindASupplier',
        'site_section': 'HomePage',
        'site_subsection': '',
    },
    'InternationalTradeIndustryContactPage': {
        'business_unit': 'FindASupplier',
        'site_section': 'Industries',
        'site_subsection': 'LandingPageContact'
    },

    # Investment Atlas
    'InvestmentOpportunityPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'InvestmentOpportunity',
        'site_subsection': 'InvestmentAtlas',
    },
    'InvestmentAtlasLandingPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'InvestmentAtlas',
        'site_subsection': 'LandingPage',
    },
    'InvestmentGeneralContentPage': {
        'business_unit': 'GreatInternational',
        'site_section': 'InvestmentAtlas',
        'site_subsection': 'ContentPage',
    }
}

HeaderConfig = namedtuple('HeaderConfig', 'section sub_section')
HEADER_SECTION_MAPPING = {
    # Home page
    r'^$': HeaderConfig(section=None, sub_section=None),

    # Invest in the UK pages
    r'^investment/why-invest-in-the-uk.*': HeaderConfig(
        section=tier_one.INVEST_IN_UK,
        sub_section=tier_two.WHY_INVEST_IN_UK
    ),
    r'^investment/regions.*': HeaderConfig(
        section=tier_one.INVEST_IN_UK,
        sub_section=tier_two.REGIONS,
    ),
    r'^investment/sectors.*': HeaderConfig(
        section=tier_one.INVEST_IN_UK,
        sub_section=tier_two.SECTORS,
    ),
    r'^investment/opportunities.*': HeaderConfig(
        section=tier_one.INVEST_IN_UK,
        sub_section=tier_two.INVESTMENT_OPPORTUNITIES,
    ),
    r'^investment/how-we-can-help.*': HeaderConfig(
        section=tier_one.INVEST_IN_UK,
        sub_section=tier_two.HOW_WE_CAN_HELP_INVESTMENT_ATLAS,
    ),
    r'^investment.*': HeaderConfig(
        section=tier_one.INVEST_IN_UK,
        sub_section=None
    ),

    # Buy from the UK
    r'^trade/contact.*': HeaderConfig(
        section=tier_one.BUY_FROM_THE_UK,
        sub_section=tier_two.CONTACT_US_TRADE
    ),
    r'^trade/how-we-help-you-buy.*': HeaderConfig(
        section=tier_one.BUY_FROM_THE_UK,
        sub_section=tier_two.HOW_WE_HELP_BUY
    ),
    r'^trade.*': HeaderConfig(section=tier_one.BUY_FROM_THE_UK, sub_section=tier_two.FIND_A_SUPPLIER),

    # Contact
    r'^contact.*': HeaderConfig(section=tier_one.CONTACT, sub_section=None),
    r'^invest/contact.*': HeaderConfig(section=tier_one.CONTACT, sub_section=None),
}

INVEST_CONTACT_URL = urls.international.EXPAND_CONTACT
CAPITAL_INVEST_CONTACT_URL = urls.international.CAPITAL_INVEST_CONTACT
EXPORTING_TO_UK_CONTACT_URL = urls.international.INTERNATIONAL_CONTACT_TRIAGE / 'exporting-to-the-uk/'
BUYING_CONTACT_URL = urls.international.TRADE_CONTACT
EUEXIT_CONTACT_URL = settings.EU_EXIT_INTERNATIONAL_CONTACT_URL
OTHER_CONTACT_URL = urls.domestic.CONTACT_US / 'international/'

EMAIL_CONSENT_LABEL = _('I would like to receive additional information by email')
PHONE_CONSENT_LABEL = _('I would like to receive additional information by telephone')
MARKETING_CONSENT_LABEL = (
    'Tick this box if you are happy to receive future marketing'
    ' communications from the great.gov.uk service.'
)

EMPLOYEES = [
    ('1-10', _('1-10')),
    ('11-50', _('11-50')),
    ('51-200', _('51-200')),
    ('201-500', _('201-500')),
    ('501-1000', _('501-1,000')),
    ('1001-10000', _('1,001-10,000')),
    ('10001+', _('10,001+')),
]
