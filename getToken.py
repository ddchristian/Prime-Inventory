import base64
import getpass


userId = input('Username:')
passwd = getpass.getpass()
userPass = userId + ':' + passwd
base64Val = base64.b64encode(userPass.encode())
primeAuthToken = base64Val.decode()
print('Your Base64 Encoded token is: \n', primeAuthToken)


