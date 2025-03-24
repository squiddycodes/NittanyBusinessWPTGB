import pandas as pd
import hashlib

#file = pd.read_csv('Users.csv')#read csv

#file['password'] = file['password'].apply(lambda x: \
#    hashlib.sha256(x.encode('utf-8')).hexdigest())#hash "password" column

#file.to_csv('Users.csv', index=False)#write finished file

import hashlib
testpw = "TbIF16hoUqGl"
hashedpw = hashlib.sha256(testpw.encode('utf-8')).hexdigest()
print(y)