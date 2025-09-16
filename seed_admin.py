from backend.apis import AccountAPI

result = AccountAPI.create_account(
    name='admin',
    phone='+11111111111',
    email='admin@smartpos.com',
    password='1234'
)

if result['success']:
    print(result['account'])
    print('Admin seeded successfully')
else:
    print(result['error'])
