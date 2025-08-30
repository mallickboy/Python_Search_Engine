## Create virtual environment

``` python -m venv search_engine ```

## Activate virtual environment (from parent folder)

```Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass```

``` .\search_engine\Scripts\activate ```

## Install required libraries

``` pip install version_requirements.txt  ```

### Add pinecone API key
```bash
PINECONE_KEY=""
PINECONE_ENVIRONMENT=""
```

## Select kernel for Jupiter Notebook ( ipynb )

From top right corner select ``` (parent_folder)/Scripts/python.exe ``` as kernel and run

For python file use ``` python file_name ``` to execute