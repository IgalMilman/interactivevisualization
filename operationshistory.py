import baseoperationclass
import json

OPERATION_NAME_STRING = "operationname"
PARAMETERS_STRING = "parameters"


class OperationHistory:

    def __init__(self):
        self.stack = []
        pass

    def append(self, dataset, operation):
        self.stack.append(operation)
        return True

    def get_previous_step(self, step_number=1):
        if len(self.stack) < step_number:
            raise ValueError('Step number is larger than the number of operations saved', step_number, len(self.stack))
        if step_number < 1:
            raise ValueError('Step number must be greater or equal to 1')

        return self.stack[len(self.stack) - step_number]

    def save_to_json(self):
        list_of_operations = []

        for i in range(len(self.stack)):
            list_of_operations.append({OPERATION_NAME_STRING: self.stack[i].operation_name,
                                       PARAMETERS_STRING: json.dumps(self.stack[i].save_parameters())})

        return json.dumps(list_of_operations)

    def load_from_json(self, json_string):
        list_of_operations = json.loads(json_string)

        for i in range(len(list_of_operations)):
            operation_class = baseoperationclass.get_operation_class(list_of_operations[i][OPERATION_NAME_STRING])
            if operation_class is None:
                print("Operation " + list_of_operations[i][OPERATION_NAME_STRING] +
                      " is not available. Please, check if all the operations were imported correctly")
            else:
                operation = operation_class()
                if operation.load_parameters(json.loads(list_of_operations[i][PARAMETERS_STRING])):
                    self.stack.append(operation)
                else:
                    print("Failed to load parameters", list_of_operations[i][PARAMETERS_STRING])

        return True
