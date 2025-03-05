import ctypes
import sys
import winreg


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    if is_admin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        return False


def change_registry_value(key_path, value_name, new_value):
    try:
        # Öffne den Registrierungsschlüssel
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)

        # Setze den Wert
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, new_value)

        # Schließe den Schlüssel
        winreg.CloseKey(key)

        print(f"Erfolgreich {value_name} auf {new_value} geändert")
    except FileNotFoundError:
        print("Registrierungsschlüssel nicht gefunden.")
    except PermissionError:
        print("Zugriff verweigert. Führen Sie das Skript als Administrator aus.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


if __name__ == "__main__":
    if run_as_admin():
        key_path = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
        value_name = "ProcessorNameString"

        change_registry_value(key_path, value_name, new_value=input("New CPU-Name: "))