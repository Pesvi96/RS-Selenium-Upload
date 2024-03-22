"""Dictionary of all the web elements needed for this process"""

links = {
    "POP_UP": ("css selector", "#rsPopup_popInvoiceHelp > div > div.rsPopupHeader > div.rsPopupClose"),
    "SIGN_IN_BTN": ("css selector", "#headerSingInText > p"),
    "SIGN_IN_USER": ("css selector", "#username"),
    "SIGN_IN_PASS": ("css selector", "#password"),
    "SIGN_IN_SUBMIT": ("css selector", "#btnLogin"),
    "SIGN_IN_ERROR": ("css selector", "#rsAlert > div"),
    "TEST_CUSTOMER_CHOICE": ("css selector", "#testUserContainer > p > l"),
    "TEST_CUSTOMER_ONE": ("css selector", "#testUserChoose > div:nth-child(1) > p > l"),
    "MODULES": ("css selector", "#PinModule > l"),
    "NEW_INVOICE_BTN": ("css selector", "#btnNewInvoice"),
    "MONTH_LIST": ("css selector", "#OperationMonth > div > select"),
    "YEAR_LIST": ("css selector", "#OperationYear > div > select"),
    "ID_INPUT": ("css selector", "#Inv_Buyer_Tin_inputID"),
    "PRODUCT_NAME": ("css selector", "#good_name_inputID"),
    "UNIT": ("css selector", "#good_unit"),
    "PRICE": ("css selector", "#good_amount"),
    "ADD_BTN": ("css selector", "#btnAddGood"),
    "SUBMIT": ("css selector", "#btnSend"),
    "COMPANY_NAME": ("css selector", "#Buyer_Name_inputID"),
    "ERROR_BOX": ("css selector", "#rsAlert > div"),
    "ERROR_BOX_QUIT": ("css selector", "#rsAlert > div > i"),
    "UPLOADED_INVOICE_LIST_NAME": ("css selector", "#rsGrid_grdInvoicesSeller > "
                                                   "table > tbody > tr:nth-child(1) > td:nth-child(6)"),
    "UPLODADED_INVOICE_LIST_PRICE": ("css selector", "#rsGrid_grdInvoicesSeller "
                                                     "> table > tbody > tr:nth-child(1) > td:nth-child(9)"),
    "VAT_LIST": ("css selector", "#good_vat_type"),
    "PRICE_SUM": ("css selector", "#rsGrid_grdInvoiceGoods > table > tfoot > tr.rsGridSummaryRow > td:nth-child(5)")

}
