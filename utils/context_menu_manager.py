import sys
import os
import winreg

def get_executable_path():
    """
    Get the full path to FileTreeGen.exe in the current directory.
    """
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    exe_path = os.path.join(exe_dir, "FileTreeGen.exe")
    return exe_path

def is_context_menu_installed():
    """
    Check if the context menu integration is installed for the current user.
    Returns True if installed, False otherwise.
    """
    key_paths = [
        r"Software\Classes\Directory\Background\shell\GenerateFileTree",
        r"Software\Classes\Directory\shell\GenerateFileTree"
    ]
    for key_path in key_paths:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            continue
    return False

def install_context_menu():
    """
    Install the context menu integration for the current user.
    Returns True if successful, False otherwise.
    """
    try:
        exe_path = get_executable_path()
        if not os.path.isfile(exe_path):
            return False, "FileTreeGen.exe not found in the current directory."

        command = f'"{exe_path}" "%V"'
        icon = f"{exe_path},0"

        # Directory background (right-click inside folder)
        bg_key_path = r"Software\Classes\Directory\Background\shell\GenerateFileTree"
        bg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, bg_key_path)
        winreg.SetValueEx(bg_key, "", 0, winreg.REG_SZ, "Generate File Tree")
        winreg.SetValueEx(bg_key, "Icon", 0, winreg.REG_SZ, icon)
        bg_cmd_key = winreg.CreateKey(bg_key, "command")
        winreg.SetValueEx(bg_cmd_key, "", 0, winreg.REG_SZ, command)
        winreg.CloseKey(bg_cmd_key)
        winreg.CloseKey(bg_key)

        # Directory (right-click on folder)
        dir_key_path = r"Software\Classes\Directory\shell\GenerateFileTree"
        dir_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, dir_key_path)
        winreg.SetValueEx(dir_key, "", 0, winreg.REG_SZ, "Generate File Tree")
        winreg.SetValueEx(dir_key, "Icon", 0, winreg.REG_SZ, icon)
        dir_cmd_key = winreg.CreateKey(dir_key, "command")
        winreg.SetValueEx(dir_cmd_key, "", 0, winreg.REG_SZ, command)
        winreg.CloseKey(dir_cmd_key)
        winreg.CloseKey(dir_key)

        return True, "Context menu installed successfully."
    except Exception as e:
        return False, f"Failed to install context menu: {e}"

def uninstall_context_menu():
    """
    Uninstall the context menu integration for the current user.
    Returns True if successful, False otherwise.
    """
    try:
        # Remove directory background entry
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Classes\Directory\Background\shell\GenerateFileTree\command")
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Classes\Directory\Background\shell\GenerateFileTree")
        except FileNotFoundError:
            pass

        # Remove directory entry
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Classes\Directory\shell\GenerateFileTree\command")
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Classes\Directory\shell\GenerateFileTree")
        except FileNotFoundError:
            pass

        return True, "Context menu uninstalled successfully."
    except Exception as e:
        return False, f"Failed to uninstall context menu: {e}"
