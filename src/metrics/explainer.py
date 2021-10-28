import re
from typing import Union
from numpy import ndarray

from aif360.explainers import MetricTextExplainer


class MetricAdditions:
    def explain(self,
                disp: bool = True) -> Union[None, str]:
        """Explain everything available for the given metric."""

        # Find intersecting methods/attributes between MetricTextExplainer and provided metric.
        inter = set(dir(self)).intersection(set(dir(self.metric)))

        # Ignore private and dunder methods
        metric_methods = [getattr(self, c) for c in inter if c.startswith('_') < 1]

        # Call methods, join to new lines
        s = "\n".join([f() for f in metric_methods if callable(f)])

        if disp:
            print(s)
        else:
            return s

    def explain_dict(self):
        # Find intersecting methods/attributes between MetricTextExplainer and provided metric.
        inter = set(dir(self)).intersection(set(dir(self.metric)))

        # Ignore private and dunder methods
        metric_methods = [getattr(self.metric, c) for c in inter if c.startswith('_') < 1]
        explain_methods = [getattr(self, c) for c in inter if c.startswith('_') < 1]

        explain_dict = {'metrics': {}}

        for i in range(len(metric_methods)):
            metric_explanation = re.split('\((.*)\):|:', explain_methods[i]())
            value = metric_methods[i]()
            value = list(value) if type(value) == ndarray else value

            method = {
                'name': metric_explanation[0].strip(),
                'value': value,
                'explanation': metric_explanation[1] if len(metric_explanation) == 3 else None
            }

            explain_dict['metrics'][metric_methods[i].__name__] = method

        return explain_dict


class EnhancedMetricTextExplainer(MetricTextExplainer, MetricAdditions):
    """Combine explainer and .explain."""
    pass