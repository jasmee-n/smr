# smrstate conversion to json string for downstream use
import json


def convert_smr_state_to_json(value):
    if hasattr(
        value,
        'model_dump_json'
    ):
        return value.model_dump_json(
            indent = 2
        )

    return json.dumps(
        value,
        indent = 2,
        ensure_ascii = False,
        default = str
    )