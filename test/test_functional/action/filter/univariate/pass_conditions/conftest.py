from collections import Callable, OrderedDict
from typing import Dict

import pytest

from polytropos.ontology.composite import Composite

from polytropos.ontology.schema import Schema
from polytropos.ontology.track import Track

@pytest.fixture()
def make_track() -> Callable:
    def _make_track(prefix: str) -> Track:
        key: str = "%s_text" % prefix
        spec: Dict = {
            key: {
                "name": key,
                "data_type": "Text",
                "sort_order": 0
            }
        }
        return Track(spec, None, prefix)
    return _make_track

@pytest.fixture()
def schema(make_track) -> Schema:
    immutable: Track = make_track("i")
    temporal: Track = make_track("t")
    return Schema(temporal, immutable)

@pytest.fixture()
def always_composite(schema) -> Composite:
    content: Dict = {
        "period_1": {
            "t_text": "A"
        },
        "period_2": {
            "t_text": "B"
        },
        "period_3": {
            "t_text": "C"
        }
    }
    return Composite(schema, content, composite_id="always")

@pytest.fixture()
def immutable_only_composite(schema) -> Composite:
    content: Dict = {
        "immutable": {
            "i_text": "D"
        }
    }
    return Composite(schema, content, composite_id="immutable_only")

@pytest.fixture()
def never_composite(schema) -> Composite:
    content: Dict = {
        "period_1": {},
        "period_2": {},
        "period_3": {},
        "immutable": {
            "i_text": "D"
        }
    }
    return Composite(schema, content, composite_id="never")

@pytest.fixture()
def middle_composite(schema) -> Composite:
    content: Dict = {
        "period_1": {},
        "period_2": {
            "t_text": "B"
        },
        "period_3": {}
    }
    return Composite(schema, content, composite_id="middle")

@pytest.fixture()
def earliest_composite(schema) -> Composite:
    content: Dict = {
        "period_1": {
            "t_text": "A"
        },
        "period_2": {},
        "period_3": {}
    }
    return Composite(schema, content, composite_id="earliest")

@pytest.fixture()
def latest_composite(schema) -> Composite:
    content: Dict = {
        "period_1": {},
        "period_2": {},
        "period_3": {
            "t_text": "C"
        }
    }
    return Composite(schema, content, composite_id="latest")

@pytest.fixture()
def composites(always_composite, immutable_only_composite, never_composite, middle_composite, earliest_composite,
               latest_composite) -> Dict[str, Composite]:

    return OrderedDict([
        ("always", always_composite),
        ("immutable_only", immutable_only_composite),
        ("never", never_composite),
        ("middle", middle_composite),
        ("earliest", earliest_composite),
        ("latest", latest_composite)
    ])
