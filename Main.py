from registrationWindow import Ui_regWin
from clientWindow import Ui_clientWin 
from ChatBox import Ui_chatBox
#from CommWin import Ui_NetWindow
from PyQt5 import QtCore,QtWidgets
import socket
import funcs
import sys
import threading
import queue
sockLock = threading.Lock()
clientSock = ''
hostUserName =''
hostUserNo = ''
hostMacAdress = ''
HOST = '192.168.1.101'
PORT = funcs.PORT

class readingThread(QtCore.QThread):

	sendingCompleteSignal = QtCore.pyqtSignal(str)

	def __init__(self,sock,uno,fno,rno,uname,fname,parent = None):
		super(readingThread,self).__init__(parent)
		self.parent = parent
		self.clientSock = sock
		self.roomNo = rno
		self.fileName = fname
		self.hostUserNo = uno
		self.fileNo = fno
		self.hostUserName = uname
		self.f = open(self.fileName,'rb')
		with sockLock:
			print("Sending - "+self.roomNo+self.fileName+" "+self.hostUserName)
			funcs.send_message(self.clientSock,self.hostUserNo,self.roomNo+self.fileName+" "+self.hostUserName,self.fileNo)	# sent first signal

class writingThread(QtCore.QThread):
	
	completeSignal = QtCore.pyqtSignal(str,str,str)

	def __init__(self,msg,q,key,parent = None):
		super(writingThread,self).__init__(parent)
		self.parent = parent
		self.key = key
		msg = msg.split(' ')
		self.fileName = msg[0]
		self.senderName = msg[1]
		self.q = q
		self.f = open(self.fileName,'wb')
		print("file "+msg[0]+ " from "+msg[1]+" opened in writing thread")

	def __del__(self):
		self.wait()
	
	def run(self):
		while True:
			data = self.q.get()
			if data == None:
				break
			self.f.write(data)
		self.f.close()
		print("File "+self.fileName+" from "+self.senderName+" completed")
		self.completeSignal.emit(self.key,self.fileName,self.senderName)
	
		
