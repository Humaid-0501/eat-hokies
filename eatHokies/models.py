from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100)

class DiningList(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.CharField(max_length=200)
    time = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=1)
    total_price = models.DecimalField(default=0, max_digits=5, decimal_places=1)
    # comment = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    creator = models.CharField(default='admin', max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        if(self.name):
            return self.name
        else:
            return self.user

    def get_absolute_url(self):
        if(self.id):
            return reverse('eatHokies:dining_details', args=[self.id])
        else:
            return reverse('users:profile', args=[self.user.username])

class Comments(models.Model):
    comment = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(DiningList, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if(self.comment):
            return self.comment[:20]
        else:
            return self.user

    def get_absolute_url(self):
        if(self.id):
            return reverse('eatHokies:dining_details', args=[self.item_id])

        else:
            return reverse('users:profile', args=[self.user.username])


# Class for item list
# class DiningList:
#     def __init__(self, id, name, description, url, time, price):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.url = url
#         self.time = time
#         self.price = price
#
# # Class for restaurant's information.
# class Restaurents:
#     def __init__(self, id, name):
#         self.id = id
#         self.name = name
#
# item1 = DiningList(
#     1,
#     "Haystack Tavern Double",
#     "Two tavern-sized patties topped with American cheese, Campfire Mayo and crispy onion straws. Upgrade to the Big to swap your two tavern-sized patties for one Gourmet beef patty.",
#     "img/burger_meal_1.jpeg",
#     10,
#     9.5
# )
#
# item2 = DiningList(
#     2,
#     "Mighty Meaty Burger",
#     "Smashed crispy beef patties with house seasoning, American cheese, pickles, diced white onion, mayo, ketchup, and brown mustard on a soft roll.",
#     "img/burger_2.jpeg",
#     10,
#     10
# )
#
# item3 = DiningList(
#     3,
#     "Bean Burger",
#     "Two smashed crispy beef patties with house seasoning, served plain with American cheese on a bun.",
#     "img/burger_3.jpeg",
#     7,
#     7.5
# )
#
# item4 = DiningList(
#     4,
#     "Chicken Teriyaki",
#     "Two fresh, hand-formed patties hot off the grill and placed on a soft, toasted sesame seed bun.",
#     "img/burger_4.jpeg",
#     8,
#     8.5
# )
#
# item5 = DiningList(
#     5,
#     "Mayo Sandwich",
#     "Creamy mayo with our fontina and mozzarella cheese blend and parmesan crisps on toasted thick-sliced Classic White Miche. ",
#     "img/Mayonnaise-sandwich.jpeg",
#     5,
#     5
# )
#
# item6 = DiningList(
#     6,
#     "Chicken Sandwich",
#     "Whole (820 Cal.), Half (410 Cal.) Smoked, pulled chicken raised without antibiotics, fresh mozzarella, salt and pepper, vine-ripened tomatoes, red onions, fresh basil and chipotle sauce on Black Pepper Focaccia.",
#     "img/chicken_sandwich.webp",
#     6,
#     6
# )
#
# item7 = DiningList(
#     7,
#     "Chicken Rice Bowl",
#     "Chilled chicken rice with Tzatziki, Skhug, feta, cucumbers, and fresh dill.",
#     "img/Chicken-Rice-bowl.jpeg",
#     8,
#     8.5
# )
#
# item8 = DiningList(
#     8,
#     "Asian Rice Bowl",
#     "Warm bowl of lentils, quinoa, farro, and rice with Tzatziki, Harissa, tomato relish, cucumbers, and fresh dill.",
#     "img/Asian-Chicken-Rice-bowl.jpeg",
#     9,
#     8.5
# )
#
# # List that hold all the items that are available
items_list = []
# items_list.ap pend(item1)
# items_list.append(item2)
# items_list.append(item3)
# items_list.append(item4)
# items_list.append(item5)
# items_list.append(item6)
# items_list.append(item7)
# items_list.append(item8)
#
# # List that holds items for the order history used in the user's dashboard
order_history = []
# order_history.append(item1)
# order_history.append(item8)
# order_history.append(item1)
# order_history.append(item5)
# order_history.append(item6)
#
# # List that holds favourite items of a user and is used in the user's dashboard
favourite = []
# favourite.append(item1)
# favourite.append(item6)

# Two user credentials.
regular_user = {"username": "john", "password": "regular"}
admin_user = {"username": "admin", "password": "admin"}

# dining1 = Restaurents(
#     1,
#     "Burger' 37"
# )
# dining2 = Restaurents(
#     2,
#     "D2"
# )
# dining3 = Restaurents(
#     3,
#     "Turner Place"
# )
# dining4 = Restaurents(
#     4,
#     "DX"
# )
# dining5 = Restaurents(
#     5,
#     "Deet's Place"
# )
# dining6 = Restaurents(
#     6,
#     "Hokie Grill"
# )
# dining7 = Restaurents(
#     7,
#     "Owens"
# )
# dining8 = Restaurents(
#     8,
#     "Jamba"
# )
# dining9 = Restaurents(
#     9,
#     "Origami"
# )
# dining10 = Restaurents(
#     10,
#     "West End Market"
# )
#
dinings = []
# dinings.append(dining1)
# dinings.append(dining2)
# dinings.append(dining3)
# dinings.append(dining4)
# dinings.append(dining5)
# dinings.append(dining6)
# dinings.append(dining7)
# dinings.append(dining8)
# dinings.append(dining9)
# dinings.append(dining10)

