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
        # 1. Garante que estamos na página inicial para listar os produtos
        self.page.goto(self.ui_base_url)
        self.page.wait_for_load_state("networkidle")

        # 2. Busca qualquer botão que adicione ao carrinho e clica no primeiro
        btn_add = self.page.locator("button:has-text('Adicionar'), button:has-text('Comprar')").first
        if btn_add.is_visible(timeout=5000):
            btn_add.click()
            self.page.wait_for_timeout(1500) # Aguarda animação/requisição de adição

        # 3. Força a navegação direta para a rota do carrinho (evita falha ao clicar em ícones)
        self.page.goto(f"{self.ui_base_url}/carrinho")
        self.page.wait_for_load_state("networkidle")

    def aplicar_cupom(self, codigo: str):
        self.garantir_item_no_carrinho()

        # Estratégia robusta: busca o primeiro "textbox" disponível na tela do carrinho
        input_cupom = self.page.get_by_role("textbox").first.or_(self.page.locator("input[type='text']").first)
        
        try:
            input_cupom.wait_for(state="visible", timeout=5000)
            input_cupom.fill(codigo)
        except Exception as e:
            # Fallback de QA: Se não achar o campo, salva um print da tela para investigarmos o bug de interface
            self.page.screenshot(path="debug_tela_carrinho.png")
            pytest.fail(f"O campo de cupom não renderizou na tela (carrinho pode estar vazio). Print salvo em 'debug_tela_carrinho.png'.")

        # Clica em aplicar
        btn_aplicar = self.page.locator("button:has-text('Aplicar'), button:has-text('Adicionar')").last
        if btn_aplicar.is_visible():
            btn_aplicar.click()
        else:
            # Se não achar o botão, simula a tecla ENTER dentro do campo
            input_cupom.press("Enter")
        
        self.page.wait_for_timeout(2000) # Tempo para a API calcular o desconto e a UI atualizar

    def obter_texto_mensagem(self) -> str:
        # Pega todo o texto visível no corpo da página para garantir que a asserção ache a mensagem
        return self.page.locator("body").text_content()