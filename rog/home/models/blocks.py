from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from django.conf import settings



class ColoredStructBlock(blocks.StructBlock):
    color = blocks.ChoiceBlock(
        choices=settings.COLOR_SCHEMES,
        label='Barva',
    )

    class Meta:
        abstract = True


class ButtonsBlock(blocks.StreamBlock):
    button = blocks.StructBlock(
    [
        # ('style', blocks.ChoiceBlock(
        #     choices = [
        #         ('underlined', 'Samo podčrtan'),
        #         ('normal', 'Z obrobo'),
        #         ('background', 'Z obrobo in ozadjem')
        #     ],
        #     label=_('Stil gumba'),
        # )),
        # ('arrow', blocks.BooleanBlock(default=False, label=_('Gumb s puščico'), required=False)),
        ('text', blocks.CharBlock("Besedilo na gumbu")),
        # ('function', blocks.ChoiceBlock(
        #     choices = [
        #         ('redirect', 'Povezava na stran'),
        #         ('new_story_modal', 'Odpre okno za oddajo nove zgodbe'),
        #     ],
        #     label=_('Funkcija gumba'),
        # )),
        ('page', blocks.PageChooserBlock(required=False, label="Stran")),
    ],
    label="Gumb",)

    class Meta:
        label = "Gumbi"
        icon = 'snippet'


class NewsBlock(blocks.StreamBlock):
    news_page = blocks.PageChooserBlock(required=False, label="Stran", page_type="news.NewsPage")

    class Meta:
        label = "Izpostavljene novice"
        icon = 'snippet'
    

class ModuleBlock(blocks.StreamBlock):
    box_emphasized = blocks.StructBlock(
        [
            ('title', blocks.CharBlock(label="Naslov")),
            ('text', blocks.RichTextBlock(required=False, label="Besedilo")),
            ('buttons', ButtonsBlock(required=False, label="Gumbi")),
        ],
        label="Poudarjeno besedilo z okvirjem",
        template='home/blocks/box_emphasized.html',
        icon='title',
    )
    news_section = ColoredStructBlock(
        [
            ('title', blocks.CharBlock(label="Naslov")),
            ('news', NewsBlock(label="Novice")),
        ],
        label="Izpostavljene novice",
        template='home/blocks/news_section.html',
        icon='title',
    )
    image_embed = ImageChooserBlock(label="Slika", template='home/blocks/image_embed.html')

    class Meta:
        label = 'Modul'
