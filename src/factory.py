from typing_extensions import List, Type

from scrapers.base_scraper import BaseScraper

scraper_registry = {}


def register_scraper(cls: Type[BaseScraper]):
    scraper_registry[cls.get_nome_organizadora()] = cls
    return cls


class ScraperFactory:
    @staticmethod
    def get_all_scrapers() -> List[BaseScraper]:
        return [scraper_class() for scraper_class in scraper_registry.values()]

    @staticmethod
    def get_scraper(nome_organizadora: str) -> BaseScraper:
        if nome_organizadora in scraper_registry:
            return scraper_registry[nome_organizadora]()
        raise ValueError(f"Provider '{nome_organizadora}' not found")
