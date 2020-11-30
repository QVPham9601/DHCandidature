# !/user/local/bin/python2.7
# -*- coding: utf-8 -*-

import os

from reportlab.lib import colors
from reportlab.platypus import TableStyle

API_KEY = '521350-1405134815-au8cmd567qxfnrb49'
FORM_ID = {
    "fr": "1006311",
    "sg": "2266863",
    "tw": "2272966"
}

URL_SUBMISSION_FORMAT = "https://123contactform.com/api/forms/{}/submissions.json"
URL_SUBMISSION_COUNT_FORMAT = "https://www.123contactform.com/api/forms/{}/submissions/count.json?apiKey={}"
URL_FIELDS_FORMAT = "https://www.123formbuilder.com/api/forms/{}/fields.json"

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_FOLDER)
OUTPUT_FOLDER = os.path.join(PROJECT_DIR, "HOSO")
RESOURCES_DIR = os.path.join(CURRENT_FOLDER, "resources")
LOGO_DIR = os.path.join(RESOURCES_DIR, "Images")
FONTS_DIR = os.path.join(RESOURCES_DIR, "Fonts")

SCHOOL_CODE_LIST = [
    'BKHN', 'TNHN', 'XD', 'GTVT1', 'CNHN',
    'VINH', 'BKDN', 'KTDN', 'SPDN',
    'NNDN', 'BKHCM', 'TNHCM', 'KTLHCM',
    'GTVT2', 'DALAT', 'CTHO', 'NNHN', 'SPKTHCM', 'KHAC', 'UNK'
]

SCHOOL_CODE_ALL = {
    'Trường Đại học Bách khoa Hà Nội': 'BKHN',
    'Trường Đại học Khoa học tự nhiên, ĐHQG Hà Nội': 'TNHN',
    'Trường Đại học Xây dựng': 'XD',
    'Trường Đại học Giao thông vận tải cơ sở I (tại Hà Nội)': 'GTVT1',
    'Trường Đại học Công nghệ, ĐHQG Hà Nội': 'CNHN',
    'Trường Đại học Vinh': 'VINH',
    'Trường Đại học Bách khoa, ĐH Đà Nẵng': 'BKDN',
    'Trường Đại học Kinh tế, ĐH Đà Nẵng': 'KTDN',
    'Trường Đại học Sư phạm, ĐH Đà Nẵng': 'SPDN',
    'Trường Đại học Ngoại ngữ, ĐH Đà Nẵng': 'NNDN',
    'Trường Đại học Bách khoa, ĐHQG TP Hồ Chí Minh': 'BKHCM',
    'Trường Đại học Khoa học tự nhiên, ĐHQG TP Hồ Chí Minh': 'TNHCM',
    'Trường Đại học Kinh tế Luật, ĐHQG TP Hồ Chí Minh': 'KTLHCM',
    'Trường Đại học Giao thông vận tải cơ sở II (tại TP Hồ Chí Minh)': 'GTVT2',
    'Trường Đại học Đà Lạt': 'DALAT',
    'Trường Đại học Cần Thơ': 'CTHO',
    'Trường Đại Học Ngoại Ngữ, ĐHQG Hà Nội': 'NNHN',
    'Trường Đại học Sư phạm Kỹ thuật TP Hồ Chí Minh': 'SPKTHCM',
    'Trường khác (ghi rõ trong thư xin học bổng)': 'KHAC',
    'Unknown': 'UNK',
}

SCHOOL_CODE = {
    'sg': {
        'Trường Đại Học Ngoại Ngữ, ĐHQG Hà Nội': 'NNHN',
        'Trường Đại học Kinh tế Luật, ĐHQG TP Hồ Chí Minh': 'KTLHCM',
        'Trường Đại học Công nghệ, ĐHQG Hà Nội': 'CNHN',
        'Trường khác (ghi rõ trong thư xin học bổng)': 'KHAC',
        'Unknown': 'UNK'
    },
    'fr': {
        'Trường Đại học Bách khoa Hà Nội': 'BKHN',
        'Trường Đại học Khoa học tự nhiên, ĐHQG Hà Nội': 'TNHN',
        'Trường Đại học Xây dựng': 'XD',
        'Trường Đại học Giao thông vận tải cơ sở I (tại Hà Nội)': 'GTVT1',
        'Trường Đại học Vinh': 'VINH',
        'Trường Đại học Bách khoa, ĐH Đà Nẵng': 'BKDN',
        'Trường Đại học Kinh tế, ĐH Đà Nẵng': 'KTDN',
        'Trường Đại học Sư phạm, ĐH Đà Nẵng': 'SPDN',
        'Trường Đại học Ngoại ngữ, ĐH Đà Nẵng': 'NNDN',
        'Trường Đại học Bách khoa, ĐHQG TP Hồ Chí Minh': 'BKHCM',
        'Trường Đại học Khoa học tự nhiên, ĐHQG TP Hồ Chí Minh': 'TNHCM',
        'Trường Đại học Giao thông vận tải cơ sở II (tại TP Hồ Chí Minh)': 'GTVT2',
        'Trường Đại học Đà Lạt': 'DALAT',
        'Trường Đại học Sư phạm Kỹ thuật TP Hồ Chí Minh': 'SPKTHCM',
        'Trường Đại học Cần Thơ': 'CTHO',
        'Trường khác (ghi rõ trong thư xin học bổng)': 'KHAC',
        'Unknown': 'UNK'
    }
}

SCHOOL_NB = {
    'Trường Đại học Bách khoa Hà Nội': '01',
    'Trường Đại học Khoa học tự nhiên, ĐHQG Hà Nội': '02',
    'Trường Đại học Xây dựng': '03',
    'Trường Đại học Giao thông vận tải cơ sở I (tại Hà Nội)': '04',
    'Trường Đại học Công nghệ, ĐHQG Hà Nội': '16',
    'Trường Đại học Vinh': '11',
    'Trường Đại học Bách khoa, ĐH Đà Nẵng': '05',
    'Trường Đại học Kinh tế, ĐH Đà Nẵng': '06',
    'Trường Đại học Sư phạm, ĐH Đà Nẵng': '07',
    'Trường Đại học Ngoại ngữ, ĐH Đà Nẵng': '08',
    'Trường Đại học Bách khoa, ĐHQG TP Hồ Chí Minh': '09',
    'Trường Đại học Khoa học tự nhiên, ĐHQG TP Hồ Chí Minh': '10',
    'Trường Đại học Kinh tế Luật, ĐHQG TP Hồ Chí Minh': '15',
    'Trường Đại học Giao thông vận tải cơ sở II (tại TP Hồ Chí Minh)': '14',
    'Trường Đại học Đà Lạt': '12',
    'Trường Đại học Cần Thơ': '17',
    'Trường Đại học Sư phạm Kỹ thuật TP Hồ Chí Minh': '18',
    'Trường Đại Học Ngoại Ngữ, ĐHQG Hà Nội': '19',
    'Trường khác (ghi rõ trong thư xin học bổng)': '21',
}

############### ----------BUILD PDF PARAMETERS---------- ###############

# Page layout
LEFT_MARGIN = 50
RIGHT_MARGIN = 50
TOP_MARGIN = 50
BOTTOM_MARGIN = 50

# Line spacing
LINE_SPACING = 6

# Icon for Yes/No questions: cross for "Yes", blank for "No"
# YES_NO_ICON = {'yes': "[ X ]", 'Yes': u"[ X ]", 'No': "[    ]", 'no': "[    ]", u'Có': "[ X ]", u'Không': "[    ]", u'có': "[ X ]", u'không': "[    ]", 'Không': "[    ]", 'Có': "[ X ]", 'Chưa từng': "[    ]", u'Chưa từng': "[     ]", '': "[     ]"}

YES_NO_ICON = {'yes': u"\u2327", 'Yes': u"\u2327", 'No': u"\u29e0", 'no': u"\u29e0", u'Có': u"\u2327",
               u'Không': u"\u29e0", u'có': u"\u2327", u'không': u"\u29e0", 'Không': u"\u29e0", 'Có': u"\u2327",
               'Chưa từng': u"\u29e0", u'Chưa từng': u"\u29e0", '': u"\u29e0"}

# Keys for all fields of the input csv
# The order of these fields must match exactly those in the input csb
# NB: For any insertion/deletion/change of positions of columns, please update this param
FIELD_NAMES = ['HoVaTen', 'GioiTinh', 'NgaySinh', 'MaSoSV', 'NamThu', 'KhoaNganh',
               'Lop', 'Truong', 'SoNhaDuongSinh', 'QuanHuyenSinh', 'TinhThanhSinh', 'SoNhaDuongTru',
               'QuanHuyenTru', 'TinhThanhTru', 'DienThoai', 'Email', 'HoTenCha', 'TuoiCha',
               'NgheNghiepCha', 'HoTenMe', 'TuoiMe', 'NgheNghiepMe', 'NguoiThan1', 'NguoiThan2',
               'NguoiThan3', 'NguoiThan4', 'NguoiThan5', 'NguoiThan6', 'NguoiThan7', 'NguoiThan8',
               'NguoiThan9', 'DiemDaiHoc', 'DiemKi1', 'DiemKi2', 'DiemKi3', 'DiemTotNghiep',
               'ThanhTichKhac1', 'ThanhTichKhac2', 'ThanhTichKhac3', 'ThanhTichKhac4', 'ThanhTichKhac5', 'THPT',
               'NhanHBDHChua', 'KiN-5', 'KiN-4', 'KiN-3', 'KiN-2', 'KiN-1',
               'CoHoTroKhac', 'HoTro1', 'HoTro2', 'HoTro3', 'HoTro4', 'HoTro5',
               'LamThem', 'HoatDongKhac', 'NhaO', 'DiLai', 'TienAn', 'TienHoc',
               'TienHocThem', 'VuiChoi', 'CacKhoanKhac', 'ThuNhapBinhQuan', 'ThuNhapGiaDinh', 'ThuNhapHocBong',
               'ThuNhapTienVay', 'ThuNhapLamThem', 'ThuNhapKhac', 'KhoKhanCuocSong', 'DongTienHocKhong',
               'DongTienHocBaoNhieu',
               'DongTienNhaKhong', 'DongTienNhaBaoNhieu', 'HocThemKhong', 'HocThemBaoNhieu', 'DongTienKhac',
               'MongMuonNhanGiTuDH',
               'KhoKhanLamHoSo', 'LienLacCachNao1', 'LienLacCachNao2', 'LienLacCachNao3', 'LienLacCachNao4',
               'DeDatNhanNhu',
               'HinhThucThu', 'KhungVietThu', 'KhungScanThu', 'BangDiemScan', 'ChungNhanKhoKhanScan', 'GiayToKhacScan',
               'GiayToKhacList', 'AnhCaNhan']

FIELD_NAMES_FULL = {'HoVaTen': 'Họ và tên', 'GioiTinh': 'Giới tính', 'NgaySinh': 'Ngày sinh',
                    'MaSoSV': 'Mã số sinh viên', 'NamThu': 'Sinh viên năm thứ', 'KhoaNganh': 'Khoa/Ngành',
                    'Lop': 'Lớp', 'Truong': 'Trường', 'DiaChiSinh': 'Địa chỉ hiện tại',
                    'DiaChiTru': 'Địa chỉ thường trú', 'DienThoai': 'Điện thoại', 'Email': 'Email',
                    'NhaO': 'Nhà ở', 'DiLai': 'Đi lại', 'TienAn': 'Tiền ăn', 'TienHoc': 'Tiền học chính khoá',
                    'TienHocThem': 'Tiền học thêm', 'VuiChoi': 'Vui chơi, giải trí', 'CacKhoanKhac': 'Các khoản khác',
                    'ThuNhapGiaDinh': 'Thu nhập gia đình', 'ThuNhapHocBong': 'Học bổng',
                    'ThuNhapTienVay': 'Tiền vay ngân hàng', 'ThuNhapLamThem': 'Thu nhập làm thêm',
                    'ThuNhapKhac': 'Thu nhập khác',
                    'DeDatNhanNhu': 'Bạn có đề đạt, nhắn gửi gì tới quỹ học bổng Đồng Hành ?',
                    'MongMuonNhanGiTuDH': 'Bạn mong muốn nhận được gì từ Đồng Hành ngoài việc giúp đỡ tài chính?',
                    'KhoKhanLamHoSo': 'Bạn gặp khó khăn gì trong quá trình làm hồ sơ xin học bổng Đồng Hành?'
                    }

# Get the index (position of column) of each fields
INDEX_OF_KEY = {}
for index in range(0, len(FIELD_NAMES)):
    INDEX_OF_KEY[FIELD_NAMES[index]] = index

# Some table styles
TRANSPARENT_TABLE = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONT', (0, 0), (-1, -1), 'UVN'),
    ('FONT', (1, 0), (1, -1), 'UVNI'),
    ('FONT', (-1, 0), (-1, -1), 'UVNI'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
])
TRANSPARENT_TABLE_WITH_MERGE = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONT', (0, 0), (-1, -1), 'UVN'),
    ('FONT', (1, 0), (1, -1), 'UVNI'),
    ('FONT', (-1, 0), (-1, -1), 'UVNI'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('SPAN', (-1, 0), (-1, -1)),
])
TRANSPARENT_REGULAR_TABLE = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONT', (0, 0), (-1, -1), 'UVN'),
    ('FONT', (1, 0), (1, -1), 'UVN'),
    ('FONT', (-1, 0), (-1, -1), 'UVN'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
])
STANDARD_TABLE = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('ALIGN', (0, 1), (0, -1), 'LEFT'),
    ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ('FONT', (0, 0), (-1, 0), 'UVNB'),
    ('FONT', (0, 1), (0, -1), 'UVN'),
    ('FONT', (1, 1), (-1, -1), 'UVNI'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
])
HORIZONTAL_NUMERIC_TABLE = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('ALIGN', (0, 1), (-1, -1), 'RIGHT'),
    ('FONT', (0, 0), (-1, 0), 'UVNB'),
    ('FONT', (0, 1), (-1, -1), 'UVN'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
])
VERTICAL_TRANSPARENT_NUMERIC_TABLE = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
    ('FONT', (0, 0), (-1, -1), 'UVN'),
    ('FONT', (-1, 0), (-1, -1), 'UVNI'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
])
