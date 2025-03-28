import os
import subprocess
import tempfile


def print_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")
    
    try:
        if os.name == 'nt':   
            print_command = ["mspaint", "/pt", image_path]
        else:  
            print_command = ["lp", image_path]  
        
        subprocess.run(print_command, check=True)
        print("Print job sent successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error printing file: {e}")

 
image_file = "example.png"  
print_image(image_file)