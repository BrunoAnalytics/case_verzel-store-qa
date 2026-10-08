from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class ItemCarrinhoCalculado(BaseModel):
    model_config = ConfigDict(strict=True)

    produtoId: str
    nome: str
    precoUnitario: float = Field(..., ge=0)
    quantidade: int = Field(..., ge=1, le=5)
    total: float = Field(..., ge=0)

class CupomInfo(BaseModel):
    model_config = ConfigDict(strict=True)

    codigo: Optional[str] = None
    aplicado: bool
    mensagem: str

class RespostaCalculoCarrinho(BaseModel):
    model_config = ConfigDict(strict=True)

    itens: List[ItemCarrinhoCalculado]
    subtotal: float = Field(..., ge=0)
    desconto: float = Field(..., ge=0)
    frete: float = Field(..., ge=0)
    freteGratis: bool
    valorFaltanteFreteGratis: float = Field(..., ge=0)
    total: float = Field(..., ge=0)
    cupom: Optional[CupomInfo] = None

class RespostaErroAPI(BaseModel):
    erro: dict