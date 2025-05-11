from configparser import ConfigParser
import os

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # remonte à la racine projet_API
    filepath = os.path.join(base_dir, filename)
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Le fichier {filepath} est introuvable.")
    parser.read(filepath)

    if parser.has_section(section):
        return {param[0]: param[1] for param in parser.items(section)}
    else:
        raise Exception(f"Section {section} non trouvée dans {filepath}")
