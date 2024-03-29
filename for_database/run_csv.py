from urllib.parse import urlparse
import csv
import re

filepath = '/home/user/Downloads/dataset/normalTrafficTest.txt'
filepath2 = '/home/user/Downloads/feautingTestAnomalousAndNormal.csv'
filepath3 = '/home/user/Downloads/feautingTraningAnomalousAndNormal.csv'

contRequest = 0

with open(filepath2, 'w', newline='') as file:
    # funções para o cabeçalho do arquivo csv
    fieldnames = ['LENGTH REQUEST','LENGTH ARGUMENTS', 'LENGTH PATH', 'SPECIAL CARACTERS PATH', 'NUMBER ARGUMENTS', 'LABEL']
    thewriter = csv.DictWriter(file, fieldnames=fieldnames)
    thewriter.writeheader()

    with open(filepath) as arq:
        line = arq.readline()
        while contRequest <= 18000:  # analisa o numero de request comparado no while 
            # zera as variaveis
            lengthRequest = 0
            lengthArguments = 0
            lengthPath = 0
            specialCaractersPath = 0
            numberArguments = 0
            # pega a primeira linha completa do request HTTP
            while line.find('HTTP/1') == -1:
                line = ''.join(arq.readline)
            # LENGTH REQUEST
            lengthRequest += len(line)
            # LENGTH ARGUMENTS
            url = urlparse(line)
            lengthArguments = len(url.query) - 11 # retira 11 por conta da versão do 'HTTP/1.1\n'
            if lengthArguments == -11:
                lengthArguments = 0
            # LENGTH PATH
            lengthPath = len(url.path)
            # SPECIAL CARACTERS PATH 
            for car in url.query: 
                if car == '&' or car == '%' or car == ' ' or car == '!' or car == '\"' or car == '#' or car == '$' or car == '\'' or car == '(' or car == ')' or car == '*' or car == '+' or car == ',' or car == '-' or car == '.' or car == '/' or car == ':' or car == ';' or car == '<' or car == '>' or car == '=' or car == '?' or car == '@' or car == '[' or car == ']' or car == '^' or car == '`' or car == '{' or car == '}' or car == '_' or car == '|' or car == '~': 
                    specialCaractersPath += 1
            # NUMBER ARGUMENTS
            numberArguments = url.query.count('=')
            # read line
            line = arq.readline()
            
            # CSV
            thewriter.writerow({'LENGTH REQUEST': lengthRequest, 'LENGTH ARGUMENTS': lengthArguments, 'LENGTH PATH': lengthPath, 'SPECIAL CARACTERS PATH': specialCaractersPath, 'NUMBER ARGUMENTS': numberArguments ,'LABEL': 0})