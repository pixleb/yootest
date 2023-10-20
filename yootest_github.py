# yookassa
from yookassa import Configuration, Payment

# program modules
from singleton import Singleton

# system
import os, sys

# misc imports
import uuid, json, logging, asyncio

class YooKassaExampleApp(Singleton):

    @classmethod
    def __init__(self) -> None:
        self.account_id: int = 123456
        
        self.secret_key: str = 'your secret key'
        
        self.python_incompatible_message: str = 'Incompatible Python version (requires Python 3.4 + )'
        self.success_message: str = 'Payment done successfully.'
        self.failed_message: str = 'Payment failed!'
        
        self.python_version: sys.version_info = sys.version_info
            
        self.payment_config: dict = {
            'amount': {
                'value': '100.00',
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': '127.0.0.1:8000'
            },
            'capture': True,
            'description': 'Тестовый заказ'
        }
        
        
        if (self.python_version.major < 3 or self.python_version.minor < 4):
            raise SystemError(self.python_incompatible_message)
        
        logging.basicConfig(level = logging.INFO, filename = 'yoolog.txt')
        logging.info('Application created, logging started.')
    
        Configuration.account_id: int = self.account_id
        Configuration.secret_key: str = self.secret_key

    
    # asynchronously waiting payment
    @classmethod
    def __update_payment_status(self) -> str:
        payment = json.loads(
            Payment.find_one(
                self.payment_id
            ).json()
        )
        return payment['status']
    
    @classmethod
    async def __await_pending(self) -> None:
        seconds_awaited: int = 0
        while self.__update_payment_status() == 'pending': 
            logging.info('waiting %d second(s)...' % seconds_awaited)
            seconds_awaited += 1
            await asyncio.sleep(1)

        if self.__update_payment_status() == 'succeeded': logging.info(self.success_message)
        else: logging.critical(self.failed_message)
    
    # entry point
    @classmethod
    def run(self) -> None:
        self.payment = json.loads(
            Payment.create(
                self.payment_config, 
                uuid.uuid4()
            ).json()
        )
        
        self.payment_id = self.payment['id']

        confirm_link = self.payment['confirmation']['confirmation_url']
        logging.info(f'Confirmation link is {confirm_link}')

        os.system(f'start "" "{confirm_link}"')
        
        # python 3.4 - 3.7
        if self.python_version.minor < 8:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.__await_pending())
            return 
        # python 3.8+
        asyncio.run(self.__await_pending())

if __name__ == '__main__':
    app: YooKassaExampleApp = YooKassaExampleApp()
    app.run()
