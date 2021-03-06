# -*- coding: utf-8 -*-
from .LineApi import LineApi
from .LineServer import url
from .LineCallback import LineCallback
from ..LineThrift.ttypes import Message
import json, requests, tempfile, shutil
import unicodedata
from random import randint

try:
    from thrift.protocol import fastbinary
except:
    fastbinary = None

def loggedIn(func):
     def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other("you want to call the function, you must login to LINE!!!!!")
     return checkLogin

class LineClient(LineApi):

    def __init__(self):
        LineApi.__init__(self)
        self._messageReq = {}
        self._session = requests.session()
        self._headers = url.Headers

    @loggedIn
    def _loginresult(self):
        if self.isLogin == True:
            print "\nVodkamod-Bot\n"
            print "-------------------------------------------------\nCredit :\nBot ini berdasarkan dari script LineVodka\nmilik merkremont dan di modding oleh Bamzky,\nOleh sebab itu jika mau mengedit botnya\nharap izin dulu ke\nid line : bamaseptituta\n\nTerima Kasih,\nBamzky\n-------------------------------------------------\n"
            print "Kode Token : " + self.authToken + "\n"
            print "Sertifikasi : " + self.certificate + "\n"
            """:type profile: Profile"""
            profile = self._client.getProfile()
            print "Nama : " + profile.displayName
            print "Bio : " + profile.statusMessage + "\n\n"
        else:
            print "Harus Login!\n"

    @loggedIn
    def post_content(self, urls, data=None, files=None):
        return self._session.post(urls, headers=self._headers, data=data, files=files)

    """Image"""

    @loggedIn
    def sendImage(self, path):
        """Send a image
        :param path: local path of image to send
        """
        message = Message(to=self.id, text=None)
        message.contentType = ContentType.IMAGE
        message.contentPreview = None
        message.contentMetadata = None

        message_id = self._client.sendMessage(message).id
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
            'oid': message_id,
            'size': len(open(path, 'rb').read()),
            'type': 'image',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self._client.post_content('https://os.line.naver.jp/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload image failure.')
        #r.content
        return True

    @loggedIn
    def sendImageWithURL(self, to_, url):
        path = '%s/pythonLine-%i.data' % (tempfile.gettempdir(), randint(0, 9))
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path, 'w') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            raise Exception('Download image failure.')
        try:
            self.sendImage(to_, path)
        except Exception as e:
            raise e
          
    @loggedIn
    def getHome(self, mid):
        header = {
                    "Content-Type": "application/json",
                    "User-Agent" : self.UA,
                    "X-Line-Mid" : self.mid,
                    "x-lct" : self.channel_access_token,
        }

    @loggedIn
    def getCover(self, mid):
        h = self.getHome(mid)
        objId = h["result"]["homeInfo"]["objectId"]
        return "http://dl.profile.line-cdn.net/myhome/c/download.nhn?userid=" + mid + "&oid=" + objId
    
    """User"""

    @loggedIn
    def getProfile(self):
        return self._client.getProfile()

    @loggedIn
    def getSettings(self):
        return self._client.getSettings()

    @loggedIn
    def getUserTicket(self):
        return self._client.getUserTicket()

    @loggedIn
    def updateProfile(self, profileObject):
        return self._client.updateProfile(0, profileObject)

    @loggedIn
    def updateSettings(self, settingObject):
        return self._client.updateSettings(0, settingObject)

    """Operation"""

    @loggedIn
    def fetchOperation(self, revision, count):
        return self._client.fetchOperations(revision, count)

    @loggedIn
    def getLastOpRevision(self):
        return self._client.getLastOpRevision()

    """Message"""

    @loggedIn
    def sendEvent(self, messageObject):
        return self._client.sendEvent(0, messageObject)

    @loggedIn
    def sendMessage(self, messageObject):
        return self._client.sendMessage(0,messageObject)

    def getLastReadMessageIds(self, chatId):
        return self._client.getLastReadMessageIds(0,chatId)

    """Image"""

    @loggedIn
    def post_content(self, url, data=None, files=None):
        return self._session.post(url, headers=self._headers, data=data, files=files)

    """Contact"""

    @loggedIn
    def blockContact(self, mid):
        return self._client.blockContact(0, mid)

    @loggedIn
    def unblockContact(self, mid):
        return self._client.unblockContact(0, mid)

    @loggedIn
    def findAndAddContactsByMid(self, mid):
        return self._client.findAndAddContactsByMid(0, mid)

    @loggedIn
    def findAndAddContactsByUserid(self, userid):
        return self._client.findAndAddContactsByUserid(0, userid)

    @loggedIn
    def findContactsByMid(self, mid):
        return self._client.findContactsByMid(mid)
    
    @loggedIn
    def findContactsByUserid(self, userid):
        return self._client.findContactByUserid(userid)

    @loggedIn
    def findContactByTicket(self, ticketId):
        return self._client.findContactByUserTicket(ticketId)

    @loggedIn
    def getAllContactIds(self):
        return self._client.getAllContactIds()

    @loggedIn
    def getBlockedContactIds(self):
        return self._client.getBlockedContactIds()

    @loggedIn
    def getContact(self, mid):
        return self._client.getContact(mid)

    @loggedIn
    def getContacts(self, midlist):
        return self._client.getContacts(midlist)

    @loggedIn
    def getFavoriteMids(self):
        return self._client.getFavoriteMids()

    @loggedIn
    def getHiddenContactMids(self):
        return self._client.getHiddenContactMids()


    """Group"""

    @loggedIn
    def acceptGroupInvitation(self, groupId):
        return self._client.acceptGroupInvitation(0, groupId)

    @loggedIn
    def acceptGroupInvitationByTicket(self, groupId, ticketId):
        return self._client.acceptGroupInvitationByTicket(0, groupId, ticketId)

    @loggedIn
    def cancelGroupInvitation(self, groupId, contactIds):
        return self._client.cancelGroupInvitation(0, groupId, contactIds)

    @loggedIn
    def createGroup(self, name, midlist):
        return self._client.createGroup(0, name, midlist)

    @loggedIn
    def getGroup(self, groupId):
        return self._client.getGroup(groupId)

    @loggedIn
    def getGroups(self, groupIds):
        return self._client.getGroups(groupIds)

    @loggedIn
    def getGroupIdsInvited(self):
        return self._client.getGroupIdsInvited()

    @loggedIn
    def getGroupIdsJoined(self):
        return self._client.getGroupIdsJoined()

    @loggedIn
    def inviteIntoGroup(self, groupId, midlist):
        return self._client.inviteIntoGroup(0, groupId, midlist)

    @loggedIn
    def kickoutFromGroup(self, groupId, midlist):
        return self._client.kickoutFromGroup(0, groupId, midlist)

    @loggedIn
    def leaveGroup(self, groupId):
        return self._client.leaveGroup(0, groupId)

    @loggedIn
    def rejectGroupInvitation(self, groupId):
        return self._client.rejectGroupInvitation(0, groupId)

    @loggedIn
    def reissueGroupTicket(self, groupId):
        return self._client.reissueGroupTicket(groupId)

    @loggedIn
    def updateGroup(self, groupObject):
        return self._client.updateGroup(0, groupObject)

    """Room"""

    @loggedIn
    def createRoom(self, midlist):
        return self._client.createRoom(0, midlist)

    @loggedIn
    def getRoom(self, roomId):
        return self._client.getRoom(roomId)

    @loggedIn
    def inviteIntoRoom(self, roomId, midlist):
        return self._client.inviteIntoRoom(0, roomId, midlist)

    @loggedIn
    def leaveRoom(self, roomId):
        return self._client.leaveRoom(0, roomId)

    """unknown function"""

    @loggedIn
    def noop(self):
        return self._client.noop()
