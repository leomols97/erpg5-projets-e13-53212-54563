import xmlrpc.client
from getpass import getpass


class OdooParser:
    def __init__(self):
        self.port = 8069
        self.url = f"http://localhost:{self.port}"
        self.db = "dev01"
        self.username = ''
        self.password = ''
        self.uid = None
        self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

    def ask_user_name(self):
        while not self.username:
            name = input("Username: ")
            self.username = name
            print()

    def ask_password(self):
        while not self.password:
            passwd = getpass("Password: ")
            self.password = passwd
            print()

    def _validate_uid(self):
        if self.username and self.password:
            self.uid = self.common.authenticate(
                self.db, self.username, self.password, {}
            )
            if not self.uid:
                raise RuntimeError("Wrong uid, please retry inserting credentials.")
        else:
            raise ValueError("Username and password aren't set.")

    def _check_access_rights(self):
        if self.models.execute_kw(
            self.db,
            self.uid,
            self.password,
            'realtor.apartment',
            'check_access_rights',
            ['read'],
            {'raise_exception': False},
        ):
            print("You have read rights on Realtor Apartments!\n")

    def _access_data(self, name):
        out = self.models.execute_kw(
            self.db,
            self.uid,
            self.password,
            'realtor.apartment',
            'search_read',
            [[['name', '=', name]]],
            {
                'fields': [
                    'name',
                    'availability_date',
                    'expected_price',
                    'apartment_area',
                    'terrace_area',
                    'total_area',
                    'user_id',
                ]
            },
        )
        if out:
            print("----------------------------------------")
            for apart in out:
                for k, v in apart.items():
                    print(f"{k:20} ==> {v}")
                print("----------------------------------------")
            print('\n')
        else:
            print("No such apartment under that name!\n")


def main():
    try:
        print(
            """
     =======================================
        Connection to the ODOO XML-RPC API

        Use Ctr-C to exit.
     =======================================
        \n"""
        )
        op = OdooParser()
        op.ask_user_name()
        op.ask_password()
        op._validate_uid()
        op._check_access_rights()

        while True:
            name = input("Enter an apartment name to look for it: ")
            op._access_data(name)

    except KeyboardInterrupt:
        print("\n\nBye!")
    except RuntimeError as e:
        print(e)


if __name__ == '__main__':
    main()
