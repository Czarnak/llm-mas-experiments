# Review Checklist — Python Supplement

Load alongside `review-checklist.md` when `.py` files are present.
Same confidence filtering and verdict rules apply.

## Diagnostic Commands

```bash
mypy .                          # type errors — flag as HIGH
ruff check .                    # lint violations — flag by rule severity
bandit -r .                     # security issues — flag as CRITICAL/HIGH
pytest --tb=short               # test failures — flag as HIGH
pip-audit                       # known vulnerable dependencies — flag as CRITICAL
```

## CRITICAL — Security (Python-specific)

- **SQL via f-string or `%` formatting** — `f"SELECT ... {user_id}"` passed to `cursor.execute` → use parameterized queries (`cursor.execute("... %s", (user_id,))`)
- **`eval()` / `exec()` on user input** — arbitrary code execution; never use with untrusted data
- **`pickle.loads` on untrusted data** — arbitrary code execution during deserialization; use `json` or `msgpack`
- **`subprocess.shell=True` with user-controlled string** — shell injection; set `shell=False` and pass a list of args
- **`os.system(user_input)`** — same risk as above; use `subprocess.run([...], shell=False)`
- **`yaml.load` without `Loader=yaml.SafeLoader`** — arbitrary Python object deserialization

## CRITICAL — Error Handling (Python-specific)

- **Bare `except:`** — catches `SystemExit`, `KeyboardInterrupt`, and `GeneratorExit`; always specify exception types
- **`except Exception: pass`** — silently swallows all errors; at minimum log and re-raise

## HIGH — Type Safety

- **Missing type annotations on public functions** — degrades mypy coverage; annotate parameters and return type
- **`# type: ignore` without a comment** — suppresses a real error silently; add `# type: ignore[error-code]  # reason`
- **`isinstance(obj, type(other))` instead of `isinstance(obj, SomeClass)`** — fragile; use the class directly

## HIGH — Resource Management

- **File/socket/DB connection opened without `with`** — resource not closed on exception; always use context managers
- **`threading.Lock` acquired manually without `with`** — lock not released on exception; use `with lock:`
- **Generator not closed** — generators holding resources (e.g. file handles) must be `.close()`d or consumed fully; wrap in `contextlib.closing`

## HIGH — Concurrency

- **Shared mutable state across threads** — `list`, `dict`, `int` mutations are not atomic; use `threading.Lock` or `queue.Queue`
- **`multiprocessing.Pool` used without closing** — zombie processes; always use as a context manager or call `.terminate()`
- **Blocking call inside `asyncio` event loop** — `time.sleep`, `requests.get`, file I/O → use `asyncio.sleep`, `aiohttp`, `aiofiles`
- **`asyncio.create_task` result not stored** — task is garbage-collected and silently cancelled; keep a reference

## MEDIUM — Error Handling

- **Exception not chained with `raise ... from`** — original traceback is lost; use `raise NewError(...) from original_err`
- **Catching `Exception` too broadly** — catches unexpected errors; catch the narrowest type that makes sense
- **Custom exception not inheriting from `AppError` or a domain base** — hard to distinguish application errors from system errors in callers

## MEDIUM — Performance (Python-specific)

- **String concatenation in a loop** — `O(n²)` due to string immutability; use `"".join(parts)` or `io.StringIO`
- **List comprehension where a generator suffices** — `sum([x*x for x in range(1_000_000)])` builds a full list; use `sum(x*x for x in ...)`
- **`re.compile` called inside a loop** — recompiles the pattern on every call; compile once at module level
- **`in` check on a list in a hot path** — `O(n)` per check; convert to `set` for `O(1)` lookup

## MEDIUM — Conventions

- **Mutable default argument** — `def f(items=[])` shares the same list across all calls; use `None` and create inside
- **`type(x) == SomeClass`** instead of `isinstance(x, SomeClass)` — doesn't handle subclasses
- **`== None` / `== True` / `== False`** — use `is None`, `is True`, `is False` (identity comparison)
- **`from module import *`** — pollutes namespace and hides where names come from; import explicitly
- **Global mutable state (`global` keyword)** — makes functions impure and untestable; pass as parameter or use class

---

## Framework Checks

### FastAPI / Pydantic

- Route handler returns a dict or raw value instead of a Pydantic response model — loses automatic validation and OpenAPI docs
- `response_model` set but handler raises unvalidated exception types — clients receive undocumented 500 responses
- `Depends()` used for security but endpoint also has an `Optional` fallback — security check bypassed when dependency fails

### SQLAlchemy

- Raw SQL string with `text()` and f-string interpolation → CRITICAL SQL injection
- `Session` not closed after use — connection pool exhaustion; use `with Session(engine) as session:`
- Lazy-loaded relationship accessed outside session scope — `DetachedInstanceError` at runtime

### Django

- `User.objects.get(pk=request.GET['id'])` — unvalidated user input + unhandled `DoesNotExist`; validate input and use `get_object_or_404`
- Missing `{% csrf_token %}` in state-changing form — CSRF vulnerability
- `DEBUG = True` in production settings — exposes full stack traces and internal paths
