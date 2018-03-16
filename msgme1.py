import asyncio
import time
import json
import re

# Hack to force us to use the latest and greatest indy bits
import sys
sys.path.insert(0, '/src/indy-sdk/wrappers/python')
from indy import crypto, wallet
from indy import signus as did
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARN)

pool_name = 'pool1'

async def main():
    await demo()

async def prep(wallet_handle, my_vk, their_vk, msg):
    with open('/home/vagrant/input.txt', 'rb') as f:
        msg = f.read()
    encrypted = await crypto.auth_crypt(wallet_handle, my_vk, their_vk, msg)
    print('encrypted = %s' % repr(encrypted))
    with open('msg.txt', 'wb') as f:
        f.write(bytes(encrypted))
    print('prepping %s' % msg)

async def init():
    me = input('Who are you? ').strip()
    wallet_name = '%s-wallet' % me

    # 1. Create Wallet and Get Wallet Handle
    try:
        await wallet.create_wallet(pool_name, wallet_name, None, None, None)
    except:
        pass
    wallet_handle = await wallet.open_wallet(wallet_name, None, None)
    print('wallet = %s' % wallet_handle)

    (my_did, my_vk) = await did.create_and_store_my_did(wallet_handle, "{}")
    print('my_did and verkey = %s %s' % (my_did, my_vk))

    their = input("Other party's DID and verkey? ").strip().split(' ')
    return wallet_handle, my_did, my_vk, their[0], their[1]

async def read(wallet_handle, my_vk):
    with open('msg.txt', 'rb') as f:
        encrypted = f.read()
    decrypted = await crypto.auth_decrypt(wallet_handle, my_vk, encrypted)
    print(decrypted)


async def demo():
    wallet_handle, my_did, my_vk, their_did, their_vk = await init()

    while True:
        argv = input('> ').strip().split(' ')
        cmd = argv[0].lower()
        rest = ' '.join(argv[1:])
        if re.match(cmd, 'prep'):
            await prep(wallet_handle, my_vk, their_vk, rest)
        elif re.match(cmd, 'read'):
            await read(wallet_handle, my_vk)
            print('reading')
        elif re.match(cmd, 'connect'):
            print('connect')
        elif re.match(cmd, 'quit'):
            break
        else:
            print('Huh?')


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        time.sleep(1)  # FIXME waiting for libindy thread complete
    except KeyboardInterrupt:
        print('')
