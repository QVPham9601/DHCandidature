# !/user/local/bin/python2.7
# -*- coding: utf-8 -*-

############### ----------IMPORT---------- ###############
import traceback

import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, Spacer, Table, PageBreak
from reportlab.platypus.flowables import Image as Flowable_Image

from constants import *
from utils.common import download_file, remove_if_exist
from utils.logger import get_logger
from utils.pdf_bootstrap import createStyles, newLine, make_tabs, money_processing, get_doc_template
from utils.unicode_utils import to_ascii

logger = get_logger(__name__)

reportlab.rl_config.warnOnMissingFontGlyphs = 0

# Import the font 'CAMBRIA' to display Vietnamese
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('UVN', os.path.join(FONTS_DIR, "cambria.ttc")))
pdfmetrics.registerFont(TTFont('UVNB', os.path.join(FONTS_DIR, "cambriab.ttf")))
pdfmetrics.registerFont(TTFont('UVNI', os.path.join(FONTS_DIR, "cambriai.ttf")))
pdfmetrics.registerFont(TTFont('UVNZ', os.path.join(FONTS_DIR, "cambriaz.ttf")))
pdfmetrics.registerFontFamily('Cambria', normal='UVN', bold='UVNB', italic='UVNI', boldItalic='UVNZ')

from PIL import Image as PIL_Image  # Import PIL to read image files
from PyPDF2.utils import PdfReadError
from PyPDF2 import PdfFileMerger, PdfFileReader  # Import pypdf2 to merge pdf file
import os

############### ----------END OF IMPORT---------- ###############

############### ----------LOCAL FUNCTIONS---------- ###############

DOC_STYLES = createStyles()


def get_field(candidate, key, is_heading=False):
    """
        Usage: get(candidate, key, is_heading=False)
        This function returns the column "key" of the candidate "candidate"
        Params(3):
            candidate:      The csv row w.r.t a candidate
            key:            The field to get
            is_heading:     True if this is the heading row of the csv
    """

    if key == 'NgaySinh' and is_heading:
        return "Ngày sinh"

    # 'DiaChiSinh' and 'DiaChiTru' are combinations of 'SoNhaDuong', 'QuanHuyen' and 'TinhThanh'
    if key == 'DiaChiSinh':
        if not is_heading:
            return candidate[INDEX_OF_KEY['SoNhaDuongSinh']] + ", " + candidate[INDEX_OF_KEY['QuanHuyenSinh']] + ", " + \
                   candidate[INDEX_OF_KEY['TinhThanhSinh']]
        else:
            return "Địa chỉ hiện tại"
    if key == 'DiaChiTru':
        if not is_heading:
            return candidate[INDEX_OF_KEY['SoNhaDuongTru']] + ", " + candidate[INDEX_OF_KEY['QuanHuyenTru']] + ", " + \
                   candidate[INDEX_OF_KEY['TinhThanhTru']]
        else:
            return "Địa chỉ gia đình"
    return candidate[INDEX_OF_KEY[key]]


def get_pdf_basename(candidate, candidate_idx):
    '''
        Usage: buildPdfName(candidate, index)
        This function builds the name for the output pdf, which is Schoolname + _ + Candidate's fullname + _ + index
        Params(2):
            candidate:      The csv row w.r.t a candidate
            index:          The order of this candidate's row in the csv file
    '''
    school_code = SCHOOL_CODE_ALL[get_field(candidate, 'Truong')]
    candidate_name = to_ascii(get_field(candidate, 'HoVaTen'))
    return f"{school_code}_{candidate_name}_{candidate_idx}"


def create_logo(school):
    '''
        This function creates logo and logo text for some pdf pages.
    '''
    # For DH Singapore
    # Names changed as this year CNHN and KTLHCM are also for DH France
    if SCHOOL_CODE_ALL[school] in ['CNHN_1', 'KTLHCM_1']:
        # read image and put to flowable object
        logo_img = PIL_Image.open(os.path.join(LOGO_DIR, 'logo_dong_hanh_sing.png'))
        imsize = logo_img.size
        imw = float(imsize[0]) * .09
        imh = float(imsize[1]) * .09
        logo_img = Flowable_Image(os.path.join(LOGO_DIR, 'logo_dong_hanh_sing.png'), imw, imh)
        logo_img.hAlign = 'LEFT'

        # create DH info
        logo_text = []
        logo_text.append(Paragraph('Quỹ học bổng Đồng Hành Singapore', DOC_STYLES['Signature Style']))
        logo_text.append(Paragraph('Website: www.donghanh.net', DOC_STYLES['Signature Style']))
        logo_text.append(Paragraph('Email: contact@donghanh.net', DOC_STYLES['Signature Style']))

        return logo_img, logo_text

    elif SCHOOL_CODE_ALL[school] in ['CTHO']:
        # read image and put to flowable object
        logo_img = PIL_Image.open(os.path.join(LOGO_DIR, 'logo_dong_hanh.png'))
        imsize = logo_img.size
        imw = float(imsize[0]) * .15
        imh = float(imsize[1]) * .15
        logo_img = Flowable_Image(os.path.join(LOGO_DIR, 'logo_dong_hanh.png'), imw, imh)
        logo_img.hAlign = 'LEFT'

        # create DH info
        logo_text = []
        logo_text.append(Paragraph('Quỹ học bổng Đồng Hành Đài Loan', DOC_STYLES['Signature Style']))
        logo_text.append(Paragraph('Website: www.donghanh.net', DOC_STYLES['Signature Style']))
        logo_text.append(Paragraph('Email: contact@donghanh.net', DOC_STYLES['Signature Style']))

        return logo_img, logo_text

    # Now for DH France
    # read image and put to flowable object
    logo_img = PIL_Image.open(os.path.join(LOGO_DIR, 'logo_dong_hanh.png'))
    imsize = logo_img.size
    imw = float(imsize[0]) * .15
    imh = float(imsize[1]) * .15
    logo_img = Flowable_Image(os.path.join(LOGO_DIR, 'logo_dong_hanh.png'), imw, imh)
    logo_img.hAlign = 'LEFT'

    # create DH info
    logo_text = []
    logo_text.append(Paragraph('Quỹ học bổng Đồng Hành', DOC_STYLES['Signature Style']))
    logo_text.append(Paragraph('16 rue Petit-Musc', DOC_STYLES['Signature Style']))
    logo_text.append(Paragraph('75004, Paris, Pháp', DOC_STYLES['Signature Style']))
    logo_text.append(Paragraph('Email: contact@donghanh.net', DOC_STYLES['Signature Style']))

    return logo_img, logo_text


def get_attach_file(merger, filename, doc_index, candidate_idx, tmp_path):
    success = True
    try:
        with open(os.path.join(tmp_path, "{}_{}.pdf".format(filename, doc_index)), 'rb') as fi:
            pdf = PdfFileReader(fi)
            if not pdf.isEncrypted:
                merger.append(pdf)
            else:
                logger.error(
                    "Không thể nối thư xin học bổng ở hồ sơ thứ " + str(candidate_idx) + ". Yêu cầu thực hiện thủ công.")
                success = False
    except PdfReadError as e:
        success = False
        formatted_lines = traceback.format_exc().splitlines()
        trace_back = "\n".join(formatted_lines)
        logger.info(trace_back)
        logger.error(e)
        logger.error("Failed file: {}".format(os.path.join(tmp_path, "{}_{}.pdf".format(filename, doc_index))))
        logger.error(
            "Không thể nối thư xin học bổng ở hồ sơ thứ " + str(candidate_idx) + ". Yêu cầu thực hiện thủ công.")
    return success


############### ----------END OF LOCAL FUNCTIONS---------- ###############

############### ----------CORE FUNCTION---------- ###############


def buildPdf(target, candidate_idx, candidate, heading_csv, semester):
    '''
        Usage: buildPdf(target, index, candidate, heading_csv)
        This function builds the output pdf.
        Params(4):
            target          The directory for output files
            index:          Index of the candidate's row in the csv
            candidate:      The csv row w.r.t a candidate
            heading_csv:    The heading row of the csv file
    '''
    # set path for temporary files
    tmp_path = os.path.join(target, 'tmp')
    #interview_dir_path = os.path.join(target, 'INTERVIEW')
    school = get_field(candidate, 'Truong')
    if school == '-':
        candidate[INDEX_OF_KEY['Truong']] = "Unknown"
        school = "Unknown"
    interview_dir_path = os.path.join(target,SCHOOL_CODE_ALL[school], 'INTERVIEW')
    basename = get_pdf_basename(candidate, candidate_idx)
    filename2 = get_pdf_basename(candidate, 0)

    # initialise document
    main_document = get_doc_template(os.path.join(tmp_path, basename + '_1.pdf'), basename)

    main_story = []

    # Sơ yếu lí lịch
    main_story = step1_basic_info(main_story, candidate, semester, heading_csv, tmp_path)

    # Phiếu điều tra
    main_story = step2_background(main_story, candidate, heading_csv)

    # Thư xin học bổng
    main_story = step3_motivation_letter(main_story, candidate)

    # create temporary file
    main_document.build(main_story)

    # Download attachments
    has_attachment = step4_attachment(candidate, os.path.join(tmp_path, basename))

    # Ý kiến đánh giá
    main_document = get_doc_template(os.path.join(tmp_path, basename + '_6.pdf'), basename)
    """
    if get_field(candidate, 'KhungVietThu') == "" and has_attachment['ThuXinHocBongScan'] == 0:
        interview_document = get_doc_template(
            os.path.join(interview_dir_path, SCHOOL_CODE_ALL[school], 'DISQUALIFIED', basename + '_6.pdf'), basename)
    else:
        interview_document = get_doc_template(
            os.path.join(interview_dir_path, SCHOOL_CODE_ALL[school], basename + '_6.pdf'), basename)
    """
    
    interview_story = []
    interview_story = step5_inteview_form(interview_story, candidate, heading_csv)
    main_document.build(interview_story)
    interview_story = step5_inteview_form(interview_story, candidate, heading_csv)
    if not(get_field(candidate, 'KhungVietThu') == "" and has_attachment['ThuXinHocBongScan'] == 0):
        interview_document = get_doc_template(
            os.path.join(interview_dir_path, basename + '_6.pdf'), basename)
        interview_document.build(interview_story)
    # Get pdf merger containing the documents created above
    if get_field(candidate, 'KhungVietThu') == "" and has_attachment['ThuXinHocBongScan'] == 0:
        final_path = os.path.join(target, SCHOOL_CODE_ALL[school], 'DISQUALIFIED', basename + '.pdf')
    else:
        final_path = os.path.join(target, SCHOOL_CODE_ALL[school], basename + '.pdf')

    success = merge_pdf(tmp_path, basename, has_attachment, candidate_idx, final_path)
    # Delete tmp files if suceess
    if success:
        logger.info('File %s.pdf đã được tạo' % basename)
        for file_idx in range(1, 7):
            remove_if_exist(os.path.join(tmp_path, "{}_{}.pdf".format(basename, file_idx)))

    remove_if_exist(os.path.join(tmp_path, filename2 + '_photo'))
    return basename


def merge_pdf(tmp_path, basename, has_attachment, candidate_idx, final_path):
    # Create a merger (an object to merge documents) then join created documents into the merger.
    merger = PdfFileMerger(strict=False)
    with open(os.path.join(tmp_path, basename + '_1.pdf'), 'rb') as fi:
        main_doc = PdfFileReader(fi)
        merger.append(main_doc)
        success = True

    # Check if need to merge pdf with attachments
    # Some pdf may be encrypted, in this case automatic merge cannot be performed.
    # Thư xin học bổng (scan)
    if has_attachment['ThuXinHocBongScan'] == 1:
        success = get_attach_file(merger, basename, 2, candidate_idx, tmp_path)

    # Bảng điểm
    if has_attachment['BangDiemScan'] == 1:
        success = get_attach_file(merger, basename, 3, candidate_idx, tmp_path)

    # Chứng nhận hoàn cảnh khó khăn/Sổ hộ nghèo
    if has_attachment['ChungNhanKhoKhanScan'] == 1:
        success = get_attach_file(merger, basename, 4, candidate_idx, tmp_path)

    # Giấy tờ khác
    if has_attachment['GiayToKhacScan'] == 1:
        success = get_attach_file(merger, basename, 5, candidate_idx, tmp_path)
	
	#The next 3 lines are to merge "interview doc" with the whole file
	
    #with open(os.path.join(tmp_path, basename + '_6.pdf'), 'rb') as fi:
    #    interview_doc = PdfFileReader(fi)
    #    merger.append(interview_doc)

    # final location to write pdf
    try:
        merger.write(final_path)
    except Exception as e:
        formatted_lines = traceback.format_exc().splitlines()
        trace_back = "\n".join(formatted_lines)
        logger.error(trace_back)
        success = False
    return success


############### ----------END OF CORE FUNCTION---------- ###############

############### ----------PARTIAL FUNCTIONS---------- ###############

def step1_basic_info(story, candidate, semester, heading_csv, TMP_PATH):
    '''
        This function creates "Sơ yếu lí lịch"
    '''
    filename = get_pdf_basename(candidate, 0)

    # add logo
    logo_img, logo_text = create_logo(get_field(candidate, 'Truong'))
    story.append(Table([[logo_img, logo_text]]))

    # add AnhCaNhan
    candidate_photo = ""
    # if get_field(candidate, 'AnhCaNhan') != "yes" and get_field(candidate, 'AnhCaNhan') != "no" and get_field(candidate, 'AnhCaNhan') != "":
    #     try:
    #         # print(get_field(candidate, 'AnhCaNhan'))
    #         # download_file(get_field(candidate, 'ChungNhanKhoKhanScan'), filename + '_4.pdf')
    #         download_file(get_field(candidate, 'AnhCaNhan'), os.path.join(TMP_PATH, filename + '_photo.jpg'))
    #         # im = Flowable_Image.open(os.path.join(TMP_PATH, filename + '_photo'))
    #         imw = 75
    #         imh = 100
    #         candidate_photo = Flowable_Image(os.path.join(TMP_PATH, filename + '_photo.jpg'), imw, imh)
    #         candidate_photo.hAlign = 'CENTER'
    #     except IOError as e:
    #         logger.error(e)
    #         logger.error("Invalid image. Discard candidate photo {}".format(filename))
    #         candidate_photo = ""

            

    # story.drawImage(filename, inch, height - 2 * inch)

    # Title
    story.append(Paragraph(u'SƠ YẾU LÍ LỊCH', DOC_STYLES['Title Style']))

    # Personal Infos
    story.append(Paragraph(u'I. Thông tin cá nhân', DOC_STYLES['Heading I Style']))

    local_needed_fields = ['HoVaTen', 'GioiTinh', 'NgaySinh', 'MaSoSV', 'NamThu', 'KhoaNganh']
    table_data = [[(FIELD_NAMES_FULL[key] + ':'),
                   Paragraph(get_field(candidate, key), DOC_STYLES['Italic Body Style']), candidate_photo] for
                  key in local_needed_fields]
    table_style = TRANSPARENT_TABLE_WITH_MERGE
    table = Table(table_data, colWidths=[136, 240, 120])
    table.setStyle(table_style)
    story.append(table)

    local_needed_fields = ['Lop', 'Truong', 'TenTruongNeuKhac', 'DiaChiSinh', 'DiaChiTru', 'DienThoai', 'Email']
    table_data = [[(FIELD_NAMES_FULL[key] + ':'),
                   Paragraph(get_field(candidate, key), DOC_STYLES['Italic Body Style'])] for key in
                  local_needed_fields]
    table_style = TRANSPARENT_TABLE
    table = Table(table_data, colWidths=[136, 360])
    table.setStyle(table_style)
    story.append(table)

    # Infos on family
    story.append(Paragraph(u'II. Thông tin về các thành viên trong gia đình', DOC_STYLES['Heading I Style']))
    table_data = [[u'Họ và tên cha:', get_field(candidate, 'HoTenCha')],
                  [u'Tuổi:', get_field(candidate, 'TuoiCha'), u'Nghề nghiệp:', get_field(candidate, 'NgheNghiepCha')],
                  [u'Họ và tên mẹ:', get_field(candidate, 'HoTenMe')],
                  [u'Tuổi:', get_field(candidate, 'TuoiMe'), u'Nghề nghiệp:', get_field(candidate, 'NgheNghiepMe')]]
    table_style = TRANSPARENT_TABLE
    table = Table(table_data, colWidths=[100, 100, 100, 200])
    table.setStyle(table_style)
    story.append(table)

    story.append(Spacer(width=0, height=1.5 * LINE_SPACING))
    story.append(Paragraph(u'Các thành viên khác trong gia đình:', DOC_STYLES['Body Style']))
    story.append(Spacer(width=0, height=1.5 * LINE_SPACING))

    # Family member table
    table_data = [[u'Họ và tên', u'Quan hệ', u'Tuổi', u'Nghề nghiệp']]
    for index in range(1, 10):
        row = get_field(candidate, 'NguoiThan' + str(index)).split(';')
        table_data += [[Paragraph(element, DOC_STYLES['Body Center Style']) for element in row]]
    table_style = STANDARD_TABLE
    table = Table(table_data, colWidths=[150, 120, 60, 170])
    table.setStyle(table_style)
    story.append(table)

    # Story.append(PageBreak()) # new page

    # Study results
    story.append(Paragraph(u'III. Kết quả học tập', DOC_STYLES['Heading I Style']))
    story.append(Paragraph(u'Điểm trung bình các học kì đại học:', DOC_STYLES['Body Style']))
    story.append(Spacer(width=0, height=2 * LINE_SPACING))
    table_data = [[u'Học kì I năm 1', u'Học kì II năm 1', u'Học kì I năm 2', u'Học kì II năm 2'], \
                  [get_field(candidate, key) for key in ['DiemKi1_Nam1', 'DiemKi2_Nam1', 'DiemKi1_Nam2', 'DiemKi2_Nam2']]]
    table = Table(table_data, colWidths=[120, 120, 120, 120])
    table_style = HORIZONTAL_NUMERIC_TABLE
    table.setStyle(table_style)
    story.append(table)
    
    story.append(Spacer(width=0, height=2 * LINE_SPACING))
    table_data = [[u'Học kì I năm 3', u'Học kì II năm 3', u'Học kì I năm 4', u'Học kì II năm 4'], \
                  [get_field(candidate, key) for key in ['DiemKi1_Nam3', 'DiemKi2_Nam3', 'DiemKi1_Nam4','DiemKi2_Nam4']]]
    table = Table(table_data, colWidths=[120, 120, 120, 120])
    table_style = HORIZONTAL_NUMERIC_TABLE
    table.setStyle(table_style)
    story.append(table)
    
    '''table_data = [[u'Điểm thi tốt nghiệp:', [Paragraph(element, DOC_STYLES['Table Cell Style']) for element in
                                             get_field(candidate, 'DiemTotNghiep').split("\n")]],
                  [u'Điểm thi đại học:', [Paragraph(element, DOC_STYLES['Table Cell Style']) for element in
                                          get_field(candidate, 'DiemTotNghiep_DaiHoc').split("\n")]]]
    '''
    
    story.append(Spacer(width=0, height= LINE_SPACING))
    table_data = [[u'Điểm thi đại học:', [Paragraph(element, DOC_STYLES['Table Cell Style']) for element in
                                          get_field(candidate, 'DiemTotNghiep_DaiHoc').split("\n")]]]
    table = Table(table_data, colWidths=[150, 330])
    table_style = TRANSPARENT_TABLE
    table.setStyle(table_style)
    story.append(table)

    story.append(Spacer(width=0, height=1.5 * LINE_SPACING))

    # Other achievements
    story.append(Paragraph(u'Các thành tích khác:', DOC_STYLES['Body Style']))
    story.append(Spacer(width=0, height=2 * LINE_SPACING))
    table_data = [[u'STT', u'Thành tích']] + \
                 [[str(index),
                   Paragraph(get_field(candidate, 'ThanhTichKhac' + str(index)), DOC_STYLES['Table Cell Style'])]
                  for index in range(1, 6)]
    table = Table(table_data, colWidths=[30, 450])
    table_style = STANDARD_TABLE
    table.setStyle(table_style)
    story.append(table)
    story.append(Spacer(width=0, height=1.5 * LINE_SPACING))
    
    # Other infos
    story.append(Paragraph(u'IV. Các thông tin khác', DOC_STYLES['Heading I Style']))
    story.append(Paragraph(('Nơi học THPT: <i>%s%s</i>' % (make_tabs(16), get_field(candidate, 'THPT'))),
                           DOC_STYLES['Body Style']))

    story.append(Paragraph(u'Bạn từng nhận được học bổng Đồng Hành bao giờ chưa? Nếu có, ở các kì nào?',
                           DOC_STYLES['Heading I Style']))
    LOCAL_TABLE_HEAD = {'NhanHBDHChua': u'Chưa từng có', 'KiN-5': u'Trước kì ' + str(semester - 4),
                        'KiN-4': u'Kì ' + str(semester - 4),
                        'KiN-3': u'Kì ' + str(semester - 3), 'KiN-2': u'Kì ' + str(semester - 2),
                        'KiN-1': u'Kì ' + str(semester - 1)}

    table_data = [
        [YES_NO_ICON[get_field(candidate, key)] + " " + LOCAL_TABLE_HEAD[key] for key in
         ['NhanHBDHChua', 'KiN-5', 'KiN-4']],
        [YES_NO_ICON[get_field(candidate, key)] + " " + LOCAL_TABLE_HEAD[key] for key in ['KiN-3', 'KiN-2', 'KiN-1']]]
    table_style = TRANSPARENT_REGULAR_TABLE
    table = Table(table_data, colWidths=[160, 160, 160])
    table.setStyle(table_style)
    story.append(table)
    story.append(Paragraph(u'Bạn từng được nhận hỗ trợ tài chính khác trong thời gian học đại học chưa?',
                           DOC_STYLES['Heading I Style']))
    story.append(Paragraph(u'Nếu có, hãy ghi lại những hỗ trợ đó trong bảng dưới đây', DOC_STYLES['Body Style']))
    
    # Tạo bảng các hỗ trợ khác
    story.append(Spacer(width=0, height=2 * LINE_SPACING))
    table_data = [[u'Tên học bổng/hỗ trợ', u'Thời gian nhận', u'Giá trị', u'Lí do được nhận']] + \
                 [[Paragraph(element, DOC_STYLES['Table Cell Style']) for element in
                   get_field(candidate, 'HoTro' + str(index)).split(';',3)] for index in range(1, 6)]
    table = Table(table_data, colWidths=[140, 100, 100, 140])
    table_style = STANDARD_TABLE
    table.setStyle(table_style)
    story.append(table)
    story.append(Spacer(width=0, height=2 * LINE_SPACING))
    
    story.append(Paragraph(u'Nếu đã từng nhận học bổng Đồng Hành và các học bổng khác, bạn đã sử dụng những tiền học bổng đó vào việc gì?',
                           DOC_STYLES['Heading I Style']))
    
    story.append(Paragraph(get_field(candidate, 'TienHocBongDaNhan'), DOC_STYLES['Body Style']))
    
    story.append(Spacer(width=0, height = LINE_SPACING))
    
    table_data = [['',Paragraph('--------------------------------------------------------', DOC_STYLES['Body Style'])],
                  [u'Các việc làm thêm:', [Paragraph(element, DOC_STYLES['Table Cell Style']) for element in
                                          get_field(candidate, 'LamThem').split("\n")]],
                  ['',Paragraph('--------------------------------------------------------', DOC_STYLES['Body Style'])],
                  [u'Những hoạt động khác:', [Paragraph(element, DOC_STYLES['Table Cell Style']) for element in
                                             get_field(candidate, 'HoatDongKhac').split("\n")]]]
    table = Table(table_data, colWidths=[150, 330])
    table_style = TRANSPARENT_TABLE
    table.setStyle(table_style)
    story.append(table)
    story.append(Spacer(width=0, height=1.5 * LINE_SPACING))
    
    
    story.append(PageBreak())
    
    return story


def step2_background(story, candidate, heading_csv):
    '''
            This function creates "Phiếu điều tra"
    '''
    # add logo
    logo_img, logo_text = create_logo(get_field(candidate, 'Truong'))
    story.append(Table([[logo_img, logo_text]]))

    # Title
    story.append(Paragraph(u'PHIẾU ĐIỀU TRA', DOC_STYLES['Title Style']))

    # Monthly costs
    story.append(Paragraph(u'1. Chi phí hằng tháng:', DOC_STYLES['Heading I Style']))
    local_needed_fields = ['NhaO', 'DiLai', 'TienAn', 'VuiChoi', 'TienHoc', 'TienHocThem']
    table_data = [[(FIELD_NAMES_FULL[key] + ': '), money_processing(get_field(candidate, key))] for key in
                  local_needed_fields]
    table_style = VERTICAL_TRANSPARENT_NUMERIC_TABLE
    table = Table(table_data, colWidths=[150, 250])
    table.setStyle(table_style)
    story.append(table)
    story.append(Spacer(width=0, height=2 * LINE_SPACING))

    # Revenu
    story.append(Paragraph(u'2. Thu nhập bình quân của gia đình:', DOC_STYLES['Heading I Style']))
    table_data = [['', money_processing(get_field(candidate, 'ThuNhapBinhQuan'))]]
    table_style = VERTICAL_TRANSPARENT_NUMERIC_TABLE
    table = Table(table_data, colWidths=[150, 250])
    table.setStyle(table_style)
    story.append(table)
    story.append(Spacer(width=0, height=2 * LINE_SPACING))

    # Resource contribution
    story.append(Paragraph(u'3. Kinh phí để trang trải cho cuộc sống và học tập của bạn hiện nay là từ:',
                           DOC_STYLES['Heading I Style']))
    local_needed_fields = ['ThuNhapGiaDinh', 'ThuNhapHocBong', 'ThuNhapTienVay', 'ThuNhapLamThem']
    table_data = [[(FIELD_NAMES_FULL[key] + ': '), money_processing(get_field(candidate, key))] for key in
                  local_needed_fields]
    table_data.append([(FIELD_NAMES_FULL['ThuNhapKhac'] + ': '),
                       Paragraph(get_field(candidate, 'ThuNhapKhac'), DOC_STYLES['Body Right Style'])])
    table_style = VERTICAL_TRANSPARENT_NUMERIC_TABLE
    table = Table(table_data, colWidths=[150, 250])
    table.setStyle(table_style)
    story.append(table)
    story.append(Spacer(width=0, height=2 * LINE_SPACING))

    # Personal Difficulties
    story.append(Paragraph(u'4. Khó khăn lớn nhất của bạn khi vào đại học:', DOC_STYLES['Heading I Style']))
    story += [Paragraph(('%s%s' % (make_tabs(14), element)), DOC_STYLES['Body Style']) for element in
              get_field(candidate, 'KhoKhanCuocSong').split('\n')]

    # Objectives
    story.append(Paragraph(u'5. Nếu được nhận học bổng Đồng Hành trong học kì này, bạn sẽ sử dụng vào mục đích gì?',
                           DOC_STYLES['Heading I Style']))
    table_data = [[u'Đóng tiền học: ', YES_NO_ICON[get_field(candidate, 'DongTienHocKhong')], u'Thời gian: ',
                   Paragraph(get_field(candidate, 'DongTienHocBaoNhieu'), DOC_STYLES['Body Right Style'])],
                  [u'Đóng tiền nhà: ', YES_NO_ICON[get_field(candidate, 'DongTienNhaKhong')], u'Thời gian: ',
                   Paragraph(get_field(candidate, 'DongTienNhaBaoNhieu'), DOC_STYLES['Body Right Style'])],
                  [u'Học thêm ngoại ngữ, tin học: ', YES_NO_ICON[get_field(candidate, 'HocThemKhong')], u'Thời gian: ',
                   Paragraph(get_field(candidate, 'HocThemBaoNhieu'), DOC_STYLES['Body Right Style'])],
                  [u'Khác (ghi rõ): ', '', '',
                   Paragraph(get_field(candidate, 'DongTienKhac'), DOC_STYLES['Body Right Style'])]]
    table_style = VERTICAL_TRANSPARENT_NUMERIC_TABLE
    table = Table(table_data, colWidths=[180, 30, 70, 150])
    table.setStyle(table_style)
    story.append(table)

    '''# Communication
    story.append(Paragraph(u'6. Sau khi nhận học bổng, bạn muốn liên lạc với Đồng Hành qua hình thức nào?',
                           DOC_STYLES['Heading I Style']))
    table_data = [
        [u'Trao đổi qua thư điện tử: ', YES_NO_ICON[get_field(candidate, 'LienLacCachNao1')],
         u'Nhận bản tin Đồng Hành: ',
         YES_NO_ICON[get_field(candidate, 'LienLacCachNao2')], ''],
        [u'Thông qua trang web, diễn đàn: ', YES_NO_ICON[get_field(candidate, 'LienLacCachNao3')],
         u'Gặp gỡ ở Việt Nam: ',
         YES_NO_ICON[get_field(candidate, 'LienLacCachNao4')], '']]
    table_style = VERTICAL_TRANSPARENT_NUMERIC_TABLE
    table = Table(table_data, colWidths=[200, 40, 200, 40, 10])
    table.setStyle(table_style)
    story.append(table)
    '''

    # Other questions
    story.append(
        Paragraph(('6. %s' % FIELD_NAMES_FULL['MongMuonNhanGiTuDH']), DOC_STYLES['Heading I Style']))
    story += [Paragraph(('<i>%s%s</i>' % (make_tabs(14), element)), DOC_STYLES['Body Style']) for
              element in get_field(candidate, 'MongMuonNhanGiTuDH').split('\n')]
    story.append(
        Paragraph(('7. %s' % FIELD_NAMES_FULL['KhoKhanLamHoSo']), DOC_STYLES['Heading I Style']))
    story += [Paragraph(('<i>%s%s</i>' % (make_tabs(14), element)), DOC_STYLES['Body Style']) for
              element in get_field(candidate, 'KhoKhanLamHoSo').split('\n')]
    story.append(Paragraph(('8. %s' % FIELD_NAMES_FULL['DeDatNhanNhu']), DOC_STYLES['Heading I Style']))
    story += [Paragraph(('<i>%s%s</i>' % (make_tabs(14), element)), DOC_STYLES['Body Style']) for
              element in get_field(candidate, 'DeDatNhanNhu').split('\n')]

    story.append(PageBreak())
    return story


def step3_motivation_letter(story, candidate):
    '''
        This function creates "Thư xin học bổng đánh máy"
    '''

    if get_field(candidate, 'KhungVietThu') != "":
        # add logo
        logo_img, logo_text = create_logo(get_field(candidate, 'Truong'))
        story.append(Table([[logo_img, logo_text]]))
        # Title
        story.append(Paragraph(u'THƯ XIN HỌC BỔNG', DOC_STYLES['Title Style']))

        # Body
        story += \
            [Paragraph(('%s' % element), DOC_STYLES['LoM Body Style']) for element in
             get_field(candidate, 'KhungVietThu').split('\n')]

    return story


def step4_attachment(candidate, filename):
    '''
        This function downloads all files w.r.t the candidate
    '''
    # Initialize x that would tell us which documents have been updated: The transcription, the attestation, or both or none of them.
    # Download the files if any.
    has_file = {'ThuXinHocBongScan': 0, 'BangDiemScan': 0, 'ChungNhanKhoKhanScan': 0, 'GiayToKhacScan': 0}
    # Thư xin học bổng scan
    if get_field(candidate, 'KhungScanThu') != "" and get_field(candidate, 'KhungScanThu') != "no":
        download_file(get_field(candidate, 'KhungScanThu'), filename + '_2.pdf')
        has_file['ThuXinHocBongScan'] = 1
    # Bảng điểm
    if get_field(candidate, 'BangDiemScan') != "" and get_field(candidate, 'BangDiemScan') != "no":
        download_file(get_field(candidate, 'BangDiemScan'), filename + '_3.pdf')
        has_file['BangDiemScan'] = 1
    # Chứng nhận khó khăn/Sổ hộ nghèo
    if get_field(candidate, 'ChungNhanKhoKhanScan') != "" and get_field(candidate, 'ChungNhanKhoKhanScan') != "no":
        download_file(get_field(candidate, 'ChungNhanKhoKhanScan'), filename + '_4.pdf')
        has_file['ChungNhanKhoKhanScan'] = 1
    # Giấy tờ khác
    if get_field(candidate, 'GiayToKhacScan') != "" and get_field(candidate, 'GiayToKhacScan') != "no":
        download_file(get_field(candidate, 'GiayToKhacScan'), filename + '_5.pdf')
        has_file['GiayToKhacScan'] = 1
    return has_file


def step5_inteview_form(Story, candidate, filename):
    '''
        This function creates "Ý kiến đánh giá" page
    '''
    # add logo
    logo_img, logo_text = create_logo(get_field(candidate, 'Truong'))
    Story.append(Table([[logo_img, logo_text]]))

    # heading
    Story.append(Paragraph(u'Ý KIẾN ĐÁNH GIÁ', DOC_STYLES['Title Style']))
    newLine(Story, DOC_STYLES, 1)
    # body
    Story.append(Paragraph(u'Họ và tên người phỏng vấn: ', DOC_STYLES['Heading I Style']))
    Story.append(Paragraph(u'<b>Họ và tên sinh viên: </b>%s' % get_field(candidate, 'HoVaTen'),
                           DOC_STYLES['Body Style']))
    newLine(Story, DOC_STYLES, 1)
    Story.append(Paragraph(u'1. Hoàn cảnh: ', DOC_STYLES['Heading I Style']))
    newLine(Story, DOC_STYLES, 15)
    Story.append(Paragraph(u'2. Học tập: ', DOC_STYLES['Heading I Style']))
    newLine(Story, DOC_STYLES, 10)
    Story.append(Paragraph(u'3. Ước mơ: ', DOC_STYLES['Heading I Style']))
    newLine(Story, DOC_STYLES, 8)
    Story.append(Paragraph(u'4. Các phần khác: ', DOC_STYLES['Heading I Style']))
    newLine(Story, DOC_STYLES, 8)
    # If the candidate declare some other documents, include them in this part to be checked by reviewer
    if len(get_field(candidate, 'GiayToKhacList')) >= 2:
        Story.append(Paragraph(u'Phần kiểm tra các giấy tờ khác', DOC_STYLES['Heading I Style']))
        Story.append(Paragraph(
            u'Người phỏng vấn đánh dấu ([X])vào ô các giấy tờ mà sinh viên có mang theo để ưu tiên khi đánh giá, xét chọn: ',
            DOC_STYLES['Body Style']))
        Story += [Paragraph(('[%s]<i>%s</i>' % (make_tabs(5), element)), DOC_STYLES['Body Style']) for
                  element in get_field(candidate, 'GiayToKhacList').split('\n')]
    Story.append(
        Paragraph((u'Tại %s, ngày %s tháng %s năm %s' % (make_tabs(30), make_tabs(5), make_tabs(5), make_tabs(10))),
                  DOC_STYLES['Signature Style']))
    Story.append(Paragraph(u'Chữ kí người phỏng vấn%s' % make_tabs(30), DOC_STYLES['Signature Style']))
    return Story
