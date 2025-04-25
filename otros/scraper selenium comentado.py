import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd 

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException


data = pd.DataFrame(columns=[''])    


def contenido_cambiado(driver, textos_anteriores):
    try: 
        filas_actuales = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")
        textos_actuales = [fila.text for fila in filas_actuales]
    except Exception:
        # print(f"Error al obtener textos: {e}")
        return False  # evita que el programa falle

    # if textos_actuales and textos_actuales != textos_anteriores:
    #     print(f"textos_actuales: {textos_actuales}")
        
    return textos_actuales and textos_actuales != textos_anteriores


def entrarespecificos(especificos, driver):
    for filtro, boton, valor in especificos:
        # print(f"\nProcesando filtro: {filtro}, botón: {boton}, valor buscado: {valor}")
        
        # Guardamos el contenido original de las filas
        filas_anteriores = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")

        textos_anteriores = [fila.text for fila in filas_anteriores]
        # print(f"textos_anteriores: {textos_anteriores}")
        
        # Esperamos a que el contenido cambie

        # Hacer clic en el botón correspondiente
        try:
            boton_elemento = driver.find_element("id", boton)
            # print(f"Botón '{boton}' encontrado. Haciendo clic...")
            globals()['f_' + filtro + 's'] = boton_elemento.click()
        except Exception as e:
            # print(f"Error al hacer clic en el botón '{boton}': {e}")
            continue

        # Esperar hasta que la fila con el valor deseado aparezca
        encontrada = False
        timeout = 5  # tiempo máximo de espera por intento
        intentos = 3  # número máximo de intentos
        intento = 0

        while not encontrada and intento < intentos:
            try:
                WebDriverWait(driver, timeout).until(lambda d: contenido_cambiado(d, textos_anteriores))
                filas = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")

                # print(f"Intento {intento+1}: {len(filas)} filas encontradas.")

                for row in filas:
                    cell = row.find_element(By.XPATH, "td[2]")
                    cell_text = cell.text.lower()
                    # print(f"Texto de celda: '{cell_text}'")

                    if valor.lower() in cell_text:
                        # print(f"Coincidencia encontrada: '{cell_text}' contiene '{valor.lower()}'")
                        cell.click()
                        encontrada = True
                        break

                if not encontrada:
                    # print(f"No se encontró coincidencia en intento {intento+1}. Esperando antes de reintentar...")
                    time.sleep(0.1)

            except Exception as e:
                print(f"Error durante la espera o búsqueda en intento {intento+1}: {e}")
            
            intento += 1

        if not encontrada:
            # print(f"¡Advertencia! No se encontró el valor '{valor}' para el filtro '{filtro}' tras {intentos} intentos.")
            return 
        
        print(f"{filtro.upper()}: {valor.upper()}")


def get_bullet(nivel):
    bullets = {
        0: "●",
        1: "○",
        2: "+",
        3: "-",
    }
    return bullets.get(nivel, "")



def clickear_si_clickable(by, selector, driver, timeout=10, intentos=5):
    # print(f"Esperando a que sea clickable: ({by}, {selector})")
    for intento in range(intentos):
        try:
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, selector)))
            driver.find_element(by, selector).click()
            # print("Click realizado exitosamente.")
            return
        except StaleElementReferenceException:
            # print("Elemento stale, reintentando...")
            if intento == intentos - 1:
                raise
        except TimeoutException:
            print("Timeout esperando elemento clickable.")
            raise
            
            
def esperar_presente(by, selector, driver, timeout=10):
    # print(f"Esperando presencia de elemento: ({by}, {selector})")
    elemento = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, selector)))
    # print("Elemento presente encontrado.")
    return elemento



def entrar(parameters, especificos, driver, nivel=0):

    if sum(1 for param in parameters if param[2] == 1) > 4:
        print("Un máximo de 4 elementos pueden ser elegidos para contarlos en la pantalla de resultados.")
        return

    if nivel == 0:
        globals()['parametersinicial'] = parameters

    var, filtername, contar = parameters[0]
    
    # Guardamos el contenido anterior de las filas
    filas_anteriores = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")

    textos_anteriores = [fila.text for fila in filas_anteriores]

    # Hacemos click en el correspondiente filtro
    clickear_si_clickable(By.ID, filtername, driver)

    # Esperamos a que cambie el contenido de las filas 
    timeout = 10
    WebDriverWait(driver, timeout).until(lambda d: contenido_cambiado(d, textos_anteriores))

    # Extraemos las filas
    rows = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")

    # print(f"rows encontradas: {len(rows)}")

    globals()[f'count_{var}s'] = len(rows)
    globals()[f'countprint_{var}s'] = len(rows)

    if contar == 1:
        print(f"{'  ' * nivel}hay {globals()[f'countprint_{var}s']} {var}s")

    if len(parameters) > 1:
        globals()[f'z_{var}'] = 0
        for z in range(0, globals()[f'count_{var}s']):
            globals()[f'z_{var}'] = z
            globals()[f'zprint_{var}'] = z 
    
            # print(globals()[f'count_{var}s'])
            idrow =  f"tr{z}" 
            
            clickear_si_clickable(By.ID, idrow, driver)
            
            if contar == 1:
                print(f"{'  ' * nivel}{get_bullet(nivel)} click en {var} {globals()[f'zprint_{var}']}")
    
            next_params = parameters[1:]
            nivel += 1
            entrar(next_params, especificos=especificos, nivel=nivel, driver=driver)
            nivel -= 1

    if len(parameters) == 1:
        globals()[f'z_{var}'] = 0
        for a in range(0, globals()[f'count_{var}s']):
            globals()[f'z_{var}'] = a
            globals()[f'zprint_{var}'] = a 

            data.loc[len(data)] = [None] * len(data.columns)
            data.at[len(data)-1, 'fechadelaconsulta'] = time.ctime(time.time())

            data.at[len(data)-1, 'actproy'] = esperar_presente(By.CSS_SELECTOR, "select[id='ctl00_CPH1_DrpActProy'] option[selected='selected']", driver).get_attribute("value")
            data.at[len(data)-1, 'ano_eje'] = esperar_presente(By.CSS_SELECTOR, "select[id='ctl00_CPH1_DrpYear'] option[selected='selected']", driver).get_attribute("value")

            xpath_base_1 = "/html/body/form/div[3]/div/div[4]/table/tbody/tr"
            fields_1 = [item[0] for item in especificos] + [param[0] for param in globals()['parametersinicial'][:-1]]

            for x, field in enumerate(fields_1):
                xpath = f"{xpath_base_1}[{x+2}]/td[2]"
                data.at[len(data)-1, field] = esperar_presente(By.XPATH, xpath, driver).text.strip()


            xpath_base_2 = f"//tr[@id='tr{a}']/td"
            fields_2 = ['POI_aprobado', 'PIA', 'POI_consistente_PIA', 'PIM', 'POI modificado', 'DEV', 'ejecutado', 'POI/PIA']
            fields_2.insert(0, globals()['parametersinicial'][-1][0])

            for x, field in enumerate(fields_2):
                xpath = f"{xpath_base_2}[{x+2}]"
                value = esperar_presente(By.XPATH, xpath, driver).text.strip()
                data.at[len(data)-1, field] = value

    time.sleep(1)
    conteobacks = len(driver.find_elements(By.XPATH, "//*[starts-with(@id, 'ctl00_CPH1_RptHistory_ctl') and substring(@id, string-length(@id) - 2) = 'TD0']"))
    clickear_si_clickable(By.ID, f"ctl00_CPH1_RptHistory_ctl{str(conteobacks).zfill(2)}_TD0", driver)

    globals()[f'conteobacks_{var}'] = conteobacks
    
    

def scrape_ceplan(gobierno_regional, categoria_presupuestal):
    
    # actproy='Proyecto'
    # actproy='Actividad'
    actproy='ActProy'
    
    year=2024
    
    #### Regional ####
    especificos = [
        ("nivel_gobierno","ctl00_CPH1_BtnTipoGobierno","regional"),
        ("sector","ctl00_CPH1_BtnSector","99: gobiernos regionales"),
        ("pliego","ctl00_CPH1_BtnPliego",gobierno_regional),
        ("categoria_pptal","ctl00_CPH1_BtnProgramaPpto",categoria_presupuestal)
        ]
    
    # parameters= [(nombre del filtro, name del boton como elemento de pagina web, dummy print, empezar desde)]
    
    parameters = [
        ("ejecutora","ctl00_CPH1_BtnEjecutora",1),
        ("c_costo","ctl00_CPH1_BtnCentroCosto",1),
        ("act_op","ctl00_CPH1_BtnActividadOperativa",1)
        ]
    
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")    
    
    # Configuración del driver de Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Acceder a la página principal
    url = "https://app.ceplan.gob.pe/ConsultaCEPLAN/consulta/Default.aspx?y=" + str(year) + "&ap="+str(actproy)
    
    driver.get(url)
    
    driver.switch_to.frame("frame0")
    
    entrarespecificos(especificos, driver)
    
    entrar(parameters, especificos, driver)
    
    # Cerrar el navegador
    # driver.quit()

    return data.dropna(axis=1, how='all')
