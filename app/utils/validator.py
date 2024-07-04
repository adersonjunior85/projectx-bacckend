def validate_cpf(cpf: str) -> bool:
    cpf = [int(d) for d in cpf]

    sum_ = sum([cpf[i] * (10 - i) for i in range(9)])
    remainder = sum_ % 11
    digit_1 = 0 if remainder < 2 else 11 - remainder

    if digit_1 != cpf[9]:
        return False

    sum_ = sum([cpf[i] * (11 - i) for i in range(10)])
    remainder = sum_ % 11
    digit_2 = 0 if remainder < 2 else 11 - remainder

    if digit_2 != cpf[10]:
        return False

    return True


def validate_cnpj(cnpj: str) -> bool:
    cnpj = [int(d) for d in cnpj]

    weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_ = sum([cnpj[i] * weights[i] for i in range(12)])
    remainder = sum_ % 11
    digit_1 = 0 if remainder < 2 else 11 - remainder

    if digit_1 != cnpj[12]:
        return False

    weights.insert(0, 6)
    sum_ = sum([cnpj[i] * weights[i] for i in range(13)])
    remainder = sum_ % 11
    digit_2 = 0 if remainder < 2 else 11 - remainder

    if digit_2 != cnpj[13]:
        return False

    return True
