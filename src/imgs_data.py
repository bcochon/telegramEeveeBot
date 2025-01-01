import os
import win32com.client
from params import IMGS_DIR

currdir = os.getcwd()
pathImgs = os.path.join(currdir.removesuffix('src'), IMGS_DIR.removeprefix('../'))
pathEevee = os.path.join(pathImgs, 'eevee')

sh = win32com.client.gencache.EnsureDispatch('Shell.Application',0)
ns = sh.NameSpace(pathEevee)

def date_formatter(rawdate) :
    dmy = rawdate.split('/')
    d = '{:02}'.format(int(dmy[0]))
    m = '{:02}'.format(int(dmy[1]))
    y = '{:04}'.format(int(dmy[2]))
    return f'{y}-{m}-{d}'

imgs_dict = {}

if ns :
    for item in ns.Items():
        completeDate=ns.GetDetailsOf(item, 3)
        if completeDate:
            date = date_formatter(completeDate.split()[0])
            imgs_dict.update({item.Name : date})

# dates = list(map((lambda date : date[5:]), imgs_dict.values()))

# print(list(filter(lambda date : date == '31-12', dates)))