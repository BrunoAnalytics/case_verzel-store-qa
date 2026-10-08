# language: pt
Funcionalidade: Cálculo de Desconto e Frete na Verzel Store
  Como cliente da Verzel Store
  Quero aplicar cupons de desconto e obter frete grátis
  Para economizar nas minhas compras

  Contexto:
    Dado que o cliente possui produtos no carrinho de compras

  Cenário: Aplicação de cupom válido com sucesso (CA01, CA02, CA09)
    Quando o cliente insere o cupom " BEMVINDO10 "
    Então o sistema deve sanitizar o código para "BEMVINDO10"
    E aplicar 10% de desconto sobre o subtotal dos produtos
    E manter a taxa de frete fixa de R$ 19,90

  Cenário: Tentativa de aplicação de cupom expirado (CA04)
    Quando o cliente insere o cupom "VERAO2026"
    Então o sistema deve recusar o cupom
    E exibir a mensagem "Cupom expirado."

  Cenário: Concessão automática de Frete Grátis (CA06, CA08)
    Dado que o subtotal dos produtos no carrinho é igual ou superior a R$ 200,00
    Quando o carrinho é calculado
    Então o valor do frete deve ser R$ 0,00
    E a indicação de frete grátis deve ser ativada

  Cenário: Tentativa de adicionar mais de 5 unidades do mesmo produto (CA10)
    Quando o cliente altera a quantidade de um item para 6 unidades
    Então a API deve retornar o status HTTP 422 Unprocessable Entity
    E exibir a mensagem de erro "QUANTIDADE_MAXIMA_EXCEDIDA"