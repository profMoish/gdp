python -m venv venv            # создать виртуальное окружение
source venv/bin/activate      # активировать (macOS / Linux)
venv\Scripts\activate         # активировать (Windows)
pip install tabulate          # установить библиотеку
python main.py --files economic1.csv economic2.csv --report average-gdp         # запустить скрипт
