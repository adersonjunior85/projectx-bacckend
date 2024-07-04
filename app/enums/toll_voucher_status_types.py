from enum import Enum


class TollVoucherStatusTypes(Enum):
    EMITTED = "emitted"
    ERROR = "error"
    CANCELED = "canceled"
    DRAFT = "draft"
