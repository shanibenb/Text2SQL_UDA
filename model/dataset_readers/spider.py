import json
import logging
import os
from typing import List, Dict

import dill
from allennlp.common.checks import ConfigurationError
from allennlp.data import DatasetReader, Tokenizer, TokenIndexer, Field, Instance
from allennlp.data.fields import TextField, ProductionRuleField, ListField, IndexField, MetadataField
from allennlp.data.token_indexers import SingleIdTokenIndexer
from allennlp.data.tokenizers import WordTokenizer
from allennlp.data.tokenizers.word_splitter import SpacyWordSplitter
from overrides import overrides
from spacy.symbols import ORTH, LEMMA

from dataset_readers.dataset_util.spider_utils import fix_number_value, disambiguate_items
from dataset_readers.fields.knowledge_graph_field import SpiderKnowledgeGraphField
from semparse.contexts.spider_db_context import SpiderDBContext
from semparse.worlds.spider_world import SpiderWorld

logger = logging.getLogger(__name__)


@DatasetReader.register("spider")
class SpiderDatasetReader(DatasetReader):
    def __init__(self,
                 lazy: bool = False,
                 question_token_indexers: Dict[str, TokenIndexer] = None,
                 keep_if_unparsable: bool = True,
                 tables_file: str = None,
                 dataset_path: str = 'dataset/database',
                 load_cache: bool = True,
                 save_cache: bool = True,
                 loading_limit = -1):
        super().__init__(lazy=lazy)

        # default spacy tokenizer splits the common token 'id' to ['i', 'd'], we here write a manual fix for that
        spacy_tokenizer = SpacyWordSplitter(pos_tags=True)
        spacy_tokenizer.spacy.tokenizer.add_special_case(u'id', [{ORTH: u'id', LEMMA: u'id'}])
        self._tokenizer = WordTokenizer(spacy_tokenizer)

        self._utterance_token_indexers = question_token_indexers or {'tokens': SingleIdTokenIndexer()}
        self._keep_if_unparsable = keep_if_unparsable

        self._tables_file = tables_file
        self._dataset_path = dataset_path

        self._load_cache = load_cache
        self._save_cache = save_cache
        self._loading_limit = loading_limit

    @overrides
    def _read(self, file_path: str):
        if not file_path.endswith('.json'):
            raise ConfigurationError(f"Don't know how to read filetype of {file_path}")

        cache_dir = os.path.join('cache', file_path.split("/")[-1])

        if self._load_cache:
            logger.info(f'Trying to load cache from {cache_dir}')
        if self._save_cache:
            os.makedirs(cache_dir, exist_ok=True)

        cnt = 0
        with open(file_path, "r") as data_file:
            json_obj = json.load(data_file)
            for total_cnt, ex in enumerate(json_obj):
                cache_filename = f'instance-{total_cnt}.pt'
                # print("debug " , total_cnt)
                cache_filepath = os.path.join(cache_dir, cache_filename)
                if self._loading_limit == cnt:
                    break

                if self._load_cache:
                    try:
                        ins = dill.load(open(cache_filepath, 'rb'))
                        if ins is None and not self._keep_if_unparsable:
                            # skip unparsed examples
                            continue
                        yield ins
                        cnt += 1
                    except Exception as e:
                        # could not load from cache - keep loading without cache
                        pass