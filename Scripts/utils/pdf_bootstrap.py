import reportlab.rl_config
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate

from constants import *
from utils.logger import get_logger

logger = get_logger(__name__)

reportlab.rl_config.warnOnMissingFontGlyphs = 0

# Import the font 'CAMBRIA' to display Vietnamese
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('UVN', os.path.join(FONTS_DIR, "cambria.ttc")))
pdfmetrics.registerFont(TTFont('UVNB', os.path.join(FONTS_DIR, "cambriab.ttf")))
pdfmetrics.registerFont(TTFont('UVNI', os.path.join(FONTS_DIR, "cambriai.ttf")))
pdfmetrics.registerFont(TTFont('UVNZ', os.path.join(FONTS_DIR, "cambriaz.ttf")))
pdfmetrics.registerFontFamily('Cambria', normal='UVN', bold='UVNB', italic='UVNI', boldItalic='UVNZ')


def createStyles():
    """
        Usage: createStyles()
        This function initializes all necessary document styles for the final output pdf
        Params(0): No param
    """

    Styles = getSampleStyleSheet()

    # logo text + signature
    Styles.add(ParagraphStyle(name='Signature Style',
                              fontName='UVNB', fontSize=10, alignment=TA_RIGHT, rightIndent=10))

    # Document title
    Styles.add(ParagraphStyle(name='Title Style',
                              fontName='UVNB', fontSize=16, alignment=TA_CENTER, spaceAfter=3 * LINE_SPACING,
                              spaceBefore=3 * LINE_SPACING))

    # Document body text
    Styles.add(ParagraphStyle(name='Body Style',
                              fontName='UVNI', fontSize=12, leading=16, alignment=TA_JUSTIFY, spaceAfter=LINE_SPACING))

    # Document body text
    Styles.add(ParagraphStyle(name='Body Right Style',
                              fontName='UVNI', fontSize=12, leading=16, alignment=TA_RIGHT, spaceAfter=LINE_SPACING))

    # Document body text
    Styles.add(ParagraphStyle(name='Body Center Style',
                              fontName='UVNI', fontSize=12, leading=16, alignment=TA_CENTER, spaceAfter=LINE_SPACING))

    # Document body text with italic
    Styles.add(ParagraphStyle(name='Italic Body Style',
                              fontName='UVNI', fontSize=12, alignment=TA_JUSTIFY, spaceAfter=LINE_SPACING))

    # Heading I
    Styles.add(ParagraphStyle(name='Heading I Style',
                              fontName='UVNB', fontSize=12, alignment=TA_JUSTIFY, spaceBefore=2 * LINE_SPACING,
                              spaceAfter=2 * LINE_SPACING))

    # Table Heading
    Styles.add(ParagraphStyle(name='Table Heading Style',
                              fontName='UVNB', fontSize=12, leading=16, alignment=TA_CENTER))

    # Table Cell
    Styles.add(ParagraphStyle(name='Table Cell Style',
                              fontName='UVNI', fontSize=12, leading=16))

    # LoM Body
    Styles.add(ParagraphStyle(name='LoM Body Style',
                              fontName='UVN', fontSize=12, alignment=TA_JUSTIFY, spaceAfter=LINE_SPACING,
                              firstLineIndent=28, leading=20))

    return Styles


def newLine(story, styles, nb_lines):
    """
        Usage: newLine(Story, nbLines)
        This function makes several empty lines in the current story of the output pdf
        Params(2):
            Story: The current reportlab story
            nbLines: The number of empty lines to make

    """
    for _ in range(nb_lines):
        story.append(Paragraph('', styles['Body Style']))


def make_tabs(nb_tabs):
    return '&nbsp;' * nb_tabs


def money_processing(raw_value):
    """
        Usage: moneyProcessing(candidate, key)
        This function transform an integer like 100000 into a "money" form like "100.000 đồng"
        Params(2):
            candidate:      The csv row w.r.t a candidate
            key:            The field to get
    """
    transformed_value = ""
    if len(raw_value) >= 7:
        l = len(raw_value)
        transformed_value = raw_value[0:-6] + '.' + raw_value[l - 6:l]
    if len(raw_value) >= 5:
        l = len(raw_value)
        transformed_value = raw_value[0:-3] + '.' + raw_value[l - 3:l]
    if transformed_value != '' and transformed_value != '0':
        transformed_value += u' đồng'
    return transformed_value


def get_doc_template(path, title):
    return SimpleDocTemplate(path, papersize=A4,
                             rightMargin=RIGHT_MARGIN, leftMargin=LEFT_MARGIN,
                             topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN,
                             title=title, author='DH\'s pdf generator v1.0', )