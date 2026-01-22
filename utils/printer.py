import subprocess
import platform
import os


def print_document(filepath, settings):
    """
    Print document using OS-level commands.
    
    Args:
        filepath: Path to PDF file
        settings: Dict with keys:
            - copies: Number of copies (int)
            - color_mode: 'color' or 'bw'
            - duplex: 'single' or 'double'
            - orientation: 'portrait' or 'landscape'
            - pages_per_sheet: 1, 2, or 4
    
    Returns:
        tuple: (success: bool, message: str)
    """
    if not os.path.exists(filepath):
        return False, "File not found"
    
    system = platform.system()
    
    try:
        if system == 'Darwin':  # macOS
            return _print_macos(filepath, settings)
        elif system == 'Windows':
            return _print_windows(filepath, settings)
        elif system == 'Linux':
            return _print_linux(filepath, settings)
        else:
            return False, f"Unsupported operating system: {system}"
    except Exception as e:
        return False, f"Print error: {str(e)}"


def _print_macos(filepath, settings):
    """Print on macOS using lpr command."""
    cmd = ['lpr']
    
    # Number of copies
    copies = settings.get('copies', 1)
    cmd.extend(['-#', str(copies)])
    
    # Duplex (double-sided)
    if settings.get('duplex') == 'double':
        cmd.extend(['-o', 'sides=two-sided-long-edge'])
    else:
        cmd.extend(['-o', 'sides=one-sided'])
    
    # Orientation
    if settings.get('orientation') == 'landscape':
        cmd.extend(['-o', 'orientation-requested=4'])
    else:
        cmd.extend(['-o', 'orientation-requested=3'])
    
    # Pages per sheet
    pages_per_sheet = settings.get('pages_per_sheet', 1)
    if pages_per_sheet > 1:
        cmd.extend(['-o', f'number-up={pages_per_sheet}'])
    
    # Color mode (if printer supports it)
    if settings.get('color_mode') == 'bw':
        cmd.extend(['-o', 'ColorModel=Gray'])
    
    # Add file path
    cmd.append(filepath)
    
    # Execute print command
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        return True, "Print job sent successfully"
    else:
        return False, f"Print failed: {result.stderr}"


def _print_windows(filepath, settings):
    """Print on Windows using native print command."""
    import win32api
    import win32print
    
    # Get default printer
    printer_name = win32print.GetDefaultPrinter()
    
    # For Windows, we use ShellExecute with 'print' verb
    # Note: Advanced settings require more complex DEVMODE manipulation
    copies = settings.get('copies', 1)
    
    for _ in range(copies):
        win32api.ShellExecute(0, 'print', filepath, None, '.', 0)
    
    return True, f"Print job sent to {printer_name}"


def _print_linux(filepath, settings):
    """Print on Linux using lp or lpr command."""
    cmd = ['lp']
    
    # Number of copies
    copies = settings.get('copies', 1)
    cmd.extend(['-n', str(copies)])
    
    # Duplex
    if settings.get('duplex') == 'double':
        cmd.extend(['-o', 'sides=two-sided-long-edge'])
    
    # Orientation
    if settings.get('orientation') == 'landscape':
        cmd.extend(['-o', 'landscape'])
    
    # Pages per sheet
    pages_per_sheet = settings.get('pages_per_sheet', 1)
    if pages_per_sheet > 1:
        cmd.extend(['-o', f'number-up={pages_per_sheet}'])
    
    # Add file path
    cmd.append(filepath)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        return True, "Print job sent successfully"
    else:
        return False, f"Print failed: {result.stderr}"
