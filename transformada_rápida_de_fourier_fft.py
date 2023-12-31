# -*- coding: utf-8 -*-
"""Transformada Rápida de Fourier - FFT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zMxj4mDPGb_Hbdj-RrjgK4Zt-ciiIg_j

OBS: Executar apenas a cédula do sinal de entrada desejado

Importação de bibliotecas
"""

import matplotlib.pyplot as plt
import numpy as np
import time
from scipy import signal

"""Criação do sinal de entrada senoidal"""

#Gerando sinal senoidal com 5 componentes de frequência:

freq_aq = 2000 #Frequência de aquisição.
n_amostras = 1024 #Número de amostras.
t = np.arange(n_amostras)/freq_aq #Vetor de pontos temporais a serem analisados.

#Determinação das frequências dos sinais
freq_1 = 100
freq_2 = 500
freq_3 = 250
freq_4 = 750
freq_5 = 900

#Determinação das amplitudes dos sinais
ampl_1 = 2
ampl_2 = 1.5
ampl_3 = 3
ampl_4 = 5
ampl_5 = 6

#Formação dos sinais senoidais
sinal_sen_1 = ampl_1*np.sin(2*np.pi*freq_1*t) #Cria sinal de 100 Hz.
sinal_sen_2 = ampl_2*np.sin(2*np.pi*freq_2*t) #Cria sinal de 500 Hz.
sinal_sen_3 = ampl_3*np.sin(2*np.pi*freq_3*t) #Cria sinal de 250 Hz.
sinal_sen_4 = ampl_4*np.sin(2*np.pi*freq_4*t) #Cria sinal de 750 Hz.
sinal_sen_5 = ampl_5*np.sin(2*np.pi*freq_5*t) #Cria sinal de 900 Hz.

sinal_sen_5_freqs = sinal_sen_1 + sinal_sen_2 + sinal_sen_3 + sinal_sen_4 + sinal_sen_5 #Cria sinal contendo as 5 frequências.
np.savetxt('sinal_entrada', sinal_sen_5_freqs) #Salva o sinal em um documento

"""Criação de um sinal quadrático"""

#Função de criação da onda quadrada
def onda_quadrada(freq, duracao, amostragem):
    t = np.linspace(0, duracao, int(amostragem * duracao), endpoint=False)
    onda = np.sign(np.sin(2 * np.pi * freq * t))
    return onda

#Parametrização da onda quadrada
freq = 5  # Frequência da onda quadrada em Hz
duracao = 2  # Duração da onda quadrada em segundos
amostragem = 1024  # Taxa de amostragem em Hz

#Geração da onda quadrada
sinal_entrada = onda_quadrada(freq, duracao, amostragem)
np.savetxt('sinal_entrada', sinal_entrada)

"""Criação de um sinal exponencial"""

#Função de criação do sinal exponencial
def sinal_exponencial(amplitude, decaimento, duracao, amostragem):
    t = np.linspace(0, duracao, int(amostragem * duracao), endpoint=False)
    sinal = amplitude * np.exp(-decaimento * t)
    return sinal

#Parametrização do sinal exponencial
amplitude = 5.0  # Amplitude do sinal exponencial
decaimento = 0.5  # Taxa de decaimento do sinal exponencial
duracao = 10  # Duração do sinal exponencial em segundos
amostragem = 1024  # Taxa de amostragem em Hz

#Geração do sinal exponencial
sinal_entrada = sinal_exponencial(amplitude, decaimento, duracao, amostragem)
np.savetxt('sinal_entrada', sinal_entrada)

"""Função FFT"""

#Função DFT do sinal de entrada
def dft_(sinal_entrada):
  sinal_entrada = np.asarray(sinal_entrada, dtype=float)
  N = sinal_entrada.shape[0]
  n = np.arange(N)
  k = n.reshape((N,1))
  M = np.exp(-2j*np.pi*k*n/N)
  return np.dot(M,sinal_entrada)

#Função FFT do sinal de entrada
#A função abaixo usa como referência a função DFT
def fft_(sinal_entrada):
  sinal_entrada = np.asarray(sinal_entrada, dtype=float)
  N = sinal_entrada.shape[0]
  if N % 2>0:
    raise ValueError("Tamanho da entrada tem que ser uma potencia de 2")
  elif N <= 32:
    return dft_(sinal_entrada)
  else:
    X_par = fft_(sinal_entrada[::2])
    X_impar = fft_(sinal_entrada[1::2])
    fator = np.exp(-2j*np.pi*np.arange(N)/N)
    sinal_saida = np.concatenate([X_par + fator[:int(N/2)] * X_impar, X_par + fator[int(N/2):] * X_impar])
  return sinal_saida

# Função para criar eixo X do gráfico no domínio da frequência:
def fft_freqs(sinal_entrada,freq_aq):
  freqs_fft = np.fft.fftfreq(len(sinal_entrada),d=1/freq_aq)
  freqs_fft = freqs_fft[:int(len(sinal_entrada)/2)] #Utiliza somente frequências abaixo da frequência de Nyquist.
  return freqs_fft

#Executando lógica do programa:
sinal_entrada = np.loadtxt('sinal_entrada') #Carrega o sinal de entrada do arquivo txt.
freq_aq = 2048 #Frequência na qual o sinal de entrada foi aquisitado.

x_tempo = np.arange(len(sinal_entrada))/freq_aq #Criação do eixo X do gráfico no tempo.
t2 = time.time()
saida_fft = fft_(sinal_entrada) # Calcula a FFT do sinal.
t3 = time.time()
time_fft = t3 - t2
frequencias = fft_freqs(sinal_entrada, freq_aq) # Criação do eixo X do gráfico na frequência.

# Tratamento das saídas para representação padrão do espectro de frequências:
saida_fft_1 = (np.abs(saida_fft)/len(sinal_entrada))*2
saida_fft_1 = saida_fft_1[:int(len(sinal_entrada)/2)]

#Tempo de execução da FFT:
print('Tempo de execução FFT')
print(time_fft)

"""Plot dos gráficos"""

# Plot 1: Sinal de Entrada
plt.figure(figsize=(10, 5))
plt.plot(x_tempo, sinal_entrada, '.-', color='#0f0')
plt.title('Sinal de Entrada')
plt.xlabel('Tempo')
plt.ylabel('Amplitude')
plt.grid()
plt.show()

# Plot 2: Saida FFT
plt.figure(figsize=(10, 5))
plt.plot(saida_fft, color='#00f')
plt.title('Saida FFT')
plt.xlabel('Frequência')
plt.grid()
plt.show()

# Plot 3: Saida FFT apos tratamento
plt.figure(figsize=(10, 5))
plt.plot(frequencias, saida_fft_1, color='#00f')
plt.title('Saida FFT apos tratamento')
plt.xlabel('Frequência')
plt.ylabel('Amplitude')
plt.grid()
plt.grid()
plt.show()