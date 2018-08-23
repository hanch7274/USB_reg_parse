import os
import sys
import winreg

usbstor = 'SYSTEM\\ControlSet001\\Enum\\USB\\'
varReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
#varKey = winreg.OpenKey(varReg,usbstor)
key = ''

def get_usbList():
    dev_num = 0
    usb_list = list()
    try:
        while True:
            varKey = winreg.OpenKey(varReg,usbstor) #키 선택
            usb_list.append(winreg.EnumKey(varKey,dev_num)) #키 출력
            dev_num+=1
    except OSError:
        return usb_list[2:]
    
def get_dev(vid,pid):
	with open('C:\\Users\\hanch\\Desktop\\usb.ids.txt','rb') as f:
		while True:
			if f.read(4).decode() == vid: #vid 찾으면
				vendor = f.readline()[2:].decode()
				#pid 탐색
				if f.read(1).decode() != '\t': #바로 다음 vid가 나올경우
					return vendor.replace('\n',''),None
				else: #1개 이상의 PID가 있을경우
					while True: #PID 탐색
						if f.read(4).decode() == pid:
							product = f.readline()[2:].decode()
							return vendor.replace('\n',''),product.replace('\n','')
						else: #만약 pid가 아니라면
							f.readline() #그줄 건너뛰고 다음줄로이동
							if f.read(1).decode() != '\t': # PID가 한개만 있는 VID였을경우
								return vendor.replace('\n',''),None
							else: #PID가 2개 이상일경우
								if f.read(4).decode() == pid:
									product = f.readline()[2:].decode()
									return vendor.replace('\n',''),product.replace('\n','')
								else:
									f.readline()
									if f.read(1).decode() == '\t':
									#다음PID가 더있다면
										continue
									else:
										return vendor.replace('\n',''),None
			else: #vid 못찾으면
				temp = f.readline()
				try:
					temp.decode()
					while True:
						if f.read(1) == '\t':
							f.readline()
							continue
						else:
							f.seek(-1,1)
							break
				except UnicodeDecodeError:
					return None,None
usbList = get_usbList()
for key in usbList:
    vid = key.split('&')[0].split('_')[1].lower()
    pid = key.split('&')[1].split('_')[1].lower()
    print(vid+' / '+pid)
    print(get_dev(vid,pid))
