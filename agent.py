import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


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

NOTE_UNIT = 100

OPENING_FLOAT = 50000 # 50,000 Naira


class TransactionError(Exception):
    """Custom exception for transaction errors."""
    pass

class InsufficientFundsError(TransactionError):
    """Raised when the account balance is insufficient for the requested amount."""
    pass


def validate_amount(amount):

    try:
        numeric_amount = float(amount)
    except (ValueError, TypeError):
        raise TransactionError(
            f"Amount {amount} is not a valid number."
            )
    
    if numeric_amount <= 0:
        raise TransactionError(
            f"Amount {amount} must be greater than zero."
            )
    
    if numeric_amount % NOTE_UNIT != 0:
        raise TransactionError(
            f"Amount {amount} must be a multiple of ₦{NOTE_UNIT}."
            )
    
    return int(numeric_amount)


def check_balance(amount, account_balance):

    if amount > account_balance:
        raise InsufficientFundsError(
            f"Insufficient funds: requested ₦{amount}, available ₦{account_balance}."
            )
    

def check_agent_float(amount, agent_float):

    if amount > agent_float:
        raise InsufficientFundsError(
            f"Agent float insufficient: requested ₦{amount}, available ₦{agent_float}."
            )
    

def charge_fee(amount):

    fee = (amount // 5000) * 100
    return fee


def process_cashout(request, agent_float):

    new_float = agent_float

    try:
        customer = request["customer"]
        amount = validate_amount(request["amount"])
        account_balance = request["account_balance"]
        
        check_balance(amount, account_balance)
        check_agent_float(amount, agent_float)

    except TransactionError as e:
        print(
            f"Transaction for {request.get('customer', 'Unknown')} rejected: {e}"
        )

    except KeyError as missing_key:
        print(
            f"Transaction for {request.get('customer', 'Unknown')} rejected: missing key {missing_key}"
        )

    except Exception as unexpected:
        print(
            f"Transaction for {request.get('customer', 'Unknown')} failed due to unexpected error: {unexpected}"
        )

    else:
        fee = charge_fee(amount)
        new_float -= amount
        print(
            f"Transaction for {customer} approved: ₦{amount} withdrawn, fee ₦{fee}, new float ₦{new_float}"
        )

    finally:
        print("--- transaction ended ---")

    return new_float


def main():

    agent_float = OPENING_FLOAT

    successes = 0
    failures = 0

    print("POS Terminal Started")
    print(f"Opening float: ₦{agent_float}")

    for request in CASHOUT_REQUESTS:
        
        name = request.get("customer", "Unknown")
        phone = request.get("phone", "Unknown")
        amount = request.get("amount", "Unknown")
        print(
            f"\nProcessing cashout request for {name} (Phone: {phone}, Amount: {amount})"
        )

        old_float = agent_float
        agent_float = process_cashout(request, agent_float)

        if agent_float != old_float:
            successes += 1
        else:
            failures += 1

        print(
            f"Current float after transaction: ₦{agent_float}"
        )

    print("\nEnd-of-Day Summary:")
    print(f"Successes: {successes}")
    print(f"Failures: {failures}")
    print(f"Final float: ₦{agent_float}")

if __name__ == "__main__":
    main()