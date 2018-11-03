class BaseOperationClass:
    _operations_dictionary = {}
    _operation_name = 'Operation basis'

    def _get_name(self):
        return self._operation_name

    operation_name = property(_get_name)

    def __init__(self):
        pass

    def save_to_queue(self, operation_queue, dataset):
        operation_queue.append(dataset, self)
        return True

    #All next functions are overloaded in classes
    def process_data(self, dataset):
        return None

    #Parameters is a collection of parameters
    def load_parameters(self, parameters):
        return True

    def set_parameters(self):
        return True

    def save_parameters(self):
        return "{}"


def register(class_to_register):
    if class_to_register._operation_name in BaseOperationClass._operations_dictionary:
        raise ValueError('This class already registered', class_to_register, class_to_register._operation_name)
    BaseOperationClass._operations_dictionary[class_to_register._operation_name] = class_to_register
    return True


def get_operation_class(operation_name):
    if operation_name in BaseOperationClass._operations_dictionary:
        return BaseOperationClass._operations_dictionary[operation_name]
    else:
        return None


try:
    register(BaseOperationClass)
except ValueError as error:
    print(repr(error))
