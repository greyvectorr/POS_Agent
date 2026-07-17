# 💳 POS Agent Cash-Out: The Machine That Must Never Crash

> You are the brain of a neighbourhood POS machine in Nigeria — customers walk up to withdraw cash, and no matter how broken their request is, your code must handle it gracefully and keep the queue moving.

**Difficulty:** ⭐ (single topic) | **Estimated time:** ~2 hours | **Topics:** Exception Handling

---

## 📖 The Story

Mama Ngozi runs a busy POS stand outside the market in Aba. Every morning she loads her machine with a **float** (cash on hand) — say ₦50,000 — and all day people come to cash out from their bank accounts.

The problem? Real customers are messy. One person types "five thousand" instead of `5000`. Another asks for ₦0. Someone tries to withdraw ₦40,000 when their balance is ₦2,000. Another wants ₦75,000 when the machine only has ₦12,000 left. And sometimes the request that reaches the machine is simply missing information.

If the software crashes on **any** of these, Mama Ngozi loses customers and money. Your job: write software that **calmly rejects bad requests, processes good ones, and never, ever crashes**. This is what exception handling is for.

---

## 🎯 Learning Objectives

By the end of this assignment you will be able to:

- Use `try` / `except` / `else` / `finally` blocks correctly.
- Catch **specific** exception types (like `KeyError`) separately from **generic** ones (`Exception`).
- Convert unreliable input (a string) into a number and handle the failure when it can't be converted.
- Guard your code against invalid values by **raising** exceptions yourself.
- Design and use a **custom exception class** (and a subclass) to model real business rules.

---

## 🛠️ Your Mission

Complete the functions in `starter.py` so the POS machine can process a queue of cash-out requests against the agent's float. Each request is validated and processed independently. A bad request should be **logged with a clear reason and skipped** — the machine moves on to the next customer. At the end, print a summary: how many succeeded, how many failed, and how much float is left.

---

## 📋 Requirements

Your program must:

1. Define a custom exception `TransactionError` (subclass of `Exception`) and a more specific `InsufficientFundsError` that inherits from `TransactionError`.
2. `validate_amount(amount)` must convert the amount to a number. If it cannot be converted (e.g. `"five thousand"`), raise a `TransactionError` with a clear message.
3. `validate_amount(amount)` must reject amounts that are **not positive** (zero or negative) by raising `TransactionError`.
4. `validate_amount(amount)` must reject amounts that are **not a multiple of ₦100** by raising `TransactionError` (the POS only dispenses ₦100 / ₦500 / ₦1000 notes).
5. `check_balance(amount, account_balance)` must raise `InsufficientFundsError` when the amount is greater than the customer's account balance.
6. `check_agent_float(amount, agent_float)` must raise `TransactionError` when the agent does not have enough cash float to pay out the amount.
7. `charge_fee(amount)` must compute a POS fee using integer division (₦100 for every ₦5,000 requested) and return it.
8. `process_cashout(request, agent_float)` must orchestrate the checks inside `try` / `except` / `else` / `finally`:
   - catch `TransactionError`, `KeyError`, and a generic `Exception` in **separate** `except` blocks, each printing a clear reason,
   - on success (`else`) print the confirmation, the fee, and the new agent float,
   - **always** print `--- transaction ended ---` in `finally`,
   - return the updated agent float (unchanged if the transaction failed).
9. `main()` must start with a float of ₦50,000, loop through `CASHOUT_REQUESTS` updating the float only on success, tally successes vs failures, and print a final summary with the remaining float.
10. The program must **run to completion without crashing**, no matter how broken the sample data is.

---

## 📂 Provided Files

| File | What it is |
| --- | --- |
| `starter.py` | Skeleton with the embedded `CASHOUT_REQUESTS` data, function stubs, docstrings, and `# TODO:` markers. Runs as-is (does nothing useful yet). |
| `instructions.md` | This file. |

There is **no external data file** — the request queue is a Python list right inside `starter.py`. This keeps the assignment 100% about exception handling.

---

## 🧭 Step-by-Step Guide

This maps directly to the TODOs in `starter.py`:

1. **TODO 1 — Custom exceptions.** Define `class TransactionError(Exception): pass` and `class InsufficientFundsError(TransactionError): pass`. That's it — the body can just be `pass`.
2. **TODO 2 — `validate_amount`.** Wrap `float(amount)` (or `int`) in a `try` / `except`. Catch the conversion error and `raise TransactionError(...)`. Then check for `<= 0` and for `amount % 100 != 0`, raising `TransactionError` for each.
3. **TODO 3 — `check_balance`.** A simple `if amount > account_balance: raise InsufficientFundsError(...)`.
4. **TODO 4 — `check_agent_float`.** A simple `if amount > agent_float: raise TransactionError(...)`.
5. **TODO 5 — `charge_fee`.** Return `(amount // 5000) * 100` (integer division — no decimals).
6. **TODO 6 — `process_cashout`.** Read `request["customer"]`, `request["amount"]`, `request["account_balance"]` (a missing key raises `KeyError` for you!). Call the validators in a `try`. Use separate `except` blocks, then `else`, then `finally`. Subtract the amount from the float on success and return it.
7. **TODO 7 — `main`.** Set `agent_float = 50000`, loop over the requests, reassign `agent_float` to whatever `process_cashout` returns, keep a success/failure count, and print the summary.

---

## 🖥️ Example Run

```
====== MAMA NGOZI POS TERMINAL ======
Opening float: ₦50,000

Processing cash-out for Chinedu Okafor (08031234567)...
✅ Approved: ₦5,000 paid out | Fee: ₦100 | Float left: ₦45,000
--- transaction ended ---

Processing cash-out for Aisha Bello (07061234567)...
❌ Rejected: amount 'five thousand' is not a valid number.
--- transaction ended ---

Processing cash-out for Emeka Nwosu (08101234567)...
❌ Rejected: ₦40,000 is more than the account balance of ₦2,000.
--- transaction ended ---

Processing cash-out for Fatima Sani (09021234567)...
❌ Rejected: amount must be a multiple of ₦100 (got ₦2,550).
--- transaction ended ---

Processing cash-out for Tunde Adeyemi (08051234567)...
❌ Rejected: agent float too low — need ₦75,000 but only ₦45,000 available.
--- transaction ended ---

Processing cash-out for Blessing Eze (07031234567)...
✅ Approved: ₦10,000 paid out | Fee: ₦200 | Float left: ₦35,000
--- transaction ended ---

Processing cash-out for Unknown Customer...
❌ Rejected: request is missing required information (KeyError: 'account_balance').
--- transaction ended ---

Processing cash-out for Ibrahim Musa (08122334455)...
❌ Rejected: amount must be positive (got ₦-3,000).
--- transaction ended ---

============ END OF DAY ============
Successful cash-outs: 2
Failed cash-outs:     6
Final float: ₦35,000
```

*(Your exact wording and which entries pass/fail will depend on the sample data — the point is that every request is handled and the program never crashes.)*

---

## 🌟 Stretch Goals

1. **Daily limit:** raise a new `DailyLimitError(TransactionError)` if a single cash-out exceeds ₦100,000.
2. **Low-float warning:** after each successful transaction, print a ⚠️ warning when the remaining float drops below ₦10,000.
3. **Retry the string:** if an amount arrives as a string like `"5000"` (digits only), convert it successfully instead of rejecting it — but still reject `"five thousand"`.

---

## 💡 Hints

- A `KeyError` is raised **automatically** when you access a dictionary key that doesn't exist. You don't need to check for missing keys manually — just let the `except KeyError:` block catch it.
- **Order matters** in `except` blocks. Because `InsufficientFundsError` *is a* `TransactionError`, catching `TransactionError` will also catch it — that's fine here since we want the same handling. Put the generic `except Exception:` **last** as your safety net.
- The `else` block runs **only when no exception was raised** in the `try`. It's the perfect place to confirm success — cleaner than putting success code at the end of the `try`.
- The `finally` block runs **no matter what** — success, failure, or even an unexpected error. That's why the "transaction ended" line belongs there.
- To reject non-multiples of ₦100, the modulo operator is your friend: `amount % 100` is `0` only for exact multiples.

---

## ✅ Submission Checklist

- [ ] `TransactionError` and `InsufficientFundsError` are defined, and the second inherits from the first.
- [ ] `validate_amount` handles non-numeric input, non-positive values, and non-multiples of ₦100.
- [ ] `check_balance` raises `InsufficientFundsError` correctly.
- [ ] `check_agent_float` raises `TransactionError` when the float is too low.
- [ ] `charge_fee` uses integer division and returns a number.
- [ ] `process_cashout` uses `try` / `except` / `else` / `finally` with **separate** `except` blocks for `TransactionError`, `KeyError`, and `Exception`.
- [ ] `finally` always prints `--- transaction ended ---`.
- [ ] `main()` updates the float only on success and prints a correct final summary.
- [ ] The program runs from top to bottom **without ever crashing**.
- [ ] Every rejection prints a **clear, human-readable reason**.
