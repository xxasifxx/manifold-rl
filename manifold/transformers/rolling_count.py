import uuid
import creme
import random
import creme.stats
from creme import utils
from manifold.base_types import Transformer
from manifold.creme_ext import HotStreak, RollingDifference, RollingCount


class SmoothRollingDifferenceTransformer(Transformer):
    def __init__(self, window=20, **kwargs) -> None:
        super().__init__()

        
        
        self.transformed = {}
        # This is basically a pipeline. We can put pipelines inside of it to
        self.proceedure = [
            {"name": "rolling_count", "transformation": RollingCount(window_size=window), "is_xy": False},
            {"name": "rolling_diff", "transformation": RollingDifference(window_size=window, ideal={0:6, 1:3, 2:2}), "is_xy": False}    
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




if __name__ == "__main__":
    smooth_jazz = HotStreak(0.2, is_range=True)
    model_id = uuid.uuid4().hex
    while True:
        action = random.randint(0, 2)
        print(smooth_jazz.update(random.normalvariate(1, 0.2)).get())