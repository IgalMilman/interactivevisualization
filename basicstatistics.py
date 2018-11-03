import pandas as pd
import baseoperationclass


class BasicStatistics(baseoperationclass.BaseOperationClass):
    _operation_name = "BasicStats"

    def __init__(self):
        pass

    def process_data(self, dataset):
        return [dataset.min(), dataset.quantile(0.25), dataset.quantile(0.5), dataset.quantile(0.75), dataset.max(),
                dataset.sum(), dataset.std()]


try:
    baseoperationclass.register(BasicStatistics)
except ValueError as error:
    print(repr(error))
