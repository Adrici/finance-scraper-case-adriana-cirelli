import unittest
import os
from scraper import YahooFinanceCrawler

class TestYahooFinanceCrawler(unittest.TestCase):

    def setUp(self):
        self.crawler = YahooFinanceCrawler()

    def tearDown(self):
        self.crawler.close()

    def test_run_and_save_to_csv(self):
        # Define os parâmetros de entrada para o teste
        filter_text = "Argentina"
        filename = "test_output"

        # Executa o método run() para capturar dados da Argentina
        self.crawler.run(filter_text, filename)

        # Verifica se o arquivo CSV foi gerado corretamente
        results_dir = 'results'
        expected_csv_file = f"{filename}.csv"
        full_path = os.path.join(results_dir, expected_csv_file)
        self.assertTrue(os.path.exists(full_path), f"Arquivo CSV {expected_csv_file} não encontrado")

        # Lê o conteúdo do arquivo CSV (opcional: verificar o conteúdo)
        with open(full_path, mode='r') as file:
            lines = file.readlines()
            self.assertGreater(len(lines), 1, "O arquivo CSV está vazio ou incompleto")

if __name__ == "__main__":
    unittest.main()
