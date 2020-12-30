import csv


class PopRawDataReader(object):
    """
    生の人口データファイルを読み込むクラス
    """

    def __init__(self, path):
        self.path = path
        self.pop_data = []
        self.read_data()

    def read_data(self):

        with open(self.path, "r", encoding="shift-jis") as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):

                # ヘッダ2行読み飛ばし
                if i <= 1:
                    continue

                # print(line)
                pop_data = PopRawData(line)
                self.pop_data.append(pop_data)

    def get_data(self):
        return self.pop_data


class PopRawData(object):
    """
    生の人口データ1行
    """

    def __init__(self, line):
        self.line = line
        self.key_code = line[0]
        self.pop = int(line[4])

    def get_key_code(self):
        return self.key_code

    def get_population(self):
        return self.pop
