# Registro de Testes Manuais e Exploratórios

## Matriz de Execução

| ID | Cenário | Tipo | Resultado Esperado | Resultado Obtido | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CT-M01** | Validação do banner de Frete Grátis | Exploratório | Exibir progresso até R$ 200 | Exibido corretamente | **PASSED** |
| **CT-M02** | Aplicação do cupom `BEMVINDO10` | Manual | Desconto de 10% no subtotal | Desconto aplicado | **PASSED** |
| **CT-M03** | Aplicação do cupom `VERAO2026` | Manual | Mensagem "Cupom expirado." | Mensagem exibida | **PASSED** |
| **CT-M04** | Subtotal R$ 200,00 com cupom aplicado | Exploratório | Frete Grátis (R$ 0,00) | Cobrou R$ 19,90 de frete | **FAILED (BUG-002)** |
| **CT-M05** | Adicionar 6 unidades do mesmo item | Exploratório | Impedir na UI / Erro 422 na API | Permitido via API (200 OK) | **FAILED (BUG-003)** |

## Premissas e Registro de Ambiguidade (Regras do Teste)
* **Ambiguidade identificada:** A regra de Frete Grátis não deixava claro se o limite de R$ 200,00 considera o valor *antes* ou *depois* do desconto do cupom. 
* **Interpretação adotada:** Conforme boas práticas de e-commerce e regra CA08, o benefício de frete grátis avalia o **subtotal bruto** dos produtos.