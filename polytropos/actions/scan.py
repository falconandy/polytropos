import os
import json
from abc import abstractmethod
from typing import Dict, Optional, Any, Iterable, Tuple
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from polytropos.ontology.composite import Composite

from polytropos.ontology.schema import Schema

from polytropos.actions.step import Step
from polytropos.ontology.task.paths import TaskPathLocator
from polytropos.util.loader import load
from polytropos.util.config import MAX_WORKERS


class Scan(Step):
    schema: Schema

    """Scan iterates through all of the composites in the task pipeline twice: once to gather global information, and
    then a second time to make alterations to the composites on the basis of the globally gathered information. In
    between, an arbitrary analysis may be performed on the basis of the global information. Example use cases include
    assigning ranks, or computing a property relative to peers sharing some other property."""
    @classmethod
    # def build(cls, path_locator: TaskPathLocator, schema: Schema, name: str, subjects: Dict):
    def build(cls, schema: Schema, name: str, subjects: Dict):
        scans = load(cls)
        variables = {
            var_name: schema.get(var_id)
            for var_name, var_id in subjects.items()
        }
        return scans[name](schema=schema, **variables)

    @abstractmethod
    def extract(self, composite: Composite) -> Optional[Any]:
        """Gather the information to be used in the analysis."""
        pass

    @abstractmethod
    def analyze(self, extracts: Iterable[Tuple[str, Any]]) -> None:
        """Collect, process, and store the global information provided from each composite during the scan() step.
        :param extracts: Tuple of (composite id, whatever is returned by extract)"""
        pass

    @abstractmethod
    def alter(self, composite_id: str, composite: Composite) -> None:
        """Alter the supplied composite in place. The resulting composite will then overwrite the original, completing
        the alteration."""
        pass

    def process_composite(self, origin_dir: str, filename: str):
        with open(os.path.join(origin_dir, filename), 'r') as origin_file:
            content: Dict = json.load(origin_file)
            composite: Composite = Composite(self.schema, content)
            return filename, self.extract(composite)

    def alter_and_write_composite(self, origin_dir, target_dir, filename):
        with open(os.path.join(origin_dir, filename), 'r') as origin_file:
            content: Dict = json.load(origin_file)
            composite: Composite = Composite(self.schema, content)
            self.alter(filename, composite)
        with open(os.path.join(target_dir, filename), 'w') as target_file:
            json.dump(composite.content, target_file)

    def __call__(self, origin_dir: str, target_dir: str):
        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            self.analyze(
                executor.map(
                    partial(self.process_composite, origin_dir),
                    os.listdir(origin_dir)
                )
            )
        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            executor.map(
                partial(self.alter_and_write_composite, origin_dir, target_dir),
                os.listdir(origin_dir)
            )
