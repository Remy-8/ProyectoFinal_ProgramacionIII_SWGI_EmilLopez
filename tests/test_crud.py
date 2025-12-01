from selenium.webdriver.common.by import By
import time


def _ir_a_pantalla_login(driver, base_url):
    driver.get(base_url + "/login.html")


def _hacer_login_valido(driver):
    user_input = driver.find_element(By.ID, "username")
    pass_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "btnLogin")

    user_input.clear()
    user_input.send_keys("usuario_valido")

    pass_input.clear()
    pass_input.send_keys("clave_valida")

    login_button.click()


def _login_si_es_necesario(driver, base_url):
    _ir_a_pantalla_login(driver, base_url)
    _hacer_login_valido(driver)
    time.sleep(0.5)


def _ir_a_form_crud(driver, base_url):
    driver.get(base_url + "/items.html")
    time.sleep(0.5)


def _crear_registro(driver, nombre: str, descripcion: str):
    nombre_input = driver.find_element(By.ID, "name")
    desc_input = driver.find_element(By.ID, "description")
    guardar_btn = driver.find_element(By.ID, "btnSave")

    nombre_input.clear()
    nombre_input.send_keys(nombre)

    desc_input.clear()
    desc_input.send_keys(descripcion)

    guardar_btn.click()
    time.sleep(0.5)


def _existe_registro_en_lista(driver, nombre: str) -> bool:
    filas = driver.find_elements(By.CSS_SELECTOR, "#itemsTbody tr")
    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if not celdas:
            continue
        if nombre in celdas[0].text:
            return True
    return False


def _editar_registro(driver, nombre_original: str, nombre_nuevo: str):
    filas = driver.find_elements(By.CSS_SELECTOR, "#itemsTbody tr")
    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if not celdas:
            continue
        if nombre_original in celdas[0].text:
            btn_editar = fila.find_element(By.CSS_SELECTOR, ".btn-edit")
            btn_editar.click()
            break

    time.sleep(0.5)
    nombre_input = driver.find_element(By.ID, "name")
    guardar_btn = driver.find_element(By.ID, "btnSave")

    nombre_input.clear()
    nombre_input.send_keys(nombre_nuevo)
    guardar_btn.click()
    time.sleep(0.5)


def _eliminar_registro(driver, nombre: str):
    filas = driver.find_elements(By.CSS_SELECTOR, "#itemsTbody tr")
    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if not celdas:
            continue
        if nombre in celdas[0].text:
            btn_eliminar = fila.find_element(By.CSS_SELECTOR, ".btn-delete")
            btn_eliminar.click()
            break

    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(0.5)


def test_crud_create_camino_feliz(driver, base_url):
    _login_si_es_necesario(driver, base_url)
    _ir_a_form_crud(driver, base_url)

    nombre = "Item de prueba"
    descripcion = "Descripción válida"

    _crear_registro(driver, nombre, descripcion)

    assert _existe_registro_en_lista(driver, nombre)


def test_crud_create_negativo_campo_obligatorio(driver, base_url):
    _login_si_es_necesario(driver, base_url)
    _ir_a_form_crud(driver, base_url)

    _crear_registro(driver, nombre="", descripcion="Desc sin nombre")

    assert not _existe_registro_en_lista(driver, "")
    msg_error = driver.find_element(By.ID, "createError").text.strip()
    assert msg_error != ""


def test_crud_create_limite_nombre_largo(driver, base_url):
    _login_si_es_necesario(driver, base_url)
    _ir_a_form_crud(driver, base_url)

    nombre_largo = "X" * 50
    descripcion = "Nombre con longitud límite"

    _crear_registro(driver, nombre_largo, descripcion)

    assert _existe_registro_en_lista(driver, nombre_largo)


def test_crud_update_camino_feliz(driver, base_url):
    _login_si_es_necesario(driver, base_url)
    _ir_a_form_crud(driver, base_url)

    nombre_original = "Item de prueba"
    nombre_nuevo = "Item de prueba editado"

    if not _existe_registro_en_lista(driver, nombre_original):
        _crear_registro(driver, nombre_original, "Descripción editada")

    _editar_registro(driver, nombre_original, nombre_nuevo)

    assert _existe_registro_en_lista(driver, nombre_nuevo)


def test_crud_delete_camino_feliz(driver, base_url):
    _login_si_es_necesario(driver, base_url)
    _ir_a_form_crud(driver, base_url)

    nombre = "Item de prueba editado"

    if not _existe_registro_en_lista(driver, nombre):
        _crear_registro(driver, nombre, "Descripción a eliminar")

    _eliminar_registro(driver, nombre)

    assert not _existe_registro_en_lista(driver, nombre)
