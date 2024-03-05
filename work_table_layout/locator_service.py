from minizinc import Instance, Model, Solver

MODEL_NAME = './minizinc/position_profit_maximization.mzn'

class LocatorService():

    def __init__(self, capacity, max_resources, security_distance, number_of_object, object_sizes, object_profit):
        self.capacity = capacity
        self.max_resources = max_resources
        self.security_distance = security_distance
        self.number_of_object = number_of_object
        self.object_sizes = object_sizes
        self.object_profit = object_profit
        self.instance = None
        self.model = None
        self.solver = None

    def __instantiate_parameter(self):
        self.instance["capacity"] = self.capacity
        self.instance["max_resources"] = self.max_resources
        self.instance["security_distance"] = self.security_distance
        self.instance["number_of_object"] = self.number_of_object
        self.instance["object_sizes"] = self.object_sizes
        self.instance["object_profit"] = self.object_profit

    def instantiate_model(self, solver_name):
        self.solver = Solver.lookup(solver_name)
        self.model = Model(MODEL_NAME)
        self.instance = Instance(self.solver, self.model)
        self.__instantiate_parameter()

    def resolve_instance(self):
        return self.instance.solve()
