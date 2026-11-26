# Usage and examples

[Docs home](README.md) › Usage and examples

Recipes for the helpers people reach for most. The architecture behind them is in [architecture.md](architecture.md).

## Point a repository at your local checkouts, then back at GitHub

From any TalkingDB repository that has a `Makefile` (this one, every `package-*` and `module-*`):

```bash
make sync MODE=local          # edit base-tdb-* side by side
# ... develop and test ...
make sync-dry-run MODE=git    # see which pins would move
make sync MODE=git            # pin to the HEAD of each sibling checkout
git diff pyproject.toml       # review the pin bump before committing
```

A real dry run from this repository on 25 November 2026, with `../base-tdb-models` checked out at its `main` (`2bfc4a3`), printed:

```text
→ talkingdb-models: would update to rev=2bfc4a3ce63a900de190125a6c64e0cf8738ded6

⚠ Updates would be applied, but --dry-run enabled
- talkingdb-models = { git = "git+https://github.com/TalkingDB/base-tdb-models.git", rev = "3295d4073e179791cfbd042430824c1303ccba38" }
+ talkingdb-models = { git = "git+https://github.com/TalkingDB/base-tdb-models.git", rev = "2bfc4a3ce63a900de190125a6c64e0cf8738ded6" }
```

It exited with code 1. That is the signal the [pre-push hook](../git-hooks/pre-push) uses to stop a push whose pins do not match your local checkouts.

## Protect a FastAPI route with an API key

```python
from fastapi import Depends, FastAPI
from talkingdb.helpers.auth import verify_api_key

app = FastAPI()

@app.get("/v1/whoami")
def whoami(user_email: str = Depends(verify_api_key)):
    return {"user": user_email}
```

The key arrives as `Authorization: Bearer <key>`. It is checked against the hashed keys in the `api_keys` table of `GRAPH_DB`. A bad key gets `401` with `{"error_code": "UNAUTHORIZED", "message": "Invalid API key"}`.

## Issue and check a login token

```python
import os
os.environ.setdefault("JWT_SECRET_KEY", "change-me")   # set this in the environment, never in code

from talkingdb.helpers.jwt import create_access_token, get_current_user

token = create_access_token({"sub": "person@example.com"})
```

Protect a route with `Depends(get_current_user)`; it returns the `sub` claim (the email) or raises `401 Invalid token`. Tokens expire after `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` (60 by default).

## Run a job through its life

```python
from talkingdb.clients.sqlite import get_connection, GRAPH_DB
from talkingdb.helpers.job import store as job_store
from talkingdb.models.job.job import JobModel
from talkingdb.models.job.type import JobType
from talkingdb.models.job.state import JobState

conn = get_connection(GRAPH_DB)
job_store.init_db(conn)

job = JobModel.new(job_type=JobType.DOCUMENT, filename="report.pdf")
job_store.insert(conn, job)

job_store.request_cancel(conn, job.job_id)        # QUEUED becomes CANCELLED at once
print(job_store.get(conn, job.job_id).state)      # JobState.CANCELLED
```

For a job that is already running, `request_cancel` moves it to `CANCELLING` and the worker calls `finalize(...)`, which writes `CANCELLED` and clears any result. The full set of transitions is drawn in [base-tdb-models](https://github.com/TalkingDB/base-tdb-models/blob/main/docs/architecture.md#job-lifecycle).

## Store an original file by its content hash

```python
from talkingdb.helpers import file_store

file_hash = file_store.compute_sha256("report.pdf")
if file_store.is_configured():
    file_store.upload_file("localhost", file_hash, "report.pdf")
    url = file_store.get_presigned_url("localhost", file_hash)
```

The first argument is the **release channel**, a folder name in the bucket. Inside a request, get it with `get_release_channel(request)`, which reads the host name and falls back to `localhost`.

## Check an upload before reading it

```python
from fastapi import UploadFile
from talkingdb.helpers.validation import validate_file_type, supported_upload_types

print(supported_upload_types())   # PDF up to 100 MB, DOCX up to 50 MB by default
```

`validate_file_type` raises `415` for anything other than PDF or DOCX. `assert_content_length_within_cap` raises `413` when the request is larger than the cap for its type. Raise the caps with `TDB_MAX_PDF_FILE_SIZE_MB` and `TDB_MAX_DOCX_FILE_SIZE_MB`.

---

**Related:** [Architecture](architecture.md) · [Troubleshooting](troubleshooting.md) · [README](../README.md)
