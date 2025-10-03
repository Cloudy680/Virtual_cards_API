def validate_card_by_luna_algorithm(card_number : str):
    card_to_check = list(card_number)
    card_to_check.reverse()
    odd = 0
    even = 0
    for i in range(len(card_to_check)):
        if (i + 1) % 2 != 0:
            odd +=  int(card_to_check[i])
        else:
            temp = int(card_to_check[i]) * 2
            while temp > 0:
                even += temp % 10
                temp //= 10

    if (odd + even) % 10 == 0:
        return True
    else:
        return False