from scraper import YahooFinanceCrawler

def main():
    crawler = YahooFinanceCrawler()
    crawler.run("Argentina", "yahoo_finance_screener")
    print("Dados salvos em arquivos CSV")

if __name__ == "__main__":
    main()


