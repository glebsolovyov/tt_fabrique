import os

MAILING_NUMBER_OF_ATTEMPTS=5
MAILING_TIME_SLEEP=5


API_TOKEN=os.environ.get('API_TOKEN')

INCORRECT_MOBILE_OPERATOR_CODES = ['907', '935', '943', '944', '945', '946', '947', '948', '949', '959', '972', '973',
                                   '974', '975', '976', '990']