from . import baseoperationclass
import pandas as pd


DESCRIPTION = ['Minimum', '25% quantile', '50% quantile', '75% quantile', 'Maximum', 'Sum', 'Standard deviation']


class BasicStatistics(baseoperationclass.BaseOperationClass):
    _operation_name = "BasicStats"

    def __init__(self):
        self.results = None

    def process_data(self, dataset):
        self.results = [dataset.min(), dataset.quantile(0.25), dataset.quantile(0.5), dataset.quantile(0.75),
                        dataset.max(), dataset.sum(), dataset.std()]
        return self.results

    def save_results(self):
        dict = {}
        for i in range(len(self.results)):
            dict[i] = self.results[i].to_json()
        return {'results': dict}

    def load_results(self, results_dict):
        if 'results' in results_dict and results_dict['results'] is not None:
            try:
                self.results = [pd.read_json(results_dict['results'][0], typ='series'),
                                pd.read_json(results_dict['results'][1], typ='series'),
                                pd.read_json(results_dict['results'][2], typ='series'),
                                pd.read_json(results_dict['results'][3], typ='series'),
                                pd.read_json(results_dict['results'][4], typ='series'),
                                pd.read_json(results_dict['results'][5], typ='series'),
                                pd.read_json(results_dict['results'][6], typ='series')]
            except:
                self.results = [pd.read_json(results_dict['results']['0'], typ='series'),
                                pd.read_json(results_dict['results']['1'], typ='series'),
                                pd.read_json(results_dict['results']['2'], typ='series'),
                                pd.read_json(results_dict['results']['3'], typ='series'),
                                pd.read_json(results_dict['results']['4'], typ='series'),
                                pd.read_json(results_dict['results']['5'], typ='series'),
                                pd.read_json(results_dict['results']['6'], typ='series')]
        return True


try:
    baseoperationclass.register(BasicStatistics)
except ValueError as error:
    print(repr(error))