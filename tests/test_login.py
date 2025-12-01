from selenium.webdriver.common.by import By


def _ir_a_pantalla_login(driver, base_url):
    driver.get(base_url + "/login.html")


def _hacer_login(driver, username: str, password: str):
    user_input = driver.find_element(By.ID, "username")
    pass_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "btnLogin")

    user_input.clear()
    user_input.send_keys(username)

    pass_input.clear()
    pass_input.send_keys(password)

    login_button.click()


def _esta_logueado(driver) -> bool:
    elementos = driver.find_elements(By.ID, "dashboardTitle")
    return len(elementos) > 0


def _mensaje_error_login(driver) -> str:
    elementos = driver.find_elements(By.ID, "loginError")
    if elementos:
        return elementos[0].text.strip()
    return ""


def test_login_camino_feliz(driver, base_url):
    _ir_a_pantalla_login(driver, base_url)

    _hacer_login(driver, username="usuario_valido", password="clave_valida")

    assert _esta_logueado(driver)


def test_login_negativo_credenciales_invalidas(driver, base_url):
    _ir_a_pantalla_login(driver, base_url)

    _hacer_login(driver, username="usuario_valido", password="clave_incorrecta")

    assert not _esta_logueado(driver)
    msg = _mensaje_error_login(driver)
    assert msg != ""


def test_login_limite_campos_vacios(driver, base_url):
    _ir_a_pantalla_login(driver, base_url)

    _hacer_login(driver, username="", password="")

    assert not _esta_logueado(driver)
    msg = _mensaje_error_login(driver)
    assert msg != ""
