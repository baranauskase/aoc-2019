def is_valid_password(password):
    '''
    It is a six-digit number.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
    '''

    last_digit = password % 10
    password = password // 10

    total_digits = 1
    repeated_vals_map = {last_digit: 1}
    has_repeated_char = False

    while password:
        digit = password % 10

        if digit in repeated_vals_map:
            repeated_vals_map[digit] += 1
        else:
            repeated_vals_map[digit] = 1

        if last_digit < digit:
            return False
        elif last_digit == digit:
            has_repeated_char = True

        total_digits += 1
        password = password // 10
        last_digit = digit

    # check if we have at least  one pair of adjacent
    # matching digits that are not part of larger
    # group
    num_pairs = 0
    for _, num_vals in repeated_vals_map.items():
        if num_vals == 2:
            num_pairs += 1

    return total_digits == 6 and has_repeated_char and num_pairs > 0


def count_password_combos(min_val, max_val):
    num_candidates = 0
    for cand in range(min_val, max_val+1):
        if is_valid_password(cand):
            num_candidates += 1

    return num_candidates


if __name__ == '__main__':
    pass_count = count_password_combos(245318, 765747)

    print(f'The number of password combos is {pass_count}')