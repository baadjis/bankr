from back.bankr.models.transaction import Transaction


def get_transactions(query=None,since_date=None,limits=10):
    transactions=Transaction.select()
    if query is not None:
        transactions=transactions.where(Transaction.label.contains(query))

    if since_date is not None:
        transactions=transactions.where(Transaction.date >= since_date)
    if len(transactions)>int(limits):
        transactions=transactions.limit(limits)
    return [transaction.get_small_data() for transaction in transactions]
