import asyncio
from indy import pool, wallet, ledger, signus
from indy.error import IndyError
import json


def print_did_verkey(did, verkey, label):
    print('%s_did: %s, %s_verkey: %s' % (label, did, label, verkey))


async def main(pool_name, pool_genesis_txn_path, seed_trustee1):
    # 1. Create ledger config from genesis txn file
    pool_config = json.dumps({"genesis_txn": str(pool_genesis_txn_path)})
    try:
        await pool.create_pool_ledger_config(pool_name, pool_config)
    except IndyError:
        pass

    # 2. Open pool ledger
    pool_handle = await pool.open_pool_ledger(pool_name, None)

    # 3. Create My Wallet and Get Wallet Handle
    try:
        await wallet.create_wallet(pool_name, 'my_wallet', None, None, None)
    except IndyError:
        pass
    my_wallet_handle = await wallet.open_wallet('my_wallet', None, None)

    # 4. Create Their Wallet and Get Wallet Handle
    try:
        await wallet.create_wallet(pool_name, 'their_wallet', None, None, None)
    except IndyError:
        pass
    their_wallet_handle = await wallet.open_wallet('their_wallet', None, None)

    # 5. Create My DID
    (my_did, my_verkey) = await signus.create_and_store_my_did(my_wallet_handle, "{}")

    # 6. Create Their DID from Trustee1 seed
    (their_did, their_verkey) = await signus.create_and_store_my_did(their_wallet_handle,
                                                                  json.dumps({"seed": seed_trustee1}))

    print_did_verkey(my_did, my_verkey, 'my')
    print_did_verkey(their_did, their_verkey, 'their')
    # 7. Store Their DID

    await signus.store_their_did(my_wallet_handle, json.dumps({'did': their_did, 'verkey': their_verkey}))
    print('Their_did: %s' % their_did)

    # 8. Prepare and send NYM transaction
    nym_txn_req = await ledger.build_nym_request(their_did, my_did, None, None, None)
    ledger.sign_and_submit_request(pool_handle, their_wallet_handle, their_did, nym_txn_req)

    # 9. Prepare and send GET_NYM request
    get_nym_txn_req = await ledger.build_get_nym_request(their_did, 'fxae8eMr1w1tTW4GvqFhN')
    get_nym_txn_resp = await ledger.submit_request(pool_handle, get_nym_txn_req)
    get_nym_txn_resp = json.loads(get_nym_txn_resp)
    print(get_nym_txn_resp)
    assert get_nym_txn_resp['dest'] == 'fxae8eMr1w1tTW4GvqFhN'

    set_attr_request = await signus.set_endpoint_for_did(their_wallet_handle, their_did, '1.2.3', their_verkey)
    set_attr_response = await ledger.submit_request(pool_handle, set_attr_request)
    print(set_attr_response)

    # get_endpoint_request = await ledger.build_get_attrib_request(their_did, my_did, 'endpoint')
    # get_endpoint_response =  await ledger.submit_request(pool_handle, get_endpoint_request)
    # print(get_endpoint_response)

    # metadata_request  = ledger.build_get_attrib_request(their_did, my_did)
    # metadata_response = await ledger.submit_request(pool_handle, metadata_request)
    # print(metadata_response)


    print(get_nym_txn_resp)

    assert get_nym_txn_resp['result']['dest'] == my_did

    # 10. Close wallets and pool
    await wallet.close_wallet(their_wallet_handle)
    await wallet.close_wallet(my_wallet_handle)
    await pool.close_pool_ledger(pool_handle)

if __name__ == '__main__':
    pool_name = "pool1"
    pool_genesis_txn_path = '/var/lib/indy/verity-dev/pool_transactions_genesis'
    seed ='000000000000000000000000Issuer08'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(pool_name=pool_name, pool_genesis_txn_path=pool_genesis_txn_path, seed_trustee1=seed))