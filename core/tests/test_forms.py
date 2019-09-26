import pytest

from core import constants
from core.forms import CapitalInvestContactForm, BusinessEnvironmentGuideForm, InternationalRoutingForm


@pytest.fixture
def capital_invest_contact_form_data(captcha_stub):
    return {
        'given_name': 'Thor',
        'family_name': 'Odinson',
        'email_address': 'most_powerful_avenger@avengers.com',
        'phone_number': '01234 567891',
        'country': 'FR',
        'city': 'Asgard',
        'company_name': 'Guardian of the Galaxy',
        'message': 'foobar',
        'g-recaptcha-response': captcha_stub,
        'terms_agreed': True,
    }


@pytest.fixture
def business_environment_form_data(captcha_stub):
    return {
        'given_name': 'Thor',
        'family_name': 'Odinson',
        'email_address': 'most_powerful_avenger@avengers.com',
        'company_name': 'Guardian of the Galaxy',
        'number_of_staff': '1-10',
        'industry': 'ADVANCED_MANUFACTURING',
        'country': 'FR',
        'mostly_interested_in': ['expand'],
        'further_information': True,
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    }


def test_capital_invest_contact_form_required():
    form = CapitalInvestContactForm()

    assert form.is_valid() is False
    assert form.fields['given_name'].required is True
    assert form.fields['family_name'].required is True
    assert form.fields['email_address'].required is True
    assert form.fields['country'].required is True
    assert form.fields['city'].required is False
    assert form.fields['message'].required is True
    assert form.fields['captcha'].required is True
    assert form.fields['terms_agreed'].required is True


def test_capital_invest_contact_form_accept_valid_data(captcha_stub, capital_invest_contact_form_data):
    form = CapitalInvestContactForm(
        data=capital_invest_contact_form_data
    )
    assert form.is_valid()


def test_capital_invest_contact_form_capcha_valid(captcha_stub):
    form = CapitalInvestContactForm({'g-recaptcha-response': captcha_stub})

    form.is_valid()

    assert 'captcha' not in form.errors


def test_capital_invest_contact_form_captcha_invalid():
    form = CapitalInvestContactForm({})

    assert form.is_valid() is False
    assert 'captcha' in form.errors


def test_capital_invest_contact_form_invalid_data(captcha_stub):
    form = CapitalInvestContactForm(
        data={
            'given_name': 'Steve',
            'family_name': 'Rogers',
            'country': 'FR',
            'message': 'foobar',
            'g-recaptcha-response': captcha_stub,
            'terms_agreed': True
        }
    )
    assert form.errors == {'email_address': ['This field is required.']}
    assert form.is_valid() is False


def test_business_environment_form_required():
    form = BusinessEnvironmentGuideForm()

    assert form.fields['given_name'].required is True
    assert form.fields['family_name'].required is True
    assert form.fields['email_address'].required is True
    assert form.fields['company_name'].required is False
    assert form.fields['number_of_staff'].required is False
    assert form.fields['industry'].required is True
    assert form.fields['country'].required is True
    assert form.fields['mostly_interested_in'].required is True
    assert form.fields['further_information'].required is False
    assert form.fields['terms_agreed'].required is True
    assert form.fields['captcha'].required is True


def test_business_environment_serialized_data(business_environment_form_data):
    form = BusinessEnvironmentGuideForm(data=business_environment_form_data)
    form.full_clean()

    data = form.serialized_data

    assert 'given_name' in data
    assert 'family_name' in data
    assert 'email_address' in data
    assert 'company_name' in data
    assert 'number_of_staff' in data
    assert 'industry' in data
    assert 'industry' in data
    assert 'mostly_interested_in' in data
    assert 'further_information' in data
    assert 'terms_agreed' not in data
    assert 'captcha' not in data


def test_business_environment_form_accepts_valid_data(business_environment_form_data):
    form = BusinessEnvironmentGuideForm(data=business_environment_form_data)
    assert form.is_valid()


@pytest.mark.parametrize('value', (True, False,))
def test_routing_forms_capital_invest_feature_flag(value, feature_flags):
    feature_flags['CAPITAL_INVEST_CONTACT_IN_TRIAGE_ON'] = value
    choices = InternationalRoutingForm().fields['choice'].choices

    assert any(value == constants.CAPITAL_INVEST_CONTACT_URL for value, label in choices) is value


@pytest.mark.parametrize('value_one,value_two', [(True, True), (False, False), (True, False), (False, True)])
def test_routing_forms_feature_flag_for_int_routing_form(value_one, value_two, feature_flags):
    feature_flags['CAPITAL_INVEST_CONTACT_IN_TRIAGE_ON'] = value_one
    feature_flags['EXPORTING_TO_UK_ON'] = value_two

    choices = InternationalRoutingForm().fields['choice'].choices

    assert any(value == constants.CAPITAL_INVEST_CONTACT_URL for value, label in choices) is value_one
    assert any(value == constants.EXPORTING_TO_UK_CONTACT_URL for value, label in choices) is value_two
