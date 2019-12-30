from loguru import logger
from abc import ABC, abstractmethod
from typing import List
import collections

pearson_window = 4
person_range = list(range(pearson_window))


class Transformer(ABC):
    def __init__(self, **kwargs) -> None:
        self.transformed = {}
        self.proceedure = []


    def _procedure_check(self):
        """ Raises an exception if there's an error in procedure. """
        if len(self.proceedure) == 0: raise AttributeError("There are no procedures components")
        for item in self.proceedure:
            if "name" not in item:
                raise AttributeError("Name not in procedure item")
            if "transformation" not in item:
                raise AttributeError("Transormation missing")

    @abstractmethod
    def process(self, variable):
        raise NotImplementedError

    def _update_procedure(self, procedure, x, y, is_xy=False):
        if is_xy:
            procedure.update(x, y)
        else:
            procedure.update(y)
        
        return procedure


    def _all_procedures(self, variable, transformed_data, transformation_id:str):
        for index, pro in enumerate(self.proceedure):
            current_name = pro.get("name")
            current_index = transformed_data.get('index')

            is_xy = pro.get("is_xy", False)
            procedure = transformed_data["transformers"].get(current_name, pro.get("transformation"))
            history = transformed_data['history'].get(current_name, [])


            if index != 0:
                last_step = self.proceedure[index-1]
                last_name = last_step.get("name")
                
                last_history = transformed_data['history'].get(last_name, [])
                
                if len(last_history) != 0:
                    last_history_item = last_history[-1]
                    procedure = self._update_procedure(procedure, current_index, last_history_item, is_xy=is_xy)
                    
            else:
                name = pro.get("name")
                history = transformed_data['history'].get(name, [])
                
                procedure = self._update_procedure(procedure, current_index, variable, is_xy=is_xy)

            history.append(procedure.get())
            transformed_data['history'][current_name] = history
            transformed_data["transformers"][current_name] = procedure
            transformed_data["index"] += 1
            self.transformed[f"{transformation_id}"] = transformed_data
    
    @abstractmethod
    def step(self, variable) -> List:
        raise NotImplementedError