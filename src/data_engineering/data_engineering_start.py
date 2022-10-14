import argparse

from src.data_engineering.data_engineering import lending_club_data_to_csv, german_data_to_csv
from src.data_engineering.get_metrics import get_metrics

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Métodos utilizados para geração e filtragem de conjuntos de dados")
    parser.add_argument("--data", help="Seleção do gerador do conjunto de dados tratado",
                        choices=['GERMAN_CREDIT', 'LENDINGCLUB', 'METRICS'])
    args = parser.parse_args()

    if args.data == 'GERMAN_CREDIT':
        german_data_to_csv()
    elif args.data == 'LENDINGCLUB':
        lending_club_data_to_csv()
    elif args.data == 'METRICS':
        get_metrics()
