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

    def setUp(self) -> None:
        self.registerUser()

        self.validBoPu = {
            "title": "public board, creator is a@gmail.com",
            "visibility": "pu",
        }
        self.validBoPr = {
            "title": "private board, creator is a@gmail.com",
            "visibility": "pr",
            "assignUsers": 2  # user 2 is user a@gmail.com
        }

        self.validListPuBo = {
            "title": "list in public board",
            "boardId": 1
        }
        self.inValidList = {
            "title": "list in public board",
            "boardId": 1
        }

        self.validCardLiPuBo = {
            "title": "",
            "description": "",
            "tag": "",
            "listId": 1,
        }
        self.inValidCard = {}

        self.validComment = {}
        self.inValidComment = {}

    def createBoard(self, board, statusCode, itemCheck=None):
        if itemCheck is None:
            response = self.client.post(reverse('board-list'), board)
            self.assertEqual(response.status_code, statusCode)
        else:
            response = self.client.post(reverse('board-list'), board)
            self.assertEqual(response.status_code, statusCode)
            self.assertEqual(response.data[itemCheck], board[itemCheck])

    def createList(self, list, statusCode, itemCheck=None):
        if itemCheck is None:
            response = self.client.post(reverse('list-list'), list)
            print('------------------status code------------------')
            print(response.status_code)
            self.assertEqual(response.status_code, statusCode)
        elif itemCheck == 'boardId':
            response = self.client.post(reverse('list-list'), list)
            self.assertEqual(response.status_code, statusCode)
            self.assertEqual(response.data['board'], list['boardId'])
        else:
            response = self.client.post(reverse('list-list'), list)
            self.assertEqual(response.status_code, statusCode)
            self.assertEqual(response.data[itemCheck], list[itemCheck])

    def testStartAll(self):
        # authenticate user a
        self.authenticate(email='a@gmail.com', password='aaaa9999')

        # create board
        self.createBoard(board=self.validBoPu, statusCode=status.HTTP_201_CREATED, itemCheck='title')
        self.createBoard(board=self.validBoPr, statusCode=status.HTTP_201_CREATED, itemCheck='title')

        # create valid list
        self.createList(list=self.validListPuBo, statusCode=status.HTTP_201_CREATED, itemCheck='boardId')
        self.client.logout()

        # authenticate user b
        self.authenticate(email='b@gmail.com', password='bbbb9999')
        # create invalid list
        # self.createList(list=self.inValidList, statusCode=status.HTTP_403_FORBIDDEN)
        res = self.client.post(reverse('list-list'), self.inValidList)
        print(res.status_code)
