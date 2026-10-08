import pytest
import allure
from src.pages.cart_page import CartPage

@allure.epic("UI Verzel Store")
@allure.feature("Validação de Cupons na Interface")
class TestCarrinhoUI:

    @allure.story("CT-UI-01: Exibição de mensagem para cupom inválido/inexistente")
    def test_mensagem_cupom_invalido_ui(self, page, ui_base_url):
        cart_page = CartPage(page)
        cart_page.navegar(ui_base_url)
        cart_page.aplicar_cupom("CUPOMINEXISTENTE")
        mensagem = cart_page.obter_texto_mensagem().lower()
        assert "inválido" in mensagem or "invalido" in mensagem

    @allure.story("CT-UI-02: Exibição de mensagem para cupom expirado")
    def test_mensagem_cupom_expirado_ui(self, page, ui_base_url):
        cart_page = CartPage(page)
        cart_page.navegar(ui_base_url)
        cart_page.aplicar_cupom("VERAO2026")
        mensagem = cart_page.obter_texto_mensagem().lower()
        assert "expirado" in mensagem

    @allure.story("CT-UI-03: Aplicação bem-sucedida de cupom válido (BEMVINDO10)")
    def test_aplicar_cupom_valido_ui(self, page, ui_base_url):
        cart_page = CartPage(page)
        cart_page.navegar(ui_base_url)
        cart_page.aplicar_cupom("BEMVINDO10")
        mensagem = cart_page.obter_texto_mensagem().lower()
        assert "aplicado" in mensagem or "10%" in mensagem or "sucesso" in mensagem