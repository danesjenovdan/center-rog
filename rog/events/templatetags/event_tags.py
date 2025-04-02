from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def can_user_register_on_event(context):

    user = context.request.user
    event_page = context.get("page")
    free_places = context.get("free_places")
    print("event tag", user, event_page)

    is_registaration_enabled = not (
        (event_page.number_of_places > 0) and (free_places < 1)
    )
    print("free_places", free_places)
    print("event_page.number_of_places", event_page.number_of_places)
    print("is_registaration_enabled", is_registaration_enabled)
    print("event_page.can_register(user)", event_page.can_register(user))

    return event_page.can_register(user) and is_registaration_enabled
