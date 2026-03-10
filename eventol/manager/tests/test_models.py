import pytest

from manager.models import Activity


@pytest.mark.django_db
def test_event_model(event1):
    assert str(event1) == event1.name


@pytest.mark.django_db
def test_activity_external_link_field(event1, event_user1):
    """Test that Activity model accepts external_link field."""
    activity = Activity.objects.create(
        event=event1,
        owner=event_user1,
        title='Test Activity',
        long_description='Test description',
        abstract='Test abstract',
        external_link='https://example.com/presentation',
    )
    assert activity.external_link == 'https://example.com/presentation'


@pytest.mark.django_db
def test_activity_external_link_can_be_blank(event1, event_user1):
    """Test that external_link field can be blank/null."""
    activity = Activity.objects.create(
        event=event1,
        owner=event_user1,
        title='Test Activity without link',
        long_description='Test description',
        abstract='Test abstract',
    )
    assert activity.external_link is None or activity.external_link == ''
