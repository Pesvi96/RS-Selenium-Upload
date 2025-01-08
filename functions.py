from data_grouped import MY_DICT
from elements import links
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    NoAlertPresentException, WebDriverException
import traceback
import time

MAX_TRIES = 3
id_tries = 0


def init(website):
    """Initialises driver options. Goes to the provided URL"""
    global driver

    # This is the normal Chrome version
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)  # Keep the browser open until .quit command comes
    # ----------------------------------------------------------

    driver = webdriver.Chrome(options=options)
    driver.get(website)
    driver.implicitly_wait(10)
    return driver


# Class for catching Error box exception
class ErrorBoxException(WebDriverException):
    def __init__(self, message="Error Box Appeared"):
        super().__init__(message)


def find(element_type, value):
    """Finds the element (using elements.py css selectors database) and returns it. returns None if not found"""
    try:
        element = driver.find_element(by=element_type, value=value)
    except NoSuchElementException:
        message = f"Element {value} does not exist. Current URL: {driver.current_url}"
        add_error(message)
        return None
    except:
        message = f"Unknown error on finding element {value}. Current URL: {driver.current_url}"
        add_error(message)
        return None
    else:
        return element


def btn_click(element):
    """Find and clicks the indicated element. Error check provided"""
    try:
        btn = find(*links[element])
        btn.click()
    except ElementClickInterceptedException:
        message = f"Element {element} not clickable. Current URL: {driver.current_url}"
        add_error(message)
        raise
    except:
        message = f"Unknown error on clicking element {element}. Current URL: {driver.current_url}"
        add_error(message)
        traceback.print_exc()
        raise


def box_type(element, value):
    """Find and types the value in the indicated element. Checks if the value in
    the element is right after typing. Error check provided"""
    try:
        btn = find(*links[element])
        btn.send_keys(value)
        while btn.get_attribute('value') != value:
            print_to_log(
                f"\t* Little hiccup in box_type func. Value received: {value}, value of input field:{btn.get_attribute('value')}\n\tTrying again...\n")
            btn.clear()
            btn.send_keys(value)
            time.sleep(0.5)
    except:
        add_error("Couldn't type in the element")
        traceback.print_exc()
        raise


def add_error(message):
    """Add error to errors.csv file"""
    try:
        with open("Logs/errors.csv", mode="a") as file:
            file.write(f"{message}\n")
            print_to_log(f"\n\t\t *** Error: {message}\n")
    except:
        with open("Logs/errors.csv", mode="w") as file:
            file.write(f"{message}\n")
            print_to_log(f"\n\t\t *** Error: {message}\n")


def get_month():
    """Returns current month as an integer"""
    month = int(time.strftime("%m", time.localtime()))
    print_to_log(f"Current month: {month}")
    return month

def get_year():
    """Returns current year as an integer"""
    year = int(time.strftime("%Y", time.localtime()))
    print(f"Current year: {year}")
    return year


# def check_url(actual):
#     """Checks if you are at the given URL"""
#     current_url = driver.current_url
#     return current_url == actual


def sign_into_test_user():
    """Sign in to the test user"""
    try:
        driver.get("https://www.rs.ge")
        btn_click("SIGN_IN_BTN")
        btn_click("TEST_CUSTOMER_CHOICE")
        btn_click("TEST_CUSTOMER_ONE")
        find(*links["MODULES"])
    except NoSuchElementException:
        message = f"Couldn't {NoSuchElementException} find module after sign in"
        add_error(message)
        sign_into_test_user()
    except ElementClickInterceptedException:
        message = f"Couldn't click element {ElementClickInterceptedException}"
        add_error(message)
        sign_into_test_user()
    else:
        print_to_log("Signed in")
        return True


def sign_into_actual_user():
    """Sign in to actual user function. Just press enter in console after signing in"""
    driver.get("https://www.rs.ge")
    btn_click("SIGN_IN_BTN")
    input("Please sign in and press Enter when ready")


def access_invoice_page():
    """Navigates to the Invoice page and turns off the pop-up"""
    try:
        driver.get("https://eservices.rs.ge/Invoices.aspx")
        driver.refresh()
        time.sleep(1)
        try:
            btn_click("POP_UP")
        except NoSuchElementException:
            message = "No popup"
            add_error(message)
        except ElementClickInterceptedException:
            message = "Couldn't click the Popup Close button. Trying again"
            add_error(message)
            time.sleep(1)
            try:
                btn_click("POP_UP")
            except ElementClickInterceptedException:
                message = "Still couldn't click the Popup Close button. Starting again"
                add_error(message)
                access_invoice_page()
        except:
            message = f"Unknown error on closing popup. Current URL: {driver.current_url}"
            add_error(message)
            traceback.print_exc()
        else:
            print_to_log("Popup shut down")
    except:
        message = f"Unknown error on accessing invoice webpage. Current URL: {driver.current_url}"
        add_error(message)
        traceback.print_exc()
        return False
    else:
        if driver.current_url == "https://eservices.rs.ge/Invoices.aspx":
            print_to_log("Invoice page accessed")
            return True
        else:
            return False


def select_vat(vat):
    """Selects vat from the drop-down list. Error check provided.
    Checks forever (TODO: !may get stuck in loop! needs reformatting)"""
    unit = find(*links["VAT_LIST"])
    if vat == "1":
        while True:
            select = Select(unit)
            select.select_by_index(0)
            unit.get_attribute('value')
            select = Select(unit)
            select.select_by_index(0)
            time.sleep(0.5)
            if unit.get_attribute('value') == '0':
                break
    elif vat == "0":
        while True:
            select = Select(unit)
            select.select_by_index(1)
            unit.get_attribute('value')
            select = Select(unit)
            select.select_by_index(1)
            time.sleep(0.5)
            if unit.get_attribute('value') == '1':
                break
    else:
        message = "Something wrong with VAT data"
        add_error(message)
        raise


def select_month_in_list():
    """Chooses previous month from the drop-down list.
    If it's January, chooses December and indicates the previous year."""
    month_select = find(*links["MONTH_LIST"])
    current_month = get_month()
    if current_month == 1:
        select_previous_year_in_list()
        month_to_indicate = 12
    else:
        month_to_indicate = current_month
    while True:
        select = Select(month_select)
        select.select_by_index(month_to_indicate)
        month_select.get_attribute('value')
        time.sleep(0.5)
        if int(month_select.get_attribute('value')) == month_to_indicate:
            break


def select_previous_year_in_list():
    year_select = find(*links["YEAR_LIST"])
    year = get_year() - 1
    while True:
        select = Select(year_select)
        select.select_by_index(1)   # Chooses second option in Select
        time.sleep(0.5)
        if int(year_select.get_attribute('value')) == int(year):
            break


def select_unit():
    """Selects მომსახურება from the drop-down list and checks (forever) if it's selected (may get stuck in loop)
    TODO: Loop problem again"""
    unit = find(*links["UNIT"])
    while True:
        select = Select(unit)
        select.select_by_index(15)
        unit.get_attribute('value')
        select = Select(unit)
        select.select_by_index(15)
        time.sleep(0.5)
        if unit.get_attribute('value') == 'მომსახურება':
            break


def check_company_name(ID):
    """If the ID indicated was right, website provides you with the company official name.
    Check if the Company name is present (therefore checks if the ID provided was right)"""
    company_name = find(*links["COMPANY_NAME"]).get_attribute('value')
    count = 0
    global id_tries

    while company_name == "" and count < 10:  # Waits for 10 sec for company name to be filled
        company_name = find(*links["COMPANY_NAME"]).get_attribute('value')
        time.sleep(1)
        count += 1
        if count == 9 and id_tries < 2:
            count = 0
            id_tries += 1
            fill_invoice(ID)
        elif id_tries == 2:
            id_tries = 0
            message = f"ID not found in database. Shutting down program. \n\n ID was {ID}"
            add_error(message)
            return False


def check_sum(ID):
    """Checks if the sum of all the invoices under this company is right,
    therefore checks if all the invoices were uploaded correctly"""
    sum = 0
    for value in MY_DICT[ID]:
        sum += float(value[0])
    sum_string = str("{:.2f}".format(sum))
    if sum >= 1000:
        sum_string = sum_string[:1] + ',' + sum_string[1:]
    print_to_log(f"\tSum in string = {sum_string}\n")
    sum_field = find(*links["PRICE_SUM"])
    if sum_string == sum_field.text:
        return True
    else:
        print_to_log("Sum was not right (message from check_sum function)")
        return False


def fill_invoice(ID, is_test_user):
    """Main Function. Fills invoice with provided info. Restarts the function (with same argument) if error occurs
    if is_test_user, types test ID instead of real ID"""
    # test ID 12345678910. This ID is for RS.ge in testing mode
    access_invoice_page()

    # if check_last_invoice(ID) is False: TODO: Doesn't work correctly, needs refining
    #     print_to_log(f"\tcheck_last_invoice duplicate warning received. Moving on to next ID\n\n")
    #     return None
    try:
        print_to_log("\n------------------------------------------\n")
        print_to_log(f"\t\t\tUploading ID: {ID}\n")
        btn_click("NEW_INVOICE_BTN")  # Open new Invoice
        select_month_in_list()
        if is_test_user:
            box_type("ID_INPUT", "12345678910")
        else:
            box_type("ID_INPUT", ID)
        # For actual usage, indicate ID variable as a value
        print_to_log(f"\tTyped ID: {ID}")

        if check_company_name(ID) == False:
            print_to_log(f"\t\t**** Company ID Error: Couldn't find company with ID {ID}."
                         f"Going for next one")
            return

        values_list = []

        for values in MY_DICT[ID]:
            box_type("PRODUCT_NAME", values[1])
            print_to_log(f"\tName uploaded {values[1]}")
            select_unit()
            box_type("PRICE", values[0])
            print_to_log(f"\tPrice uploaded: {values[0]}")
            select_vat(values[2])
            time.sleep(1)
            btn_click("ADD_BTN")
            print_to_log(f"\tUpload Finished\n")
            values_list.append(f"Purpose: {values[1]}, Price: {values[0]}, VAT: {values[2]}")

        time.sleep(1)

        if check_sum(ID):
            btn_click("SUBMIT")
        else:
            message = "\t*** Sum was not right. Starting access&fill again"
            add_error(message)
            fill_invoice(ID, is_test_user)


    except NoSuchElementException:
        traceback.print_exc()
        message = f"ID: {ID} Couldn't find element during fill_invoice process"
        add_error(message)
        fill_invoice(ID, is_test_user)
    except ElementClickInterceptedException:
        message = f"ID: {ID} Couldn't click element"
        add_error(message)
        fill_invoice(ID, is_test_user)
    except NoAlertPresentException:
        message = f"ID: {ID} No alert is present to finish uploading invoice"
        add_error(message)
        fill_invoice(ID, is_test_user)
    except ErrorBoxException:
        if find(*links["ERROR_BOX"]):
            btn_click("ERROR_BOX_QUIT")
        message = f"ID: {ID} Error Box appeared"
        add_error(message)
        fill_invoice(ID, is_test_user)
    except:
        message = f"ID: {ID} Unknown error occurred during filling invoice"
        traceback.print_exc()
        add_error(message)
        fill_invoice(ID, is_test_user)
    else:
        try:
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            WebDriverWait(driver, 10).until_not(EC.alert_is_present())
        except:
            message = f"ID: {ID} \tCouldn't accept the upload alert"
            add_error(message)
            fill_invoice(ID, is_test_user)
        else:
            print_to_log(f"\t\t\tID {ID} uploaded successfully")
            print_to_log("\n------------------------------------------\n")
            upload_to_csv(ID, values_list)


# def check_last_invoice(ID):
#     try:
#         full_name = find(*links["UPLOADED_INVOICE_LIST_NAME"]).text
#         company_id = re.findall(r'^\(([0-9]*)-', str(full_name))[0]
#         print_to_log(f"The last ID in the list is: {company_id}")
#     except:
#         traceback_str = traceback.format_exc()
#         print_to_log(f"\t** ERROR: error with check_last_invoice func. "
#                      f"Full_name var: {full_name}, company_id var: {company_id}."
#                      f"\n traceback:\n {traceback_str}\n*******")
#         return True
#     if company_id == ID:
#         print_to_log(f"\t** Duplicate ID error. Last uploaded invoice ID was {company_id}. Now we are working on {ID}."
#                      f"Please jump to the next one")
#         return False
#     else:
#         return True


def print_to_log(message):
    """Prints to log.txt"""
    with open("Logs/logs.txt", mode="a", encoding='utf-8') as file:
        print(message)
        file.write(f"{message}\n")


def upload_to_csv(ID, values):
    """Uploads the data list received from Excel file into data_list.csv"""
    try:
        with open("Logs/data_list.csv", mode="a", encoding='utf-8') as file:
            file.write(f"ID: {ID}. {values}\n")
    except:
        with open("Logs/data_list.csv", mode="w", encoding='utf-8') as file:
            file.write(f"ID: {ID}. {values}\n")
