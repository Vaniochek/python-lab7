import csv
import os
import matplotlib.pyplot as plt
import numpy as np

import os

# Автоматично знаходимо путь до папку де лежить lab7.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(CURRENT_DIR, "gdp_dynamics.csv")
DEFAULT_COUNTRY_1 = "Ukraine"
DEFAULT_COUNTRY_2 = "Poland"


def load_data_from_csv(filepath: str) -> dict | None:
    #Зчитує дані з CSV-файлу та групує їх за країнами: {Country: {Year: Value}}.
    data_by_country = {}

    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл '{filepath}' не знайдено.")

        with open(filepath, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            if not rows:
                print(f"[ПОПЕРЕДЖЕННЯ] Файл '{filepath}' порожній.")
                return None

            for row in rows:
                country = row.get("Country Name", "").strip()
                year = int(row.get("Year", 0))
                value = float(row.get("Value", 0.0))

                if country not in data_by_country:
                    data_by_country[country] = {}
                data_by_country[country][year] = value

        print(f"[УСПІХ] Завантажено дані для країн: {', '.join(data_by_country.keys())}")
        return data_by_country

    except FileNotFoundError as err:
        print(f"[ПОМИЛКА] {err}")
        return None
    except PermissionError:
        print(f"[ПОМИЛКА] Відсутній доступ до файлу '{filepath}'.")
        return None
    except (ValueError, KeyError) as err:
        print(f"[ПОМИЛКА ФОРМАТУ ДАНИХ] Пошкоджені дані у CSV: {err}")
        return None


def plot_line_dynamics(data: dict, country1: str, country2: str) -> None:
    #Завдання 2: Лінійний графік динаміки показника для двох країн.
    if country1 not in data or country2 not in data:
        print(f"[ПОМИЛКА] Дані для '{country1}' або '{country2}' відсутні.")
        return

    years1 = sorted(data[country1].keys())
    years2 = sorted(data[country2].keys())
    common_years = sorted(list(set(years1) & set(years2)))

    values1 = [data[country1][y] for y in common_years]
    values2 = [data[country2][y] for y in common_years]

    plt.figure(figsize=(9, 5))
    plt.plot(common_years, values1, marker="o", linewidth=2, label=country1, color="#0057B7")
    plt.plot(common_years, values2, marker="s", linewidth=2, label=country2, color="#DC143C")

    plt.title(f"Динаміка GDP per capita: {country1} та {country2} (2015–2022)", fontsize=13, fontweight="bold")
    plt.xlabel("Рік", fontsize=11)
    plt.ylabel("GDP per capita (current US$)", fontsize=11)
    plt.xticks(common_years)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


def plot_bar_for_input_country(data: dict) -> None:
    #Завдання 3: Стовпчаста діаграма для країни, введеної користувачем.
    print("\nДоступні країни у файлі:", ", ".join(data.keys()))
    user_country = input("Введіть назву країни для побудови стовпчастої діаграми: ").strip()

    #Пошук без урахування регістру
    matched_country = None
    for c in data.keys():
        if c.lower() == user_country.lower():
            matched_country = c
            break

    if not matched_country:
        print(f"[ПОМИЛКА] Країну '{user_country}' не знайдено в наборі даних!")
        return

    years = sorted(data[matched_country].keys())
    values = [data[matched_country][y] for y in years]

    plt.figure(figsize=(9, 5))
    bars = plt.bar(years, values, color="#4CAF50", edgecolor="#2E7D32", width=0.55)

    #Підпис значень над стовпчиками
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f"{int(height)}$", ha="center", va="bottom", fontsize=8)

    plt.title(f"GDP per capita за роками: {matched_country}", fontsize=13, fontweight="bold")
    plt.xlabel("Рік", fontsize=11)
    plt.ylabel("ВВП на душу населення (US$)", fontsize=11)
    plt.xticks(years)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


def plot_pie_comparison_for_year(data: dict, country1: str, country2: str) -> None:
    #Завдання 4: Кругова діаграма порівняння часток двох країн за обраний рік.
    if country1 not in data or country2 not in data:
        print(f"[ПОМИЛКА] Дані для порівняння недоступні.")
        return

    years1 = set(data[country1].keys())
    years2 = set(data[country2].keys())
    common_years = sorted(list(years1 & years2))

    print(f"\nДоступні спільні роки для порівняння: {common_years}")
    year_input = input("Введіть рік для кругової діаграми: ").strip()

    if not year_input.isdigit() or int(year_input) not in common_years:
        print(f"[ПОМИЛКА] Некоректний рік або даних за цей рік немає.")
        return

    target_year = int(year_input)
    val1 = data[country1][target_year]
    val2 = data[country2][target_year]

    values = np.array([val1, val2])
    labels = [country1, country2]
    colors = ["#FFD700", "#1E88E5"]

    def autopct_format(pct):
        total = np.sum(values)
        val = pct * total / 100.0
        return f"{pct:.1f}%\n({val:.1f} $)"

    plt.figure(figsize=(6, 6))
    plt.pie(
        values,
        labels=labels,
        autopct=autopct_format,
        startangle=90,
        colors=colors,
        explode=(0.05, 0),
        textprops={"fontsize": 11, "fontweight": "bold"},
    )
    plt.title(f"Частки GDP per capita: {country1} проти {country2} ({target_year})", fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.show()


def main():
    data = load_data_from_csv(CSV_FILE)
    if not data:
        return

    while True:
        print("\n" + "=" * 55)
        print("     ПРАКТИЧНА РОБОТА 7: ВІЗУАЛІЗАЦІЯ ДАНИХ")
        print("=" * 55)
        print("1. Лінійний графік динаміки (Україна та Польща)")
        print("2. Стовпчаста діаграма (країна на вибір користувача)")
        print("3. Кругова діаграма порівняння (за обраний рік)")
        print("0. Вихід")
        print("=" * 55)

        choice = input("Оберіть пункт меню (0-3): ").strip()

        if choice == "1":
            plot_line_dynamics(data, DEFAULT_COUNTRY_1, DEFAULT_COUNTRY_2)
        elif choice == "2":
            plot_bar_for_input_country(data)
        elif choice == "3":
            plot_pie_comparison_for_year(data, DEFAULT_COUNTRY_1, DEFAULT_COUNTRY_2)
        elif choice == "0":
            print("\nРоботу завершено.")
            break
        else:
            print("[ПОМИЛКА] Невірний пункт меню!")


if __name__ == "__main__":
    main()