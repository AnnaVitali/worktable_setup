from minizinc import Instance, Model, Solver

MODEL_NAME = './minizinc/workpiece_heat_map.mzn'

class KeypointDetectorService():

    def __init__(self, workpiece_processing, workpiece_width, workpiece_height):
        self.workpiece_processing = workpiece_processing
        self.workpiece_width = workpiece_width
        self.workpiece_height = workpiece_height
        self.instance = None
        self.model = None
        self.solver = None

    def __instantiate_parameter(self):
        self.instance["workpiece_processing"] = self.workpiece_processing
        self.instance["workpiece_width"] = self.workpiece_width
        self.instance["workpiece_height"] = self.workpiece_height

    def instantiate_model(self, solver_name):
        self.solver = Solver.lookup(solver_name)
        self.model = Model(MODEL_NAME)
        self.instance = Instance(self.solver, self.model)
        self.__instantiate_parameter()

    def resolve_instance(self):
        return self.instance.solve()