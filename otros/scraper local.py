import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service

data = pd.DataFrame(columns=[''])
app_streamlit_render = 0




def contenido_cambiado(driver, textos_anteriores):
    try:
        filas_actuales = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")
        textos_actuales = [fila.text for fila in filas_actuales]

        print(f"[DEBUG] Cantidad de filas anteriores: {len(textos_anteriores)}")
        print(f"[DEBUG] Cantidad de filas actuales: {len(textos_actuales)}")

        if not textos_actuales:
            print("[DEBUG] No se encontraron filas actuales.")
            return False

        cambio_valido = False

        # Comparación línea por línea
        for i, (antes, ahora) in enumerate(zip(textos_anteriores, textos_actuales)):
            if antes != ahora and ahora.strip() != "":
                print(f"[DEBUG] Fila {i} cambió:\n  Antes: '{antes}'\n  Ahora: '{ahora}'")
                cambio_valido = True

        # Si hay filas nuevas que no están vacías, también cuenta como cambio
        if len(textos_actuales) > len(textos_anteriores):
            for i in range(len(textos_anteriores), len(textos_actuales)):
                nueva = textos_actuales[i]
                if nueva.strip() != "":
                    print(f"[DEBUG] Fila nueva {i}: '{nueva}'")
                    cambio_valido = True

        if cambio_valido:
            print("[DEBUG] Cambio válido detectado en el contenido.")
        else:
            print("[DEBUG] No hay cambios válidos en el contenido.")

        return cambio_valido

    except Exception as e:
        print(f"[ERROR] Al verificar cambio de contenido: {e}")
        return False



def esperar_presente(by, selector, driver, timeout=2):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, selector)))


def entrarespecificos(especificos, driver):
    for filtro, boton, valor in especificos:
        print(f"\nProcesando filtro: {filtro}, botón: {boton}, valor: {valor}")
        
        filas_anteriores = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")
        textos_anteriores = [fila.text for fila in filas_anteriores]
        print(f"Filas anteriores encontradas: {len(filas_anteriores)}")

        try:
            boton_elemento = driver.find_element("id", boton)
            print(f"Botón '{boton}' encontrado. Haciendo clic...")
            boton_elemento.click()
        except Exception as e:
            print(f"[ERROR] No se encontró el botón '{boton}': {e}")
            continue

        encontrada = False
        timeout = 2
        intentos = 2
        intento = 0

        while not encontrada and intento < intentos:
            print(f"Intento {intento + 1} de {intentos}")
            try:
                WebDriverWait(driver, timeout).until(lambda d: contenido_cambiado(d, textos_anteriores))
                filas = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")
                print(f"Nuevas filas detectadas: {len(filas)}")

                for i, row in enumerate(filas):
                    try:
                        cell = row.find_element(By.XPATH, "td[2]")
                        cell_text = cell.text.lower()
                        print(f"Fila {i}: '{cell_text}'")

                        if valor.lower() in cell_text:
                            print(f"Coincidencia encontrada: '{cell_text}' contiene '{valor.lower()}'")
                            cell.click()
                            encontrada = True
                            break
                    except Exception as e:
                        print(f"[ERROR] No se pudo acceder a td[2] en fila {i}: {e}")

                if not encontrada:
                    print("No se encontró la coincidencia en este intento. Esperando un poco...")
                    time.sleep(0.1)

            except Exception as e:
                print(f"[ERROR] Timeout esperando cambio de contenido: {e}")

            intento += 1

        if not encontrada:
            print(f"[ERROR] No se encontró el valor '{valor}' para el filtro '{filtro}' tras {intentos} intentos.")
            return
        
        print(f"[OK] {filtro.upper()}: {valor.upper()}")


def clickear_si_clickable(by, selector, driver, timeout=2, intentos=2):
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





def get_bullet(nivel):
    bullets = {
        0: "●",
        1: "○",
        2: "+",
        3: "-",
    }
    return bullets.get(nivel, "")



def entrar(parameters, especificos, driver, nivel=0):
    if nivel == 0:
        print("\n[Inicio de recursion] Parámetros iniciales:", parameters)
        globals()['parametersinicial'] = parameters

    var, filtername, contar = parameters[0]
    print(f"{'  ' * nivel}[Nivel {nivel}] Procesando variable: {var}, filtro: {filtername}, contar: {contar}")

    filas_anteriores = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")
    textos_anteriores = [fila.text for fila in filas_anteriores]

    print(f"{'  ' * nivel}Click en filtro: {filtername}")
    clickear_si_clickable(By.ID, filtername, driver)

    timeout = 2
    WebDriverWait(driver, timeout).until(lambda d: contenido_cambiado(d, textos_anteriores))

    rows = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'tr')]")
    count = len(rows)
    globals()[f'count_{var}s'] = count

    print(f"{'  ' * nivel}Filas encontradas para {var}: {count}")
    if contar == 1:
        print(f"{'  ' * nivel}hay {count} {var}s")

    if len(parameters) > 1:
        globals()[f'z_{var}'] = 0
        for z in range(count):
            globals()[f'z_{var}'] = z
            globals()[f'zprint_{var}'] = z
            idrow = f"tr{z}"

            print(f"{'  ' * nivel}Click en fila: {idrow}")
            clickear_si_clickable(By.ID, idrow, driver)

            if contar == 1:
                print(f"{'  ' * nivel}{get_bullet(nivel)} click en {var} {z}")

            next_params = parameters[1:]
            nivel += 1
            entrar(next_params, especificos=especificos, nivel=nivel, driver=driver)
            nivel -= 1

    if len(parameters) == 1:
        print(f"{'  ' * nivel}Último nivel. Extrayendo información de tabla detallada...")
        globals()[f'z_{var}'] = 0
        for a in range(count):
            print(f"{'  ' * nivel}Procesando fila {a} de {count}")
            globals()[f'z_{var}'] = a
            globals()[f'zprint_{var}'] = a

            data.loc[len(data)] = [None] * len(data.columns)
            data.at[len(data)-1, 'fechadelaconsulta'] = time.ctime(time.time())

            actproy = esperar_presente(By.CSS_SELECTOR, "select[id='ctl00_CPH1_DrpActProy'] option[selected='selected']", driver).get_attribute("value")
            anoeje = esperar_presente(By.CSS_SELECTOR, "select[id='ctl00_CPH1_DrpYear'] option[selected='selected']", driver).get_attribute("value")

            data.at[len(data)-1, 'actproy'] = actproy
            data.at[len(data)-1, 'ano_eje'] = anoeje

            print(f"{'  ' * nivel}Extraídos actproy: {actproy}, ano_eje: {anoeje}")

            xpath_base_1 = "/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr"
            fields_1 = [item[0] for item in especificos] + [param[0] for param in globals()['parametersinicial'][:-1]]

            for x, field in enumerate(fields_1):
                xpath = f"{xpath_base_1}[{x+2}]/td[2]"
                value = esperar_presente(By.XPATH, xpath, driver).text.strip()
                data.at[len(data)-1, field] = value
                print(f"{'  ' * nivel}Extraído {field}: {value}")

            xpath_base_2 = f"//tr[@id='tr{a}']/td"
            fields_2 = ['POI_aprobado', 'PIA', 'POI_consistente_PIA', 'PIM', 'POI modificado', 'DEV', 'ejecutado', 'POI/PIA']
            fields_2.insert(0, globals()['parametersinicial'][-1][0])

            for x, field in enumerate(fields_2):
                xpath = f"{xpath_base_2}[{x+2}]"
                value = esperar_presente(By.XPATH, xpath, driver).text.strip()
                data.at[len(data)-1, field] = value
                print(f"{'  ' * nivel}Extraído {field}: {value}")

    conteobacks = len(driver.find_elements(By.XPATH, "//*[starts-with(@id, 'ctl00_CPH1_RptHistory_ctl') and substring(@id, string-length(@id) - 2) = 'TD0']"))
    print(f"{'  ' * nivel}Número de retrocesos posibles: {conteobacks}")

    click_id = f"ctl00_CPH1_RptHistory_ctl{str(conteobacks).zfill(2)}_TD0"
    print(f"{'  ' * nivel}Click en volver: {click_id}")
    clickear_si_clickable(By.ID, click_id, driver)
    
    WebDriverWait(driver, 5).until(
        lambda d: (nuevo := len(d.find_elements(By.XPATH, "//*[starts-with(@id, 'ctl00_CPH1_RptHistory_ctl') and substring(@id, string-length(@id) - 2) = 'TD0']"))) > 0 and nuevo != conteobacks
    )

    

# import tempfile
# user_data_dir = tempfile.mkdtemp()

actproy = 'ActProy'
year = 2024

especificos = [
    ("nivel_gobierno", "ctl00_CPH1_BtnTipoGobierno", "regional"),
    ("sector", "ctl00_CPH1_BtnSector", "99: gobiernos regionales"),
    ("pliego", "ctl00_CPH1_BtnPliego", "ucayali"),
    ("categoria_pptal", "ctl00_CPH1_BtnProgramaPpto", "57")
]

parameters = [
    ("ejecutora", "ctl00_CPH1_BtnEjecutora", 1),
    ("prod_proy", "ctl00_CPH1_BtnProdProy", 1),
    ("rubro", "ctl00_CPH1_BtnRubro", 1),
    ("generica","ctl00_CPH1_BtnGenerica",1),
    ("subgenerica","ctl00_CPH1_BtnSubGenerica",0)
]


chrome_options = Options()


if app_streamlit_render ==1:
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/chromium"
    # chrome_options.add_argument(f"--user-data-dir={user_data_dir}")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = f"https://apps5.mineco.gob.pe/transparencia/Navegador/default.aspx?y={year}&ap={actproy}"

driver.get(url)

driver.switch_to.frame("frame0")

entrarespecificos(especificos, driver)
entrar(parameters, especificos, driver)

# import shutil
driver.quit()
# shutil.rmtree(user_data_dir)

# return data.dropna(axis=1, how='all')
