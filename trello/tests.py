import json

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class TestTrello(APITestCase):
    def registerUser(self):
        # for create account user a
        self.client.post(reverse("user-register"), {
            "firstName": "a",
            "lastName": "a",
            "email": "a@gmail.com",
            "password": "aaaa9999",
            "confirmPassword": "aaaa9999"
        })
        # for create account user b
        self.client.post(reverse("user-register"), {
            "firstName": "b",
            "lastName": "b",
            "email": "b@gmail.com",
            "password": "bbbb9999",
            "confirmPassword": "bbbb9999"
        })

    def authenticate(self, email, password):
        # remove old credentials
        self.client.credentials(HTTP_AUTHORIZATION=None)
        # for get access token
        tokenUser = self.client.post(reverse('access-token'), {
            "email": email,
            "password": password
        })
        accessToken = tokenUser.data['access']

        credential = f"Bearer {accessToken}"
        self.client.credentials(HTTP_AUTHORIZATION=credential)

    def createBoard(self, board, statusCode, itemCheck=None):
        if itemCheck is None:
            response = self.client.post(reverse('board-list'), board)
            self.assertEqual(response.status_code, statusCode)
        else:
            response = self.client.post(reverse('board-list'), board)
            self.assertEqual(response.status_code, statusCode)
            self.assertEqual(response.data[itemCheck], board[itemCheck])

    def createList(self, listCreate, statusCode, itemCheck=None):
        if itemCheck is None:
            response = self.client.post(reverse('list-list'), listCreate)
            self.assertEqual(response.status_code, statusCode)
        elif itemCheck == 'boardId':
            response = self.client.post(reverse('list-list'), listCreate)
            self.assertEqual(response.status_code, statusCode)
            self.assertEqual(response.data['board'], listCreate['boardId'])
        else:
            response = self.client.post(reverse('list-list'), listCreate)
            self.assertEqual(response.status_code, statusCode)
            self.assertEqual(response.data[itemCheck], listCreate[itemCheck])

    def createCard(self, card, statusCode, itemCheck=None):
        if itemCheck is None:
            response = self.client.post(reverse('card-list'), card)
            self.assertEqual(response.status_code, statusCode)
        elif itemCheck == 'listId':
            response = self.client.post(reverse('card-list'), card)
            self.assertEqual(response.status_code, statusCode)
            self.assertEqual(response.data['list'], card['listId'])
        else:
            response = self.client.post(reverse('card-list'), card)
            self.assertEqual(response.status_code, statusCode)
            self.assertEqual(response.data[itemCheck], card[itemCheck])

    def checkUserLogin(self, email, userId):
        res = self.client.get(reverse('user-detail', args=(userId,)))
        self.assertEqual(email, res.data['email'])

    def checkObjectAccess(self, objectId, statusCode, urlName):
        responseStatusCode = self.client.get(reverse(urlName, args=(objectId,))).status_code
        self.assertEqual(responseStatusCode, statusCode)

    def setUp(self) -> None:
        self.registerUser()

        # Boards data
        self.validBoPu = {
            "title": "public board, creator is a@gmail.com",
            "visibility": "pu",
        }
        self.validBoPrAssignUser = {
            "title": "private board, creator is a@gmail.com",
            "visibility": "pr",
            "assignUsers": 2  # user 2 is user a@gmail.com
        }
        self.validBoPr = {
            "title": "private board, creator is a@gmail.com",
            "visibility": "pr",
        }

        # Lists data
        self.validListPuBo = {
            "title": "list in public board",
            "boardId": 1
        }
        self.ValidListPrBoAssignUser = {
            "title": "list in public board",
            "boardId": 2
        }
        self.validListPrBo = {
            "title": "list in public board",
            "boardId": 3
        }

        # Cards data
        self.validCardLiPuBo = {
            "title": "card in list of public board",
            "description": "this card just for test",
            "tag": "test",
            "listId": 1,
        }
        self.validCardLiPrBo = {
            "title": "card in list of private board white assign user",
            "description": "this card just for test",
            "tag": "test",
            "listId": 3,
        }
        self.validCardLiPrBoAssignUser = {
            "title": "card in list of private board white assign user",
            "description": "this card just for test",
            "tag": "test",
            "listId": 2,
        }
        self.validCardAssignUser = {
            "title": "card1",
            "description": "this card just for debuging",
            "tag": "debug",
            "listId": 3,
            "assignUsers": [2]
        }

        self.validComment = {}
        self.inValidComment = {}

    def testStartAll(self):
        # authenticate user a
        self.authenticate(email='a@gmail.com', password='aaaa9999')
        # check user is login
        self.checkUserLogin('a@gmail.com', 1)

        # create board
        self.createBoard(board=self.validBoPu, statusCode=status.HTTP_201_CREATED, itemCheck='title')
        self.createBoard(board=self.validBoPrAssignUser, statusCode=status.HTTP_201_CREATED, itemCheck='title')
        self.createBoard(board=self.validBoPr, statusCode=status.HTTP_201_CREATED, itemCheck='title')

        # create list
        self.createList(listCreate=self.validListPuBo, statusCode=status.HTTP_201_CREATED, itemCheck='boardId')
        self.createList(listCreate=self.ValidListPrBoAssignUser, statusCode=status.HTTP_201_CREATED,
                        itemCheck='boardId')
        self.createList(listCreate=self.validListPrBo, statusCode=status.HTTP_201_CREATED, itemCheck='boardId')

        # create card
        self.createCard(card=self.validCardLiPuBo, statusCode=status.HTTP_201_CREATED, itemCheck='listId')
        self.createCard(card=self.validCardLiPrBoAssignUser, statusCode=status.HTTP_201_CREATED, itemCheck='listId')
        self.createCard(card=self.validCardAssignUser, statusCode=status.HTTP_201_CREATED, itemCheck='listId')

        self.client.logout()

        # -------------------------------------------------------------------------------------------------------------

        # authenticate user b
        self.authenticate(email='b@gmail.com', password='bbbb9999')
        # check user is login
        self.checkUserLogin('b@gmail.com', 2)

        # create list in private board without assign user
        self.createList(listCreate=self.validListPrBo, statusCode=status.HTTP_403_FORBIDDEN)

        # create card in private list of board without assign user
        self.createCard(card=self.validCardLiPrBo, statusCode=status.HTTP_403_FORBIDDEN)

        # get card by id 3
        self.checkObjectAccess(objectId=3, statusCode=status.HTTP_403_FORBIDDEN, urlName='card-detail')
        self.checkObjectAccess(objectId=2, statusCode=status.HTTP_403_FORBIDDEN, urlName='card-detail')

        self.objectList(urlName='card-list')

        # update card

        self.client.logout()

    def objectList(self, urlName):
        resData = self.client.get(reverse(urlName)).data
        jsonData = json.dumps(resData, indent=4)
        print(jsonData)
