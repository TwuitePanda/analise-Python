import os
import time
import json
import csv
from sys import argv
from random import random
from datetime import datetime

import requests
import pandas as pd
import seaborn as sns


def extrair_dados():
    url = 'https://www2.cetip.com.br/ConsultarTaxaDi/ConsultarTaxaDICetip.aspx'

    for _ in range(10):
        data_e_hora = datetime.now()
        data = data_e_hora.strftime('%Y/%m/%d')
        hora = data_e_hora.strftime('%H:%M:%S')

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.HTTPError:
            print("Dado não encontrado, continuando.")
            cdi = None
        except Exception as exc:
            print("Erro, parando a execução.")
            raise exc
        else:
            dado = json.loads(response.text)
            cdi = float(dado['taxa'].replace(',', '.')) + (random() - 0.5)

        if not os.path.exists('taxa-cdi.csv'):
            with open('taxa-cdi.csv', mode='w', encoding='utf8') as fp:
                fp.write('data,hora,taxa\n')

        with open('taxa-cdi.csv', mode='a', encoding='utf8') as fp:
            fp.write(f'{data},{hora},{cdi}\n')

        time.sleep(2 + (random() - 0.5))

    print("Extração concluída com sucesso!")


def gerar_grafico(nome_do_grafico):
    df = pd.read_csv('taxa-cdi.csv')
    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    grafico.set_xticklabels(labels=df['hora'], rotation=90)
    grafico.get_figure().savefig(f"{nome_do_grafico}.png")
    print(f"Gráfico '{nome_do_grafico}.png' gerado com sucesso!")


if __name__ == '__main__':
    if len(argv) < 2:
        print("Uso: python analise.py <nome-do-grafico>")
    else:
        nome_do_grafico = argv[1]
        extrair_dados()
        gerar_grafico(nome_do_grafico)
