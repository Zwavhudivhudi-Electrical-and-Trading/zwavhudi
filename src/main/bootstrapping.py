
def bootstrapper():
    from src.database.sql.user import UserORM,  PayPalORM
    from src.database.sql.bank_account import BankAccountORM
    from src.database.sql.contacts import AddressORM, PostalAddressORM, ContactsORM

    classes_to_create = [UserORM, PayPalORM, BankAccountORM, AddressORM, PostalAddressORM, ContactsORM]

    for cls in classes_to_create:
        cls.create_if_not_table()
