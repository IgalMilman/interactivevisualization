"""
Basic methods to react to different forms
"""
from core import calc
import io
import os.path
from datetime import datetime
import pandas as pd

SAVED_FILES_PATH = 'core/datafiles/'


def pandas_to_js_list(dataset):
    results = []
    for i in range(len(dataset.index)):
        results.append([[dataset.index[i]], [dataset.values[i].tolist()]])
    return results


def save_data(original_dataset, norm_dataset, op_history):
    filename = str(datetime.now().timestamp())
    while os.path.isfile(SAVED_FILES_PATH + filename):
        filename = filename + 't'
    file = open(SAVED_FILES_PATH + filename, "w")
    file.write(original_dataset.to_json(orient='table'))
    file.write('\n')
    file.write(norm_dataset.to_json(orient='table'))
    file.write('\n')
    file.write(op_history.save_to_json())
    file.close()
    return filename


def load_data(filename):
    if not os.path.isfile(SAVED_FILES_PATH + filename):
        return [None, None]
    file = open(SAVED_FILES_PATH + filename, "r")
    data = file.readline()
    original_dataset = pd.read_json(data, orient='table')
    data = file.readline()
    norm_dataset = pd.read_json(data, orient='table')
    data = file.readline()
    op_history = calc.operationshistory.OperationHistory()
    op_history.load_from_json(data)
    file.close()
    return [original_dataset, norm_dataset, op_history]


def prepare_basic(dataset, op_history):
    idx = [dataset.index.name]
    columns = dataset.columns.tolist()
    dim_names = idx + columns

    metrics = calc.basicstatistics.BasicStatistics()
    met_numb_or = metrics.process_data(dataset)
    met_numb = []
    for i in range(len(met_numb_or)):
        met_numb.append(met_numb_or[i].tolist())
    data = {
        'dataset': dataset,
        'dim_names': dim_names,
        'metrics': [calc.basicstatistics.DESCRIPTION, met_numb],
        'operation_history': op_history,
        # 'norm_dataset': norm_dataset,
        'norm_slice': pandas_to_js_list(dataset),
        'idx': idx,
    }
    return data


def new_csv_file_upload(request):
    if 'customFile' in request.FILES:
        dataset = calc.importcsv.import_csv_file(io.StringIO(request.FILES['customFile'].read().decode('utf-8')), True,
                                                 True)
    else:
        return {}
    dataset_slice = dataset
    columns = dataset_slice.columns.tolist()
    calc.importcsv.clean_dataset(dataset_slice)
    calc.importcsv.dropNA(dataset_slice)
    norm_slice = calc.importcsv.normalization(dataset_slice, columns)
    calc.importcsv.dropNA(norm_slice)

    op_history = calc.operationshistory.OperationHistory()
    metrics = calc.basicstatistics.BasicStatistics()
    metrics.process_data(norm_slice)
    op_history.append(norm_slice, metrics)
    data = prepare_basic(norm_slice, op_history)
    data['request'] = request
    data['saveid'] = save_data(dataset, norm_slice, op_history)
    return data


def clusterize(request):
    if 'fdid' not in request.POST:
        return {}
    original, dataset, op_history = load_data(request.POST['fdid'])
    if dataset is None:
        return {}

    # idx = [dataset.index.name]
    # columns = dataset.columns.tolist()
    # dim_names = idx + columns
    # metrics = calc.basicstatistics.BasicStatistics()
    # met_numb_or = metrics.process_data(dataset)
    # met_numb = []
    # for i in range(len(met_numb)):
    #     met_numb[i] = met_numb_or[i].tolist()
    #
    # data = {
    #     'dataset': dataset,
    #     # 'dataset': dataset,
    #     'request': request.POST,
    #     # 'new_file': True,
    #     'dim_names': dim_names,
    #     'metrics': [calc.basicstatistics.DESCRIPTION, met_numb],
    #     'operation_history': op_history,
    #     # 'norm_dataset': norm_dataset,
    #     'norm_slice': pandas_to_js_list(dataset),
    #     'idx': idx
    # }
    data = prepare_basic(dataset, op_history)
    data['request'] = request
    if 'algorithm' in request.POST:
        if request.POST['algorithm'] == 'KMeans' and 'numberofcl' in request.POST:
            operation = calc.KMeansClustering.KMeansClustering()
            operation.set_parameters(int(request.POST['numberofcl']))
            result = operation.process_data(dataset)
            if result is not None:
                op_history.append(dataset, operation)
                data['clusters'] = result.tolist()
                data['count_of_clusters'] = int(request.POST['numberofcl'])
                data['cluster_ready'] = True
            else:
                print('couldn\'t clusterize')
        else:
            print('unknown methond')
    else:
        print('No method')
    data['saveid'] = save_data(original, dataset, op_history)
    return data
