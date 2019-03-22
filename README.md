# great-international-ui
[Great International UI](https://www.directory.exportingisgreat.gov.uk/)

[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]

---

## Requirements

[Python 3.6](https://www.python.org/downloads/release/python-360/)

## Local installation

    $ git clone https://github.com/uktrade/great-international-ui
    $ cd great-international-ui
    $ make

## Directory Forms

Form submissions are powered by [directory-forms-api](https://github.com/uktrade/directory-forms-api). Set that up locally then generate a API client [here](http://forms.trade.great:8011/admin/client/client/) and add the following entries to your `conf/.env` file.

| Environment variable                                  | Notes                             |
| ----------------------------------------------------- | --------------------------------- |
| DIRECTORY_FORMS_API_API_KEY                           | Populate from client `access_key` |
| DIRECTORY_FORMS_API_SENDER_ID                         | Populate from client `identifier` |

## Debugging

### Setup debug environment

    $ make debug

### Run debug webserver

    $ make debug_webserver

### Run debug tests

    $ make debug_test

## CSS development

### Requirements
[node](https://nodejs.org/en/download/)
[SASS](http://sass-lang.com/)
[gulp](https://gulpjs.com/)

	$ npm install  # to install yarn
	$ yarn install # use yarn for installing all other javascript dependencies

### Update CSS under version control

	$ make compile_css

### Rebuild the CSS files when the scss file changes

	$ make watch_css

## Session

Signed cookies are used as the session backend to avoid using a database. We therefore must avoid storing non-trivial data in the session, because the browser will be exposed to the data.

## Cookies

To be able to test cookies locally add the following to your `/etc/hosts`:

```
127.0.0.1       international.trade.great
```

Then run the server and visit `international.trade.great:8012`


[circle-ci-image]: https://circleci.com/gh/uktrade/great-international-ui/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/great-international/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/great-international-ui/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/great-international-ui
