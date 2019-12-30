import uuid
import creme
import creme.stats
from manifold.base_types import Transformer


class SmoothPearsonTransformer(Transformer):
    def __init__(self, window=20, **kwargs) -> None:
        super().__init__()

        rolling_window = kwargs.get("mean_window", None)
        if rolling_window is None:
            rolling_window = window
        
        pearson_window = kwargs.get("pearson_window", None)
        if pearson_window is None:
            pearson_window = window
        
        self.transformed = {}
        # This is basically a pipeline. We can put pipelines inside of it to
        self.proceedure = [
            {"name": "rolling_mean", "transformation": creme.stats.RollingMean(window_size=rolling_window), "is_xy": False},
            {"name": "pearson", "transformation": creme.stats.AutoCorrelation(lag=pearson_window), "is_xy": False}    
        ]
        self._procedure_check()

        

    def process(self, variable, transformation_id:str):
        transformed_data = self.transformed.get(transformation_id, {"transformers": {}, "index": 0, "history": {}})
        self._all_procedures(variable, transformed_data, transformation_id)

    
    def _get_final_transformed(self, transformation_id):
        if len(self.proceedure) == 0: raise AttributeError("You don't have any proceedure steps")
        transformed = self.transformed.get(f"{transformation_id}", {})
        if len(transformed.keys()) == 0:
            return 0.0
        last_step = self.proceedure[-1]
        last_name = last_step.get("name")
        last_item = transformed["transformers"].get(last_name)
        return last_item.get()


    def step(self, variable, model_id=uuid.uuid4().hex):
        self.process(variable, model_id)
        return self._get_final_transformed(model_id)


