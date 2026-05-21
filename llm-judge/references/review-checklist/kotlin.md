# Review Checklist — Kotlin Supplement

Load alongside `review-checklist.md` when `.kt` or `.kts` files are present.
Same confidence filtering and verdict rules apply.

## Diagnostic Commands

```bash
./gradlew build                        # compilation errors — fix before review
./gradlew detekt                       # static analysis — flag issues by severity
./gradlew test                         # test failures — flag as HIGH
./gradlew ktlintCheck                  # format drift — flag as LOW
```

## CRITICAL — Security (Kotlin-specific)

- **SQL via string interpolation** — `"SELECT ... $userId"` passed to JDBC/Exposed → parameterized queries or ORM API
- **Unsafe `@Suppress("UNCHECKED_CAST")`** — suppresses a runtime `ClassCastException` risk; require justification and a comment
- **Storing secrets in companion object `const val`** — compiled into bytecode; use environment variables or a secrets manager
- **Missing authorization check on Ktor route or Spring endpoint** — flag as CRITICAL if route handles sensitive data

## CRITICAL — Null Safety (Kotlin-specific)

- **Force-unwrap `!!`** — `user!!.name` throws `NullPointerException` if null; use safe call `?.`, Elvis `?:`, or `requireNotNull`
- **Platform type leakage from Java** — Java return types are unboxed without null annotation; assign to a nullable type explicitly (`val x: String? = javaMethod()`)

## HIGH — Coroutines

- **`GlobalScope.launch`** — escapes structured concurrency; use `coroutineScope`, `viewModelScope`, or an injected `CoroutineScope`
- **`runBlocking` in a suspend function or on the main thread** — blocks the thread and can deadlock
- **`CancellationException` caught and swallowed** — must always be rethrown so structured cancellation propagates (`catch (e: CancellationException) { throw e }`)
- **Missing `ensureActive()` in a long CPU loop** — coroutine ignores cancellation; check cancellation on each iteration
- **`async` result never `await`ed** — exception from the `Deferred` is silently lost

## HIGH — Flow

- **`SharedFlow`/`StateFlow` collected in `lifecycleScope.launch` without `Lifecycle.State`** — collects in the background; use `repeatOnLifecycle(STARTED)`
- **Hot flow subscribed inside `map`/`flatMap`** — new subscription created on each upstream emission; lift the subscription out
- **`flow { }` performing blocking I/O without `withContext(Dispatchers.IO)`** — starves the coroutine dispatcher

## HIGH — Type Safety

- **`Any` or `*` (star projection) in non-generic utility code** — loses compile-time type guarantees; use generics or sealed types
- **Unchecked cast suppressed without comment** — see CRITICAL above
- **`when` on a sealed type without `else`** — IDE warns when a new subtype is added; if `else` is present, new subtypes silently fall through

## MEDIUM — Immutability

- **`var` where `val` suffices** — prefer `val`; mutability should be intentional
- **Mutable data class** — `data class User(var name: String)` defeats `copy()` semantics and thread safety
- **Returning a mutable collection from a public API** — return `List`/`Set`/`Map` instead of `MutableList`/`MutableSet`/`MutableMap`

## MEDIUM — Error Handling

- **`runCatching` with `getOrNull()` discarding the cause** — log or propagate the exception before discarding
- **`require`/`check` without a message lambda** — exception message is empty; always provide `{ "descriptive message: $value" }`
- **Exceptions used for control flow** — `NotFoundException` thrown and caught in the same layer → use nullable return or `Result`

## MEDIUM — Performance (Kotlin-specific)

- **`sequence { }` followed by `.toList()` on a small collection** — overhead of lazy evaluation exceeds the gain; use direct collection operations
- **Deeply nested scope functions** — `?.let { ?.let { ?.let { } } }` → use direct safe-call chain `a?.b?.c`
- **`copy()` in a tight loop on a large data class** — allocates on every call; accumulate changes and copy once

## MEDIUM — Conventions

- **`object` used for stateful singleton with mutable fields** — object lifetime is process-scoped; prefer DI-scoped instances
- **Extension function on `Any` or `String` in a shared module** — pollutes autocompletion for everyone importing the module; scope it with a context receiver or move it closer to the consumer
- **Missing trailing comma in multi-line argument/parameter list** — causes noisy diffs when adding parameters; Kotlin style guide recommends trailing commas

---

## Framework Checks

### Ktor

- `call.receiveOrNull()` result not checked for null — missing null guard leads to `NullPointerException` at runtime
- Missing `call.respond(HttpStatusCode.BadRequest)` before `return` in validation branches — response never sent
- `routing { }` block grows unbounded — extract routes into separate modules via `Route.xxx()` extension functions

### Spring Boot (Kotlin)

- `@Transactional` on a `final` class or method — Spring cannot create a proxy; add `open` or enable the `kotlin-spring` plugin
- Injecting by field (`@Autowired var`) instead of constructor injection — prevents `val` and makes testing harder
- `@RestController` method returning nullable type without `ResponseEntity` — `null` is serialized as `null` JSON rather than a 404

### Exposed ORM

- `transaction { }` wrapping a `suspend` call — `transaction` is blocking; use `newSuspendedTransaction` with `Dispatchers.IO`
- Missing `.alias()` on joined tables with duplicate column names — silent column shadowing in query results
