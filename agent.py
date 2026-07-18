"""
POS Agent Exception Handling - The Machine That Must Never Crash
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
# No imports are needed for this project.
# The lines below just make sure the Naira symbol (₦) prints correctly on
# Windows terminals.
# ---------------------------------------------------------------------------

import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    # older Pythons / unusual terminals: safe to ignore
    pass


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


# The float loaded into the machine at the start of the day.

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

class TransactionError(Exception):
    """Custom exception for transaction errors."""
    pass

class InsufficientFundsError(TransactionError):
    """Raised when the account balance is insufficient for the requested amount."""
    pass # Inheritance from TransactionError, no additional implementation needed.



# ---------------------------------------------------------------------------
# TODO 2: AMOUNT VALIDATION
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
    """

    # Step 1: try to convert whatever came in (could already be a number,
    # or a string like "five thousand" that will fail) into a float.

    try:
        numeric_amount = float(amount)
    except (ValueError, TypeError):
        raise TransactionError(
            f"Amount {amount} is not a valid number."
            )
    
    # Step 2: check that the number is positive (greater than zero).

    if numeric_amount <= 0:
        raise TransactionError(
            f"Amount {amount} must be greater than zero."
            )
    
    # Step 3: check that the number is a multiple of NOTE_UNIT.

    if numeric_amount % NOTE_UNIT != 0:
        raise TransactionError(
            f"Amount {amount} must be a multiple of ₦{NOTE_UNIT}."
            )
    
    # Step 4: return the clean number as an integer (no decimal places).
    
    return int(numeric_amount)


# ---------------------------------------------------------------------------
# TODO 3: CHECK THE CUSTOMER'S ACCOUNT BALANCE
# ---------------------------------------------------------------------------

def check_balance(amount, account_balance):
    """Ensure the customer actually has enough money in their account.

    If `amount` is greater than `account_balance`, raise
    InsufficientFundsError with a clear message. Otherwise do nothing.
    """

    # Check if the requested amount exceeds the account balance.
    # If it does, raise InsufficientFundsError with a clear message.

    if amount > account_balance:
        raise InsufficientFundsError(
            f"Insufficient funds: requested ₦{amount}, available ₦{account_balance}."
            )
    

# ---------------------------------------------------------------------------
# TODO 4: CHECK THE AGENT'S FLOAT (CASH ON HAND)
# ---------------------------------------------------------------------------

def check_agent_float(amount, agent_float):
    """Ensure the POS Service Owner actually has enough cash to pay this out.

    Even if the customer's account is fine, the machine can only dispense
    cash it physically has. If `amount` is greater than `agent_float`, raise
    TransactionError. Otherwise do nothing.
    """

    # Check if the requested amount exceeds the agent's float.
    # If it does, raise InsufficientFundsError with a clear message.

    if amount > agent_float:
        raise InsufficientFundsError(
            f"Agent float insufficient: requested ₦{amount}, available ₦{agent_float}."
            )
    

    
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
    """

    # Calculate the fee based on the amount using integer division.

    fee = (amount // 5000) * 100
    return fee



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
    """

    # Start with the current float as the "new" float. If the transaction
    # fails, we will return this unchanged. If it succeeds, we will update it.

    new_float = agent_float

    try:
        # Read the request data and validate it. Each of these steps can raise
        # an exception, which will be caught by the appropriate except block.
        
        customer = request["customer"]
        amount = validate_amount(request["amount"])
        account_balance = request["account_balance"]
        
        check_balance(amount, account_balance)
        check_agent_float(amount, agent_float)

    except TransactionError as e:
        # The transaction was rejected due to a known issue (invalid amount,
        # insufficient funds, etc.). Print the reason.

        print(
            f"Transaction for {request.get('customer', 'Unknown')} rejected: {e}"
        )

    except KeyError as missing_key:
        # The request was missing a required key (customer, amount, or account_balance).

        print(
            f"Transaction for {request.get('customer', 'Unknown')} rejected: missing key {missing_key}"
        )

    except Exception as unexpected:
        # Catch-all for any other unexpected errors. Print the error message.
        # Intentionally comes LAST so it does not override the more specific exceptions above.

        print(
            f"Transaction for {request.get('customer', 'Unknown')} failed due to unexpected error: {unexpected}"
        )

    else:
        # No exceptions occurred, so the transaction is approved. Charge the fee,
        # reduce the float, and print the approval message.

        fee = charge_fee(amount)
        new_float -= amount
        print(
            f"Transaction for {customer} approved: ₦{amount} withdrawn, fee ₦{fee}, new float ₦{new_float}"
        )

    finally:
        # Always print that the transaction has ended, regardless of success or failure.

        print("--- Transaction Ended ---")

    return new_float


# ---------------------------------------------------------------------------
# TODO 7: MAIN — run the whole day
# ---------------------------------------------------------------------------

def main():
    """Run the POS terminal for a day, processing all cash-out requests."""

    # Opening Amount
    agent_float = OPENING_FLOAT

    # Two simple counters to tally how the day went.
    successes = 0
    failures = 0

    print("POS Terminal Started")
    print(f"Opening Amount: ₦{agent_float}")

    for request in CASHOUT_REQUESTS:
        # Display current customer details.
        # .get() so a missing name does not crash the program.

        name = request.get("customer", "Unknown")
        phone = request.get("phone", "Unknown")
        amount = request.get("amount", "Unknown")
        print(
            f"\nProcessing cashout request for {name} (Phone: {phone}, Amount: {amount})"
        )

        # Remember the float before this attempt, to track
        # if changes were actually made. (i.e. The Transaction Succeeded)

        old_float = agent_float
        agent_float = process_cashout(request, agent_float)

        if agent_float != old_float:
            successes += 1
        else:
            failures += 1

        print(
            f"Current float after transaction: ₦{agent_float}"
        )

    # print the end-of-day summary (Successes, Failures, Final Float(Amount))
    print("\nEnd-of-Day Summary:")
    print(f"Successes: {successes}")
    print(f"Failures: {failures}")
    print(f"Final float: ₦{agent_float}")


# Launch the program

if __name__ == "__main__":
    main()