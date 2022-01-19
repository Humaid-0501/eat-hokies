from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import regular_user, admin_user, DiningList, Restaurant, User, Comments
from actions.models import Action
from users.models import Details
from django.contrib.humanize.templatetags.humanize import naturaltime

# Create your views here.
# For displaying the item list.
def dining_list(request, restaurant_id):
    items_list = DiningList.objects.all().filter(restaurant_id=restaurant_id).order_by('price')
    # dinings = Restaurant.objects.all()
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    if (not items_list):
        messages.add_message(request, messages.ERROR,
                             "Currently there are no items available. Please check again later.")
        return render(request, "eatHokies/dining_list/list.html", {"items": items_list, "resID": restaurant})
    return render(request,
                  "eatHokies/dining_list/list.html",
                  {"items": items_list, "resID": restaurant}
                  )

#This controller is for sorting
def dining_sort(request, restaurant_id):
    item_list = DiningList.objects.order_by('name')
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(request, "eatHokies/dining_list/list.html", {"items": item_list, "resID": restaurant})

# This controller is for displaying the details page of a selected item.
def dining_details(request, item_id):
    item = DiningList.objects.get(pk=item_id)
    comment = Comments.objects.filter(item_id=item.id).order_by('-created')[:4]
    # for item in items_list:
    #     if item.id == item_id:
    #         break
    return render(request, "eatHokies/dining_list/details.html",
                  {"details": item, "comments": comment}
                  )

#Controller for increasing the item quantity
def item_quantity_plus(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        item_id = request.POST.get('item_id')
        try:
            item = DiningList.objects.get(id=item_id)
            quantity = item.quantity + 1
            if quantity > 10:
                # messages.add_message(request, messages.INFO, "Maximum quantity is 10")
                return JsonResponse({'error': 'Maximum quantity is 10'}, status=200)
            price = item.price*quantity
            item.quantity = quantity
            item.total_price = price
            item.save()
            return JsonResponse({'success': 'success', 'quantity': item.quantity, 'price': price}, status=200)
        except DiningList.DoesNotExist:
            return JsonResponse({'error': 'No item found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)

#Controller for reducing the item quantity
def item_quantity_minus(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        item_id = request.POST.get('item_id')
        try:
            item = DiningList.objects.get(id=item_id)
            quantity = item.quantity - 1
            if quantity < 1:
                # messages.add_message(request, messages.INFO, "Minimum quantity is 1")
                return JsonResponse({'error': 'Minimum quantity is 1'}, status=200)
            price = item.price * quantity
            item.quantity = quantity
            item.total_price = price
            item.save()
            return JsonResponse({'success': 'success', 'quantity': item.quantity, 'price': price}, status=200)
        except DiningList.DoesNotExist:
            return JsonResponse({'error': 'No item found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)

# This controller renders the home page.
def dining_home(request):
    order_history = DiningList.objects.all().order_by('-id')[:6]
    favourite = DiningList.objects.all().order_by('id')[:4]
    actions = Action.objects.all().order_by('-created')
    return render(request, "eatHokies/dining_list/home.html",
                  {"order_hostory": order_history, "favourite": favourite, "actions": actions}
                  )

# This controller is for adding a new item to the list and is only accessible to the admin.
def dining_add_item(request):
    if ('username' in request.session):
        if (request.session['role'] == 'admin'):
            return render(request, "eatHokies/dining_list/add.html")
        return redirect("eatHokies:dining_home")
    else:
        return redirect("eatHokies:dining_home")

# For creating a new item, fetches information from the add form and adds it to the list in models.py
def create_item(request):
    if request.method=='POST':
        items_list = DiningList.objects.all()
        # obj=DiningList.objects.last()
        name = request.POST.get("name")
        description = request.POST.get("description")
        category = request.POST.get("category")
        # dining = request.POST.get("dining")
        dining = request.POST.get("dining")
        dining = dining.split('.')
        price = request.POST.get("price")
        image = request.POST.get("image")
        time = request.POST.get("time")
        creator = request.session['username']
        user = User.objects.get(username=request.session.get("username"))
        if (name==None or description==None or price==None or image==None or time==None):
            return redirect('eatHokies:dining_add_item')
        if image:
            image = "img/" + image

        new_item = DiningList(
            name=name,
            description=description,
            url=image,
            time=time,
            price=price,
            total_price=price,
            creator=creator,
            user=user,
            restaurant_id=dining[0],
        )
        new_item.save()
        #log the action
        action = Action(
            user=user,
            verb="added a new item",
            target=new_item
        )
        action.save()

        messages.add_message(request, messages.SUCCESS, "Item successfully added: %s" % new_item.name)
        return redirect('eatHokies:dining_list', dining[0])
    else:
        return redirect('eatHokies:dining_add_item')

# For editing an item.
def edit_item(request, item_id):
    items_list = DiningList.objects.all()
    if ('username' in request.session):
        if (request.session['role']=='admin'):
            for items in items_list:
                if items.id == item_id:
                    break
            return render(request, "eatHokies/dining_list/edit.html", {"items_list": items})
        return redirect("eatHokies:dining_home")
    else:
        return redirect("eatHokies:dining_home")

# Updates the information after using the edit functionality.
def edit(request, item_id):
    # items_list = DiningList.objects.all()
    user = User.objects.get(username=request.session.get("username"))
    if request.method == 'POST':
        if ('username' in request.session):
            if (request.session['role']=='admin'):
                name = request.POST.get("name")
                description = request.POST.get("description")
                # category = request.POST.get("category")
                # dining = request.POST.get("dining")
                # dining = dining.split('.')
                price = request.POST.get("price")
                time = request.POST.get("time")
                obj = DiningList.objects.get(id=item_id)
                if (name==None or description==None or price==None or time==None):
                    return redirect('eatHokies:edit_item')
                if obj.name != name:
                    verb = "edited the item name of "
                elif obj.description != description:
                    verb = "edited the item description of "
                else:
                    verb = "edited the item details"
                obj.name = name
                obj.description = description
                # obj.restaurant_id = dining[0]
                obj.price = price
                obj.time = time
                obj.save()

                # log the edit action.
                action = Action(
                    user=user,
                    verb=verb,
                    target=obj
                )
                action.save()
                messages.add_message(request, messages.INFO, "Item successfully updated: %s" % obj.name)

                return redirect('eatHokies:dining_details', item_id)
            return redirect("eatHokies:dining_home")
        return redirect("eatHokies:dining_home")
    else:
        return redirect('eatHokies:edit_item')

#Controller for displaying the delete view
def delete_item(request, item_id):
    items_list = DiningList.objects.all()
    if ('username' in request.session):
        if (request.session['role']=='admin'):
            for i in range(len(items_list)):
                if items_list[i].id == item_id:
                    break
            return render(request, "eatHokies/dining_list/delete.html", {"id":items_list[i].id})
        return redirect("eatHokies:dining_home")
    else:
        return redirect("eatHokies:dining_home")

#Controller for deteling an item from the database
def delete(request):
    # items_list = DiningList.objects.all()
    item_id = request.POST.get("id")
    user = User.objects.get(username=request.session.get("username"))
    if request.method == 'POST':
        if ('username' in request.session):
            if (request.session['role']=='admin'):
                confirmation = request.POST.get("confirmation")
                if confirmation == 'yes':
                    obj = DiningList.objects.get(pk=item_id)
                    dining = obj.restaurant_id
                    # action = Action.objects.get(target_id=item_id)
                    name=obj
                    obj.delete()
                    action = Action(
                        user=user,
                        verb="deleted  the item: "+name.name,
                        target=name
                    )
                    # action.delete()
                    action.save()
                    messages.add_message(request, messages.WARNING, "Item successfully deleted: %s" % name)

                return redirect("eatHokies:dining_list", dining)
            return redirect("eatHokies:dining_home")
        return redirect("eatHokies:dining_home")
    else:
        return redirect('eatHokies:delete_item', item_id)

#Controller for adding a comment
def comment(request, item_id):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    comments = []
    if is_ajax and request.method == 'POST':
        # item_id = request.POST.get('_id')
        user_comment = request.POST.get('_user_review')
        try:
            item = DiningList.objects.get(pk=item_id)
            user = User.objects.get(username=request.session.get("username"))
            comment = Comments(
                comment=user_comment,
                user=user,
                item=item)
            comment.save()

            # log the action
            action = Action(
                user=user,
                verb="added a new comment!",
                target=comment
            )
            action.save()
            comments.append(
                {"id": comment.id, "review": comment.comment, "date": naturaltime(comment.created), "user": comment.user.username})
            return JsonResponse({'success': 'success', 'comment': comments}, status=200)
        except DiningList.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid AJAX request'}, status=400)

#Controller for viewing a comment
def view_comment(request, item_id):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    comments = []

    if is_ajax and request.method == 'GET':
        try:
            if 'username' in request.session:
                userID = User.objects.get(username=request.session.get("username")).id
                userRole = Details.objects.get(user_id=userID)
                role = userRole.role
            else:
                role = None
            item = Comments.objects.filter(item_id=item_id).order_by("-created")
            for i in item:
                comments.append({"id": i.id, "review": i.comment, "date": naturaltime(i.created), "user": i.user.username, "role": role})
            return JsonResponse({'success': 'success', 'review': comments}, status=200)
        except DiningList.DoesNotExist:
            return JsonResponse({'error': 'Item Not Found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Request'}, status=400)

#Controller for editing a comment
def edit_comment(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        comment_id = request.POST.get('_comment_id')
        updated_comment = request.POST.get('_new_comment')
        try:
            comment = Comments.objects.get(pk=comment_id)
            comment.comment = updated_comment
            comment.save()

            return JsonResponse({'success': 'success'}, status=200)
        except DiningList.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid AJAX request'}, status=400)

#Controller for deleting a comment
def delete_comment(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        comment_id = request.POST.get('_comment_id')
        try:
            comment = Comments.objects.get(pk=comment_id)
            comment.delete()
            return JsonResponse({'success': 'success'}, status=200)
        except DiningList.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid AJAX request'}, status=400)