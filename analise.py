import os
import time
import json
import requests
from datetime import datetime
from random import random

def extrair_dados():
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

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
            dados = json.loads(response.text)
            ultimo_dado = dados[-1]
            cdi = float(ultimo_dado['valor'].replace(
                ',', '.')) + (random() - 0.5)

        if not os.path.exists('taxa-cdi.csv'):
            with open('taxa-cdi.csv', mode='w', encoding='utf8') as fp:
                fp.write('data,hora,taxa\n')

        with open('taxa-cdi.csv', mode='a', encoding='utf8') as fp:
            fp.write(f'{data},{hora},{cdi}\n')

        time.sleep(2 + (random() - 0.5))

    print("Extração concluída com sucesso!")
