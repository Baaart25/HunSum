import glob
from os import path
from pathlib import Path
from typing import List

import pandas as pd
from pandarallel import pandarallel

from summarization.preprocess.language_detector import LanguageDetector
from summarization.utils.config_reader import get_config_from_yaml
from summarization.utils.data_helpers import make_dir_if_not_exists
from summarization.utils.logger import get_logger
from summarization.utils.tokenizer import Tokenizer


class ArticleCleaner:
    def __init__(self, config_path):
        self.config = get_config_from_yaml(config_path)
        self.language_detector = LanguageDetector(model_path=self.config.lang_detector_model_path)
        pandarallel.initialize(progress_bar=True, nb_workers=self.config.num_process)

    def clean_articles(self, sites):
        all_jsonl_files = glob.glob(f'{self.config.clean_src_dir}/*.jsonl.gz')
        sites_to_clean = all_jsonl_files if sites == 'all' \
            else [x for x in all_jsonl_files if self._is_site_in_sites(Path(x).name, sites.split(','))]

        make_dir_if_not_exists(self.config.clean_out_dir)
        log_file = path.join(self.config.clean_out_dir, 'clean_log.txt')
        logger = get_logger('logger', log_file)
        for site in sites_to_clean:
            self.clean(site, logger)

    def _is_site_in_sites(self, site: str, sites: List[str]):
        for x in sites:
            if x in site:
                return True
        return False

    def clean(self, site, logger):
        df_site = pd.read_json(f'{site}', lines=True)
        df_site = df_site[df_site['lead'] != '']
        logger.info(f'Cleaning {site}, size: {len(df_site)}')

        # drop articles where lead is longer than article
        df_site = df_site[df_site['article'].str.len() > df_site['lead'].str.len()]
        logger.info(f'Dropped articles where lead is longer than article, size: {len(df_site)}')

        df_site = df_site[df_site['article'].str.len().between(self.config.min_article_len,
                                                               self.config.max_article_len)]
        logger.info(f'Dropped articles where article is too long or short, size: {len(df_site)}')

        df_site = self._filter_by_max_lead_sentences(df_site)
        logger.info(f'Dropped articles where lead is longer than {self.config.max_lead_sentences} '
                    f'sentence, size: {len(df_site)}')

        df_site = self._filter_by_min_lead_tokens(df_site)
        logger.info(f'Dropped articles where lead is not at least {self.config.min_lead_tokens} '
                    f'token, size: {len(df_site)}')

        df_site = self._filter_by_min_article_sentences(df_site)
        logger.info(f'Dropped articles where article is not at least {self.config.min_article_sentences} '
                    f'sentence, size: {len(df_site)}')

        df_site = self._drop_non_hungarian_sentences(df_site)
        logger.info(f'Dropped non-Hungarian sentences, size: {len(df_site)}')

        make_dir_if_not_exists(self.config.clean_out_dir)
        domain = self._get_domain_of_site(df_site)
        df_site.to_json(f'{self.config.clean_out_dir}/{domain}.jsonl.gz', orient='records',
                        lines=True, compression='gzip')

    def _drop_non_hungarian_sentences(self, df):
        return df[df['article']
                  .parallel_apply(lambda x: x.replace('\n', ' '))
                  .map(self.language_detector.predict) == 'hu']

    def _get_domain_of_site(self, df):
        return df.iloc[0].domain.split('.')[0]

    def _filter_by_min_article_sentences(self, df):
        return df[df['article'].parallel_map(Tokenizer.count_sentences) > self.config.min_article_sentences]

    def _filter_by_min_lead_tokens(self, df):
        return df[df['lead'].parallel_map(Tokenizer.count_tokens) > self.config.min_lead_tokens]

    def _filter_by_max_lead_sentences(self, df):
        return df[df['lead'].parallel_map(Tokenizer.count_sentences) < self.config.max_lead_sentences]
