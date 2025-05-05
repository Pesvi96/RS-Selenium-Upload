import logging
from data_grouped import MY_DICT
from elements import links
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    NoAlertPresentException, WebDriverException
import traceback
import time


def set_up_logger() -> logging.Logger:
    logger = logging.getLogger("main_logger")
    logger.setLevel(logging.DEBUG)

    debug_log_handler = logging.FileHandler("full_log.log", mode='w', encoding='utf-8')
    debug_log_handler.setLevel(logging.DEBUG)
    debug_log_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s\n'))

    main_log_handler = logging.FileHandler("main_log.log", mode='w', encoding='utf-8')
    main_log_handler.setLevel(logging.INFO)
    main_log_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s\n'))

    logger.addHandler(main_log_handler)
    logger.addHandler(debug_log_handler)

    return logger


log = set_up_logger()


def init(website: str) -> WebDriver:
    """Initialises driver options. Opens Chrome Driver. Goes to the provided URL"""

    # This is the normal Chrome version
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument("--start-maximized")
    webdriver_options.add_experimental_option("detach",
                                              True)  # Keep the browser open until .quit command comes (even if execution stops)
    # ----------------------------------------------------------

    driver = webdriver.Chrome(options=webdriver_options)
    driver.implicitly_wait(10)

    try:
        log.debug(f"init: Initializing webdriver. url: '{website}'")
        driver.get(website)
    except Exception as err:
        log.critical(err)
        raise
    else:
        return driver


driver = init("https://rs.ge/")


def retries_decorator(func):
    def wrapper(*args, **kwargs):
        for x in range(1, 4):
            try:
                return func(*args, **kwargs)
            except Exception:
                log.error(f"{func.__name__} failed. Attempt {x}")
                time.sleep(1)
        log.critical(f"{func.__name__} failed after 3 attempts. Stopping execution")
        raise

    return wrapper


def find(element_name: str) -> WebElement | None:
    """Finds the element (using elements.py css selectors database) and returns it. returns None if not found"""
    try:
        log.debug(f"find: Element name: '{element_name}'. Current url {driver.current_url}")
        element_selector_type, element_selector_path = links[
            element_name]  # Gets selector type and selector from dictionary in hidden elements.py file
        element = driver.find_element(by=element_selector_type, value=element_selector_path)
    except NoSuchElementException as err:
        message = f"find: NoSuchElementException. '{element_name}' does not exist. Current URL: {driver.current_url}"
        log.error(message)
        log.debug(err)
        return None
    except Exception as err:
        message = (f"find: Unknown error on finding element '{element_name}'. Current URL: {driver.current_url}."
                   f"Error: {err}")
        log.error(message)
        log.debug(f"Traceback: {traceback.format_exc()}")
        return None
    else:
        return element


@retries_decorator
def btn_click(element) -> None:
    """Finds and clicks the indicated element. Error check provided"""
    try:
        btn = find(element)
        log.debug(f"btn_click: element: {element}. Current url {driver.current_url}")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(btn))
        btn.click()
    except ElementClickInterceptedException:
        message = f"btn_click: ElementClickInterceptedException. '{element}' not clickable. Current URL: {driver.current_url}"
        log.error(message)
        raise
    except NoSuchElementException:  # Doesn't log message because it was already logged in find method
        raise
    except Exception as err:
        message = (f"btn_click: Unknown error on finding element '{element}'. Current URL: {driver.current_url}."
                   f"Error: {err}")
        log.error(message)
        log.debug(f"Traceback: {traceback.format_exc()}")
        raise


# TODO: box_type needs reformatting as well
@retries_decorator
def box_type(element: str, value: str) -> None:
    """Finds and types the value in the indicated element. Checks if the value in
    the element is right after typing. Error check provided"""
    try:
        btn = find(element)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(btn))
        btn.send_keys(value)
        while btn.get_attribute('value') != value:
            log.error(
                f"\t* Little hiccup in box_type func. Value received: {value}, value of input field:{btn.get_attribute('value')}\n\tTrying again...\n")
            btn.clear()
            btn.send_keys(value)
            time.sleep(0.5)
    except:
        log.error("Couldn't type in the element")
        traceback.format_exc()
        raise


print("For Debugging")
print("End of debugging")
