from tests.data_loader_test import load_data


def main():
    FILE_ID = "1gJrXyvqIVSZCEjqhGhvisyMyxI0zBald"  # ID файла на Google Drive
    raw_data = load_data(FILE_ID)
    print("Данные загружены")
    return raw_data


if __name__ == "__main__":
    main()
