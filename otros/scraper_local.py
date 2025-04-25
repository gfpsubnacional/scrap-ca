import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


data = pd.DataFrame(columns=[''])

def contenido_cambiado(driver, textos_anteriores):
    try:
        filas_actuales = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")
        textos_actuales = [fila.text for fila in filas_actuales]
    except Exception:
        return False
    return textos_actuales and textos_actuales != textos_anteriores


def entrarespecificos(especificos, driver):
    for filtro, boton, valor in especificos:
        filas_anteriores = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")
        textos_anteriores = [fila.text for fila in filas_anteriores]

        try:
            boton_elemento = driver.find_element("id", boton)
            globals()['f_' + filtro + 's'] = boton_elemento.click()
        except Exception:
            continue

        encontrada = False
        timeout = 5
        intentos = 3
        intento = 0

        while not encontrada and intento < intentos:
            try:
                WebDriverWait(driver, timeout).until(lambda d: contenido_cambiado(d, textos_anteriores))
                filas = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")

                for row in filas:
                    cell = row.find_element(By.XPATH, "td[2]")
                    cell_text = cell.text.lower()

                    if valor.lower() in cell_text:
                        cell.click()
                        encontrada = True
                        break

                if not encontrada:
                    time.sleep(0.1)

            except Exception:
                pass

            intento += 1

        if not encontrada:
            return
        
        print(f"{filtro.upper()}: {valor.upper()}")


def clickear_si_clickable(by, selector, driver, timeout=10, intentos=5):
    for intento in range(intentos):
        try:
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, selector)))
            driver.find_element(by, selector).click()
            return
        except StaleElementReferenceException:
            if intento == intentos - 1:
                raise
        except TimeoutException:
            raise


def esperar_presente(by, selector, driver, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, selector)))



def get_bullet(nivel):
    bullets = {
        0: "●",
        1: "○",
        2: "+",
        3: "-",
    }
    return bullets.get(nivel, "")



def entrar(parameters, especificos, driver, nivel=0):
    if sum(1 for param in parameters if param[2] == 1) > 4:
        return

    if nivel == 0:
        globals()['parametersinicial'] = parameters

    var, filtername, contar = parameters[0]

    filas_anteriores = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")
    textos_anteriores = [fila.text for fila in filas_anteriores]

    clickear_si_clickable(By.ID, filtername, driver)

    timeout = 10
    WebDriverWait(driver, timeout).until(lambda d: contenido_cambiado(d, textos_anteriores))

    rows = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")

    globals()[f'count_{var}s'] = len(rows)

    if contar == 1:
        print(f"{'  ' * nivel}hay {globals()[f'count_{var}s']} {var}s")
        
    if len(parameters) > 1:
        globals()[f'z_{var}'] = 0
        for z in range(0, globals()[f'count_{var}s']):
            globals()[f'z_{var}'] = z
            globals()[f'zprint_{var}'] = z

            idrow = f"tr{z}"

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




gobierno_regional = "Loreto"
categoria_presupuestal = "57"

actproy = 'ActProy'
year = 2024

especificos = [
    ("nivel_gobierno", "ctl00_CPH1_BtnTipoGobierno", "regional"),
    ("sector", "ctl00_CPH1_BtnSector", "99: gobiernos regionales"),
    ("pliego", "ctl00_CPH1_BtnPliego", gobierno_regional),
    ("categoria_pptal", "ctl00_CPH1_BtnProgramaPpto", categoria_presupuestal)
]

parameters = [
    ("ejecutora", "ctl00_CPH1_BtnEjecutora", 1),
    ("c_costo", "ctl00_CPH1_BtnCentroCosto", 1),
    ("act_op", "ctl00_CPH1_BtnActividadOperativa", 1)
]

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/chromium"

driver = webdriver.Chrome(options=chrome_options)

url = f"https://app.ceplan.gob.pe/ConsultaCEPLAN/consulta/Default.aspx?y={year}&ap={actproy}"
driver.get(url)

driver.switch_to.frame("frame0")

entrarespecificos(especificos, driver)
entrar(parameters, especificos, driver)

data.to_excel 