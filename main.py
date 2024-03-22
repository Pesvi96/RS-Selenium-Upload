from datetime import date
from functions import *
from data_grouped import MY_DICT, ID_LIST
import time
import ctypes

is_test_user = True  # Change test_user into False if you want actual upload


def main():
    # Create logs.txt file (if already created, clears the file)
    with open("Logs/logs.txt", mode="w", encoding='utf-8') as file:
        file.write(f"Date: {date.today().strftime("%B %d, %Y")}\n")

    driver = init("https://www.rs.ge")
    if is_test_user:
        sign_into_test_user()
    else:
        sign_into_actual_user()
    access_invoice_page()
    # Iterates through the data dictionary and uploads each company invoices to rs.ge
    for ID in MY_DICT:
        fill_invoice(ID, is_test_user)

    upload_to_csv("Dictionary: ", MY_DICT)
    print_to_log("\n\n\n\t\tCongrats! Upload complete!")

    driver.quit()


ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)  # this will prevent the screen saver or sleep.

# For counting time needed for execution
start_time = time.time()
main()

# Statistics of amount of invoices, companies and time taken to upload it all
execution_time = int(time.time() - start_time)
execution_minutes = execution_time // 60
execution_seconds = execution_time - (execution_minutes * 60)
print_to_log(f"--- {execution_minutes}.{execution_seconds} minutes ---")
print_to_log(f"Amount of Companies: {len(MY_DICT)}\nAmount of invoices: {len(ID_LIST)}")

ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)  # set the setting screen saver setting back to normal
