from django import template
from django.utils import timezone
from events.models import EventPage
from home.models import StudioPage
from news.models import NewsPage

register = template.Library()


@register.filter
def with_up_to_15_upcoming_events(field):
    if not field:
        return []

    event_ids = set()
    events = []

    for event in field:
        event_ids.add(event.value.id)
        events.append(event.value)

    today = timezone.now().date()
    num_other_events = 15 - len(events)
    other_events = (
        EventPage.objects.live()
        .exclude(id__in=event_ids)
        .filter(start_day__gte=today)
        .order_by("start_day", "start_time")[:num_other_events]
    )

    for event in other_events:
        events.append(event)

    return events


@register.filter
def with_up_to_15_recent_news(field):
    if not field:
        return []

    news_ids = set()
    news = []

    for news_item in field:
        news_ids.add(news_item.value.id)
        news.append(news_item.value)

    num_other_news = 15 - len(news)
    other_news = (
        NewsPage.objects.live()
        .exclude(id__in=news_ids)
        .order_by("-first_published_at")[:num_other_news]
    )

    for news_item in other_news:
        news.append(news_item)

    return news


@register.filter
def with_up_to_15_random_studios(field):
    if not field:
        return []

    studio_ids = set()
    studios = []

    for studio in field:
        studio_ids.add(studio.id)
        studios.append(studio)

    num_other_studios = 15 - len(studios)
    other_studios = (
        StudioPage.objects.live()
        .exclude(id__in=studio_ids)
        .order_by("?")[:num_other_studios]
    )

    for studio in other_studios:
        studios.append(studio)

    return studios
