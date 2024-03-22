### Upload Invoices from an Excel file into rs.ge invoice list via Selenium

Receives Excel file worksheet with a preset structure. Processes it into Python dictionary. Dictionary is then uploaded
into RS.ge via Selenium, one by one, under previous month.

Working sheet - grouped.xlsx file data is not eligible for actual upload, it is designed for rs.ge test user.

For actual upload, change Excel file data with real data and in main.py (line 7) change is_test_user variable to False

