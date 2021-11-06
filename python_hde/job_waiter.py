from abc import ABC, abstractmethod
import time
from typing import Optional

from python_hde.model.filter import FilterElement, FilterCondition
from python_hde.model.job import Job
from python_hde.model.sort import SortConfiguration
from python_hde.paginator import HostingDePaginator


class AsynchronousClient(ABC):

    @abstractmethod
    def jobs_find(self,
                  limit: Optional[int] = None,
                  filter: Optional[FilterElement] = None,
                  sort: Optional[SortConfiguration] = None,
                  *args, **kwargs) -> HostingDePaginator[Job]:
        """
        Retrieves a list of Job objects from the generic filtering and sorting API.

        :param limit: The limit of objects to retrieve per call. If not set, defaults to 25.
        :param filter: A filter that is applied to the query
        :param sort: Configuration how results are sorted.
        :return: An iterator that yields ZoneConfig objects.
        """
        pass


class JobWaiter:

    def __init__(self, service: AsynchronousClient, id: str):
        self.service = service
        self.id = id

    def wait(self):
        while True:
            jobs = self.service.jobs_find(
                filter=FilterCondition('jobObjectId').eq(self.id)
                       & FilterCondition('jobStatus').ne('successful')
                       & FilterCondition('jobStatus').ne('failed')
                       & FilterCondition('jobStatus').ne('canceled')
            ).fetchall()

            if len(jobs) == 0:
                break

            time.sleep(1)
