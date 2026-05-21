# Review Checklist — C++ Supplement

Load alongside `review-checklist.md` when `.cpp`, `.cc`, or `.h` files are present.
Same confidence filtering and verdict rules apply.

## Diagnostic Commands

```bash
cmake --build . 2>&1 | head -50        # compilation errors — fix before review
clang-tidy src/**/*.cpp                # static analysis — flag issues by severity
cppcheck --enable=all src/             # additional checks
valgrind --leak-check=full ./binary    # memory errors at runtime
```

## CRITICAL — Security (C++-specific)

- **Buffer overflows** — `strcpy`, `sprintf`, `gets` with unbounded input → use `std::string`, `snprintf`, or `std::getline`
- **Use-after-free** — raw pointer used after `delete` → smart pointers eliminate this class
- **Integer overflow in array indexing** — `arr[user_controlled_int]` without bounds check
- **`const_cast` to remove `const`** and then mutate — undefined behaviour (ES.50)
- **Format string injection** — `printf(user_input)` → always use `printf("%s", user_input)`

## CRITICAL — Resource Management (C++-specific)

- **Naked `new`/`delete`** — use `std::make_unique` / `std::make_shared` (R.11)
- **Resource leak on exception path** — non-RAII resources not wrapped; destructors won't fire
- **`malloc`/`free` in C++ code** — incompatible with constructors/destructors (R.10)

## HIGH — Memory Safety

- **Dangling reference** — returning reference or pointer to a local variable (F.43)
- **Rule of Five violation** — class manages a resource but defines fewer than all five special members (C.21)
- **`memset`/`memcpy` on non-trivial types** — skips constructors/destructors (C.90)
- **Missing `virtual` destructor** on polymorphic base class — sliced destruction (C.35)

## HIGH — Concurrency

- **Data race** — shared mutable state accessed from multiple threads without synchronization (CP.2)
- **Manual `lock()`/`unlock()`** — use `std::lock_guard` or `std::scoped_lock` (CP.20)
- **Unnamed lock guard** — `std::lock_guard<std::mutex>(m);` destroys immediately, provides no protection (CP.44)
- **`volatile` for synchronization** — `volatile` does not provide atomic semantics; use `std::atomic` (CP.8)
- **Holding lock while calling unknown code** — deadlock risk (CP.22)

## HIGH — Type Safety

- **Plain `enum` instead of `enum class`** — names leak into enclosing scope (Enum.3)
- **C-style cast `(T)expr`** — hides what conversion is happening; use `static_cast`, `reinterpret_cast` explicitly (ES.48)
- **`NULL` or `0` as null pointer** — use `nullptr` (ES.47)
- **Narrowing conversion** — `int x = long_val;` silently truncates (ES.46)
- **Unconstrained template parameter** — no concept constraint → confusing errors at instantiation (T.10)

## MEDIUM — Object Design

- **Single-argument constructor not `explicit`** — triggers unintended implicit conversions (C.46)
- **Calling virtual function in constructor/destructor** — dispatches to base, not derived (C.82)
- **`shared_ptr` where `unique_ptr` suffices** — unnecessary reference counting overhead (R.21)
- **`struct` with invariants** — use `class` when members must be kept consistent (C.2)

## MEDIUM — Performance (C++-specific)

- **`std::endl` instead of `'\n'`** — `endl` flushes the buffer on every call (SL.io.50)
- **`vector<unique_ptr<T>>` in hot path** — pointer indirection kills cache performance; prefer `vector<T>` (Per.19)
- **Unnecessary copies** — passing large objects by value instead of `const&` (F.16)
- **Premature optimization** — no profiling data cited; flag as LOW if performance claims are unsubstantiated (Per.1, Per.6)

## MEDIUM — Conventions

- **`using namespace std;` in a header** — pollutes every translation unit that includes it (SF.7)
- **Header without include guard or `#pragma once`** — multiple-inclusion errors (SF.8)
- **Header not self-contained** — requires a specific include order from the consumer (SF.11)
- **Magic numbers** — unnamed numeric literals in logic; use `constexpr` constants (ES.45)
- **`typedef` instead of `using`** — less readable for function pointer and template aliases (T.43)

---

## Framework Checks

### CMake / Build System

- Missing `target_include_directories(... PRIVATE ...)` → headers leak into consumers
- Linking against a target as `PUBLIC` when it should be `PRIVATE` → ABI contamination

### Standard Library Usage

- `std::vector` used where `std::array` is appropriate (fixed size known at compile time)
- `std::string` constructed from `const char*` in hot loop → prefer `std::string_view` for read-only access (SL.str.2)
- `std::list` chosen without profiling — `std::vector` is almost always faster due to cache locality
