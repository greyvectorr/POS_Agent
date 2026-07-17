"""
POS Agent Cash-Out — Exception Handling Assignment
Python Advanced Cohort 35

You are writing the software for a neighbourhood POS (agent-banking) machine
in Nigeria. Customers walk up to withdraw cash. The machine processes a queue
of cash-out requests against the agent's float (cash on hand) and each
customer's account balance.

THE GOLDEN RULE: the machine must NEVER crash, no matter how broken a request
is. Every bad request should be rejected with a clear reason, and the machine
should move on to the next customer.

This assignment is PURE exception handling — no files, no regex, no internet.

------------------------------------------------------------------------------
TODO SUMMARY (details are in the docstrings and comments below):
  TODO 1: Define the custom exceptions TransactionError and
          InsufficientFundsError.
  TODO 2: validate_amount()   -> convert + check positive + check multiple of 100
  TODO 3: check_balance()     -> raise InsufficientFundsError if too poor
  TODO 4: check_agent_float() -> raise TransactionError if agent can't pay
  TODO 5: charge_fee()        -> compute the POS fee (integer division)
  TODO 6: process_cashout()   -> try / except / else / finally orchestration
  TODO 7: main()              -> loop the queue, tally results, print summary
------------------------------------------------------------------------------
Run it any time with:  python starter.py
Right now it runs without crashing but does not do the real work yet.
"""

# ---------------------------------------------------------------------------
# No imports are needed for the exception-handling work itself — that is built
# into Python, which is the whole point! (You may add imports for stretch goals.)
#
# The two lines below just make sure the Naira symbol (₦) prints correctly on
# Windows terminals. You do not need to touch or understand them for this
# assignment — leave them as they are.
# ---------------------------------------------------------------------------
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass  # older Pythons / unusual terminals: safe to ignore


# ---------------------------------------------------------------------------
# EMBEDDED DATA
# This is the queue of cash-out requests waiting at the POS stand.
# It is DELIBERATELY messy — several entries are broken so your exception
# handling has something to catch. Do NOT "fix" the data; fix your code so it
# survives the data.
#
# Each request is a dict with: customer, phone, amount, account_balance.
# (One entry is intentionally missing a key — that is on purpose!)
# ---------------------------------------------------------------------------
CASHOUT_REQUESTS = [
    {"customer": "Chinedu Okafor", "phone": "08031234567", "amount": 5000,  "account_balance": 20000},
    {"customer": "Aisha Bello",    "phone": "07061234567", "amount": "five thousand", "account_balance": 15000},
    {"customer": "Emeka Nwosu",    "phone": "08101234567", "amount": 40000, "account_balance": 2000},
    {"customer": "Fatima Sani",    "phone": "09021234567", "amount": 2550,  "account_balance": 30000},
    {"customer": "Tunde Adeyemi",  "phone": "08051234567", "amount": 75000, "account_balance": 90000},
    {"customer": "Blessing Eze",   "phone": "07031234567", "amount": 10000, "account_balance": 50000},
    {"customer": "Unknown Customer","phone": "08099887766", "amount": 3000},  # <-- missing "account_balance"!
    {"customer": "Ibrahim Musa",   "phone": "08122334455", "amount": -3000, "account_balance": 10000},
    {"customer": "Ngozi Uche",     "phone": "09033445566", "amount": 0,     "account_balance": 8000},
]

# The note denominations the POS can dispense. Any amount must be a multiple
# of the smallest note (₦100).
NOTE_UNIT = 100

# The float Mama Ngozi loads into the machine at the start of the day.
OPENING_FLOAT = 50000


# ---------------------------------------------------------------------------
# TODO 1: CUSTOM EXCEPTIONS
# ---------------------------------------------------------------------------
# TODO: Define a custom exception called TransactionError that inherits from
#       the built-in Exception. The body can simply be `pass`.
# TODO: Define InsufficientFundsError that inherits from TransactionError
#       (NOT from Exception directly) so it is a MORE SPECIFIC kind of
#       transaction error.
#
# Hint:
#   class TransactionError(Exception):
#       pass
#
# Replace the placeholders below.

class TransactionError(Exception):
    """Base error for anything that goes wrong during a cash-out."""
    pass  # TODO: nothing more is needed here, but keep this class.


class InsufficientFundsError(TransactionError):
    """Raised when a customer tries to withdraw more than their balance."""
    pass  # TODO: keep this class; it should inherit from TransactionError.


# ---------------------------------------------------------------------------
# TODO 2: VALIDATE THE AMOUNT
# ---------------------------------------------------------------------------
def validate_amount(amount):
    """Convert `amount` to a number and make sure it is a valid cash-out.

    Rules:
      * If `amount` cannot be turned into a number (e.g. "five thousand"),
        raise TransactionError with a friendly message.
      * If the number is zero or negative, raise TransactionError.
      * If the number is not a multiple of NOTE_UNIT (₦100), raise
        TransactionError.

    Returns:
        The amount as a clean number (e.g. an int) when it is valid.

    TODO:
      1. Try to convert `amount` to a number inside a try/except. If the
         conversion fails (ValueError / TypeError), raise TransactionError.
      2. After a successful conversion, check it is positive.
      3. Then check it is a multiple of NOTE_UNIT using the % operator.
      4. Return the clean number.
    """
    # TODO: implement the conversion + checks described above.
    return amount  # placeholder so the file runs; replace with real logic.


# ---------------------------------------------------------------------------
# TODO 3: CHECK THE CUSTOMER'S ACCOUNT BALANCE
# ---------------------------------------------------------------------------
def check_balance(amount, account_balance):
    """Ensure the customer actually has enough money in their account.

    If `amount` is greater than `account_balance`, raise
    InsufficientFundsError with a clear message. Otherwise do nothing.

    TODO: write a single `if` that raises InsufficientFundsError when the
          customer is trying to take out more than they have.
    """
    # TODO: raise InsufficientFundsError when amount > account_balance.
    pass


# ---------------------------------------------------------------------------
# TODO 4: CHECK THE AGENT'S FLOAT (CASH ON HAND)
# ---------------------------------------------------------------------------
def check_agent_float(amount, agent_float):
    """Ensure Mama Ngozi actually has enough cash to pay this out.

    Even if the customer's account is fine, the machine can only dispense
    cash it physically has. If `amount` is greater than `agent_float`, raise
    TransactionError. Otherwise do nothing.

    TODO: write a single `if` that raises TransactionError when the agent's
          float is too low to cover this request.
    """
    # TODO: raise TransactionError when amount > agent_float.
    pass


# ---------------------------------------------------------------------------
# TODO 5: CHARGE THE POS FEE
# ---------------------------------------------------------------------------
def charge_fee(amount):
    """Work out the POS service fee for this cash-out.

    Use a simple rule: ₦100 for every full ₦5,000 requested, using INTEGER
    division so there are no kobo/decimals. For example:
        ₦4,000  -> ₦0
        ₦5,000  -> ₦100
        ₦10,000 -> ₦200
        ₦12,000 -> ₦200

    Returns:
        The fee as a whole number.

    TODO: return (amount // 5000) * 100  (this is the only line you need).
    """
    # TODO: compute and return the fee using integer division (//).
    return 0  # placeholder; replace with the real calculation.


# ---------------------------------------------------------------------------
# TODO 6: PROCESS ONE CASH-OUT (the heart of the assignment)
# ---------------------------------------------------------------------------
def process_cashout(request, agent_float):
    """Process a single cash-out request safely and never crash.

    This is where try / except / else / finally all come together.

    Flow:
      * In the TRY block:
          - read customer, amount and account_balance from `request`
            (accessing a missing key raises KeyError automatically!),
          - call validate_amount(...) to clean/validate the amount,
          - call check_balance(...) and check_agent_float(...).
      * Use SEPARATE except blocks:
          - except TransactionError: print the clear reason it was rejected.
          - except KeyError: the request was missing information; say so.
          - except Exception: a catch-all safety net for anything unexpected.
      * In the ELSE block (runs only if NO exception happened):
          - the transaction succeeded! Charge the fee, reduce the float,
            print the approval + fee + new float, and remember the new float.
      * In the FINALLY block (runs ALWAYS):
          - print "--- transaction ended ---".

    Returns:
        The updated agent_float. If the transaction FAILED, return the
        agent_float UNCHANGED (the money never left the machine).

    TODO: build the try / except / else / finally structure described above.
    """
    # Start by assuming the float does not change (failed transactions leave
    # the float exactly as it was).
    new_float = agent_float

    # TODO: replace the body below with a real try/except/else/finally.
    #
    # Skeleton to fill in:
    #
    # try:
    #     customer = request["customer"]
    #     amount = validate_amount(request["amount"])
    #     balance = request["account_balance"]
    #     check_balance(amount, balance)
    #     check_agent_float(amount, agent_float)
    # except TransactionError as error:
    #     print("Rejected:", error)
    # except KeyError as missing:
    #     print("Rejected: request is missing", missing)
    # except Exception as unexpected:
    #     print("Rejected: unexpected problem -", unexpected)
    # else:
    #     fee = charge_fee(amount)
    #     new_float = agent_float - amount
    #     print("Approved! Paid out, fee charged, new float:", new_float)
    # finally:
    #     print("--- transaction ended ---")

    return new_float


# ---------------------------------------------------------------------------
# TODO 7: MAIN — run the whole day
# ---------------------------------------------------------------------------
def main():
    """Run the POS terminal for the day.

    TODO:
      1. Start agent_float at OPENING_FLOAT and print an opening banner.
      2. Keep two counters: successes and failures (start both at 0).
      3. Loop over CASHOUT_REQUESTS. For each request:
           - call process_cashout(request, agent_float),
           - reassign agent_float to whatever it returns,
           - decide whether it succeeded (hint: the float changed) and update
             your counters.
      4. After the loop, print an end-of-day summary: successes, failures,
         and the final float.
    """
    agent_float = OPENING_FLOAT

    print("====== MAMA NGOZI POS TERMINAL ======")
    print(f"Opening float: ₦{agent_float:,}")
    print()

    # TODO: set up your success/failure counters here.

    # TODO: loop over CASHOUT_REQUESTS and process each one, updating the
    #       float and your counters. A starter loop is sketched below.
    for request in CASHOUT_REQUESTS:
        # Print which customer we are serving. (Use .get() so a missing name
        # would not crash — though our data always has a name.)
        name = request.get("customer", "Unknown")
        phone = request.get("phone", "")
        print(f"Processing cash-out for {name} ({phone})...")

        # TODO: call process_cashout(...) and update agent_float + counters.
        agent_float = process_cashout(request, agent_float)
        print()

    # TODO: print the end-of-day summary (successes, failures, final float).
    print("============ END OF DAY ============")
    # print(f"Successful cash-outs: {successes}")
    # print(f"Failed cash-outs:     {failures}")
    print(f"Final float: ₦{agent_float:,}")


if __name__ == "__main__":
    main()
