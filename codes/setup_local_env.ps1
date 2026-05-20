# Run from repository root in PowerShell.
# This assumes Anaconda/Miniconda is installed.

conda create -n LangAzure python=3.11 -y
conda activate LangAzure

python -m pip install --upgrade pip
python -m pip install -r codes/requirements_local.txt

python -c "import langgraph; import fastapi; import pandas; print('Local setup OK')"
