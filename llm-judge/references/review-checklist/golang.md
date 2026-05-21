# Review Checklist — Go Supplement

Load alongside `review-checklist.md` when `.go` files are present.
Same confidence filtering and verdict rules apply.

## Diagnostic Commands

```bash
go build ./...                # compilation errors — fix before review
go vet ./...                  # suspicious constructs — flag as HIGH
go test -race ./...           # data races — flag as CRITICAL
staticcheck ./...             # advanced static analysis
golangci-lint run             # comprehensive lint suite
```

## CRITICAL — Security (Go-specific)

- **SQL injection** — `fmt.Sprintf("SELECT ... %s", input)` passed to `db.Query` → use parameterized queries (`db.Query("... $1", input)`)
- **Path traversal** — user-controlled path joined with `filepath.Join` without cleaning → validate with `filepath.Clean` and confirm it is within expected root
- **`exec.Command` with unsanitized input** — shell injection risk; never pass user input directly
- **Serving files with `http.ServeFile`** — ensure the path cannot escape the intended directory

## CRITICAL — Error Handling (Go-specific)

- **Ignored error with `_`** — `result, _ := doSomething()` silently swallows failures; always handle or explicitly document why safe to ignore
- **`panic` for expected errors** — panics are for programmer errors only; return errors for expected failure cases
- **Error swallowed in `defer`** — `defer f.Close()` discards the error; use a named return or check explicitly if the error matters

## HIGH — Concurrency

- **Goroutine leak** — goroutine started with no guarantee it will ever exit; always provide a stop signal via `context.Context` or channel close
- **Unbuffered channel send with no receiver guarantee** — goroutine will block forever if the receiver exits early
- **Shared mutable state without synchronization** — concurrent reads/writes to maps, slices, or struct fields without a mutex or `sync/atomic`
- **`sync.Mutex` copied by value** — passing or returning a struct containing a mutex by value; use pointer receiver or pointer to struct
- **`time.Sleep` for synchronization** — non-deterministic; use channels, `sync.WaitGroup`, or `errgroup`

## HIGH — Context

- **Missing `context.Context` on public I/O functions** — prevents timeout and cancellation propagation
- **`context.Background()` deep in a call stack** — cancellation signals from the caller are lost; thread the context through
- **Context stored in a struct** — context should be the first parameter, not a field

## HIGH — Error Wrapping

- **Missing `%w` in `fmt.Errorf`** — callers cannot use `errors.Is`/`errors.As` to inspect the root cause
- **Wrapping an already-descriptive sentinel** — double-wrapping loses unwrap chain; use `%w` consistently

## MEDIUM — Type Safety and Interfaces

- **Interface satisfied accidentally** — large interface used as a function parameter; prefer small, single-method interfaces
- **Interface defined in the provider package** — define interfaces in the consumer package to avoid tight coupling
- **Returning `interface{}` / `any`** — loses type safety; use concrete types or generics

## MEDIUM — Performance (Go-specific)

- **Slice grown element-by-element** — preallocate with `make([]T, 0, expectedLen)` when final size is known
- **String concatenation in a loop** — use `strings.Builder` or `strings.Join` instead
- **`fmt.Sprintf` for simple string building** — expensive reflection; use `+` or `strings.Builder` in hot paths
- **Map with `string` keys in hot path** — consider `sync.Map` only when the write-rarely/read-often pattern applies; `map` + `sync.Mutex` is usually simpler

## MEDIUM — Conventions

- **Package name is `util`, `common`, or `helpers`** — names should describe the package's purpose, not its utility
- **Exported function without godoc comment** — public API should document intent, parameters, and return values
- **Naked return in a long function** — hard to trace what is returned; use explicit returns
- **`init()` with side effects** — initialization order between packages is fragile; use explicit constructors

---

## Framework Checks

### net/http

- Handler doesn't call `w.WriteHeader` before `w.Write` when a non-200 status is intended — headers sent implicitly on first write
- Missing `r.Body` close — leak on handlers that read the body; `defer r.Body.Close()` should be present
- Missing timeout on `http.Server` (`ReadTimeout`, `WriteTimeout`, `IdleTimeout`) — susceptible to slowloris

### database/sql

- `rows.Close()` not deferred — connection leak if iteration exits early
- `rows.Err()` not checked after loop — silent data truncation on query error
- Using `db.Exec` with string interpolation — CRITICAL SQL injection (see above)

### Testing

- Test uses `t.Error`/`t.Log` after goroutine exits — race on `testing.T`; use `t.Parallel()` carefully
- No table-driven tests for multiple similar cases — missed coverage and poor readability
