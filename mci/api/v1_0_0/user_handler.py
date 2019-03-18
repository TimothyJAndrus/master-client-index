"""User Handler

Handle user endpoint requests from the API.

"""


class UserHandler(object):
    """User Handler

    """

    def get_all_users(self):
        """ Retrireve all users. """

        return [
            {
                'mci_id': '1qaz2wsx',
                'first_name': 'John',
                'last_name': 'Doe'
            },
            {
                'mci_id': '2ws3edc',
                'first_name': 'Jane',
                'last_name': 'Smith'
            },
            {
                'mci_id': '456tgv',
                'first_name': 'Arnold',
                'last_name': 'Stiffelbacher'
            }
        ]
