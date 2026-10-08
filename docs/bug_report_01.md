# Relatório de Bugs Encontrados — Verzel Store

## BUG-001: Ausência de Validação de Nome e Sobrenome na API
* **Severidade:** Média
* **Endpoint:** `POST /api/pedidos`
* **Descrição:** Enviar nome sem sobrenome registra o pedido com HTTP 201 em vez de rejeitar.

---

## BUG-002: Falha no Cálculo de Frete Grátis com Subtotal de R$ 200,00
* **Severidade:** Alta
* **Endpoint:** `POST /api/carrinho/calcular`
* **Descrição:** Para o payload `{"itens": [{"produtoId": "P005", "quantidade": 2}], "cupom": "BEMVINDO10"}`, o subtotal é R$ 200,00, porém a API cobra R$ 19,90 de frete e marca `freteGratis: false`.
* **Causa Provável:** A regra de frete grátis está avaliando o valor com desconto (R$ 180,00) em vez do subtotal bruto dos produtos.

---

## BUG-003: API Aceita Quantidades Superiores a 5 Unidades (CA10)
* **Severidade:** Alta
* **Endpoint:** `POST /api/carrinho/calcular`
* **Descrição:** Enviar `quantidade: 6` no item retorna HTTP 200 OK.
* **Resultado Esperado:** HTTP 422 Unprocessable Entity com mensagem de quantidade máxima excedida.