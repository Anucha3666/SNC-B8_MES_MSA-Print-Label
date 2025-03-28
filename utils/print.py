import os
import subprocess
import tempfile


def print_zpl(zpl_data, printer_name):
    """
    Print ZPL data to a printer using CUPS on Linux systems.

    Args:
        zpl_data (str): The ZPL data to be printed
        printer_name (str): The name of the printer to use
    """
    try:
        # Get list of available printers
        result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
        if result.returncode != 0:
            raise ValueError("Failed to get list of printers")

        available_printers = []
        for line in result.stdout.splitlines():
            if line.startswith('printer '):
                available_printers.append(line.split()[1])

        if printer_name not in available_printers:
            raise ValueError(f"Printer '{printer_name}' not found in available printers: {available_printers}")

        # Create a temporary file with the ZPL data
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(zpl_data.encode('utf-8'))
            temp_filename = temp_file.name

        # Print the file using lp command
        print_result = subprocess.run(['lp', '-d', printer_name, '-o', 'raw', temp_filename],
                                      capture_output=True,
                                      text=True)

        if print_result.returncode != 0:
            raise ValueError(f"Printing failed: {print_result.stderr}")

        print(f"Started printing on {printer_name}")

        # Remove the temporary file
        os.unlink(temp_filename)

    except Exception as e:
        print(f"An error occurred while printing: {e}")

def print_image(image_path, printer_name):
    """
    Print an image file to a printer using CUPS on Linux systems.

    Args:
        image_path (str): The path to the image file to be printed
        printer_name (str): The name of the printer to use
    """
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file '{image_path}' not found.")

        result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
        if result.returncode != 0:
            raise ValueError("Failed to get list of printers")

        available_printers = [
            line.split()[1] for line in result.stdout.splitlines() if line.startswith('printer ')
        ]

        if printer_name not in available_printers:
            raise ValueError(f"Printer '{printer_name}' not found in available printers: {available_printers}")

        print_result = subprocess.run(
            ['lp', '-d', printer_name, '-o', 'fit-to-page', '-o', 'media=A4', '-o', 'cut'],
            capture_output=True,
            text=True
        )

        if print_result.returncode != 0:
            raise ValueError(f"Printing failed: {print_result.stderr}")

        print(f"Started printing {image_path} on {printer_name}")

    except Exception as e:
        print(f"An error occurred while printing: {e}")


def print_ascii_art():
    print("-------------------------------------------")
    print("#  ____  __ ___              _            #")
    print("# |__ / / // __| ___ _ ___ _(_)__ ___ ___ #")
    print("#  |_ \/ _ \__ \/ -_) '_\ V / / _/ -_|_-< #")
    print("# |___/\___/___/\___|_|  \_/|_\__\___/__/ #")
    print("#                                         #")
    print("-------------------------------------------")
