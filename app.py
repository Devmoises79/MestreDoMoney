import locale
import random
import plotext as plt
import math

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# -------------------- Boas-vindas --------------------
print(" Bem-vindo(a) ao Simulador Financeiro Gamificado! \n")
print("Aqui você vai explorar sua jornada financeira de forma divertida e educativa.")
print("Você poderá calcular investimentos, planejar sua aposentadoria e simular ações,")
print("enquanto acumula pontos e evolui de nível conforme aprende e pratica.\n")
print(" Dica: faça escolhas conscientes, acompanhe seu patrimônio e veja seu progresso!")
print("Vamos começar essa jornada?\n")

# -------------------- Funções de leitura --------------------
def ler_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Entrada inválida. Digite um número inteiro válido.")

def ler_float(prompt):
    while True:
        try:
            entrada = input(prompt).replace(',', '.').replace('%','').strip()
            return float(entrada)
        except ValueError:
            print("❌ Entrada inválida. Digite um número válido, ex: 1000,50 ou 3%")

# -------------------- Cálculos --------------------
def calcular_valor_futuro_series(idade_inicial, idade_final, aporte_mensal, taxa_juros_mensal, inflacao_mensal=0, aporte_variavel=0):
    n = (idade_final - idade_inicial) * 12
    valores = []
    valor_total = 0
    for mes in range(n):
        valor_total = (valor_total + aporte_mensal) * (1 + taxa_juros_mensal)
        aporte_mensal *= (1 + aporte_variavel)
        valor_real = valor_total / max(((1 + inflacao_mensal) ** (mes+1)), 1e-6)
        valores.append(valor_real)
    return valores

def calcular_valor_presente(pagamento_mensal, taxa_juros_mensal, numero_periodos):
    return pagamento_mensal * (1 - (1 + taxa_juros_mensal) ** -numero_periodos) / taxa_juros_mensal

def simular_acoes_series(investimento_inicial, meses, retorno_medio_mensal=0.01, desvio_mensal=0.02):
    valores = [investimento_inicial]
    for _ in range(1, meses):
        rendimento = random.normalvariate(retorno_medio_mensal, desvio_mensal)
        valores.append(valores[-1]*(1+rendimento))
    return valores

# -------------------- Gamificação --------------------
pontos = 0
def adicionar_pontos(valor):
    global pontos
    pontos += valor
    nivel = "Iniciante"
    if pontos >= 50:
        nivel = "Mestre das Finanças"
    elif pontos >= 25:
        nivel = "Investidor em Treinamento"
    elif pontos >= 10:
        nivel = "Planejador"
    print(f" Pontos ganhos: {valor}. Total: {pontos} | Nível atual: {nivel}")

# -------------------- Função para resumo --------------------
def mostrar_resumo():
    nivel = "Iniciante"
    if pontos >= 50:
        nivel = "Mestre das Finanças"
    elif pontos >= 25:
        nivel = "Investidor em Treinamento"
    elif pontos >= 10:
        nivel = "Planejador"

    print("\n🎉 Resumo da sua jornada financeira gamificada 🎉")
    print(f"Total de pontos acumulados: {pontos}")
    print(f"Nível alcançado: {nivel}")
    print("Continue praticando para evoluir ainda mais seus conhecimentos em finanças!\n")

# -------------------- Menu --------------------
while True:
    print("\n Simulador Financeiro com Gráficos")
    print("1 - Calcular valor acumulado até aposentadoria")
    print("2 - Calcular capital necessário para saques após aposentadoria")
    print("3 - Calcular patrimônio necessário para receber X por mês até certa idade limite")
    print("4 - Simulação de ações com risco")
    print("0 - Sair")
    
    escolha = input("Escolha uma opção: ").strip()
    
    if escolha == '1':
        idade_inicial = ler_int("Digite a idade inicial: ")
        idade_final = ler_int("Digite a idade final: ")
        aporte_mensal = ler_float("Digite o valor do aporte mensal (R$): ")
        taxa_juros_mensal = ler_float("Digite a taxa de juros mensal (em %): ") / 100
        inflacao_anual = ler_float("Digite a inflação anual estimada (em %, ou 0 se não quiser considerar): ")
        inflacao_mensal = (1 + inflacao_anual/100)**(1/12) - 1
        aporte_tipo = input("Deseja aporte crescente, decrescente ou fixo? (crescente/decrescente/fixo): ").strip().lower()
        if aporte_tipo == "crescente":
            aporte_variavel = 0.01
        elif aporte_tipo == "decrescente":
            aporte_variavel = -0.01
        else:
            aporte_variavel = 0

        valores_real = calcular_valor_futuro_series(idade_inicial, idade_final, aporte_mensal, taxa_juros_mensal, inflacao_mensal, aporte_variavel)
        print(f"\n✅ Valor final acumulado ajustado pela inflação: {locale.currency(valores_real[-1])}")
        adicionar_pontos(5)

        plt.clf()
        plt.plot(valores_real, label="Patrimônio real")
        plt.title("Evolução do patrimônio")
        plt.xlabel("Meses")
        plt.ylabel("Valor (R$)")
        plt.show()

    elif escolha == '2':
        saque_mensal = ler_float("Digite o valor do saque mensal desejado (R$): ")
        anos_saques = ler_int("Digite o número de anos para os saques: ")
        taxa_juros_mensal = ler_float("Digite a taxa de juros mensal (em %): ") / 100
        numero_periodos = anos_saques*12
        capital_necessario = calcular_valor_presente(saque_mensal, taxa_juros_mensal, numero_periodos)
        print(f"\n✅ Capital necessário: {locale.currency(capital_necessario)}")
        adicionar_pontos(5)

    elif escolha == '3':
        saque_mensal = ler_float("Digite o valor que deseja receber por mês (R$): ")
        idade_inicio = ler_int("A partir de que idade você começará a receber?: ")
        idade_final = ler_int("Até que idade deseja receber?: ")
        taxa_juros_mensal = ler_float("Digite a taxa de rendimento mensal (em %): ") / 100
        numero_periodos = (idade_final - idade_inicio) * 12
        capital_necessario = calcular_valor_presente(saque_mensal, taxa_juros_mensal, numero_periodos)
        print(f"\n✅ Capital necessário: {locale.currency(capital_necessario)}")
        adicionar_pontos(5)

    elif escolha == '4':
        investimento_inicial = ler_float("Digite o valor inicial (R$): ")
        meses = ler_int("Digite por quantos meses deseja simular: ")
        valores_acoes = simular_acoes_series(investimento_inicial, meses)
        print(f"\n✅ Valor final simulado: {locale.currency(valores_acoes[-1])}")
        adicionar_pontos(10)

        plt.clf()
        plt.plot(valores_acoes, label="Simulação Ações")
        plt.title("Evolução de investimento em ações")
        plt.xlabel("Meses")
        plt.ylabel("Valor (R$)")
        plt.show()

    elif escolha == '0':
        print("\nObrigado por usar o simulador! Até a próxima.")
        mostrar_resumo()
        break

    else:
        print("Opção inválida, tente novamente.")
