from enum import Enum


class TollVoucherProviders(Enum):
    SEM_PARAR = "sem_parar"
    CONECTCAR = "conectcar"


class TollVoucherProvidersStrEnum(str, Enum):
    conectcar = "conectcar"
    semparar = "semparar"
