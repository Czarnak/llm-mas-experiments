# Review Checklist — C# / .NET Supplement

Load alongside `review-checklist.md` when `.cs` files are present.
Same confidence filtering and verdict rules apply.

## Diagnostic Commands

```bash
dotnet build                       # compilation errors — fix before review
dotnet format --verify-no-changes  # format drift — flag as LOW
dotnet test --no-build             # test failures — flag as HIGH
```

## CRITICAL — Security (C#-specific)

- **SQL via interpolation** — `$"SELECT ... {userId}"` → parameterized queries or EF Core
- **`BinaryFormatter`** — removed in .NET 7+, insecure deserialization
- **`JsonSerializer` with `TypeNameHandling.All`** — type confusion attacks
- **Missing `[ValidateAntiForgeryToken]`** on state-changing Razor actions
- **Missing `[Authorize]`** on protected controllers/Minimal API endpoints

## CRITICAL — Error Handling (C#-specific)

- **Missing `using`/`await using`** for `IDisposable`/`IAsyncDisposable`
- **Blocking async** — `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` → deadlocks

## HIGH — Async

- **Missing `CancellationToken`** on public async methods
- **`async void`** except in event handlers → return `Task`/`Task<T>`
- **Missing `ConfigureAwait(false)`** in library code
- **Sync-over-async wrappers** — propagate `async` upward instead

## HIGH — Type Safety

- **Unexplained `!` operator** — suppresses nullability without guarantee
- **Unsafe casts** — `(T)obj` without type check → `obj is T t`
- **Magic strings** for config keys, routes → constants, `nameof()`
- **`dynamic` in application code** → generics or interfaces

## HIGH — Code Quality (C#-specific)

- **Mutable static state** shared across requests → `ConcurrentDictionary`, DI-scoped
- **`new`-ing services** instead of DI injection

## MEDIUM — Performance (C#-specific)

- **N+1 in EF Core** — lazy loading in loops → `Include`/`ThenInclude`
- **Missing `AsNoTracking`** on read-only queries
- **`IEnumerable<T>` enumerated multiple times** → `.ToList()`
- **LINQ in hot paths** → `for` loops with pre-allocated buffers

## MEDIUM — Conventions

- **`record` vs `class`** — immutable DTOs should be `record`
- **Missing `sealed`** on non-inherited concrete classes
- **`IEnumerable` returns** when always materialized → `IReadOnlyList<T>`

---

## Framework Checks

### ASP.NET Core

- Missing `[ApiController]` → no automatic ModelState validation
- Wrong middleware order: `UseAuthentication` before `UseAuthorization`, `UseRouting` before `UseEndpoints`
- `IConfiguration["key"]` in services → `IOptions<T>` pattern
- Minimal APIs: use `TypedResults` over `Results`

### EF Core

- Destructive migrations without compatibility window → HIGH
- `FromSqlRaw`/`ExecuteSqlRaw` with user input → CRITICAL (SQL injection)

### Blazor

- Missing Dispose on components subscribing to events
- Unnecessary `StateHasChanged` inside `InvokeAsync`
- `IJSObjectReference` not disposed

### Background Services

- `ExecuteAsync` must respect `CancellationToken` on every loop iteration
- Unhandled exceptions silently stop the service → wrap in try/catch
