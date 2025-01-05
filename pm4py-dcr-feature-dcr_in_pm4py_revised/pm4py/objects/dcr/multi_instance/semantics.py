from typing import Set

from pm4py.objects.dcr.semantics import DcrSemantics

class MultiInstanceSemantics(DcrSemantics):
    """
    Execution semantics for MultiInstanceDcrGraph, supporting dynamic event spawning.
    """
    @classmethod

    def execute(cls, graph, event):

        if event in graph.spawn:#e.g. A
            for s_prime in graph.spawn[event]:#e.g. P
                graph.multipleInstances[s_prime]['occurrences'] += 1
                for sub_events in graph.subprocesses[s_prime]:#e.g. B, C
                    graph.multipleInstances[s_prime]['elements'].add(sub_events)
                    #crete new event, give same label but different name
                    name = f"{sub_events}:{s_prime}{graph.multipleInstances[s_prime]['occurrences']}"
                    label = graph.label_map[sub_events]
                    graph.label_map[name] = label
                    graph.events.add(name)
                    graph.marking.included.add(name)
                    #propagate relations on same label
                        
                    if graph.label_map[name] in graph.responses.keys():
                        for relationWith in graph.responses[graph.label_map[name]]:
                            if any(relationWith in value for value in graph.subprocesses.values()):
                                graph.responses.setdefault(name, set()).add(f"{relationWith}:{s_prime}{graph.multipleInstances[s_prime]['occurrences']}")
                            else :
                                graph.responses.setdefault(name, set()).add(relationWith)

                    if any(graph.label_map[name] in value for value in graph.responses.values()):
                        key_with_match = next(
                            (key for key, value in graph.responses.items() if graph.label_map[name] in value),
                            None)

                        if key_with_match:
                            graph.responses[key_with_match].add(name)

                    if graph.label_map[name] in graph.conditions.keys():
                        for relationWith in graph.conditions[graph.label_map[name]]:
                            if any(relationWith in value for value in graph.subprocesses.values()):
                                graph.conditions.setdefault(name, set()).add(f"{relationWith}:{s_prime}{graph.multipleInstances[s_prime]['occurrences']}")
                            else :
                                graph.conditions.setdefault(name, set()).add(relationWith)
                    if graph.label_map[name] in graph.excludes.keys(): #e.g B in the ones that have an exclude relation
                        for relationWith in graph.excludes[graph.label_map[name]]:#e.g for elements that B has an exclude relation with
                            if any(relationWith in value for value in graph.subprocesses.values()):
                                graph.excludes.setdefault(name, set()).add(f"{relationWith}:{s_prime}{graph.multipleInstances[s_prime]['occurrences']}")
                            else :
                                graph.excludes.setdefault(name, set()).add(relationWith)#check for correctness
                    if graph.label_map[name] in graph.includes.keys():
                        for relationWith in graph.includes[graph.label_map[name]]:
                            if any(relationWith in value for value in graph.subprocesses.values()):
                                graph.includes.setdefault(name, set()).add(f"{relationWith}:{s_prime}{graph.multipleInstances[s_prime]['occurrences']}")
                            else :
                                graph.includes.setdefault(name, set()).add(relationWith)                                           

        
        return super().execute(graph, event)

