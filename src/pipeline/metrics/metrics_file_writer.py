import hashlib
import json
import os
from typing import Dict, Any

from src.pipeline.pipe_filter.pipe import BaseFilter


class MetricsFileWriterFilter(BaseFilter):
    base_folder = 'output/metrics'

    def dict_hash(self, dictionary: Dict[str, Any]) -> str:
        """MD5 hash of a dictionary."""
        dhash = hashlib.md5()

        encoded = json.dumps(dictionary, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.hexdigest()

    def execute(self):
        os.makedirs(self.base_folder, exist_ok=True)
        file_name = self.dict_hash(self.input) + '.json'

        with open(self.base_folder + '/' + file_name, 'w') as metrics_file:
            json.dump(self.input, metrics_file, indent=4)

        self.output = self.input
