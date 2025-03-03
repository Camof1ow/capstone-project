from django.test import TestCase
from django.urls import reverse
from restaurant.models import Menu
from restaurant.serializers import MenuSerializer
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class MenuViewTest(TestCase):
    def setUp(self):
        """Setup test data and authenticated user"""
        self.client = APIClient()

        # Unauthenticated client
        self.unauthenticated_client = APIClient()

        # Create a test user and generate a token
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')  # Add authentication token

        # Create test menu data
        self.menu1 = Menu.objects.create(name="Pizza", price=15, menu_item_description="Cheesy")
        self.menu2 = Menu.objects.create(name="Burger", price=10, menu_item_description="Juicy")

    def test_get_all_menu_items(self):
        """Test retrieving all menu items (Accessible by unauthenticated users)"""
        response = self.unauthenticated_client.get(reverse('menu-list'))  # ✅ Using unauthenticated client
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = MenuSerializer([self.menu1, self.menu2], many=True).data
        self.assertEqual(response.json(), expected_data)

    def test_post_menu_item_authenticated(self):
        """Test creating a new menu item (Only authenticated users can access)"""
        data = {"name": "Pasta", "price": 12, "menu_item_description": "Creamy"}
        response = self.client.post(reverse('menu-list'), data, format='json')  # ✅ Using authenticated client
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Menu.objects.count(), 3)  # ✅ Verify new item is added

    def test_post_menu_item_unauthenticated(self):
        """Test creating a new menu item (Unauthenticated users should be denied)"""
        data = {"name": "Salad", "price": 8, "menu_item_description": "Healthy"}
        response = self.unauthenticated_client.post(reverse('menu-list'), data, format='json')  # ❌ Using unauthenticated client
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_single_menu_item(self):
        """Test retrieving a specific menu item (Accessible by unauthenticated users)"""
        response = self.unauthenticated_client.get(reverse('menu-detail', args=[self.menu1.id]))  # ✅ Using unauthenticated client
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = MenuSerializer(self.menu1).data
        self.assertEqual(response.json(), expected_data)

    def test_put_menu_item_authenticated(self):
        """Test updating a menu item (Only authenticated users can access)"""
        data = {"name": "Updated Pizza", "price": 18, "menu_item_description": "Cheesy and Crispy"}
        response = self.client.put(reverse('menu-detail', args=[self.menu1.id]), data, format='json')  # ✅ Using authenticated client
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.menu1.refresh_from_db()
        self.assertEqual(self.menu1.name, "Updated Pizza")  # ✅ Verify changes

    def test_put_menu_item_unauthenticated(self):
        """Test updating a menu item (Unauthenticated users should be denied)"""
        data = {"name": "New Name", "price": 18, "menu_item_description": "Changed"}
        response = self.unauthenticated_client.put(reverse('menu-detail', args=[self.menu1.id]), data, format='json')  # ❌ Using unauthenticated client
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_menu_item_authenticated(self):
        """Test deleting a menu item (Only authenticated users can access)"""
        response = self.client.delete(reverse('menu-detail', args=[self.menu1.id]))  # ✅ Using authenticated client
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Menu.objects.filter(id=self.menu1.id).exists())  # ✅ Verify deletion

    def test_delete_menu_item_unauthenticated(self):
        """Test deleting a menu item (Unauthenticated users should be denied)"""
        response = self.unauthenticated_client.delete(reverse('menu-detail', args=[self.menu2.id]))  # ❌ Using unauthenticated client
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
