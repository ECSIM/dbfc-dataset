import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from art import tprint

NOTEBOOKS_LIST = [
    "Pd-Decorated-Ni-Co_rGO Catalyst",
    "Pd-C Catalyst",
    "Pt-C Catalyst"]

EXTENSION = ".ipynb"


if __name__ == "__main__":
    tprint("DBFC-DATASET","bulbhead")
    tprint("NOTEBOOKS","bulbhead")
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    print("Processing ...")
    for index, notebook in enumerate(NOTEBOOKS_LIST):
        path = os.path.join("Notebooks", notebook)
        with open(path + EXTENSION) as f:
            nb = nbformat.read(f, as_version=4)
            ep.preprocess(nb, {'metadata': {'path': 'Notebooks/'}})
        with open(path + EXTENSION, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("{0}.{1} [OK]".format(str(index + 1), notebook))