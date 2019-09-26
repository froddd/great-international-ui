from django.conf.urls import url

from core.views import QuerystringRedirectView

redirects = [
    url(
        r'^international/eu-exit-news/contact/$',
        QuerystringRedirectView.as_view(pattern_name='brexit-international-contact-form'),
        name='eu-exit-international-contact-form'
    ),
    url(
        r'^international/eu-exit-news/contact/success/$',
        QuerystringRedirectView.as_view(pattern_name='brexit-international-contact-form-success'),
        name='eu-exit-international-contact-form-success'
    ),
    url(
        r'^international/content/industries/advanced-manufacturing/$',
        QuerystringRedirectView.as_view(pattern_name=''),
        name='advanced-manufacturing-redirect'
    ),
    url(
        r'^international/content/about-uk/industries/advanced-manufacturing/$',
        QuerystringRedirectView.as_view(pattern_name=''),
        name='advanced-manufacturing-redirect'
    ),
]
