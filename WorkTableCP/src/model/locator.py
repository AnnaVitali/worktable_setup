import os
from minizinc import Model, Solver, Instance

SOLVER_NAME = "chuffed"

class Locator():

    def __init__(self, capacity, max_resources, number_of_object, object_sizes, position_profit):
        self.capacity = capacity
        self.max_resources = max_resources
        self.number_of_object = number_of_object
        self.object_sizes = object_sizes
        self.position_profit = position_profit
        self.instance = None
        self.model = None
        self.solver = None

    def __create_data_file_minizinc(self):
        file_name = os.path.join('../resources/minizinc',"position_profit_maximization.dzn")
        file_dzn = open(file_name, "w")
        file_dzn.write(f"capacity={self.capacity}; \n"
                       f"max_resources={self.max_resources}; \n"
                       f"max_positions={len(self.position_profit)}; \n"
                       f"object_size_in_x={self.object_sizes}; \n"
                       f"position_profit={self.position_profit}; \n")
        file_dzn.close()

    def resolve_instance(self):
        self.__create_data_file_minizinc()
        solver = Solver.lookup(SOLVER_NAME)
        position_profit = Model("../resources/minizinc/position_profit_maximization.mzn")
        position_profit.add_file("../resources/minizinc/position_profit_maximization.dzn")
        instance = Instance(solver, position_profit)
        print("Minizinc solving...")
        solution = instance.solve()
        print(solution)
        if(solution["objective"] != 0): #for chuffed values
            result = solution["object_x"]
        else:
            result = []

        return [value - 1 for value in result if value != -1]