import logging
import pandas as pd


logger = logging.getLogger(__name__)
TABLE_FORMAT_FILE = 'data.csv'


class Transformer(object):
    def transform(self, data):
        logger.info("read data")
        df = pd.DataFrame(data)

        logger.info("save to csv")
        df.to_csv(TABLE_FORMAT_FILE, sep=',', encoding='utf-8', index=False)