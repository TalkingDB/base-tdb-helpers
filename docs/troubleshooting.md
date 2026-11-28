# Troubleshooting

[Docs home](README.md) › Troubleshooting

| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| Push refused: "Your pyproject.toml is out of sync with local repos" | The pre-push hook ran `make sync-dry-run MODE=git` and a pin differs from your sibling checkout's HEAD | Decide which is right. If the new commit should be pinned, run `make sync MODE=git`, review and commit. If not, check out the pinned commit in the sibling folder |
| `make sync` prints "local path missing" | The sibling folder named in [`git-packages.json`](../git-packages.json) does not exist | Clone the base repositories next to this one, or run `make clone` from [infra-tdb-platform](https://github.com/TalkingDB/infra-tdb-platform) |
| A pin moved to a commit that is not on `main` | `make sync MODE=git` pins to whatever your sibling folders have checked out | Check out `main` in the sibling folders and run it again |
| `make: command not found` or Bash errors on Windows | The Makefiles and hooks are Bash | Use [WSL](https://learn.microsoft.com/en-us/windows/wsl/about) Ubuntu, Git Bash or a dev container |
| `401 {"error_code": "UNAUTHORIZED", "message": "Invalid API key"}` | The key is unknown in `api_keys`, or the service reads a different `GRAPH_DB` file than the one the key was created in | Create a key through the owning service (for TTT, `POST /auth/api-keys`) and make sure both use the same `GRAPH_DB` |
| `401 Invalid token` on a [JWT](https://jwt.io/introduction) route | Token expired, signed with another `JWT_SECRET_KEY`, or missing `sub` | Log in again; make sure every instance shares the same `JWT_SECRET_KEY` |
| Creating a token fails with a key error | `JWT_SECRET_KEY` is not set | Set it in the service environment |
| `413 Request Entity Too Large` | The upload is larger than the cap for its type (PDF 100 MB, DOCX 50 MB by default) | Raise `TDB_MAX_PDF_FILE_SIZE_MB` or `TDB_MAX_DOCX_FILE_SIZE_MB`, or split the file |
| `415 Unsupported Media Type` | Only PDF and DOCX are accepted | Convert the file first |
| `503` with a `Retry-After` header during upload | The spool folder has less free space than `TDB_MIN_FREE_SPOOL_MB` | Free disk space under `TDB_SPOOL_DIR` or point it at a larger disk |
| A file lands under the `localhost` folder in production | The request host did not match a release channel pattern, so the default was used | Check the `Host` or `X-Forwarded-Host` header your proxy sends |
| A graph edit is not visible for a few minutes | The graph cache keeps a loaded graph for up to 5 minutes after last use | Call `invalidate(graph_id)` after writing |

## Further reading

- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [HTTP 413](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/413) and [HTTP 415](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/415)

---

**Related:** [Architecture](architecture.md) · [Usage and examples](usage-and-examples.md) · [README](../README.md)
