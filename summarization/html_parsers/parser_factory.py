from summarization.html_parsers.delmagyar_parser import RegionalParser
from summarization.html_parsers.hvg_parser import HvgParser
from summarization.html_parsers.index_parser import IndexParser
from summarization.html_parsers.kisalfold_parser import KisalfoldParser
from summarization.html_parsers.m4sport_parser import M4SportParser
from summarization.html_parsers.metropol_parser import MetropolParser
from summarization.html_parsers.nepszava_parser import NepszavaParser
from summarization.html_parsers.nlc_parser import NLCParser
from summarization.html_parsers.origo_parser import OrigoParser
from summarization.html_parsers.parser_24 import Parser24
from summarization.html_parsers.parser_base import ParserBase
from summarization.html_parsers.portfolio_parser import PortfolioParser
from summarization.html_parsers.telex_parser import TelexParser


class HtmlParserFactory:
    parsers = {
        'telex': TelexParser,
        'index': IndexParser,
        '24': Parser24,
        'metropol': MetropolParser,
        'nlc': NLCParser,
        'hvg': HvgParser,
        'origo': OrigoParser,
        'm4sport': M4SportParser,
        'nepszava': NepszavaParser,
        'portfolio': PortfolioParser,
        'kisalfold': KisalfoldParser,
        'delmagyar': RegionalParser,
        'szon': RegionalParser,
        'vaol': RegionalParser,
        'zaol': RegionalParser,
        'duol': RegionalParser,
        'feol': RegionalParser,
        'heol': RegionalParser,
        'veol': RegionalParser,
        'teol': RegionalParser,
        'beol': RegionalParser,
        'haon': RegionalParser,
        'baon': RegionalParser,
        'boon': RegionalParser,
        'nool': RegionalParser,
        'bama': RegionalParser,
        'kemma': RegionalParser,
    }

    @classmethod
    def get_parser(cls, site) -> ParserBase:
        return cls.parsers[site]()
