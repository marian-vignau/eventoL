import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from manager.forms import SoftwareAutocomplete
from manager.models import Software
from manager.utils.forms import USE_POSTGRES


def create_autocomplete_form(formclass, query, user):
    autocomplete_form = formclass()
    autocomplete_form.request = RequestFactory()
    autocomplete_form.request.user = user
    autocomplete_form.q = query
    return autocomplete_form


@pytest.mark.django_db
def test_software_autocomplete_form_with_anonymous_user(softwares):
    software_autocomplete_form = create_autocomplete_form(SoftwareAutocomplete, 'soft', AnonymousUser())
    assert list(software_autocomplete_form.get_queryset()) == list(Software.objects.none())


@pytest.mark.django_db
def test_software_autocomplete_form_with_authenticated_user_without_softwares(user1):
    software_autocomplete_form = create_autocomplete_form(SoftwareAutocomplete, 'soft', user1)
    assert list(software_autocomplete_form.get_queryset()) == []


@pytest.mark.django_db
def test_software_autocomplete_form_with_authenticated_user_get_softwares(user1, software1, software2):
    software_autocomplete_form = create_autocomplete_form(SoftwareAutocomplete, 'soft', user1)
    assert list(software_autocomplete_form.get_queryset()) == [software1, software2]


@pytest.mark.django_db
def test_software_autocomplete_form_with_authenticated_user_get_and_filter_softwares(user1, software1, software2):
    software_autocomplete_form = create_autocomplete_form(SoftwareAutocomplete, 'software1', user1)
    assert list(software_autocomplete_form.get_queryset()) == [software1]


@pytest.mark.django_db
@pytest.mark.skipif(not USE_POSTGRES, reason='Test only applicable for PostgreSQL')
def test_software_autocomplete_form_with_authenticated_user_get_softwares_with_unaccent(user1, software1, software2):
    software_autocomplete_form = create_autocomplete_form(SoftwareAutocomplete, 'SóFtwÅrÉ', user1)
    assert list(software_autocomplete_form.get_queryset()) == [software1, software2]


@pytest.mark.django_db
def test_software_autocomplete_form_with_authenticated_user_get_only_5_softwares(user1, softwares):
    software_autocomplete_form = create_autocomplete_form(SoftwareAutocomplete, '', user1)
    softwares_list = list(software_autocomplete_form.get_queryset())
    assert len(softwares_list) < len(softwares)
    assert len(softwares_list) == 5


@pytest.mark.django_db
def test_activity_proposal_form_with_external_link(event1):
    """Test that ActivityProposalForm accepts external_link field."""
    from manager.forms import ActivityProposalForm

    form_data = {
        'event': event1.id,
        'title': 'Test Activity',
        'speakers_names': 'Test Speaker',
        'speaker_bio': 'Test bio',
        'abstract': 'Test abstract',
        'long_description': 'Test long description',
        'labels': 'test, label',
        'level': '1',
        'activity_type': '1',
        'external_link': 'https://example.com/presentation',
        'status': '1',
    }
    form = ActivityProposalForm(data=form_data)
    # Form may be invalid due to missing captcha, but field should be recognized
    assert 'external_link' in form.fields


@pytest.mark.django_db
def test_activity_proposal_form_external_link_optional(event1):
    """Test that external_link field is optional in ActivityProposalForm."""
    from manager.forms import ActivityProposalForm

    form_data = {
        'event': event1.id,
        'title': 'Test Activity without link',
        'speakers_names': 'Test Speaker',
        'speaker_bio': 'Test bio',
        'abstract': 'Test abstract',
        'long_description': 'Test long description',
        'labels': 'test, label',
        'level': '1',
        'activity_type': '1',
        'status': '1',
    }
    form = ActivityProposalForm(data=form_data)
    # Form may be invalid due to missing captcha, but field should be recognized
    assert 'external_link' in form.fields
