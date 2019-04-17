import json
from abc import ABC, abstractmethod
from typing import List

from grafanalib._gen import DashboardEncoder
from grafana_api.grafana_face import GrafanaFace
from grafana_api.api.dashboard import Dashboard as ApiDashboard
from grafanalib.core import *

AUTH = ('admin', '4Hh4eFZykqTq9weWnuwuWoweiTUIz5JuVNTZCoZc')
HOST = 'grafana.default.svc.cluster.local'
grafana_face = GrafanaFace(auth=AUTH, host=HOST)
api_dashboard = ApiDashboard(grafana_face.api)

class Selector(dict):

    @property
    def selector(self) -> str:
        kv = ','.join(self._dump())
        return f"{{{kv}}}"

    def _dump(self) -> List[str]:
        return [f'{key}="{value}"' for key, value in self.items()]


class PrometheusHistogram:

    def __init__(self, prefix: str) -> None:
        self._prefix = prefix

    @property
    def prefix(self):
        return self._prefix

    @property
    def sum(self) -> str:
        return f"{self.prefix}_sum"

    @property
    def count(self) -> str:
        return f"{self.prefix}_count"

    @property
    def bucket(self) -> str:
        return f"{self.prefix}_bucket"

    @property
    def created(self) -> str:
        return f"{self.prefix}_created"


class BasePrometheusGraph(ABC):

    def __init__(self, data_source_name: str) -> None:
        self._data_source = data_source_name

    @property
    def data_source(self) -> str:
        return self._data_source

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def graph(self) -> Graph:
        pass


class RateAllRequestsGraph(BasePrometheusGraph):

    def __init__(self, data_source_name: str) -> None:
        super().__init__(data_source_name)

    @property
    def title(self):
        return 'Rate all requests'

    @property
    def graph(self) -> Graph:
        return Graph(
            title=self.title,
            dataSource=self.data_source,
            targets=[
                Target(
                    expr=self.__expr_rate_all(self.selector.selector, '5m'),
                    refId='A',
                ),
            ],
        )

    @property
    def selector(self) -> Selector:
        return Selector({
            'app': "ctc-billing-api"
        })

    def __expr_rate_all(self, selector: str, measured_time: str) -> str:
        histogram = PrometheusHistogram('request_latency_seconds')
        new = f"sum(rate({histogram.sum}{selector}[{measured_time}])) / sum(rate({histogram.count}{selector}[{measured_time}]))"
        return new
