from flask import Flask
from sqlalchemy.exc import OperationalError

from src.database.models.customers import CustomerDetails
from src.database.sql.customer import CustomerDetailsORM
from src.controller import Controllers, error_handler
from src.database.models.bank_accounts import BankAccount
from src.database.models.contacts import Address, PostalAddress, Contacts
from src.database.sql.bank_account import BankAccountORM
from src.database.sql.contacts import AddressORM, PostalAddressORM, ContactsORM


class CustomerController(Controllers):

    def __init__(self):
        super().__init__()

        self.countries = [
            "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde",
            "Cameroon", "Central African Republic", "Chad", "Comoros",
            "Democratic Republic of the Congo", "Republic of the Congo", "Djibouti",
            "Equatorial Guinea", "Eritrea", "Ethiopia", "Gabon", "Gambia", "Ghana",
            "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia",
            "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Mozambique",
            "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe",
            "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa",
            "South Sudan", "Sudan", "Swaziland", "Tanzania", "Togo", "Uganda",
            "Zambia", "Zimbabwe"
        ]

    def init_app(self, app: Flask):
        super().init_app(app=app)

    async def add_personal_details(self, customer_details: CustomerDetails):
        with self.get_session() as session:
            # Query the database for the customer details
            customer_orm = session.query(CustomerDetailsORM).filter_by(customer_id=customer_details.customer_id).first()
            if customer_orm:
                # Update the existing customer details
                customer_orm.uid = customer_details.uid
                customer_orm.full_names = customer_details.full_names
                customer_orm.email = customer_details.email
                customer_orm.contact_number = customer_details.contact_number

                customer_orm.date_joined = customer_details.date_joined
                customer_orm.is_active = customer_details.is_active
                customer_orm.address_id = customer_details.address_id
                customer_orm.contact_id = customer_details.contact_id
                customer_orm.postal_id = customer_details.postal_id
                customer_orm.bank_account_id = customer_details.bank_account_id
            else:
                # Create a new customer entry
                customer_orm = CustomerDetailsORM(
                    customer_id=customer_details.customer_id,
                    uid=customer_details.uid,
                    full_names=customer_details.full_names,
                    email=customer_details.email,
                    contact_number=customer_details.contact_number,

                    date_joined=customer_details.date_joined,
                    is_active=customer_details.is_active,
                    address_id=customer_details.address_id,
                    contact_id=customer_details.contact_id,
                    postal_id=customer_details.postal_id,
                    bank_account_id=customer_details.bank_account_id
                )
                session.add(customer_orm)
            session.commit()
            return customer_details

    @error_handler
    async def add_update_address(self, address: Address) -> Address | None:
        """

        :param address:
        :return:
        """
        with self.get_session() as session:
            branch_address_orm = session.query(AddressORM).filter_by(address_id=address.address_id).first()

            if isinstance(branch_address_orm, AddressORM):
                if address.street:
                    branch_address_orm.street = address.street
                if address.city:
                    branch_address_orm.city = address.city
                if address.state_province:
                    branch_address_orm.state_province = address.state_province
                if address.postal_code:
                    branch_address_orm.postal_code = address.postal_code
                session.commit()
                return address
            try:
                session.add(AddressORM(**address.dict()))
                session.commit()
                return address
            except OperationalError as e:
                print(str(e))
                return None

    @error_handler
    async def get_address(self, address_id: str) -> Address | None:
        with self.get_session() as session:
            branch_address = session.query(AddressORM).filter_by(address_id=address_id).first()
            if isinstance(branch_address, AddressORM):
                return Address(**branch_address.to_dict())
            return None

    @error_handler
    async def add_postal_address(self, postal_address: PostalAddress) -> PostalAddress | None:
        """

        :param postal_address:
        :return:
        """
        with self.get_session() as session:

            _postal_id = postal_address.postal_id
            branch_postal_orm = session.query(PostalAddressORM).filter_by(postal_id=_postal_id).first()

            if isinstance(branch_postal_orm, PostalAddressORM):
                if postal_address.address_line_1:
                    branch_postal_orm.address_line_1 = postal_address.address_line_1
                if postal_address.town_city:
                    branch_postal_orm.town_city = postal_address.town_city
                if postal_address.province:
                    branch_postal_orm.province = postal_address.province
                if postal_address.country:
                    branch_postal_orm.country = postal_address.country
                if postal_address.postal_code:
                    branch_postal_orm.postal_code = postal_address.postal_code
                session.commit()
                return postal_address

            session.add(PostalAddressORM(**postal_address.dict()))
            session.commit()
            return postal_address

    @error_handler
    async def get_postal_address(self, postal_id: str) -> PostalAddress | None:
        """

        :param postal_id:
        :return:
        """
        with self.get_session() as session:
            postal_address_orm = session.query(PostalAddressORM).filter_by(postal_id=postal_id).first()
            if isinstance(postal_address_orm, PostalAddressORM):
                return PostalAddress(**postal_address_orm.to_dict())
            return None

    @error_handler
    async def add_contacts(self, contact: Contacts) -> Contacts | None:
        """
        Add branch contacts to the database.

        :param contact: Instance of Contacts containing contact details.
        :return: Added Contacts instance if successful, None otherwise.
        """
        with self.get_session() as session:
            contact_orm = session.query(ContactsORM).filter_by(contact_id=contact.contact_id).first()
            if isinstance(contact_orm, ContactsORM):
                # Update existing contact details
                if contact.cell:
                    contact_orm.cell = contact.cell
                if contact.tel:
                    contact_orm.tel = contact.tel
                if contact.email:
                    contact_orm.email = contact.email
                if contact.facebook:
                    contact_orm.facebook = contact.facebook
                if contact.twitter:
                    contact_orm.twitter = contact.twitter
                if contact.whatsapp:
                    contact_orm.whatsapp = contact.whatsapp
                session.commit()
                return contact
            # Add new contact details
            session.add(ContactsORM(**contact.dict()))
            session.commit()
            return contact

    @error_handler
    async def get_contact(self, contact_id: str) -> Contacts | None:
        """
        Retrieve branch contact details from the database.

        :param contact_id: The ID of the branch whose contact details to retrieve.
        :return: Contacts instance if found, None otherwise.
        """
        with self.get_session() as session:
            # Query the database for the contact details associated with the given branch_id
            branch_contact_orm = session.query(ContactsORM).filter_by(contact_id=contact_id).first()

            if isinstance(branch_contact_orm, ContactsORM):
                # If contact details exist, create a Contacts instance from the retrieved data
                branch_contact = Contacts(**branch_contact_orm.to_dict())
                return branch_contact

            return None

    @error_handler
    async def get_countries(self):
        return self.countries
