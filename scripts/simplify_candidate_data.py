# !/user/local/bin/python3
# -*- coding: utf-8 -*-

import csv
import sys

from constants import *
from utils.unicode_utils import titlestyle

SCHOOL_YEAR = {
    'Năm thứ nhất': 1, 'Năm thứ hai': 2, 'Khác': 3
}


def city(string1, string2):
    if string1 == '' or string2 == '':
        return ''
    else:
        return titlestyle(string1) \
                   .replace('Huyện ', '') \
                   .replace('Quận ', '') \
                   .replace('Thị Xã ', '') \
                   .replace(',', '-') \
               + "; " + string2


def transform_csv_to_list(filename):
    with open(os.path.abspath(filename), 'r', encoding='utf-8') as f:
        data = list(list(rec) for rec in csv.reader(f, delimiter=','))
        f.close()
    return data

# headers sample
# "Approval Status","Date","Họ và Tên","Giới tính","Ngày, tháng, năm sinh","Mã số sinh viên","Sinh viên năm thứ","Khoa/Ngành","Lớp","Trường","Số nhà, đường hoặc Thôn, xã","Quận, huyện, thị xã, thành phố (trực thuộc tỉnh)","Tỉnh/thành phố","Số nhà, đường hoặc Thôn, xã","Quận, huyện, thị xã (hoặc thành phố trực thuộc tỉnh)","Tỉnh/thành phố","Điện thoại","Email","Họ và tên bố","Tuổi","Nghề nghiệp","Họ và tên mẹ","Tuổi","Nghề nghiệp","Thành viên 1","Thành viên 2","Thành viên 3","Thành viên 4","Thành viên 5","Thành viên 6","Thành viên 7","Thành viên 8","Thành viên 9","Điểm xét tuyển đại học (ghi rõ từng môn)","Điểm trung bình học kì I năm thứ nhất (nếu có)","Điểm trung bình học kì II năm thứ nhất (nếu có)","Điểm trung bình học kì I năm thứ hai (nếu có)","Tổng điểm thi tốt nghiệp","Thành tích 1","Thành tích 2","Thành tích 3","Thành tích 4","Thành tích 5","Nơi bạn học phổ thông trung học","Bạn đã từng được nhận học bổng Đồng Hành chưa? Nếu có, ở kì nào?-Chưa từng","Bạn đã từng được nhận học bổng Đồng Hành chưa? Nếu có, ở kì nào?-Trước kì 35","Bạn đã từng được nhận học bổng Đồng Hành chưa? Nếu có, ở kì nào?-Kì 35","Bạn đã từng được nhận học bổng Đồng Hành chưa? Nếu có, ở kì nào?-Kì 36","Bạn đã từng được nhận học bổng Đồng Hành chưa? Nếu có, ở kì nào?-Kì 37","Bạn đã từng được nhận học bổng Đồng Hành chưa? Nếu có, ở kì nào?-Kì 38","Trong vòng 2 năm trở lại đây, bạn có được nhận hỗ trợ tài chính nào khác (ngoài học bông Đồng Hành) không ?","Hỗ trợ 1","Hỗ trợ 2","Hỗ trợ 3","Hỗ trợ 4","Hỗ trợ 5","Làm thêm (ghi rõ công việc, địa điểm và thời gian, ví dụ: gia sư tại Thủ Đức, 10 tiếng/tuần)","Các hoạt động tập thể, xã hội khác","a. Nhà ở","b. Đi lại","c. Tiền ăn","d. Tiền học chính khoá","e. Tiền học thêm","f. Vui chơi, giải trí","g. Các khoản khác","2. Thu nhập bình quân hằng tháng của gia đình","Gia đình","Học bổng","Tiền vay ngân hàng","Đi làm thêm","Khác (ghi rõ số tiền và nguồn)","4. Khó khăn lớn nhất khi bạn mới vào đại học:","Đóng tiền học: ","Nếu có, trong bao lâu?","Đóng tiền nhà: ","Nếu có, trong bao lâu?","Học thêm tin học, tiếng Anh: ","Nếu có, trong bao lâu?","Khác:","Bạn mong muốn nhận được gì từ Đồng Hành ngoài việc giúp đỡ tài chính?","Bạn gặp khó khăn gì trong quá trình làm hồ sơ xin học bổng Đồng Hành?","Bạn thấy việc liên lạc với Đồng Hành sau khi nhận học bổng sau khi nhận học bổng có cần thiết không? Nếu có, bằng hình thức nào?-Trao đổi qua thư điện tử","Bạn thấy việc liên lạc với Đồng Hành sau khi nhận học bổng sau khi nhận học bổng có cần thiết không? Nếu có, bằng hình thức nào?-Nhận bản tin Đồng Hành","Bạn thấy việc liên lạc với Đồng Hành sau khi nhận học bổng sau khi nhận học bổng có cần thiết không? Nếu có, bằng hình thức nào?-Thông qua trang web, diễn đàn","Bạn thấy việc liên lạc với Đồng Hành sau khi nhận học bổng sau khi nhận học bổng có cần thiết không? Nếu có, bằng hình thức nào?-Gặp gỡ ở Việt Nam","Bạn có đề đạt, nhắn gửi gì tới quỹ học bổng Đồng Hành?","Bạn chọn hình thức nào?","Khung thư","Hãy tải thư của bạn tại đây","Bảng điểm","Xác nhận hộ nghèo, hoàn cảnh khó khăn","Dành cho các giấy tờ khác","Nêu các giấy chứng nhận, giấy khen khác mà bạn có (trừ những tài liệu đã upload ở trên), cơ quan hoặc người cấp và thời gian kí. Bạn cần mang theo những tài liệu này trong buổi phỏng vấn.","Ảnh thẻ (tỉ lệ tốt nhất là 3x4)","Xác nhận-Tôi xác nhận mọi thông tin trên đây là đúng sự thật.","Quiz Score","Reference ID","IP","Country","Payment Amount","Payment Currency","Payment Completed","Coupon codes","Browser","Referrer","Form Host","Entry ID","Status"
def simplify(record, semester):
    new_record = [""] * 12
    fullname = titlestyle(record[2]).split(" ")
    new_record[0] = str(semester) + SCHOOL_NB.get(record[9], '21')
    new_record[1] = " ".join(fullname[:-1])
    new_record[2] = fullname[-1]
    new_record[3] = record[3]
    new_record[4] = record[4]
    new_record[5] = SCHOOL_YEAR[record[6]] if record[6] in SCHOOL_YEAR else ""
    new_record[6] = record[8].replace(',', ';')
    new_record[7] = SCHOOL_CODE_ALL.get(record[9], 'KHAC')
    new_record[8] = city(record[11], record[12])
    new_record[9] = record[16]
    new_record[10] = record[17]
    # last column is for result
    return new_record


def get_key_to_compare(item):
    return item[7].ljust(10, '0') + item[2].ljust(12, '0') + item[1].ljust(40, '0')


if __name__ == '__main__':
    data = transform_csv_to_list(sys.argv[1])
    semester = sys.argv[2]
    newdata = []
    for i in range(1, len(data)):
        res = simplify(data[i], semester)
        newdata.append(res)
    newdata = sorted(newdata, key=get_key_to_compare)
    with open(sys.argv[1][:-4] + '_Simplified.csv', 'w', encoding='utf-8') as fo:
        for i in range(len(newdata)):
            fo.write(newdata[i][0])
            for j in range(1, len(newdata[0])):
                fo.write(',')
                fo.write(str(newdata[i][j]))
            fo.write('\n')
    print("Successfully finished.")
