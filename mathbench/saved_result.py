"""Store one replayable record for the best result of each task."""
import gzip
import json
from pathlib import Path
from tempfile import NamedTemporaryFile


_PREFIX = b'{\n  "result": '
_WITNESS = b'\n  "solution": '
_END = b'\n}\n'


def best_record_path(directory):
    path = Path(directory) / "result.json"
    compressed = path.with_suffix(".json.gz")
    return compressed if not path.is_file() and compressed.is_file() else path


def read_best_record(path):
    contents = path.read_bytes()
    return json.loads(gzip.decompress(contents) if path.suffix == ".gz" else contents)


def extract_witness(contents):
    """Return the original witness bytes, including their JSON whitespace."""
    if contents.startswith(_PREFIX) and contents.endswith(_END):
        _, marker, witness = contents.partition(_WITNESS)
        if marker:
            return witness[:-len(_END)]
    return contents


def write_best_record(path, result, provenance, witness):
    # Embed the witness verbatim so the saved witness digest still applies.
    if not isinstance(json.loads(witness), dict):
        raise ValueError("The saved construction must be a JSON object")
    header = json.dumps(
        {"result": result, "provenance": provenance}, ensure_ascii=False, indent=2,
    ).encode("utf-8")
    contents = header[:-2] + b"," + _WITNESS + witness + _END
    if path.suffix == ".gz":
        contents = gzip.compress(contents, mtime=0)
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(contents)
            stream.close()
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
