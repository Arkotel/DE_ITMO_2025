import pandas as pd
import os


def val_file_exists(file_path):
    """Проверяет существует ли файл"""
    return os.path.exists(file_path)


def check_file_csv_exists(raw, filename):
    """Проверяет существует ли файл .csv"""
    file_path = os.path.join(raw, filename)
    if os.path.exists(file_path):
        return file_path
    else:
        return False


def check_file_parquet_exists(processed, filename):
    """Проверяет существует ли файл .parquet"""
    file_path = os.path.join(processed, filename)
    return os.path.exists(file_path)


def val_csv(raw_data):
    errors = False

    print("\nПропуски:\n")
    raw_data = raw_data.replace(["", "-", "null", "NULL", "NA", "N/A"], pd.NA)
    empty_values = raw_data.isnull().sum()

    for column, count in empty_values.items():
        if count >= 0:
            print(f"{column}: {count} пропусков")

    if empty_values.sum() == 0:
        print("В данных нет пропусков")

    print("\nНаличие столбцов:")
    expected_columns = [
        "Violation_ID",
        "Violation_Type",
        "Fine_Amount",
        "Location",
        "Date",
        "Time",
        "Vehicle_Type",
        "Vehicle_Color",
        "Vehicle_Model_Year",
        "Registration_State",
        "Driver_Age",
        "Driver_Gender",
        "License_Type",
        "Penalty_Points",
        "Weather_Condition",
        "Road_Condition",
        "Officer_ID",
        "Issuing_Agency",
        "License_Validity",
        "Number_of_Passengers",
        "Helmet_Worn",
        "Seatbelt_Worn",
        "Traffic_Light_Status",
        "Speed_Limit",
        "Recorded_Speed",
        "Alcohol_Level",
        "Breathalyzer_Result",
        "Towed",
        "Fine_Paid",
        "Payment_Method",
        "Court_Appearance_Required",
        "Previous_Violations",
        "Comments",
    ]

    ib = 0
    for col in expected_columns:
        if col in raw_data.columns:
            ib += 0
        else:
            print(f" {col}: Отсутствует")
            ib += 1
    if ib == 0:
        print("Все признаки присутствуют\n")

    print(
        f"Валидация исходных данных: {'пройдена\n' if not errors else 'не пройдена\n'}"
    )
    return not errors


def val_parquet(clean_data):

    errors = False

    print("\nПропуски:")
    clean_data = clean_data.replace(
        ["", "-", "null", "NULL", "NA", "N/A"], pd.NA
    )  # noqa
    empty_values = clean_data.isnull().sum()
    for column, count in empty_values.items():
        if count > 0:
            print(f"{column}: {count} пропусков")
    if empty_values.sum() == 0:
        print("В данных нет пропусков")

    print("\nТипы данных:")
    features_types = {
        "violation_id": "object",
        "violation_type": "category",
        "fine_amount": "int16",
        "location": "category",
        "vehicle_type": "category",
        "vehicle_color": "category",
        "vehicle_model_year": "int16",
        "registration_state": "category",
        "driver_age": "uint8",
        "driver_gender": "category",
        "license_type": "category",
        "penalty_points": "uint8",
        "weather_condition": "category",
        "road_condition": "category",
        "officer_id": "object",
        "issuing_agency": "category",
        "license_validity": "category",
        "number_of_passengers": "uint8",
        "helmet_worn": "category",
        "seatbelt_worn": "category",
        "traffic_light_status": "category",
        "breathalyzer_result": "category",
        "towed": "bool",
        "fine_paid": "bool",
        "payment_method": "category",
        "court_appearance_required": "bool",
        "speed_exceeded": "bool",
        "datetime": "datetime64[ns]",
        "previous_violations": "uint8",
    }

    ia = 0
    errors = False
    for column, expected_type in features_types.items():
        if column in clean_data.columns:
            ia += 0
            actual_type = str(clean_data[column].dtype)
            if actual_type == expected_type:
                print(f"{column}: {actual_type}")
            else:
                print(
                    f"{column}: {actual_type} Ошибка (ожидался {expected_type})"
                )  # noqa
                errors = True
        else:
            print(f" {column}: Отсутствует")
            ia += 1
            errors = True
    if ia == 0:
        print("Все признаки присутствуют")

    print(f"\nДубликаты: {clean_data.duplicated().sum()} записей\n")

    print("\n---Уникальность данных---\n")
    if "violation_id" in clean_data.columns:
        unique_ID = clean_data["violation_id"].nunique()
        uniq = unique_ID / len(clean_data["violation_id"])
        print(f"Уникальных violation_id: {unique_ID}")
        print(f"Уникальность: {uniq}")

    print(
        f"\nВалидация выходных данных: {'пройдена \n---Валидация завершена---\n' if not errors else 'не пройдена'}"
    )
    return not errors
