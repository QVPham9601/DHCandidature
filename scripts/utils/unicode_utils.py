# A python dictionary to transform Vietnamese letters and accents into ASCII-letters.
REMOVE_ACCENT = {
    'a': 'a', 'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
    'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
    'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
    'e': 'e', 'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
    'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
    'i': 'i', 'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
    'o': 'o', 'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
    'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
    'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
    'u': 'u', 'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
    'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
    'y': 'y', 'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
    'đ': 'd',
    'A': 'A', 'À': 'A', 'Á': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
    'Ă': 'A', 'Ằ': 'A', 'Ắ': 'A', 'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A',
    'Â': 'A', 'Ầ': 'A', 'Ấ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
    'E': 'E', 'È': 'E', 'É': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
    'Ê': 'E', 'Ề': 'E', 'Ế': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E',
    'I': 'I', 'Ì': 'I', 'Í': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
    'O': 'O', 'Ò': 'O', 'Ó': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
    'Ô': 'O', 'Ồ': 'O', 'Ố': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
    'Ơ': 'O', 'Ờ': 'O', 'Ớ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O',
    'U': 'U', 'Ù': 'U', 'Ú': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
    'Ư': 'U', 'Ừ': 'U', 'Ứ': 'U', 'Ử': 'U', 'Ữ': 'U', 'Ự': 'U',
    'Y': 'Y', 'Ỳ': 'Y', 'Ý': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y',
    'Đ': 'D',
    '\xcc\x80': '', '\xcc\x81': '', '\xcc\x89': '', '\xcc\x83': '', '\xbb\xa4': '',
    ' ': ' ',
}

LOWERCASE_TO_UPPERCASE = {
    'a': 'A', 'à': 'À', 'á': 'Á', 'ả': 'Ả', 'ã': 'Ã', 'ạ': 'Ạ',
    'ă': 'Ă', 'ằ': 'Ằ', 'ắ': 'Ắ', 'ẳ': 'Ẳ', 'ẵ': 'Ẵ', 'ặ': 'Ặ',
    'â': 'Â', 'ầ': 'Ầ', 'ấ': 'Ấ', 'ẩ': 'Ẩ', 'ẫ': 'Ẫ', 'ậ': 'Ậ',
    'e': 'E', 'è': 'È', 'é': 'É', 'ẻ': 'Ẻ', 'ẽ': 'Ẽ', 'ẹ': 'Ẹ',
    'ê': 'Ê', 'ề': 'Ề', 'ế': 'Ế', 'ể': 'Ể', 'ễ': 'Ễ', 'ệ': 'Ệ',
    'i': 'I', 'ì': 'Ì', 'í': 'Í', 'ỉ': 'Ỉ', 'ĩ': 'Ĩ', 'ị': 'Ị',
    'o': 'O', 'ò': 'Ò', 'ó': 'Ó', 'ỏ': 'Ỏ', 'õ': 'Õ', 'ọ': 'Ọ',
    'ô': 'Ô', 'ồ': 'Ồ', 'ố': 'Ố', 'ổ': 'Ổ', 'ỗ': 'Ỗ', 'ộ': 'Ộ',
    'ơ': 'Ơ', 'ờ': 'Ờ', 'ớ': 'Ớ', 'ở': 'Ở', 'ỡ': 'Ỡ', 'ợ': 'Ợ',
    'u': 'U', 'ù': 'Ù', 'ú': 'Ú', 'ủ': 'Ủ', 'ũ': 'Ũ', 'ụ': 'Ụ',
    'ư': 'Ư', 'ừ': 'Ừ', 'ứ': 'Ứ', 'ử': 'Ử', 'ữ': 'Ữ', 'ự': 'Ự',
    'y': 'Y', 'ỳ': 'Ỳ', 'ý': 'Ý', 'ỷ': 'Ỷ', 'ỹ': 'Ỹ', 'ỵ': 'Ỵ',
    'đ': 'Đ'
}

UPPERCASE_TO_LOWERCASE = {
    'A': 'a', 'À': 'à', 'Á': 'á', 'Ả': 'ả', 'Ã': 'ã', 'Ạ': 'ạ',
    'Ă': 'ă', 'Ằ': 'ằ', 'Ắ': 'ắ', 'Ẳ': 'ẳ', 'Ẵ': 'ẵ', 'Ặ': 'ặ',
    'Â': 'â', 'Ầ': 'ầ', 'Ấ': 'ấ', 'Ẩ': 'ẩ', 'Ẫ': 'ẫ', 'Ậ': 'ậ',
    'E': 'e', 'È': 'è', 'É': 'é', 'Ẻ': 'ẻ', 'Ẽ': 'ẽ', 'Ẹ': 'ẹ',
    'Ê': 'ê', 'Ề': 'ề', 'Ế': 'ế', 'Ể': 'ể', 'Ễ': 'ễ', 'Ệ': 'ệ',
    'I': 'i', 'Ì': 'ì', 'Í': 'í', 'Ỉ': 'ỉ', 'Ĩ': 'ĩ', 'Ị': 'ị',
    'O': 'o', 'Ò': 'ò', 'Ó': 'ó', 'Ỏ': 'ỏ', 'Õ': 'õ', 'Ọ': 'ọ',
    'Ô': 'ô', 'Ồ': 'ồ', 'Ố': 'ố', 'Ổ': 'ổ', 'Ỗ': 'ỗ', 'Ộ': 'ộ',
    'Ơ': 'ơ', 'Ờ': 'ờ', 'Ớ': 'ớ', 'Ở': 'ở', 'Ỡ': 'ỡ', 'Ợ': 'ợ',
    'U': 'u', 'Ù': 'ù', 'Ú': 'ú', 'Ủ': 'ủ', 'Ũ': 'ũ', 'Ụ': 'ụ',
    'Ư': 'ư', 'Ừ': 'ừ', 'Ứ': 'ứ', 'Ử': 'ử', 'Ữ': 'ữ', 'Ự': 'ự',
    'Y': 'y', 'Ỳ': 'ỳ', 'Ý': 'ý', 'Ỷ': 'ỷ', 'Ỹ': 'ỹ', 'Ỵ': 'ỵ',
    'Đ': 'đ', 'Đ': 'đ'
}


def to_ascii(my_string):
    '''
        Usage: rename(my_string)
        This function transforms a Vietnamese string into standard ASCII-string, eg. "Đường" into "Duong"
        Params(1):
            my_string: The string to be transformed.
    '''
    my_new_string = ''
    current = ''
    for index in range(len(my_string)):
        # Only transform letters in the REMOVE_ACCENT dictionary
        if current in REMOVE_ACCENT:
            my_new_string += REMOVE_ACCENT[current]
            current = ''

        # All ASCII letters should be conserved
        if ord(my_string[index]) <= 123 and ord(my_string[index]) >= 65:
            my_new_string += my_string[index]
            current = ''
        else:
            current += my_string[index]

    if current in REMOVE_ACCENT:
        my_new_string += REMOVE_ACCENT[current]
    return my_new_string.title().replace(' ', '_')


def lowercase(my_string):
    '''
        Usage: rename(my_string)
        This function transforms a Vietnamese string into its decapitalized form, "TRưƠnG" to "trương"
        Params(1):
            my_string: The string to be transformed.
    '''
    my_new_string = ''
    current = ''
    for index in range(len(my_string)):
        # Only transform letters in the REMOVE_ACCENT dictionary
        if current in UPPERCASE_TO_LOWERCASE:
            my_new_string += UPPERCASE_TO_LOWERCASE[current]
            current = ''

        if current in LOWERCASE_TO_UPPERCASE:
            my_new_string += current
            current = ''

        # All ASCII letters should be conserved
        if ord(my_string[index]) <= 122 and ord(my_string[index]) >= 65:
            my_new_string += current + my_string[index].lower()
            current = ''
        else:
            current += my_string[index]
    if current in UPPERCASE_TO_LOWERCASE:
        my_new_string += UPPERCASE_TO_LOWERCASE[current]
    if current in LOWERCASE_TO_UPPERCASE:
        my_new_string += current
    return my_new_string


def titlestyle(my_string):
    my_new_string = ''
    current = ''
    firstletter = True
    for index in range(len(my_string)):
        # Only transform letters in the REMOVE_ACCENT dictionary
        if current in UPPERCASE_TO_LOWERCASE:
            if firstletter:
                my_new_string += current
            else:
                my_new_string += UPPERCASE_TO_LOWERCASE[current]
            firstletter = False
            current = ''

        elif current in LOWERCASE_TO_UPPERCASE:
            if firstletter:
                my_new_string += LOWERCASE_TO_UPPERCASE[current]
            else:
                my_new_string += current
            firstletter = False
            current = ''

        # All ASCII letters should be conserved
        if ord(my_string[index]) <= 122 and ord(my_string[index]) >= 40:
            if firstletter:
                my_new_string += current + my_string[index].upper()
            else:
                my_new_string += current + my_string[index].lower()
            firstletter = False
            current = ''

        elif my_string[index] == ' ':
            firstletter = True
            current = ''
            my_new_string += ' '
        else:
            current += my_string[index]

    if current in UPPERCASE_TO_LOWERCASE:
        if firstletter:
            my_new_string += current
        else:
            my_new_string += UPPERCASE_TO_LOWERCASE[current]

    if current in LOWERCASE_TO_UPPERCASE:
        if firstletter:
            my_new_string += LOWERCASE_TO_UPPERCASE[current]
        else:
            my_new_string += current

    my_new_string = my_new_string.replace('  ', ' ').strip()

    return my_new_string
