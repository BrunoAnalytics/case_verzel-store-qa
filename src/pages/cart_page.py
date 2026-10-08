import pytest
from playwright.sync_api import Page

class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.ui_base_url = ""

    def navegar(self, ui_base_url: str):
        self.ui_base_url = ui_base_url.rstrip("/")
        self.page.goto(self.ui_base_url)
        self.page.wait_for_load_state("networkidle")

    def garantir_item_no_carrinho(self):
        # Acessa a página inicial para carregar a listagem de produtos
        self.page.goto(self.ui_base_url)
        self.page.wait_for_load_state("networkidle")

        # Localiza botões de adição ao carrinho e interage com o primeiro disponível
        btn_add = self.page.locator("button:has-text('Adicionar'), button:has-text('Comprar')").first
        if btn_add.is_visible(timeout=5000):
            btn_add.click()
            self.page.wait_for_timeout(1500) # Aguarda animação ou requisição de adição

        # Navega diretamente para a rota do carrinho
        self.page.goto(f"{self.ui_base_url}/carrinho")
        self.page.wait_for_load_state("networkidle")

    def aplicar_cupom(self, codigo: str):
        self.garantir_item_no_carrinho()

        # Localiza o input de cupom
        input_cupom = self.page.get_by_role("textbox").first.or_(self.page.locator("input[type='text']").first)
        
        try:
            input_cupom.wait_for(state="visible", timeout=5000)
            input_cupom.fill(codigo)
        except Exception as e:
            # Salva screenshot em caso de falha de renderização do elemento
            self.page.screenshot(path="debug_tela_carrinho.png")
            pytest.fail("O campo de cupom não renderizou na tela. Print salvo em 'debug_tela_carrinho.png'.")

        # Localiza e clica no botão de aplicar, com fallback para a tecla Enter
        btn_aplicar = self.page.locator("button:has-text('Aplicar'), button:has-text('Adicionar')").last
        if btn_aplicar.is_visible():
            btn_aplicar.click()
        else:
            input_cupom.press("Enter")
        
        self.page.wait_for_timeout(2000) # Aguarda processamento da API e atualização da interface

    def obter_texto_mensagem(self) -> str:
        # Retorna o texto de todo o body para cobrir notificações e toasts dinâmicos
        return self.page.locator("body").text_content()