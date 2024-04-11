from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

# Text Blocks

class HeadingBlock(blocks.CharBlock):
    class Meta:
        icon = 'fa-header'
        form_classname = 'title'
        template = 'blocks/heading_block.html'


class LeadTextBlock(blocks.TextBlock):
    class Meta:
        template = 'blocks/lead_text_block.html'
        icon = 'pilcrow'


class BodyTextBlock(blocks.RichTextBlock):
    class Meta:
        template = 'blocks/body_text_block.html'
        icon = 'code'


# Component Blocks

class ValueCardBlock(blocks.StructBlock):
    icon = ImageChooserBlock(required=False)
    title = blocks.CharBlock()
    description = blocks.TextBlock(required=False)

    class Meta:
        template = 'includes/value_card.html'
        icon = 'pick'

class BlockBlock(blocks.StructBlock):
    icon = ImageChooserBlock()
    background_image = ImageChooserBlock()
    title = blocks.CharBlock()
    url = blocks.PageChooserBlock(required=False, label='URL')

    class Meta:
        label = 'block'
        template = 'blocks/block_block.html'


# Static Blocks

class ContactFormBlock(blocks.StaticBlock):
    class Meta:
        label = 'Contact Form'
        admin_text = f'{label}: Pre-built contact form.'
        icon = 'form'
        template = 'includes/contact_form.html'


# Content Block

class ContentStreamBlock(blocks.StreamBlock):
    heading = HeadingBlock()
    lead_text = LeadTextBlock()
    body_text = BodyTextBlock()
    value_cards = blocks.ListBlock(ValueCardBlock(), template='blocks/card_list.html', icon='pick')
    contact_form = ContactFormBlock()
    raw_html = blocks.RawHTMLBlock(label='Raw HTML', icon='code')



# Section Block

class SectionBlock(blocks.StructBlock):
    section_id = blocks.CharBlock(required=False, label='Section ID', help_text='Used for admin readability & anchor creation (e.g., <section id="section-name">).')
    background_image = ImageChooserBlock(required=False)
    css_classes = blocks.CharBlock(label='Section CSS Classes', required=False, default='text-center py-5', help_text='Add additional predefined CSS Classes for this whole section.')
    custom_css = blocks.CharBlock(label='Section Custom CSS', required=False, help_text='Add inline css to the section tag for this section.')
    container = blocks.BooleanBlock(required=False, default=True)
    content = ContentStreamBlock(required=False)

    class Meta:
        template = 'blocks/section_block.html'


# Main Blocks

class SectionStreamBlock(blocks.StreamBlock):
    section = SectionBlock()
    block_list = blocks.ListBlock(BlockBlock(), template='blocks/block_list_block.html', icon='placeholder')