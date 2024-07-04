from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class Qsa(BaseModel):
    pais: Optional[str]
    nome_socio: str
    codigo_pais: Optional[int]
    faixa_etaria: str
    cnpj_cpf_do_socio: str
    qualificacao_socio: str
    codigo_faixa_etaria: int
    data_entrada_sociedade: date
    identificador_de_socio: int
    cpf_representante_legal: str
    nome_representante_legal: Optional[str]
    codigo_qualificacao_socio: int
    qualificacao_representante_legal: str
    codigo_qualificacao_representante_legal: int


class CnaesSecundarios(BaseModel):
    codigo: int
    descricao: str


class ErrorResponseSchema(BaseModel):
    error: str
    message: str
    status_code: int
    details: Optional[str] = None


class Empresa(BaseModel):
    uf: str
    cep: str
    qsa: List[Qsa]
    cnpj: str
    pais: Optional[str]
    email: Optional[str]
    porte: str
    bairro: str
    numero: str
    ddd_fax: Optional[str]
    municipio: str
    logradouro: str
    cnae_fiscal: int
    codigo_pais: Optional[int]
    complemento: str
    codigo_porte: int
    razao_social: str
    nome_fantasia: str
    capital_social: int
    ddd_telefone_1: Optional[str]
    ddd_telefone_2: Optional[str]
    opcao_pelo_mei: Optional[bool]
    descricao_porte: Optional[str]
    codigo_municipio: int
    cnaes_secundarios: List[CnaesSecundarios]
    natureza_juridica: str
    situacao_especial: Optional[str]
    opcao_pelo_simples: Optional[bool]
    situacao_cadastral: int
    data_opcao_pelo_mei: Optional[date]
    data_exclusao_do_mei: Optional[date]
    cnae_fiscal_descricao: str
    codigo_municipio_ibge: int
    data_inicio_atividade: date
    data_situacao_especial: Optional[date]
    data_opcao_pelo_simples: Optional[date]
    data_situacao_cadastral: date
    nome_cidade_no_exterior: Optional[str]
    codigo_natureza_juridica: int
    data_exclusao_do_simples: Optional[date]
    motivo_situacao_cadastral: int
    ente_federativo_responsavel: Optional[str]
    identificador_matriz_filial: int
    qualificacao_do_responsavel: int
    descricao_situacao_cadastral: str
    descricao_tipo_de_logradouro: str
    descricao_motivo_situacao_cadastral: str
    descricao_identificador_matriz_filial: str