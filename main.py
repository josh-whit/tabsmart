# TabSmart: takes input from a user to calculate how much each person owes when dining out,
#           taking into account tip and tax and divvying it up proportional to the size of their orders.
#
#           Helpful for large parties when everyone orders different things and one person puts their card down.


def calc_total_bill(orders, tax_percent, tip_percent):
    """Calculates the total bill, taking orders (dict) and tax and tip (floats)
    as params and returning the total bill (float)"""
    total_amount = sum(orders.values())
    tax_amount = total_amount * (tax_percent / 100)
    tip_amount = total_amount * (tip_percent / 100)
    total_bill = total_amount + tax_amount + tip_amount
    return total_bill


def calc_individual_shares(orders, tax_percent, tip_percent):
    """Calculates each diner's share of the bill.
    Takes orders (dict), tax and tip (float) as params.
    Returns dict with diners as keys (str) and their share of the bill as value (float)"""
    total_bill = calc_total_bill(orders, tax_percent, tip_percent)
    individual_shares = {}
    total_order_value = sum(orders.values())

    for diner, order_value in orders.items():
        diner_share = (order_value / total_order_value) * total_bill
        individual_shares[diner] = diner_share

    return individual_shares


def main():
    num_diners = int(input("Enter the number in your party: "))
    orders = {}

    for i in range(num_diners):
        diner_name = input(f"Enter name {i + 1}: ")
        order_amount = input(f"Enter the order amounts for {diner_name} (separated by commas): ")
        order_values = [float(amount.strip()) for amount in order_amount.replace(",", " ").split()]
        orders[diner_name] = (sum(order_values))

    tax_percent = float(input(f"Enter the % tax (e.g. 8.5): "))
    tip_percent = float(input(f"Enter the % tip (e.g. 20): "))

    individual_shares = calc_individual_shares(orders, tax_percent, tip_percent)
    total_bill = calc_total_bill(orders, tax_percent, tip_percent)
    total_amount = sum(orders.values())
    tip_amount = total_amount * (tip_percent / 100)

    print(f"\nTip ({tip_percent}%): ${tip_amount:.2f}")
    print(f"Total bill: ${total_bill:.2f}")
    for diner, share in individual_shares.items():
        print(f"{diner} owes: ${share:.2f}")


if __name__ == "__main__":
    main()
