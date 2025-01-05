from pm4py.objects.dcr.hierarchical.obj import HierarchicalDcrGraph
from typing import Set, Dict, Union
from collections import defaultdict


class MultiInstanceDcrGraph(HierarchicalDcrGraph):
    
    def __init__(self, template=None):
        super().__init__(template)
        self.__spawnOf = {} if template is None else template['spawnOf']
        self.__multipleInstances = defaultdict(lambda: {'elements': set(), 'occurrences': 0}) if template is None else template['multipleInstances']



    def obj_to_template(self):
        res = super().obj_to_template()
        res['spawnOf'] = self.__spawnOf
        res['multipleInstances'] = self.__multipleInstances
        return res


    @property
    def spawn(self) -> Dict[str, Set[str]]:
        return self.__spawnOf

    @spawn.setter
    def spawn(self, value: Dict[str, Set[str]]):
        self.__spawnOf = value

    @property
    def multipleInstances(self) -> Dict[str, Dict[str, Union[Set[str], int]]]:
        return self.__multipleInstances
    
    @multipleInstances.setter
    def multipleInstances(self, value: Dict[str, Dict[str, Union[Set[str], int]]]):
        self.__multipleInstances = value

