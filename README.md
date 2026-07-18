# 💳 POS Agent Cash-Out System

A command-line simulation of a neighbourhood POS (agent-banking) machine in Nigeria — built to demonstrate robust **exception handling** in Python. No matter how broken a customer's request is, the machine logs a clear reason and keeps the queue moving. It never crashes.

---

## 📖 Overview

Agent-banking POS machines are everywhere in Nigerian neighbourhoods — customers walk up, hand over their card or account details, and cash out against their bank balance. In real life, requests are messy: malformed amounts, empty account fields, withdrawals that exceed either the customer's balance or the machine's physical cash on hand.

This project simulates that environment end-to-end. A queue of cash-out requests — deliberately seeded with bad data — is processed one at a time against:

- the **customer's account balance**, and
- the **agent's float** (the physical cash loaded into the machine that day).

Every request either succeeds or is rejected with a specific, human-readable reason. The program is built entirely around `try` / `except` / `else` / `finally`, with a custom exception hierarchy modeling the actual business rules of the machine.

---

## ✨ Features

- Custom exception hierarchy (`TransactionError` → `InsufficientFundsError`) modeling real business failures, not just generic errors
- Input validation that safely handles non-numeric amounts, without ever raising an unhandled `ValueError`
- Separate, ordered `except` blocks — specific business errors, missing data (`KeyError`), and a generic safety net, each handled and reported differently
- Fee calculation using integer division (no floating-point kobo rounding issues)
- A running agent float that only changes on a genuinely successful transaction
- An end-of-day summary: total successes, failures, and remaining float
- Guaranteed to run to completion, regardless of how malformed an individual request is

---

## 🧰 Requirements

- Python 3.6 or later (uses f-strings)
- No external dependencies — standard library only (`sys`, for UTF-8 output on Windows terminals)

---

## 🚀 Getting Started

Clone the repository and run the script directly:

```bash
git clone <https://github.com/greyvectorr/POS_Agent>
cd <POS_Agent>
python agent.py
```

There is no configuration step and no external data file — the queue of requests is a Python list embedded directly in `agent.py`, which keeps the project self-contained and focused purely on exception handling.

---

## 🗂️ Project Structure

```
.
├── agent.py       # Entire program: exceptions, validation, processing loop, main()
└── README.md      # You are here
```

---

## 🧠 How It Works

Each request in the queue is a dictionary with `customer`, `phone`, `amount`, and `account_balance`. For every request, `process_cashout()` runs it through three checks, in order:

| Step | Function | Rejects when... | Raises |
|---|---|---|---|
| 1 | `validate_amount()` | amount isn't a valid number | `TransactionError` |
| 1 | `validate_amount()` | amount is zero or negative | `TransactionError` |
| 1 | `validate_amount()` | amount isn't a multiple of ₦100 | `TransactionError` |
| 2 | `check_balance()` | amount exceeds the customer's account balance | `InsufficientFundsError` |
| 3 | `check_agent_float()` | amount exceeds the agent's available cash | `TransactionError` |

If a request dictionary is missing a required key entirely (e.g. no `account_balance`), Python raises a `KeyError` automatically the moment that key is accessed — no manual checking required.

### Exception hierarchy

```
Exception
 └── TransactionError
      └── InsufficientFundsError
```

`InsufficientFundsError` is a subclass of `TransactionError`, so it's caught by the same `except TransactionError` block as any other business-rule rejection — while still being distinct enough to raise and identify separately if needed later.

### `process_cashout()` control flow

```
try:
    → read customer, amount, account_balance from the request
    → validate the amount
    → check customer balance
    → check agent float
except TransactionError:
    → known business rule failure — print the reason
except KeyError:
    → request was missing a required field — print which one
except Exception:
    → anything unexpected — caught last, so it never masks the specific errors above
else:
    → nothing went wrong — charge the fee, reduce the float, confirm the payout
finally:
    → always runs — prints the transaction-ended marker
```

---

## 📋 Sample Output

Running `python agent.py` against the embedded (intentionally messy) request queue produces:

<details>
<summary>Click to expand full output</summary>

```
POS Terminal Started
Opening Amount: ₦50000

Processing cashout request for Chinedu Okafor (Phone: 08031234567, Amount: 5000)
Transaction for Chinedu Okafor approved: ₦5000 withdrawn, fee ₦100, new float ₦45000
--- Transaction Ended ---
Current amount after transaction: ₦45000

Processing cashout request for Aisha Bello (Phone: 07061234567, Amount: five thousand)
Transaction for Aisha Bello rejected: Amount five thousand is not a valid number.
--- Transaction Ended ---
Current amount after transaction: ₦45000

Processing cashout request for Emeka Nwosu (Phone: 08101234567, Amount: 40000)
Transaction for Emeka Nwosu rejected: Insufficient funds: requested ₦40000, available ₦2000.
--- Transaction Ended ---
Current amount after transaction: ₦45000

Processing cashout request for Fatima Sani (Phone: 09021234567, Amount: 2550)
Transaction for Fatima Sani rejected: Amount 2550 must be a multiple of ₦100.
--- Transaction Ended ---
Current amount after transaction: ₦45000

Processing cashout request for Tunde Adeyemi (Phone: 08051234567, Amount: 75000)
Transaction for Tunde Adeyemi rejected: Agent amount insufficient: requested ₦75000, available ₦45000.
--- Transaction Ended ---
Current amount after transaction: ₦45000

Processing cashout request for Blessing Eze (Phone: 07031234567, Amount: 10000)
Transaction for Blessing Eze approved: ₦10000 withdrawn, fee ₦200, new float ₦35000
--- Transaction Ended ---
Current amount after transaction: ₦35000

Processing cashout request for Unknown Customer (Phone: 08099887766, Amount: 3000)
Transaction for Unknown Customer rejected: missing key 'account_balance'
--- Transaction Ended ---
Current amount after transaction: ₦35000

Processing cashout request for Ibrahim Musa (Phone: 08122334455, Amount: -3000)
Transaction for Ibrahim Musa rejected: Amount -3000 must be greater than zero.
--- Transaction Ended ---
Current amount after transaction: ₦35000

Processing cashout request for Ngozi Uche (Phone: 09033445566, Amount: 0)
Transaction for Ngozi Uche rejected: Amount 0 must be greater than zero.
--- Transaction Ended ---
Current amount after transaction: ₦35000

End-of-Day Summary:
Successes: 2
Failures: 7
Final float: ₦35000
```

</details>

Nine requests go in — a mix of valid, malformed, underfunded, and incomplete — and all nine come out the other side handled, with the program never once crashing.

---

## 🧪 Test Cases Covered by the Sample Data

| Scenario | Customer | Result |
|---|---|---|
| Valid cash-out | Chinedu Okafor | ✅ Approved |
| Non-numeric amount (`"five thousand"`) | Aisha Bello | ❌ Rejected |
| Amount exceeds account balance | Emeka Nwosu | ❌ Rejected |
| Amount not a multiple of ₦100 | Fatima Sani | ❌ Rejected |
| Amount exceeds agent's float | Tunde Adeyemi | ❌ Rejected |
| Valid cash-out | Blessing Eze | ✅ Approved |
| Missing `account_balance` key | Unknown Customer | ❌ Rejected |
| Negative amount | Ibrahim Musa | ❌ Rejected |
| Zero amount | Ngozi Uche | ❌ Rejected |

---

## 🔑 Key Design Decisions

- **The POS fee is charged but not deducted from the float.** The float only decreases by the amount physically paid out to the customer — the fee is a reported figure, not a float adjustment.
- **Success/failure is tracked by comparing the float before and after each transaction** in `main()`, rather than `process_cashout()` returning a separate status flag. Since every valid amount is strictly positive, any successful transaction is guaranteed to change the float, making this comparison a reliable success signal.
- **`except Exception` is always last.** Ordering the `except` blocks from most specific to most general ensures business-rule errors and missing-data errors are reported precisely, while still catching anything genuinely unforeseen without ever letting the program crash.

---

## 🎓 Learning Objectives Demonstrated

- Using `try` / `except` / `else` / `finally` blocks correctly and in the right order
- Catching specific exception types separately from generic ones
- Converting unreliable input into a usable type and handling the failure case
- Raising exceptions deliberately to enforce business rules
- Designing a custom exception hierarchy (base class + a more specific subclass) to model real-world failure modes

---

## 📄 License

This project was built as a coursework exercise (Python Advanced Cohort 35). Add a license here if you intend to share or reuse this code beyond that context.
