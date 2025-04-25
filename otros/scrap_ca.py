# -*- coding: utf-8 -*-
"""
Created on Wed May 31 14:34:03 2023

@author: joaquin.rivadeneyra
"""

import os
import time
from selenium import webdriver
from time import sleep
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# driver_path = 'D:\\chromedriver\\chromedriver.exe' 
driver_path = r'C:\Users\joaquin.DESKTOP-RQGFIKL\Downloads\scrap_cets\chromedriver.exe' 

actproy='Proyecto'
# actproy='Actividad'
# actproy='ActProy'

headless = 1 # cambiar a 1 para headless (sin abrir navegador)

year=2024

#### Nacional ####
especificos = [
    ("nivel_gobierno","ctl00$CPH1$BtnTipoGobierno","gobierno nacional"),
    ("sector","ctl00$CPH1$BtnSector","salud"),
    ]
# especificos = [
#    ("nivel_gobierno","ctl00$CPH1$BtnTipoGobierno","gobierno nacional"),
#    ("sector","ctl00$CPH1$BtnSector","agrario y de riego") 
#    ] # del 2021 a adelante

#### Regional ####
 
# especificos = [
#     ("nivel_gobierno","ctl00$CPH1$BtnTipoGobierno","gobiernos regionales"),
#     ("sector","ctl00$CPH1$BtnSector","gobiernos regionales"),
#     ("funcion", "ctl00$CPH1$BtnFuncion", "agropecuaria")
#     ]

#### Local ####
 
# especificos = [
#     ("nivel_gobierno","ctl00$CPH1$BtnTipoGobierno","gobiernos locales"),
#     ("gob_loc","ctl00$CPH1$BtnSubTipoGobierno","municipalidades"),
#     ("funcion", "ctl00$CPH1$BtnFuncion", "agropecuaria")
#     ]



# parameters= [(nombre del filtro, name del boton como elemento de pagina web, dummy print, empezar desde)]

#### Nacional ####
parameters = [
    # ("sector","ctl00$CPH1$BtnSector",1,1),
    # ("pliego", "ctl00$CPH1$BtnPliego", 1, 1),
    # ("ejecutora", "ctl00$CPH1$BtnEjecutora", 1,1),
    ("categoria_pptal","ctl00$CPH1$BtnProgramaPpto",1,1),
    # ("funcion","ctl00$CPH1$BtnFuncion",0, 1),
    # ("div_funcional", "ctl00$CPH1$BtnDivFuncional", 0, 1),
    # ("grupo_funcional","ctl00$CPH1$BtnGrupoFuncional", 0, 1),
    # ("fuente", "ctl00$CPH1$BtnFuenteAgregada", 0,1),
    # ("rubro", "ctl00$CPH1$BtnRubro", 0, 1),
    # ("tiporec","ctl00$CPH1$BtnTipoRecurso",0,1),
    # ("gen", "ctl00$CPH1$BtnGenerica", 0,1),
    # ("subgen","ctl00$CPH1$BtnSubGenerica",0,1),
    # ("detsubgen","ctl00$CPH1$BtnSubGenericaDetalle",0,1),
    # ("especifica","ctl00$CPH1$BtnEspecifica",0,1),
    # ("det_espeficica","ctl00$CPH1$BtnEspecificaDetalle",0,1),
    # ("departamento", "ctl00$CPH1$BtnDepartamentoMeta", 0, 1),
    ("prodproy","ctl00$CPH1$BtnProdProy",0,1),
    # ("act_accinver_obra", "ctl00$CPH1$BtnAAO",0,1),
    # ("meta", "ctl00$CPH1$BtnMeta", 0, 1),
    # ("mes", "ctl00$CPH1$BtnMes", 0, 1)
    ]

#### Regional ####

# parameters = [
#     ("pliego", "ctl00$CPH1$BtnPliego", 1, 1),
#     ("ejecutora", "ctl00$CPH1$BtnEjecutora", 1,1),
#     ("categoria_pptal","ctl00$CPH1$BtnProgramaPpto",0,1),
#     ("prodproy","ctl00$CPH1$BtnProdProy",0,1),
#     ("act_accinver_obra", "ctl00$CPH1$BtnAAO",0,1),
#     ("div_funcional", "ctl00$CPH1$BtnDivFuncional", 0, 1),
#     ("grupo_funcional","ctl00$CPH1$BtnGrupoFuncional", 0, 1),
#     ("meta", "ctl00$CPH1$BtnMeta", 0, 1),
#     #("fuente", "ctl00$CPH1$BtnFuenteAgregada", 0,1),
#     #("rubro", "ctl00$CPH1$BtnRubro", 0, 1),
#     #("generica", "ctl00$CPH1$BtnGenerica", 1,1),
#     #("departamento", "ctl00$CPH1$BtnDepartamentoMeta", 0, 1),
#     ("mes", "ctl00$CPH1$BtnMes", 0, 1)
#     ]

#### Local ####

# parameters = [
#     ("departamento", "ctl00$CPH1$BtnDepartamento", 1, 1),
#     ("categoria_pptal","ctl00$CPH1$BtnProgramaPpto",0,1),
#     ("prodproy","ctl00$CPH1$BtnProdProy",0,1),
#     ("act_accinver_obra", "ctl00$CPH1$BtnAAO",0,1),
#     ("div_funcional", "ctl00$CPH1$BtnDivFuncional", 0, 1),
#     ("grupo_funcional","ctl00$CPH1$BtnGrupoFuncional", 0, 1),
#     ("meta", "ctl00$CPH1$BtnMeta", 0, 1),
#     #("fuente", "ctl00$CPH1$BtnFuenteAgregada", 0,1),
#     #("rubro", "ctl00$CPH1$BtnRubro", 0, 1),
#     #("generica", "ctl00$CPH1$BtnGenerica", 1,1),
#     #("departamento", "ctl00$CPH1$BtnDepartamentoMeta", 0, 1),
#     ("mes", "ctl00$CPH1$BtnMes", 0, 1)
#     ]

#### Local ####

# parameters = [
#     ("pliego", "ctl00$CPH1$BtnPliego", 1, 1),
#     ("ejecutora", "ctl00$CPH1$BtnEjecutora", 1,1),
#     ("categoria_pptal","ctl00$CPH1$BtnProgramaPpto",0,1),
#     ("prodproy","ctl00$CPH1$BtnProdProy",0,1),
#     ("act_accinver_obra", "ctl00$CPH1$BtnAAO",0,1),
#     ("funcion","ctl00$CPH1$BtnFuncion",0, 1),
#     ("div_funcional", "ctl00$CPH1$BtnDivFuncional", 0, 1),
#     ("grupo_funcional","ctl00$CPH1$BtnGrupoFuncional", 0, 1),
#     ("meta", "ctl00$CPH1$BtnMeta", 0, 1),
#     #("fuente", "ctl00$CPH1$BtnFuenteAgregada", 0,1),
#     #("rubro", "ctl00$CPH1$BtnRubro", 0, 1),
#     #("generica", "ctl00$CPH1$BtnGenerica", 1,1),
#     #("departamento", "ctl00$CPH1$BtnDepartamentoMeta", 0, 1),
#     ("mes", "ctl00$CPH1$BtnMes", 0, 1)
#     ]


data = pd.DataFrame(columns=['tipodeconsulta1'])

chrome_options = Options()
if headless==1:
    chrome_options.add_argument("--headless=new") # for Chrome >= 109
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
service = webdriver.ChromeService()
service = webdriver.ChromeService(executable_path=driver_path, options=chrome_options)



def entrarespecificos(especificos):
    for filtro, boton, valor in especificos:
        print(f"\nProcesando filtro: {filtro}, botón: {boton}, valor buscado: {valor}")
        
        # Hacer clic en el botón correspondiente
        try:
            boton_elemento = b.find_element("name", boton)
            print(f"Botón '{boton}' encontrado. Haciendo clic...")
            globals()['f_' + filtro + 's'] = boton_elemento.click()
        except Exception as e:
            print(f"Error al hacer clic en el botón '{boton}': {e}")
            continue

        # Esperar hasta que la fila con el valor deseado aparezca
        encontrada = False
        timeout = 10  # tiempo máximo de espera por intento
        intentos = 3  # número máximo de intentos
        intento = 0

        while not encontrada and intento < intentos:
            try:
                WebDriverWait(b, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr"))
                )
                filas = b.find_elements(By.XPATH, "/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr")
                print(f"Intento {intento+1}: {len(filas)} filas encontradas.")

                for row in filas:
                    cell = row.find_element(By.XPATH, "td[2]")
                    cell_text = cell.text.lower()
                    print(f"Texto de celda: '{cell_text}'")

                    if valor.lower() in cell_text:
                        print(f"Coincidencia encontrada: '{cell_text}' contiene '{valor.lower()}'")
                        cell.click()
                        encontrada = True
                        break

                if not encontrada:
                    print(f"No se encontró coincidencia en intento {intento+1}. Esperando antes de reintentar...")
                    time.sleep(2)

            except Exception as e:
                print(f"Error durante la espera o búsqueda en intento {intento+1}: {e}")
            
            intento += 1

        if not encontrada:
            print(f"¡Advertencia! No se encontró el valor '{valor}' para el filtro '{filtro}' tras {intentos} intentos.")

        print(f"{filtro.upper()}: {valor.upper()}")


def get_bullet(nivel):
    bullets = {
        0: "●",
        1: "○",
        2: "+",
        3: "-",
    }
    return bullets.get(nivel, "")




def esperar_clickable(by, selector, timeout=10):
    return WebDriverWait(b, timeout).until(EC.element_to_be_clickable((by, selector)))

def esperar_presente(by, selector, timeout=10):
    return WebDriverWait(b, timeout).until(EC.presence_of_element_located((by, selector)))


def entrar(parameters, nivel=0, mes=0):
    for n in range(len(parameters)):
        if parameters[n][1] in ["ctl00$CPH1$BtnProdProy", "ctl00$CPH1$BtnMeta"]:
            parameters[n] = (parameters[n][0], parameters[n][1], parameters[n][2], parameters[n][3] * 2 - 1)

    if sum(1 for param in parameters if param[2] == 1) > 4:
        print("Un máximo de 4 elementos pueden ser elegidos para contarlos en la pantalla de resultados.")
        return

    if parameters[-1][1] == "ctl00$CPH1$BtnMes":
        parameters = parameters[0:-1]
        mes = 1

    if nivel == 0:
        globals()['parametersinicial'] = parameters

    var, filtername, contar, inicio = parameters[0]

    esperar_clickable(By.NAME, filtername).click()

    rows = b.find_elements(By.XPATH, "/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr")
    print(f"rows encontradas: {len(rows)}")

    globals()[f'count_{var}s'] = len(rows)

    if filtername not in ["ctl00$CPH1$BtnProdProy", "ctl00$CPH1$BtnMeta"]:
        globals()[f'countprint_{var}s'] = len(rows)
    else:
        globals()[f'countprint_{var}s'] = len(rows) // 2

    if contar == 1:
        print(f"{'  ' * nivel}hay {globals()[f'countprint_{var}s']} {var}s")

    if len(parameters) > 1:
        globals()[f'z_{var}'] = 0
        for z in range(globals()[f'inicio_{var}'], globals()[f'count_{var}s'] + 1):
            if filtername not in ["ctl00$CPH1$BtnProdProy", "ctl00$CPH1$BtnMeta"] or z % 2 == 1:
                globals()[f'z_{var}'] = z
                globals()[f'zprint_{var}'] = z if filtername not in ["ctl00$CPH1$BtnProdProy", "ctl00$CPH1$BtnMeta"] else (z + 1) // 2

                xpath = f"/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[{z}]"
                esperar_clickable(By.XPATH, xpath).click()

                if contar == 1:
                    print(f"{'  ' * nivel}{get_bullet(nivel)} click en {var} {globals()[f'zprint_{var}']}")

                next_params = parameters[1:]
                nivel += 1
                entrar(next_params, nivel, mes)
                nivel -= 1

    if len(parameters) == 1:
        globals()[f'z_{var}'] = 0
        for a in range(globals()[f'inicio_{var}'], globals()[f'count_{var}s'] + 1):
            if filtername not in ["ctl00$CPH1$BtnProdProy", "ctl00$CPH1$BtnMeta"] or a % 2 == 1:
                globals()[f'z_{var}'] = a
                globals()[f'zprint_{var}'] = a if filtername not in ["ctl00$CPH1$BtnProdProy", "ctl00$CPH1$BtnMeta"] else (a + 1) // 2

                data.loc[len(data)] = [None] * len(data.columns)
                data.at[len(data)-1, 'fechadelaconsulta'] = time.ctime(time.time())

                data.at[len(data)-1, 'tipodeconsulta1'] = esperar_presente(By.XPATH, "/html/body/form/div[3]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/span").text.strip()
                data.at[len(data)-1, 'tipodeconsulta2'] = esperar_presente(By.XPATH, "/html/body/form/div[3]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/b/span").text.strip()

                data.at[len(data)-1, 'actproy'] = esperar_presente(By.CSS_SELECTOR, "select[name='ctl00$CPH1$DrpActProy'] option[selected='selected']").get_attribute("value")
                data.at[len(data)-1, 'ano_eje'] = esperar_presente(By.CSS_SELECTOR, "select[name='ctl00$CPH1$DrpYear'] option[selected='selected']").get_attribute("value")

                xpath_base_1 = "/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr"
                fields_1 = [item[0] for item in especificos] + [param[0] for param in globals()['parametersinicial'][:-1]]

                for x, field in enumerate(fields_1):
                    xpath = f"{xpath_base_1}[{x+2}]/td[2]"
                    data.at[len(data)-1, field] = esperar_presente(By.XPATH, xpath).text.strip()

                xpath_base_2 = f"/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[{a}]/td"
                fields_2 = ['MTO_PIA', 'MTO_PIM', 'certificacion', 'compromisoanual', 'compromisomensual', 'DEV_TOTAL', 'girado', 'avance']
                fields_2.insert(0, globals()['parametersinicial'][-1][0])

                for x, field in enumerate(fields_2):
                    xpath = f"{xpath_base_2}[{x+2}]"
                    value = esperar_presente(By.XPATH, xpath).text.strip()
                    data.at[len(data)-1, field] = value

                    aux = next((param[1] for param in parameters_original if param[0] == field), None)

                    if aux == "ctl00$CPH1$BtnProdProy":
                        data.at[len(data)-1, "cod_prodproy"] = value.split(":")[0]
                        if not data.at[len(data)-1, "cod_prodproy"].startswith("3"):
                            data.at[len(data)-1, "link_ssi"] = f"https://ofi5.mef.gob.pe/ssi/Ssi/Index?codigo={data.at[len(data)-1, 'cod_prodproy']}&tipo=2"

                    if filtername == "ctl00$CPH1$BtnMeta":
                        xpath_metadet = f"/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[{a+1}]/td"
                        data.at[len(data)-1, "meta_detalle"] = esperar_presente(By.XPATH, xpath_metadet).text.strip()

                if mes == 1:
                    esperar_clickable(By.XPATH, f"/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[{a}]").click()
                    esperar_clickable(By.NAME, "ctl00$CPH1$BtnMes").click()

                    fields_3 = ['certificacion', 'compromisoanual', 'compromisomensual', 'DEV_TOTAL', 'girado']
                    months = {
                        ('Enero', 1, 'ENE'), ('Febrero', 2, 'FEB'), ('Marzo', 3, 'MAR'), ('Abril', 4, 'ABR'),
                        ('Mayo', 5, 'MAY'), ('Junio', 6, 'JUN'), ('Julio', 7, 'JUL'), ('Agosto', 8, 'AGO'),
                        ('Setiembre', 9, 'SET'), ('Octubre', 10, 'OCT'), ('Noviembre', 11, 'NOV'), ('Diciembre', 12, 'DIC')
                    }

                    rows = b.find_elements(By.XPATH, "/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr")

                    for i in range(1, len(rows) + 1):
                        for month, number, abrev in months:
                            label = esperar_presente(By.XPATH, f"/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[{i}]/td[2]").text.strip()
                            if label == f"{number}: '{month}":
                                for x, field in enumerate(fields_3):
                                    xpath = f"/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[{i}]/td[{x+5}]"
                                    data.at[len(data)-1, f"{field}_{abrev}"] = esperar_presente(By.XPATH, xpath).text.strip()

                    conteobacks_mes = len(b.find_elements(By.XPATH, "//*[starts-with(@id, 'ctl00_CPH1_RptHistory_ctl') and substring(@id, string-length(@id) - 2) = 'TD0']"))
                    esperar_clickable(By.ID, f"ctl00_CPH1_RptHistory_ctl{str(conteobacks_mes).zfill(2)}_TD0").click()

    conteobacks = len(b.find_elements(By.XPATH, "//*[starts-with(@id, 'ctl00_CPH1_RptHistory_ctl') and substring(@id, string-length(@id) - 2) = 'TD0']"))
    esperar_clickable(By.ID, f"ctl00_CPH1_RptHistory_ctl{str(conteobacks).zfill(2)}_TD0").click()
    globals()[f'conteobacks_{var}'] = conteobacks
    globals()[f'inicio_{var}'] = 1


#Guardar archivo sin sobreescribir, guardando un archivo readme txt:
def GuardarArchivo(data, year, especificos, parameters, final):
    
    data.replace({None: np.nan}, inplace=True)
    #filename = f'D:\\Presupuesto Público\\Scraping\\output\\GN_{year}.dta'
    filename = r'C:\Users\joaquin.DESKTOP-RQGFIKL\Downloads\scrap_cets\output\GN_{year}.dta'
    suffix = '(1)'
    counter = 1

    while os.path.exists(filename.replace('.dta', f'{suffix}.dta')):
        counter += 1
        suffix = f'({counter})'
    
    finaltexto="incompleta"
    if  final == 1:
        suffix += '(final)'
        finaltexto="completa"
        
    if parameters[-1][1]=="ctl00$CPH1$BtnMes":
        mensual=", con detalle mensual"
    else:
        mensual=", sin detalle mensual"

    content = f'''Este archivo contiene información {finaltexto} del año {year}{mensual} \n'''
    
    # Define the maximum length for alignment
    max_length_especificos = max(len(item[0]) for item in especificos)  # Calculate the longest item[0] in 'especificos'
    max_length_parameters = max(len(item[0]) for item in parameters[:-1])

    # Adding each specific line to the content
    for item in especificos:
        content += f"{item[0].ljust(max_length_especificos)}: {item[2]}\n"
    
    content += f"   {parameters[0][0].ljust(max_length_parameters)}: desde {globals()[f'inicio_original_{parameters[0][0]}']} hasta {globals()[f'zprint_{parameters[0][0]}']} de {globals()[f'countprint_{parameters[0][0]}s']} \n"

    previous_item = parameters[0]  
    for item in parameters[1:-1]:
        print(item)
        content += f"   {item[0].ljust(max_length_parameters)}: desde {globals()[f'inicio_original_{item[0]}']} hasta {globals()[f'zprint_{item[0]}']} de {globals()[f'countprint_{item[0]}s']} del último {previous_item[0]} \n"
        previous_item = item  # Actualiza el elemento anterior

    readme_filename = filename.replace('.dta', f'{suffix}_readme.txt')

    with open(readme_filename, 'w') as file:
        file.write(content)

    new_filename = filename.replace('.dta', f'{suffix}.dta')
    data.to_stata(new_filename, version=118)

    if final == 1:
        print('Archivo completo guardado')
    else:
        print('Archivo incompleto guardado y readme.txt guardado')


parameters_original=parameters 

for param in parameters_original:
    name = param[0]
    last_element = param[-1]
    globals()[f"inicio_{name}"] = last_element
    globals()[f"inicio_original_{name}"] = globals()[f"inicio_{name}"]


# INICIO DE SCRAPING 


# indicador si terminó el scraping
final=0

print("AÑO "+str(year))
print("TIPO: "+actproy) 

while True: 
    
    try:
        b = webdriver.Chrome(service=service)
    
        # Set the window position and size
        screen_width = b.execute_script("return window.screen.width;")
        screen_height = b.execute_script("return window.screen.height;")
        b.set_window_position(screen_width//1.71, 0)
        b.set_window_size(screen_width//2.4, screen_height//1.03)
    
        # b.get('https://apps5.mineco.gob.pe/transparencia/mensual/default.aspx?y='+ str(year)+'&ap='+str(productoproyecto)) 
        b.get("https://apps5.mineco.gob.pe/transparencia/Navegador/default.aspx?y="+ str(year)+"&ap="+str(actproy)) 
    
    
        frame = b.find_element("xpath",'//frame[@name="frame0"]') #Find and define frame of the page, it's called "frame0". "frame0" is found on inspect-name="frame0".
        b.switch_to.frame(frame) #switch the focus of a Selenium WebDriver to a specified frame on a webpage.
    
        entrarespecificos(especificos)
    
        entrar(parameters)
        
        break 
    except Exception as e:
        # print(str(e).splitlines()[0])  # Print the first line of the exception message
        print(str(e))  # Print ALL exception message

        parameters = [
            (name, selector, value, globals().get(f'zprint_{name}', _))
            for name, selector, value, _ in parameters
        ]
        
        for param in parameters:
            name = param[0]
            last_element = param[-1]
            globals()[f"inicio_{name}"] = last_element


final=1
print ("Se terminó el scraping")
sleep(5)
# b.quit()    


#Guardar archivo evitando sobreescritura. 
GuardarArchivo(data, year, especificos, parameters, final)