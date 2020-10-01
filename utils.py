def get_digits(string):
    digits = []
    for char in string:
        if char.isdigit():
            digits.append(char)
    return digits
