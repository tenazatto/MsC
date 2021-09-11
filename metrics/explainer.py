from typing import Union

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


class EnhancedMetricTextExplainer(MetricTextExplainer, MetricAdditions):
    """Combine explainer and .explain."""
    pass