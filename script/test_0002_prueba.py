import pandas as pd
import requests
import json

#Declaro listas vacías donde se almacenarán que conformarán la tabla excel
base = []
quote = []
precio = []
#Creo constante tupla ya que seran los mismos pares siempre
pares = ("BTC_USDC", "BTC_ARS", "ETH_USDC", "ETH_ARS", "USDC_ARS", "RPC_USDC", "DAI_ARS", "BCH_ARS", "ZEC_ARS",
         "RCN_BTC", "ETH_BTC", "UBI_USDC")
#Variable de url obtenida delinspector Network de la url enviada en el challenge
website = 'https://api.exchange.ripio.com/api/v1/tradehistory/'

#Primera iteración obtengo el par y el response en formato json
for i in range (len(pares)):
    website = website + pares[i] #Esta url compuesta por la url base y el par correspondiente a la iteración
    divisor = (pares[i]).split('_')#Separo el par para obtener BASE y QUOTE de la iteración
    base.append(divisor[0]) #Se obtiene BASE de la iteración y se agrega a la lista base
    quote.append(divisor[1]) #Se obtiene QUOTE de la iteración y se agrega a la lista quote
    response = requests.get(website) #Se obtiene el response de la API
    response = response.content #Se obtiene el contenido del response
    response = json.loads(response.decode('utf-8')) #Se convierte en json el contenido del response
    #Se inicializan variables suma y contador en cero para calcular AVERAGE
    suma = 0
    contador = 0
    try:
      for operaciones in response: #Segunda iteración para calcular y obtener AVERAGE
        suma = suma + float(operaciones['price']) #Se obtiene atributo price de cada dato del response y se suma
        contador = contador + 1 #Se incrementea en uno el contador para luego sacar el promedio
      average = suma / contador #Se obtiene el promedio o AVERAGE
      average = round(average, 2) #Se simplifica el AVERAGE a un float con dos decimales
      average = str(average) #Se convierte en string el AVERAGE
      precio.append(average) #Se agrega AVERAGE a la lista
    except (ValueError, ZeroDivisionError): #Captura error en caso de que algún par no tenga operaciones y contador =0
      print('Par ' + pares[i] + ' no registra operaciones.') #Imprime por consola el par que no tuvo operaciones
      precio.append('null') #Agrega como valor a la tabla null en caso de no tener operaciones
    finally:
      website = 'https://api.exchange.ripio.com/api/v1/tradehistory/' #Limpia la website y la deja lista para la
      # siguiente iteración
      data = {'BASE': base,
              'QUOTE': quote,
              'AVERAGE_PRICE': precio} #Se crea la data con los datos de las listas

df = pd.DataFrame(data) #Se crea DataFrame y se le pasa la data
writer = pd.ExcelWriter('prices.xlsx') #Se escribe el excel y se le colola nombre y ruta al excel
df.to_excel(writer, sheet_name="Prices", index=False) #Se escribe el archivo, se le da nombre a la hoja y se coloca...
# index = False para eliminar la columna con el índice
writer.save() #Salva los cambios del archivo
print('Archivo creado con éxito')