from uncertainties import ufloat
from uncertainties.umath import *
import math
import sys

def lista():
	return None

def propagando():

	contador = 1
	valor_erro = []

	print('\n')
	operacao = input('Seleciona a operação: * + / - ')

	while True:

		print('\n')
		valor = float(input(f"Informe o valor {contador}: "))
		erro = float(input(f"Informe o erro associado ao valor {contador}: "))

		v_e = ufloat(valor, erro)
		valor_erro.append(v_e)

		print('\n')
		continuar = input(f"Gostaria de continuar? S/N: ")

		if continuar == 'N':

			s = valor_erro[0]
			VALOR = []

			if operacao == '+':
				soma = sum(valor_erro)
				VALOR.append(soma)

			if operacao == "*":
				multiplicacao = math.prod(valor_erro)
				VALOR.append(multiplicacao)

			if operacao == '/':
				for valor in valor_erro[1:]:
					s = s/valor
				VALOR.append(s)

			if operacao == '-':
				for valor in valor_erro[1:]:
					s = s - valor
				VALOR.append(s)
			print('\n')
			print('='*45)
			print(f'Valor final com erro propagado: {VALOR[-1]}')
			print('='*45)
			break

		else:
			contador = contador + 1

def propagando2():

	contador = 1
	valor_erro = []

	print('\n')
	v = float(input(f'Digite o valor {contador}: '))
	e = float(input(f'Digite o erro {contador}: '))

	valor_prop_acuml = ufloat(v, e)

	while True:

		print('\n')
		operacao = input('Digite a operação: * / + - ')

		print('\n')
		v2 = float(input(f'Digite o valor {contador + 1}: '))
		e2 = float(input(f'Digite o erro {contador + 1}: '))
		ve2 = ufloat(v2, e2)

		if operacao == '*':
			valor_prop_acuml = valor_prop_acuml * ve2

		if operacao == '/':
			valor_prop_acuml = valor_prop_acuml / ve2

		if operacao == '+':
			valor_prop_acuml = valor_prop_acuml + ve2

		if operacao == '-':
			valor_prop_acuml = valor_prop_acuml - ve2

		print('\n')
		continuar = input('Gostaria de continuar? (S/N): ')

		if continuar == 'N':
			print('\n')
			print('='*45)
			print(f'Valor final com erro propagado: {valor_prop_acuml}')
			print('='*45)
			break

		else:
			contador = contador + 1

def introducao():
	print('='*45)

	print("Programa para calculo de incertezas propagadas. Você poderá escolher a operação e a quantidade de termos a serem aplicados")
	print("\n")
	print("Pode fornece uma lista ou digitar os dados a mão, apenas escolha qual voce quer usar: \n")
	print("1 - Lista")
	print("2 - Digitar com propagação fixa")
	print("3 - Digitar com propagação variável")
	print("\n")

	escolha = int(input("Digite qual você quer: "))

	if escolha == 1:
		print('Formato: Lista.\n')
		print('Observação: A lista deve ter a primeira coluna com os valores, e a segunda com os erros')
		lista()

	if escolha == 2:
		print('Formato: Digitado com propagação fixa.\n')
		propagando()

	if escolha == 3:
		print('Formato: Digitado com propagação variável.\n')
		propagando2()

	print("\n")

introducao()
