# Verzel Store — Plano de Engenharia e Automação de QA (VZS-142)

Este repositório contém o pacote completo de Garantia da Qualidade para a entrega **VZS-142 (Cupons de Desconto e Frete Grátis)** da Verzel Store. O projeto contempla cenários BDD em Gherkin, testes manuais/exploratórios, relatórios de bugs, automação E2E/API e relatórios visuais de execução.

---

## 📁 1. Estrutura de Entregáveis e Documentação

Para facilitar a avaliação, todas as evidências e documentações técnicas do desafio estão organizadas no diretório [`/docs`](./docs/):

| Entregável Solicitado | Arquivo / Caminho no Repositório | Descrição |
| :--- | :--- | :--- |
| **Cenários em Gherkin** | [`docs/cenarios.feature`](./docs/cenarios.feature) | Cobertura BDD cobrindo todos os Critérios de Aceite (CA01 a CA11). |
| **Execução Manual & Exploratória** | [`docs/execucao_manual.md`](./docs/execucao_manual.md) | Matriz de testes manuais, resultados obtidos e registro de ambiguidades. |
| **Report de Bugs** | [`docs/bug_report_01.md`](./docs/bug_report_01.md) | Detalhamento técnico dos bugs encontrados (BUG-002 e BUG-003). |
| **Automação (Playwright + Pytest)** | [`tests/ui/`](./tests/ui/) e [`tests/api/`](./tests/api/) | Testes automatizados de UI e API com Page Object Model (POM). |

---

## 🧠 2. Registro de Premissas e Ambiguidades

De acordo com as regras do desafio, as seguintes premissas foram adotadas durante a análise técnica:

* **Regra de Frete Grátis vs. Cupom de Desconto:** A documentação não especificava explicitamente se o limite de R$ 200,00 para frete grátis deve ser avaliado antes ou depois do desconto do cupom.
* **Interpretação Adotada:** Seguindo o padrão de mercado de e-commerces e o Critério de Aceite **CA08**, o benefício de frete grátis é validado com base no **subtotal bruto** dos produtos (antes da aplicação do desconto do cupom).

---

## 📊 3. Cobertura de Testes e Matriz de Rastreabilidade

| Critério | Descrição Resumida | Tipo de Teste | Status na Automação |
| :--- | :--- | :--- | :--- |
| **CA01/CA02** | Desconto 10% `BEMVINDO10` + Sanitização (Trim/Case Insensitive) | API & UI | `PASSED` |
| **CA03** | Cupom inexistente exibe "Cupom inválido." sem aplicar desconto | API & UI | `PASSED` |
| **CA04** | Cupom expirado (`VERAO2026`) exibe "Cupom expirado." | API & UI | `PASSED` |
| **CA05** | Apenas um cupom por vez no carrinho | UI E2E | `PASSED` |
| **CA06/CA08** | Frete grátis para subtotal $\ge$ R$ 200,00 (antes do desconto) | API | `XFAIL` *(BUG-002)* |
| **CA07** | Frete fixo R$ 19,90 e cálculo do valor faltante para frete grátis | API & UI | `PASSED` |
| **CA09** | Desconto do cupom incide apenas sobre subtotal dos produtos | API | `PASSED` |
| **CA10** | Limite máximo de 5 unidades por produto | API BVA | `XFAIL` *(BUG-003)* |
| **CA11** | Arredondamento exato em 2 casas decimais | API Schema | `PASSED` |

> *Nota:* Os testes que falham devido a bugs conhecidos do sistema foram mapeados com a anotação `@pytest.mark.xfail` para garantir a integridade da suíte de Integração Contínua (CI).

---

## 🛠️ 4. Arquitetura do Fluxo de Automação e CI/CD

```mermaid
graph TD
    A[VS Code: Desenvolvimento Local] -->|Execução do Pytest| B[Suíte de Testes API/UI]
    B -->|Validação de Contrato| C[Pydantic v2 Schemas]
    A -->|Git Source Control| D[Push para GitHub: main]
    D -->|Gatilho Automático| E[GitHub Actions CI Pipeline]
    E -->|Instalação de Deps| F[Python 3.10 + Playwright Chromium]
    F -->|Execução Automática| G[Pytest com Geração Allure]
    G -->|Artefato de Evidências| H[Allure Report]