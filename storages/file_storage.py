import os
import re
import ast

from storages.storage import Storage


class FileStorage(Storage):

    def __init__(self, file_name):
        self.file_name = file_name

    def read_data(self):
        if not os.path.exists(self.file_name):
            raise StopIteration

        data = []

        with open(self.file_name) as f:
            for line in f:
                data.append(ast.literal_eval(re.search(r'\{.*\}', line.strip()).group(0)))

        return data

    def write_data(self, data_array):
        """
        :param data_array: collection of strings that
        should be written as lines
        """
        with open(self.file_name, 'w') as f:
            data_array = data_array.replace('},', '},\n')
            f.write(data_array)

    def append_data(self, data):
        """
        :param data: string
        """
        with open(self.file_name, 'a') as f:
            for line in data:
                if line.endswith('\n'):
                    f.write(line)
                else:
                    f.write(line + '\n')
