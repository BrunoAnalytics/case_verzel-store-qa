import pytest
import requests
import allure
from src.schemas.cart_schema import RespostaCalculoCarrinho, RespostaErroAPI

@allure.epic("API Verzel Store")
@allure.feature("Cálculos de Carrinho e Pedidos (VZS-142)")
class TestCalculoCarrinhoAPI:

    @allure.story("CA01, CA02, CA09, CA11 - Cupom Válido e Sanitização")
    def test_calcular_carrinho_cupom_valido_sanitizacao(self, api_base_url):
        payload = {
            "itens": [{"produtoId": "P005", "quantidade": 1}],
            "cupom": " bemvindo10 "
        }
        response = requests.post(f"{api_base_url}/carrinho/calcular", json=payload)
        assert response.status_code == 200
        
        validado = RespostaCalculoCarrinho(**response.json())
        assert validado.subtotal == 100.00
        assert validado.desconto == 10.00
        assert validado.frete == 19.90
        assert validado.total == 109.90
        assert validado.cupom.codigo == "BEMVINDO10"
        assert validado.cupom.aplicado is True

    @pytest.mark.xfail(reason="BUG-002: API cobra frete com subtotal R$ 200,00 ao usar cupom")
    @allure.story("CA06, CA08 - Frete Grátis com Subtotal >= R$ 200,00")
    def test_regra_frete_gratis_limite(self, api_base_url):
        payload = {
            "itens": [{"produtoId": "P005", "quantidade": 2}],
            "cupom": "BEMVINDO10"
        }
        response = requests.post(f"{api_base_url}/carrinho/calcular", json=payload)
        assert response.status_code == 200
        
        validado = RespostaCalculoCarrinho(**response.json())
        assert validado.subtotal == 200.00
        assert validado.frete == 0.00
        assert validado.freteGratis is True

    @pytest.mark.xfail(reason="BUG-003: API aceita quantidade > 5 e retorna HTTP 200 em vez de 422")
    @allure.story("CA10 - Rejeitar item com quantidade maior que 5 (Status 422)")
    def test_quantidade_excedida_rejeicao(self, api_base_url):
        payload = {
            "itens": [{"produtoId": "P001", "quantidade": 6}]
        }
        response = requests.post(f"{api_base_url}/carrinho/calcular", json=payload)
        assert response.status_code == 422