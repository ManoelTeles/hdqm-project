import pandas as pd
import numpy as np
import re
from datetime import datetime


class Measure():
    def __init__(self):
        pass

    def read_json(self, path):        
        return pd.read_json(path)

    def read_csv(self, path):        
        return pd.read_csv(path)


    def valid_email(self, email):
        valid = re.search(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z\.a-zA-Z]{1,3}', email)
        domain = ['com', 'br']
        if valid :
            valid_domain = email.split('.')[-1]
            if valid_domain not in domain:
                return False
            return True
        else:
            return False

    def valid_tel(self, telefone):
        # TODO: Aceitar ddd no formato de entrada do telefone

        if isinstance(telefone, str):
            # TODO: Adicionar funcionalidade para tratar telefone
            pass

        if isinstance(telefone, float):
            valid = False
            if not np.isnan(telefone):               
                if len(str(int(telefone))) == 8 or len(str(int(telefone))) == 9:
                    valid = True

            return valid

    def valid_date(self, date):
        valid = re.search(r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', date)
        if valid :
            return True
        else:
            return False

    def convert_date_valid_format(self, date, pattern):
        format_date = ''
        if 'iso':            
            format_date = str(date).replace('.000Z', '')
            format_date = format_date.replace('T', ' ')        
        try:
            format_date = datetime.strptime(format_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            format_date = '9999-99-99 99:99:99'
        return str(format_date)

    def accuracy(self, column, module):
        num_rows = len(column)
        linhas_invalidas = 0
        linhas_validas = 0

        if module == 'email':        
            for row in column:
                if self.valid_email(row):
                    linhas_validas += 1
                else:
                    linhas_invalidas += 1

        elif module == 'telefone':
            for row in column:
                if self.valid_tel(row):
                    linhas_validas += 1
                else:
                    linhas_invalidas += 1                    

        report = {'acuracia':{}}
        report['acuracia']['nome_coluna'] = column.name
        report['acuracia']['numero_de_linhas'] = num_rows
        report['acuracia']['numero_de_linhas_validas'] = linhas_validas
        report['acuracia']['numero_de_linhas_invalidas'] = linhas_invalidas
        report['acuracia']['percentual_de_acuracia'] = linhas_validas * 100 / num_rows

        if linhas_invalidas == 0:
            report['percentual_de_acuracia'] = linhas_validas  * 100 / num_rows        
        return report            

    
    def completeness(self, column):
        num_rows = len(column)
        linhas_invalidas = 0
        linhas_validas = 0
        
        for row in column:
            if isinstance(row, str):
                if row is None or row == '':
                    linhas_invalidas += 1
                else:
                    linhas_validas += 1                    
            if isinstance(row, float):
                if np.isnan(row):
                    linhas_invalidas += 1
                else:
                    linhas_validas += 1                    

        report = {'completude':{}}
        report['completude']['nome_coluna'] = column.name
        report['completude']['numero_de_linhas'] = num_rows
        report['completude']['numero_de_linhas_validas'] = linhas_validas
        report['completude']['numero_de_linhas_invalidas'] = linhas_invalidas
        report['completude']['percentual_de_completude'] = linhas_validas  * 100 / num_rows

        if linhas_invalidas == 0:
            report['percentual_de_completude'] = num_rows  * 100 / num_rows        
        return report


    def atualidade(self, key_pk, key_value, data_type, column_a, column_b):
        df_merge = pd.merge(column_a, column_b, how='inner', on=key_pk)
        num_rows = len(df_merge)
        value_x = '{}_x'.format(key_value)
        value_y = '{}_y'.format(key_value)
        df_atualidade = df_merge[[key_pk, value_x, value_y]]
        linhas_invalidas = 0
        linhas_validas = 0

        if data_type == 'date':
            for row in df_atualidade.itertuples():
                date_a = str(row[2])
                date_b = str(row[3])

                if not self.valid_date(date_a):
                    date_a = self.convert_date_valid_format(date_a, 'iso')

                if not self.valid_date(date_b):
                    date_b = self.convert_date_valid_format(date_b, 'iso')

                if date_a != date_b:
                    linhas_invalidas += 1
                else:
                    linhas_validas += 1                    

        report = {'atualidade':{}}
        report['atualidade']['nome_coluna'] = key_value
        report['atualidade']['numero_de_linhas'] = num_rows
        report['atualidade']['numero_de_linhas_validas'] = linhas_validas
        report['atualidade']['numero_de_linhas_invalidas'] = linhas_invalidas
        report['atualidade']['percentual_de_atualidade'] = linhas_validas  * 100 / num_rows

        if linhas_invalidas == 0:
            report['percentual_de_atualidade'] = num_rows  * 100 / num_rows        
        return report

    def confiabilidade(self, df, column_validar, column_validacao):
        num_rows = len(df)
        linhas_invalidas = 0
        linhas_validas = 0

        for row in df[[column_validar, column_validacao]].itertuples():
            valid = row[2]
            if valid == 'N':
                linhas_invalidas += 1
            else:
                linhas_validas += 1

        report = {'confiabilidade':{}}
        report['confiabilidade']['nome_coluna'] = column_validar
        report['confiabilidade']['numero_de_linhas'] = num_rows
        report['confiabilidade']['numero_de_linhas_validas'] = linhas_validas
        report['confiabilidade']['numero_de_linhas_invalidas'] = linhas_invalidas
        report['confiabilidade']['percentual_de_confiabilidade'] = linhas_validas  * 100 / num_rows  
        return report       

        

