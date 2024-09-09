from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ErrorDetailSchema(BaseModel):
    message: str = Field(..., description="Descrição do erro")
    code: int = Field(..., description="Código do erro")
    details: Optional[str] = Field(
        None, description="Detalhes adicionais sobre o erro"
    )


class ErrorResponseSchema(BaseModel):
    error: ErrorDetailSchema


class SuccessDataSchema(BaseModel):
    MinhaReceita: Optional[Dict[str, Any]] = Field(
        None, description="Dados da MinhaReceita"
    )


class SuccessResponseSchema(BaseModel):
    status_code: int = Field(
        200, description="Código de status HTTP da resposta"
    )
    data: list[Any]
    message: Optional[str] = Field(
        None, description="Mensagem explicativa da resposta"
    )
