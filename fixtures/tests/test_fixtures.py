import json
import os

from fixtures.app.fixtures_tut import save_dict


def test_save_dict(tmpdir, capsys):
    filepath = os.path.join(tmpdir, "test.json")
    message = {"a": 1, "b": 2}

    save_dict(message, filepath)
    assert json.load(open(filepath, 'r')) == message
    assert capsys.readouterr().out == "saved\n"
