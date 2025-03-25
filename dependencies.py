import subprocess
import sys
import warnings

def check_and_install_dependencies():
    """
    Check if required packages are installed and install them if not.
    Also suppress specific openpyxl warnings.
    """
    # Suppress specific openpyxl warnings about unknown extensions
    warnings.filterwarnings("ignore", message="Unknown extension is not supported and will be removed", 
                          category=UserWarning, module="openpyxl")

    # Check and install required dependencies
    required_packages = ['pandas', 'numpy', 'requests', 'openpyxl', 'xlrd', 'tqdm']
    missing_dependencies = False
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_dependencies = True
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    # Show appropriate message based on dependency check
    if missing_dependencies:
        print("✅ Todas as dependências foram instaladas com sucesso!")
    else:
        print("✅ Todas as dependências já estão instaladas e prontas para uso!")
if __name__ == "__main__":
    check_and_install_dependencies()
