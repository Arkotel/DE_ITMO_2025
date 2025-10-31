import pandas as pd
import numpy as np


def conv_data(raw_data):

    # --- Создаем копию для обработки ---
    proc_data = raw_data.copy(deep=True)

    # --- Замена данных, изменение типов ---
    RS = proc_data["Recorded_Speed"]
    SL = proc_data["Speed_Limit"]
    proc_data["Speed_Exceeded"] = RS > SL
    proc_data = proc_data.drop(["Speed_Limit", "Recorded_Speed"], axis=1)
    proc_data["Towed"] = proc_data["Towed"].map({"Yes": True, "No": False})
    proc_data["Towed"] = proc_data["Towed"].astype(bool)
    proc_data["Fine_Paid"] = (
        proc_data["Fine_Paid"].map({"Yes": True, "No": False}).astype(bool)
    )
    proc_data["Court_Appearance_Required"] = (
        proc_data["Court_Appearance_Required"]
        .map({"Yes": True, "No": False})
        .astype(bool)
    )
    # Удаляем столбец Comments
    proc_data = proc_data.drop("Comments", axis=1)
    # Удаляем столбец Alcohol_Level
    proc_data = proc_data.drop("Alcohol_Level", axis=1)
    proc_data["DateTime"] = pd.to_datetime(
        proc_data["Date"] + " " + proc_data["Time"], format="%d.%m.%Y %H:%M"
    )  # Объединяем столбцы
    # Удаляем столбцы Data и Time
    proc_data = proc_data.drop(["Date", "Time"], axis=1)

    # Категориальные преобразования
    category_columns = [
        "Violation_Type",
        "Location",
        "Vehicle_Type",
        "Vehicle_Color",
        "Registration_State",
        "Driver_Gender",
        "License_Type",
        "Weather_Condition",
        "Road_Condition",
        "Issuing_Agency",
        "License_Validity",
        "Traffic_Light_Status",
        "Breathalyzer_Result",
        "Payment_Method",
    ]
    for col in category_columns:
        proc_data[col] = proc_data[col].astype("category")

    # Создаем понятные категории для Helmet_Worn
    helmet_mapping = {
        "Yes": "worn",  # надет
        "No": "not_worn",  # не надет
        np.nan: "not_required",  # не предусмотрен
    }
    proc_data["Helmet_Worn"] = (
        proc_data["Helmet_Worn"].map(helmet_mapping).astype("category")
    )
    # Создаем понятные категории для Seatbelt_Worn
    seatbelt_mapping = {
        "Yes": "worn",  # надет
        "No": "not_worn",  # не надет
        np.nan: "not_required",  # не предусмотрен
    }
    proc_data["Seatbelt_Worn"] = (
        proc_data["Seatbelt_Worn"].map(seatbelt_mapping).astype("category")
    )

    # Числовые преобразования
    numeric_conversions = {
        "Fine_Amount": "int16",
        "Vehicle_Model_Year": "int16",
        "Driver_Age": "uint8",
        "Penalty_Points": "uint8",
        "Number_of_Passengers": "uint8",
        "Previous_Violations": "uint8",
    }
    for col, dtype in numeric_conversions.items():
        proc_data[col] = proc_data[col].astype(dtype)

    new_column_names = {col: col.lower() for col in proc_data.columns}

    clean_data = proc_data.rename(columns=new_column_names)

    print("\nТипы данных до обработки:")
    print(raw_data.info())
    print("\nТипы данных после обработки:")
    print(clean_data.info())

    return clean_data
