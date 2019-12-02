import pytest
from directory_constants import choices

from euexit import forms


@pytest.fixture
def international_contact_form_data(captcha_stub):
    return {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'country': choices.COUNTRIES_AND_TERRITORIES[1][0],
        'city': 'London',
        'comment': 'hello',
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    }


def test_contact_form_set_field_attributes():
    form_one = forms.InternationalContactForm(
        field_attributes={},
        ingress_url='http://www.ingress.com',
        disclaimer='disclaim',
    )
    form_two = forms.InternationalContactForm(
        field_attributes={
            'first_name': {
                'label': 'Your given name',
            },
            'last_name': {
                'label': 'Your family name'
            }
        },
        ingress_url='http://www.ingress.com',
        disclaimer='disclaim',
    )

    assert form_one.fields['first_name'].label is None
    assert form_one.fields['last_name'].label is None
    assert form_one.fields['terms_agreed'].widget.label.endswith('disclaim')
    assert form_two.fields['first_name'].label == 'Your given name'
    assert form_two.fields['last_name'].label == 'Your family name'
    assert form_two.fields['terms_agreed'].widget.label.endswith('disclaim')


@pytest.mark.parametrize(
    'country_name,form_is_valid,expected_error',
    (
        (choices.COUNTRIES_AND_TERRITORIES[2][0], True, None),
        ('HK', True, None),
        ('AE-AJ', False, {'country': ['Select a valid choice. AE-AJ is not one of the available choices.']}),
    )
)
def test_international_contact_form_serialize(captcha_stub, country_name, form_is_valid, expected_error):
    form = forms.InternationalContactForm(
        field_attributes={},
        ingress_url='http://www.ingress.com',
        disclaimer='disclaim',
        data={
            'first_name': 'test',
            'last_name': 'example',
            'email': 'test@example.com',
            'organisation_type': 'COMPANY',
            'company_name': 'thing',
            'country': country_name,
            'city': 'London',
            'comment': 'hello',
            'terms_agreed': True,
            'g-recaptcha-response': captcha_stub,
        }
    )

    assert form.is_valid() is form_is_valid
    if form_is_valid:
        assert form.serialized_data == {
            'first_name': 'test',
            'last_name': 'example',
            'email': 'test@example.com',
            'organisation_type': 'COMPANY',
            'company_name': 'thing',
            'country': country_name,
            'city': 'London',
            'comment': 'hello',
            'ingress_url': 'http://www.ingress.com',
        }
    if expected_error:
        assert form.errors == expected_error
