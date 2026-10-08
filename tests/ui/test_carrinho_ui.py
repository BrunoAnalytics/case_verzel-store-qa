import pytest
import allure
from src.pages.cart_page import CartPage

@allure.epic("UI Verzel Store")
@allure.feature("Validação de Cupons na Interface")
class TestCarrinhoUI:

    @pytest.fixture(autouse=True)
    def setup(self, page, ui_base_url):
        # Fixture executada antes de cada teste para inicializar a página
        self.cart_page = CartPage(page)
        self.cart_page.navegar(ui_base_url)

    @allure.story("CT-UI-01: Exibição de mensagem para cupom inválido/inexistente")
    def test_mensagem_cupom_invalido_ui(self):
        with allure.step("Aplicar cupom inexistente"):
            self.cart_page.aplicar_cupom("CUPOMINEXISTENTE")
            
        with allure.step("Validar mensagem de erro"):
            mensagem = self.cart_page.obter_texto_mensagem()
            assert "Cupom inválido" in mensagem, f"Mensagem esperada não encontrada. Texto retornado: '{mensagem}'"

    @allure.story("CT-UI-02: Exibição de mensagem para cupom expirado")
    def test_mensagem_cupom_expirado_ui(self):
        with allure.step("Aplicar cupom fora da validade"):
            self.cart_page.aplicar_cupom("VERAO2026")
            
        with allure.step("Validar notificação de cupom expirado"):
            mensagem = self.cart_page.obter_texto_mensagem()
            assert "Cupom expirado" in mensagem, f"Mensagem esperada não encontrada. Texto retornado: '{mensagem}'"

    @allure.story("CT-UI-03: Aplicação bem-sucedida de cupom válido (BEMVINDO10)")
    def test_aplicar_cupom_valido_ui(self):
        with allure.step("Aplicar cupom válido de 10%"):
            self.cart_page.aplicar_cupom("BEMVINDO10")
            
        with allure.step("Validar confirmação de sucesso"):
            mensagem = self.cart_page.obter_texto_mensagem().lower()
            assert "aplicado" in mensagem or "sucesso" in mensagem, f"Feedback de sucesso não encontrado. Texto retornado: '{mensagem}'"