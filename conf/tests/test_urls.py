from importlib import import_module, reload
import sys
from unittest.mock import patch

import pytest

from django.urls import clear_url_caches, reverse
from django.urls.exceptions import NoReverseMatch

from core.tests.helpers import create_response


def reload_urlconf(settings):
    clear_url_caches()
    if settings.ROOT_URLCONF in sys.modules:
        reload(sys.modules[settings.ROOT_URLCONF])
    else:
        import_module(settings.ROOT_URLCONF)


def test_investment_support_directory_feature_off(settings):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = False
    reload_urlconf(settings)

    with pytest.raises(NoReverseMatch):
        reverse('investment-support-directory:home')


def test_investment_support_directory_feature_on(settings):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True
    reload_urlconf(settings)

    assert reverse('investment-support-directory:home')


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_url_redirect_expand_page_on(mock_get_page, client, settings):

    settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] = True
    reload_urlconf(settings)

    mock_get_page.return_value = create_response(
        json_payload={
            'meta': {
                'slug': 'page',
                'languages': [['en-gb', 'English']],
            },
            'page_type': 'InvestInternationalHomePage',
        }
    )

    response = client.get('/international/invest/incoming/foo/')
    assert response.status_code == 302
    assert response.url == '/international/invest/'

    response = client.get('/international/invest/')
    assert response.status_code == 302
    assert response.url == '/international/expand/'

    response = client.get('/international/content/invest/')
    assert response.status_code == 302
    assert response.url == '/international/expand/'

    response = client.get('/international/invest/contact/')
    assert response.status_code == 302
    assert response.url == '/international/expand/contact'

    response = client.get('/international/invest/contact/success/')
    assert response.status_code == 302
    assert response.url == '/international/expand/contact/success'

    response = client.get('/international/content/invest/high-potential-opportunities/')
    assert response.status_code == 302
    assert response.url == '/international/content/expand/high-potential-opportunities'

    response = client.get('/international/content/expand/high-potential-opportunities/')
    assert response.status_code == 302
    assert response.url == '/international/content/expand/#high-potential-opportunities'

    response = client.get('/international/invest/incoming/')
    assert response.status_code == 302
    assert response.url == '/international/expand/'


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_url_redirect_expand_page_off(mock_get_page, client, settings):

    settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] = False
    reload_urlconf(settings)

    mock_get_page.return_value = create_response(
        json_payload={
            'meta': {
                'slug': 'page',
                'languages': [['en-gb', 'English']],
            },
            'page_type': 'InvestInternationalHomePage',
        }
    )

    response = client.get('/international/invest/incoming/foo/')
    assert response.status_code == 302
    assert response.url == '/international/invest/'

    response = client.get('/international/expand/')
    assert response.status_code == 200

    response = client.get('/international/invest/')
    assert response.status_code == 200

    response = client.get('/international/content/invest/')
    assert response.status_code == 302
    assert response.url == '/international/invest/'

    response = client.get('/international/content/expand/')
    assert response.status_code == 302
    assert response.url == '/international/expand/'

    response = client.get('/international/content/invest/high-potential-opportunities/')
    assert response.status_code == 302
    assert response.url == '/international/content/invest/#high-potential-opportunities'

    response = client.get('/international/invest/incoming/')
    assert response.status_code == 302
    assert response.url == '/international/invest/'


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_url_redirect_how_set_up_expand_page_on(mock_get_page, client, settings):

    settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] = True
    settings.FEATURE_FLAGS['HOW_TO_SET_UP_REDIRECT_ON'] = True
    reload_urlconf(settings)

    mock_get_page.return_value = create_response(
        json_payload={
            'meta': {
                'slug': 'page',
                'languages': [['en-gb', 'English']],
            },
            'page_type': 'InternationalGuideLandingPage',
            'guides': [
                {
                    'title': 'Set up guide',
                    'meta': {
                        'languages': [
                            ['en-gb', 'English']
                        ]
                    },
                    'page_type': 'InternationalArticlePage',
                },
            ]
        }
    )

    assert reverse('how-to-set-up-home-expand-redirect')

    response = client.get('/international/content/how-to-setup-in-the-uk/')
    assert response.status_code == 302
    assert response.url == '/international/content/expand/how-to-setup-in-the-uk/'

    response = client.get('/international/content/how-to-setup-in-the-uk/some-set-up-guide/')
    assert response.status_code == 302
    assert response.url == '/international/content/expand/how-to-setup-in-the-uk/some-set-up-guide'


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_url_redirect_how_set_up_invest_page_on(mock_get_page, client, settings):

    settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] = False
    settings.FEATURE_FLAGS['HOW_TO_SET_UP_REDIRECT_ON'] = True
    reload_urlconf(settings)

    mock_get_page.return_value = create_response(
        json_payload={
            'meta': {
                'slug': 'page',
                'languages': [['en-gb', 'English']],
            },
            'page_type': 'InternationalGuideLandingPage',
            'guides': [
                {
                    'title': 'Set up guide',
                    'meta': {
                        'languages': [
                            ['en-gb', 'English']
                        ]
                    },
                    'page_type': 'InternationalArticlePage',
                },
            ]
        }
    )

    assert reverse('how-to-set-up-home-invest-redirect')
    response = client.get('/international/content/how-to-setup-in-the-uk/')
    assert response.status_code == 302
    assert response.url == '/international/content/invest/how-to-setup-in-the-uk/'

    response = client.get('/international/content/how-to-setup-in-the-uk/some-set-up-guide/')
    assert response.status_code == 302
    assert response.url == '/international/content/invest/how-to-setup-in-the-uk/some-set-up-guide'


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_url_redirect_how_set_up_expand_page_off(mock_get_page, client, settings):

    settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] = True
    settings.FEATURE_FLAGS['HOW_TO_SET_UP_REDIRECT_ON'] = False
    reload_urlconf(settings)

    mock_get_page.return_value = create_response(
        json_payload={
            'meta': {
                'slug': 'page',
                'languages': [['en-gb', 'English']],
            },
            'page_type': 'InternationalGuideLandingPage',
            'guides': [
                {
                    'title': 'Set up guide',
                    'meta': {
                        'languages': [
                            ['en-gb', 'English']
                        ]
                    },
                    'page_type': 'InternationalArticlePage',
                },
            ]
        }
    )

    response = client.get('/international/content/how-to-setup-in-the-uk/')
    assert response.status_code == 200

    response = client.get('/international/content/how-to-setup-in-the-uk/some-set-up-guide/')
    assert response.status_code == 200


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_url_redirect_how_set_up_redirect_off(mock_get_page, client, settings):

    settings.FEATURE_FLAGS['EXPAND_REDIRECT_ON'] = False
    settings.FEATURE_FLAGS['HOW_TO_SET_UP_REDIRECT_ON'] = False
    reload_urlconf(settings)

    mock_get_page.return_value = create_response(
        json_payload={
            'meta': {
                'slug': 'page',
                'languages': [['en-gb', 'English']],
            },
            'page_type': 'InternationalGuideLandingPage',
            'guides': [
                {
                    'title': 'Set up guide',
                    'meta': {
                        'languages': [
                            ['en-gb', 'English']
                        ]
                    },
                    'page_type': 'InternationalArticlePage',
                },
            ]
        }
    )

    response = client.get('/international/content/how-to-setup-in-the-uk/')
    assert response.status_code == 200

    response = client.get('/international/content/how-to-setup-in-the-uk/some-set-up-guide/')
    assert response.status_code == 200


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_url_redirect_industries_to_about_uk_page_on(mock_get_page, client, settings):

    settings.FEATURE_FLAGS['INDUSTRIES_REDIRECT_ON'] = True
    reload_urlconf(settings)

    mock_get_page.return_value = create_response(
        json_payload={
            'meta': {
                'slug': 'page',
                'languages': [['en-gb', 'English']],
            },
            'page_type': 'InternationalTopicLandingPage',
            'landing_page_title': 'title',
            'child_pages': [
                {
                    'meta': {
                        'slug': 'page',
                        'languages': [['en-gb', 'English']],
                    },
                    'landing_page_title': 'title',
                    'heading': 'heading'
                }
            ]
        }
    )

    response = client.get('/international/content/industries/')
    assert response.status_code == 302
    assert response.url == '/international/content/about-uk/industries/'

    response = client.get('/international/content/industries/automotive/')
    assert response.status_code == 302
    assert response.url == '/international/content/about-uk/industries/automotive'
    assert reverse('industries-home-to-about-uk-redirect')


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_url_redirect_industries_to_about_uk_page_off(mock_get_page, client, settings):

    settings.FEATURE_FLAGS['INDUSTRIES_REDIRECT_ON'] = False
    reload_urlconf(settings)

    mock_get_page.return_value = create_response(
        json_payload={
            'meta': {
                'slug': 'page',
                'languages': [['en-gb', 'English']],
            },
            'page_type': 'InternationalTopicLandingPage',
            'landing_page_title': 'title',
            'child_pages': [
                {
                    'meta': {
                        'slug': 'page',
                        'languages': [['en-gb', 'English']],
                    },
                    'heading': 'heading'
                }
            ]
        }
    )

    response = client.get('/international/content/industries/')
    assert response.status_code == 200

    response = client.get('/international/content/industries/automotive/')
    assert response.status_code == 200
    with pytest.raises(NoReverseMatch):
        reverse('industries-home-to-about-uk-redirect')
