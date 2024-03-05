from keypoint_detector_service import KeypointDetectorService


class WorkpieceModel():

    def __init__(self, workpiece_processing, workpiece_width, workpiece_height):
        self.workpiece_processing = workpiece_processing
        self.workpiece_width = workpiece_width
        self.workpiece_height = workpiece_height
        self.heat_map_model = None

    def compute_heat_map(self, solver_name):
        self.heat_map_model = KeypointDetectorService(self.workpiece_processing, self.workpiece_width, self.workpiece_height)
        self.heat_map_model.instantiate_model(solver_name)
        return self.heat_map_model.resolve_instance()["workpiece_heat_map"]



