from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.images import ImageFile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from datetime import datetime, date, time
import json

from wagtail.images.models import Image
from wagtailmedia.models import Media, MediaType

from home import models
from news import models as news_models
from events import models as events_models


class Command(BaseCommand):
    help = "Setup testing data"

    def create_image(self, image_name):
        img_directory = "rog/static/images"
        img_path = f"{img_directory}/{image_name}"
        image_file = ImageFile(open(img_path, 'rb'), name=image_name)
        image = models.CustomImage(title=image_name, file=image_file)
        image.save()
        return image

    def create_media(self, media_name):
        media_directory = "rog/static/images"
        media_path = f"{media_directory}/{media_name}"
        media_file = File(open(media_path, 'rb'), name=media_name)
        media = Media(title=media_name, file=media_file, type=MediaType.VIDEO)
        media.save()
        return media

    def handle(self, *args, **options):

        ## create user
        User = get_user_model()
        user = User.objects.create_superuser("test@test.si", "changeme")
        user.first_name = "Janez"
        user.last_name = "Novak"
        user.prima_id = "5"
        user.save()

        ## stock image
        stock_img_name = "stock-hills.jpg"
        stock_img = self.create_image(stock_img_name)

        ## create pages
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

        # 3D laboratorij
        three_d_lab_img_name = "labs/3D-lab.jpg"
        three_d_lab_img = self.create_image(three_d_lab_img_name)

        three_d_lab_animation_name = "labs/3D-lab.webm"
        three_d_lab_animation = self.create_media(three_d_lab_animation_name)

        three_d_lab = models.LabPage(
            title="3D laboratorij",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            email="3dlab@dolorsit.com",
            phone="041123456",
            link_1="https://www.loremipsum.com",
            link_2="https://www.dolor-sit-amet.com",
            contact_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            thumbnail=three_d_lab_img,
            thumbnail_animation=three_d_lab_animation,
            image=stock_img
        )

        # kovinarski laboratorij
        kovinarski_lab_img_name = "labs/kovinarski-lab.jpg"
        kovinarski_lab_img = self.create_image(kovinarski_lab_img_name)

        kovinarski_lab_animation_name = "labs/kovinarski-lab.webm"
        kovinarski_lab_animation = self.create_media(kovinarski_lab_animation_name)

        kovinarski_lab = models.LabPage(
            title="Kovinarski laboratorij",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            email="kovinarskilab@dolorsit.com",
            phone="041123456",
            link_1="https://www.loremipsum.com",
            link_2="https://www.dolor-sit-amet.com",
            contact_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            thumbnail=kovinarski_lab_img,
            thumbnail_animation=kovinarski_lab_animation,
            image=stock_img
        )

        # kuharski laboratorij
        kuharski_lab_img_name = "labs/kuharski-lab.jpg"
        kuharski_lab_img = self.create_image(kuharski_lab_img_name)

        kuharski_lab_animation_name = "labs/kuharski-lab.webm"
        kuharski_lab_animation = self.create_media(kuharski_lab_animation_name)

        kuharski_lab = models.LabPage(
            title="Kuharski laboratorij",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            email="kuharski-laboratorij@dolorsit.com",
            phone="041123456",
            link_1="https://www.loremipsum.com",
            link_2="https://www.dolor-sit-amet.com",
            contact_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            thumbnail=kuharski_lab_img,
            thumbnail_animation=kuharski_lab_animation,
            image=stock_img
        )

        # lesni laboratorij
        lesni_lab_img_name = "labs/lesni-lab.jpg"
        lesni_lab_img = self.create_image(lesni_lab_img_name)

        lesni_lab_animation_name = "labs/lesni-lab.webm"
        lesni_lab_animation = self.create_media(lesni_lab_animation_name)

        lesni_lab = models.LabPage(
            title="Lesni laboratorij",
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            email="lesnilab@dolorsit.com",
            phone="041123456",
            link_1="https://www.loremipsum.com",
            link_2="https://www.dolor-sit-amet.com",
            contact_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            thumbnail=lesni_lab_img,
            thumbnail_animation=lesni_lab_animation,
            image=stock_img
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
            thumbnail=stock_img
        )

        novica2 = news_models.NewsPage(
            title="Consectetur adipiscing elit",
            short_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            category=newscategory2,
            thumbnail=stock_img
        )

        novica3 = news_models.NewsPage(
            title="Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
            short_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            category=newscategory3,
            thumbnail=stock_img
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
            hero_image=stock_img,
            category=eventscategory1,
            start_time=time(15, 0, 0),
            end_time=time(20, 0, 0),
            start_day = date(2023, 1, 23),
            end_day = date(2023, 1, 23),
            location="Lesni lab"
        )

        event2 = events_models.EventPage(
            title="Consectetur adipiscing elit",
            short_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            hero_image=stock_img,
            category=eventscategory2,
            start_time=time(9, 30, 0),
            end_time=time(10, 30, 0),
            start_day = date(2023, 2, 23),
            end_day = date(2023, 2, 24),
            location="Velika dvorana, Center Rog"
        )

        event3 = events_models.EventPage(
            title="Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
            short_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            hero_image=stock_img,
            category=eventscategory3,
            start_time=time(20, 0, 0),
            end_time=time(21, 0, 0),
            start_day = date(2023, 3, 23),
            end_day = date(2023, 4, 12),
            location=""
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

        lablistpage.add_child(instance=three_d_lab)
        lablistpage.add_child(instance=kovinarski_lab)
        lablistpage.add_child(instance=kuharski_lab)
        lablistpage.add_child(instance=lesni_lab)

        newslistpage.add_child(instance=novica1)
        newslistpage.add_child(instance=novica2)
        newslistpage.add_child(instance=novica3)

        eventslistpage.add_child(instance=event1)
        eventslistpage.add_child(instance=event2)
        eventslistpage.add_child(instance=event3)

        # add pages to header
        meta_settings = models.MetaSettings()
        meta_settings.organization_name = "Center Rog"
        meta_settings.organization_address = "Trubarjeva 72"
        meta_settings.organization_postal_number = 1000
        meta_settings.organization_post = "Ljubljana"
        meta_settings.organization_country = "Slovenija"
        meta_settings.organization_email = "info@center-rog.si"
        meta_settings.organization_phone_number = "+386 1 251 6301"
        meta_settings.organization_working_hours = json.dumps([
            {
                "type": "time",
                "value": {
                    "day": "pon - pet",
                    "start_time": "08:00:00",
                    "end_time": "20:00:00",
                }
            },
            {
                "type": "time",
                "value": {
                    "day": "sob",
                    "start_time": "10:00:00",
                    "end_time": "15:00:00",
                }
            },
        ])

        meta_settings.header_links = json.dumps([
            {
                "type": "page_link",
                "value": {
                    "page": newslistpage.pk
                }
            },
            {
                "type": "page_link",
                "value": {
                    "page": eventslistpage.pk
                }
            },
            {
                "type": "page_link",
                "value": {
                    "page": studiolistpage.pk
                }
            },
            {
                "type": "page_link",
                "value": {
                    "page": marketstorelistpage.pk
                }
            },
            {
                "type": "page_link",
                "value": {
                    "page": residencelistpage.pk
                }
            },
            {
                "type": "page_link",
                "value": {
                    "page": lablistpage.pk
                }
            },
        ])

        meta_settings.save()

        ## create homepage models
        homepage.body = json.dumps([
            {
                "type": "bulletin_board",
                "value": {
                    "title": "Dobrodošli v Centru Rog!",
                    "notice": "To je obvestilo."
                }
            },
            {
                "type": "labs_section",
                "value": {
                    "title": "Laboratoriji",
                    "intro_text": "V pritličju in v drugem nadstropju bo 7 proizvodnih laboratorijev oziroma delavnic, tako takšnih s sodobnimi, računalniško vodenimi tehnologijami kot takšnih za tradicionalnejše sodobnimi, računalniško tehnike.",
                    "labs": [ three_d_lab.id, kovinarski_lab.id, kuharski_lab.id, lesni_lab.id ]
                }
            },
            {
                "type": "white_list",
                "value": {
                    "title": "Naslov sekcije",
                    "intro_text": "V pritličju in v drugem nadstropju bo 7 proizvodnih laboratorijev oziroma delavnic, tako takšnih s sodobnimi, računalniško vodenimi tehnologijami kot takšnih za tradicionalnejše sodobnimi, računalniško tehnike.",
                    "links": [
                        {
                            "type": "link",
                            "value": {
                                "url": "https://www.google.com",
                                "text": "Google"
                            }
                        },
                        {
                            "type": "link",
                            "value": {
                                "url": "https://www.google.com",
                                "text": "Povezava"
                            }
                        },
                        {
                            "type": "link",
                            "value": {
                                "url": "https://www.google.com",
                                "text": "Povezava z malo daljšim imenom"
                            }
                        },
                        {
                            "type": "link",
                            "value": {
                                "url": "https://www.google.com",
                                "text": "Google"
                            }
                        },
                        {
                            "type": "link",
                            "value": {
                                "url": "https://www.google.com",
                                "text": "Google"
                            }
                        },
                        {
                            "type": "link",
                            "value": {
                                "url": "https://www.google.com",
                                "text": "Google"
                            }
                        },
                        {
                            "type": "link",
                            "value": {
                                "url": "https://www.google.com",
                                "text": "Še ena povezava s še malo daljšim imenom"
                            }
                        },
                        {
                            "type": "link",
                            "value": {
                                "url": "https://www.google.com",
                                "text": "Google"
                            }
                        },
                        {
                            "type": "link",
                            "value": {
                                "url": "https://www.google.com",
                                "text": "Google"
                            }
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
            },
            {
                "type": "gallery",
                "value": {
                    "title": "Galerija",
                    "color": "light-blue",
                    "gallery": [stock_img.id, stock_img.id, stock_img.id]
                }
            },
            {
                "type": "studios",
                "value": {
                    "title": "Naslov sekcije",
                    "intro_text": "V pritličju in v drugem nadstropju bo 7 proizvodnih laboratorijev oziroma delavnic, tako takšnih s sodobnimi, računalniško vodenimi tehnologijami kot takšnih za tradicionalnejše sodobnimi, računalniško tehnike.",
                    "studios": [studio1.pk, studio2.pk]
                }
            },
            {
                "type": "marketplace",
                "value": {
                    "title": "Tržnica",
                    "intro_text": "V pritličju in v drugem nadstropju bo 7 proizvodnih laboratorijev oziroma delavnic, tako takšnih s sodobnimi, računalniško vodenimi tehnologijami kot takšnih za tradicionalnejše sodobnimi, računalniško tehnike.",
                    "markets": [
                        {
                            "color": "pink",
                            "market": market1.pk
                        },
                        {
                            "color": "orange",
                            "market": market2.pk
                        },
                        {
                            "color": "dark-blue",
                            "market": market3.pk
                        },
                        {
                            "color": "purple",
                            "market": market1.pk
                        },
                        {
                            "color": "dark-green",
                            "market": market2.pk
                        },
                        {
                            "color": "light-green",
                            "market": market3.pk
                        }
                    ]
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
                "type": "image_embed",
                "value": {
                    "color": "dark-green",
                    "text": "Tovarna Rog, simbol kultnih Rogovih koles, je najpomembnejši del industrijske kulturne dediščine 20. stoletja v Ljubljani. S projektom prenove in v njeni prvotni funkciji: v prihodnje bo delovala kot javni proizvodni prostor 21. stoletja, namenjen kulturnemu in kreativnemu sektorju, s poudarkom na izdelovalništvu, uporabnih umetnostih in oblikovanju.",
                    "image": stock_img.id,
                }
            },
            {
                "type": "colored_text",
                "value": {
                    "color": "light-blue",
                    "text": "Tovarna Rog, simbol kultnih Rogovih koles, je najpomembnejši del industrijske kulturne dediščine 20. stoletja v Ljubljani. S projektom prenove in v njeni prvotni funkciji: v prihodnje bo delovala kot javni proizvodni prostor 21. stoletja, namenjen kulturnemu in kreativnemu sektorju, s poudarkom na izdelovalništvu, uporabnih umetnostih in oblikovanju.",
                }
            },
            {
                "type": "colored_text",
                "value": {
                    "color": "red",
                    "title": "Naslov sekcije",
                    "text": "Tovarna Rog, simbol kultnih Rogovih koles, je najpomembnejši del industrijske kulturne dediščine 20. stoletja v Ljubljani. S projektom prenove in v njeni prvotni funkciji: v prihodnje bo delovala kot javni proizvodni prostor 21. stoletja, namenjen kulturnemu in kreativnemu sektorju, s poudarkom na izdelovalništvu, uporabnih umetnostih in oblikovanju.",
                    "image": stock_img.id,
                    "image_position": "align-left"
                }
            },
            {
                "type": "residents_section",
                "value": {
                    "title": "Naslov sekcije",
                    "intro_text": "Tovarna Rog, simbol kultnih Rogovih koles, je najpomembnejši del industrijske kulturne dediščine 20. stoletja v Ljubljani. S projektom prenove in v njeni prvotni funkciji: v prihodnje bo delovala kot javni proizvodni prostor 21. stoletja, namenjen kulturnemu in kreativnemu sektorju, s poudarkom na izdelovalništvu, uporabnih umetnostih in oblikovanju.",
                    "residents": [
                        rezidenca1.pk,
                        rezidenca2.pk
                    ]
                }
            },
        ])

        homepage.save()
