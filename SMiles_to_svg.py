from rdkit import Chem
from rdkit.Chem import Draw
import os
import re
import hashlib

def hash_smiles(smiles):
    return hashlib.md5(smiles.encode()).hexdigest()[:8]

def sanitize_filename(smiles, max_length=1000):
    sanitized = re.sub(r'[^a-zA-Z0-9]', '_', smiles)
    return sanitized[:max_length]

def fix_smiles(smiles):
    
    smiles = smiles.replace('[*]', '').replace('=*', '')
    smiles = re.sub(r'\[.*\]', '', smiles)  
    return smiles

string = "insert your smiles here"

smiles_list = string.strip().split(".")

output_dir = ""
os.makedirs(output_dir, exist_ok=True)

smiles_list2 = [element for element in smiles_list if element != "CC"]
valid_smiles = []
invalid_smiles = []

for i, smiles in enumerate(smiles_list2):
    try:
    
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            valid_smiles.append(smiles)
            unique_hash = hash_smiles(smiles)
            output_file = os.path.join(output_dir, f"{i+1}_{sanitize_filename(smiles)}.svg")
            Draw.MolToFile(mol, output_file)
            print(f"Molecule structure saved to {output_file}")
        else:
            raise ValueError("Invalid SMILES")
    except Exception:
     
        fixed_smiles = fix_smiles(smiles)
        mol = Chem.MolFromSmiles(fixed_smiles)
        if mol:
            valid_smiles.append(fixed_smiles)
            unique_hash = hash_smiles(fixed_smiles)
            output_file = os.path.join(output_dir, f"{i+1}_{sanitize_filename(fixed_smiles)}_fixed.svg")
            Draw.MolToFile(mol, output_file)
            print(f"Fixed and saved molecule structure to {output_file}")
        else:
            invalid_smiles.append(smiles)
            print(f"Invalid SMILES: {smiles}")

print(f"Valid SMILES count: {len(valid_smiles)}")
print(f"Invalid SMILES count: {len(invalid_smiles)}")


valid_file_path = os.path.join(output_dir, "valid_smiles_5.txt")
invalid_file_path = os.path.join(output_dir, "invalid_smiles_5.txt")

with open(valid_file_path, "w") as valid_file:
    for smiles in valid_smiles:
        valid_file.write(smiles + "\n"+ "\n")

with open(invalid_file_path, "w") as invalid_file:
    for smiles in invalid_smiles:
        invalid_file.write(smiles + "\n"+ "\n")

print(f"Valid SMILES saved to {valid_file_path}")
print(f"Invalid SMILES saved to {invalid_file_path}")
