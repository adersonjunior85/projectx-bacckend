import re

from app.utils.validator import validate_cnpj, validate_cpf


def format_cpf_cnpj(document: str) -> tuple:
    document = re.sub(r"\D", "", document)

    if len(document) == 11:
        valid = validate_cpf(document)
        doc_type = "CPF"
    elif len(document) == 14:
        valid = validate_cnpj(document)
        doc_type = "CNPJ"
    else:
        raise ValueError("Document must have 11 or 14 digits")

    if len(document) == 11:
        formatted_document = (
            f"{document[:3]}.{document[3:6]}.{document[6:9]}-{document[9:]}"
        )
    else:
        formatted_document = f"{document[:2]}.{document[2:5]}.{document[5:8]}/{document[8:12]}-{document[12:]}"

    return formatted_document, valid, doc_type
