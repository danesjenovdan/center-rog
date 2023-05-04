from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from datetime import datetime, date, time

import json

from home import models
from news import models as news_models
from events import models as events_models


class Command(BaseCommand):
    help = "Setup testing data"

    def handle(self, *args, **options):

        homepage = models.HomePage.objects.get(
            title="Home"
        ).specific

        studiolistpage = models.StudioListPage(
            title="Seznam studiev",
            intro_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        )

        studio1 = models.StudioPage(
            title="Plesni studio",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            email="lorem-ipsum@dolorsit.com",
            phone="041123456",
            link_1="https://www.loremipsum.com",
            link_2="https://www.dolor-sit-amet.com",
            contact_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        )

        studio2 = models.StudioPage(
            title="Slikarski studio",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            email="lorem-ipsum@dolorsit.com",
            link_1="https://www.loremipsum.com",
            link_2="https://www.dolor-sit-amet.com",
            link_3="https://www.dolor-sit-amet.com",
            contact_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        )

        marketstorelistpage = models.MarketStoreListPage(
            title="Market",
            intro_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        )

        market1 = models.MarketStorePage(
            title="Restavracija Njam",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            email="lorem-ipsum@dolorsit.com",
            phone="041123456",
            link_1="https://www.loremipsum.com",
            link_2="https://www.dolor-sit-amet.com",
            contact_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        )

        market2 = models.MarketStorePage(
            title="Restavracija Ham",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            email="lorem-ipsum@dolorsit.com",
            phone="041123456",
            link_1="https://www.loremipsum.com",
            link_2="https://www.dolor-sit-amet.com",
            contact_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        )

        market3 = models.MarketStorePage(
            title="Kavarna pri Lizi",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            email="lorem-ipsum@dolorsit.com",
            phone="041123456",
            link_1="https://www.loremipsum.com",
            link_2="https://www.dolor-sit-amet.com",
            contact_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        )

        residencelistpage = models.ResidenceListPage(
            title="Rezidence",
            intro_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        )

        rezidenca1 = models.ResidencePage(
            title="Janez Novak",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            email="janez.novak@dolorsit.com",
            phone="041123456",
            link_1="https://www.loremipsum.com",
            link_2="https://www.dolor-sit-amet.com",
            contact_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        )

        rezidenca2 = models.ResidencePage(
            title="Marija Lah",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            email="marijalah@dolorsit.com",
            phone="041123456",
            link_1="https://www.loremipsum.com",
            link_2="https://www.dolor-sit-amet.com",
            contact_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        )

        lablistpage = models.LabListPage(
            title="Laboratoriji",
            intro_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        )

        lab1 = models.LabPage(
            title="Lesni laboratorij",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            email="lesnilab@dolorsit.com",
            phone="041123456",
            link_1="https://www.loremipsum.com",
            link_2="https://www.dolor-sit-amet.com",
            contact_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        )

        lab2 = models.LabPage(
            title="Kovinarski laboratorij",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            email="kovinarskilab@dolorsit.com",
            phone="041123456",
            link_1="https://www.loremipsum.com",
            link_2="https://www.dolor-sit-amet.com",
            contact_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        )

        newslistpage = news_models.NewsListPage(
            title="Novice"
        )

        newscategory1 = news_models.NewsCategory(
            name="Dogajanje v Centru Rog",
            color_scheme="red"
        )

        newscategory1.save()

        newscategory2 = news_models.NewsCategory(
            name="Aktualno",
            color_scheme="dark-blue"
        )

        newscategory2.save()

        newscategory3 = news_models.NewsCategory(
            name="Novo",
            color_scheme="dark-green"
        )

        newscategory3.save()

        novica1 = news_models.NewsPage(
            title="Lorem ipsum dolor sit amet",
            short_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            category=newscategory1,
        )

        novica2 = news_models.NewsPage(
            title="Consectetur adipiscing elit",
            short_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            category=newscategory2,
        )

        novica3 = news_models.NewsPage(
            title="Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
            short_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            category=newscategory3,
        )

        eventslistpage = events_models.EventListPage(
            title="Dogodki"
        )

        eventscategory1 = events_models.EventCategory(
            name="Delavnica",
            color_scheme="pink"
        )

        eventscategory1.save()

        eventscategory2 = events_models.EventCategory(
            name="Nov rezident",
            color_scheme="light-green"
        )

        eventscategory2.save()

        eventscategory3 = events_models.EventCategory(
            name="Izobraževanje",
            color_scheme="yellow"
        )

        eventscategory3.save()

        event1 = events_models.EventPage(
            title="Lorem ipsum dolor sit amet",
            short_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            category=eventscategory1,
            start_time=time(15, 0, 0),
            end_time=time(20, 0, 0)
        )

        event2 = events_models.EventPage(
            title="Consectetur adipiscing elit",
            short_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            category=eventscategory2,
            start_time=time(9, 30, 0),
            end_time=time(10, 30, 0)
        )

        event3 = events_models.EventPage(
            title="Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
            short_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            category=eventscategory3,
            start_time=time(20, 0, 0),
            end_time=time(21, 0, 0)
        )

        homepage.add_child(instance=studiolistpage)
        homepage.add_child(instance=marketstorelistpage)
        homepage.add_child(instance=residencelistpage)
        homepage.add_child(instance=lablistpage)
        homepage.add_child(instance=newslistpage)
        homepage.add_child(instance=eventslistpage)

        studiolistpage.add_child(instance=studio1)
        studiolistpage.add_child(instance=studio2)

        marketstorelistpage.add_child(instance=market1)
        marketstorelistpage.add_child(instance=market2)
        marketstorelistpage.add_child(instance=market3)

        residencelistpage.add_child(instance=rezidenca1)
        residencelistpage.add_child(instance=rezidenca2)

        lablistpage.add_child(instance=lab1)
        lablistpage.add_child(instance=lab2)

        newslistpage.add_child(instance=novica1)
        newslistpage.add_child(instance=novica2)
        newslistpage.add_child(instance=novica3)

        eventslistpage.add_child(instance=event1)
        eventslistpage.add_child(instance=event2)
        eventslistpage.add_child(instance=event3)

        homepage.body = json.dumps([
            {
                "type": "bulletin_board",
                "value": {
                    "title": "Dobrodošli v Centru Rog!",
                    "notice": "To je obvestilo."
                }
            },
            {
                "type": "news_section",
                "value": {
                    "title": "Izpostavljene novice",
                    "exposed_news": [
                        {
                            "type": "news_page",
                            "value": novica1.pk
                        },
                        {
                            "type": "news_page",
                            "value": novica2.pk
                        },
                        {
                            "type": "news_page",
                            "value": novica3.pk
                        }
                    ]
                }
            },
            {
                "type": "events_section",
                "value": {
                    "title": "Izpostavljeni dogodki",
                    "exposed_events": [
                        {
                            "type": "event",
                            "value": event1.pk
                        },
                        {
                            "type": "event",
                            "value": event2.pk
                        },
                        {
                            "type": "event",
                            "value": event3.pk
                        }
                    ]
                }
            }
        ])

        homepage.save()