import argparse
import csv
from tabulate import tabulate

def parse_args():
    parser = argparse.ArgumentParser(
        description="Скрипт для анализа макроэкономических данных"
    )

    parser.add_argument(
        "--files",
        nargs="*", # или "+" для обязательного указания хотя бы одного файла
        type=str,
        # required=True,
        help="Список CSV-файлов c данными для анализа"
    )

    parser.add_argument(
        "--report",
        type=str,
        # required=True,
        default="average-gdp",
        help="Название отчета"
    )

    return parser.parse_args()


def read_files(file_list):
    all_rows = []

    for filename in file_list:
        try:
            with open(filename, newline="") as file:
                reader = csv.DictReader(file)

                if "country" not in reader.fieldnames or "gdp" not in reader.fieldnames:
                    raise ValueError(
                        f"Файл {filename} не содержит необходимых колонок (country, gdp)"
                    )

                for row in reader:
                    all_rows.append(row)
                
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
        except Exception as e:
            print(f"Ошибка при чтении файла {filename}: {e}")
    return all_rows


def build_average_gdp_report(rows):
    country_data = {}

    for row in rows:
        country = row["country"]
        gdp = float(row["gdp"])

        if country not in country_data:
            country_data[country] = {"sum": 0, "count": 0}

        country_data[country]["sum"] += gdp
        country_data[country]["count"] += 1


    result = []
    for country, data in country_data.items():
        avg = data["sum"] / data["count"]
        result.append((country, avg))

    result.sort(key=lambda x: x[1], reverse=True)

    return result


def print_report(report_data):
    print(
        tabulate(
            report_data,
            headers=["country", "gdp"],
            floatfmt=".2f",
            tablefmt="grid",
            showindex=range(1, len(report_data) + 1)
        )
    )


def main():
    args = parse_args()

    if not args.files:
        print("Не указаны файлы для анализа. Используйте --files для указания CSV-файлов.")
        return

    rows = read_files(args.files)

    if args.report == "average-gdp":
        report = build_average_gdp_report(rows)
        print_report(report)
    else:
        print(f"Отчет {args.report} не поддерживается.")


if __name__ == "__main__":
    main()