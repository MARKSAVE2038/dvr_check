# Automatic DVR status email

## Installation

1. [**Install** `python`](https://www.freecodecamp.org/italian/news/come-installare-python-su-windows/) with `pip` and add them to the **PATH**

2. Create a *virtual environment*:
```shell
python -m venv .venv
```

3. [OPTIONAL] If needed, lower Powershell execution policy:
```shell
set-executionpolicy remotesigned
```

4. **Activate** the virtual environment:
    - CMD:
        ```shell
        call ./.venv/Scripts/activate.bat
        ```
    - Powershell:
        ```shell
        ./.venv/Scripts/Activate.ps1
        ```

5. **Install** dependencies:
```shell
pip install -r .\requirements.txt
```

## Usage

1. Create `.env` file with the `MAILJET_API_KEY` and `MAILJET_SECRET_KEY` variables.

2. **Run** the program:
```shell
python ./src/main.py
```