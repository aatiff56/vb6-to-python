import winreg


def save_registry(k='Program', v="ColorSaveMS"):
    try:
        key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE,
                               r"SOFTWARE\\Wow6432Node\\")
        newKey = winreg.CreateKey(key, "Emerald")
        winreg.SetValueEx(newKey, k, 0, winreg.REG_SZ, str(v))
        if newKey:
            winreg.CloseKey(newKey)
        return True
    except Exception as e:
        print(e)
        return False


def read_registry(k='Program'):
    try:
        key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE,
                               r"SOFTWARE\\Wow6432Node\\Emerald")
        value = winreg.QueryValueEx(key, k)
        if key:
            winreg.CloseKey(key)
        return value[0]
    except Exception as e:
        print(e)
    return None


save_registry()
# print(read_registry())
