from django.http import HttpResponse
from django.shortcuts import render,redirect
from . models import *
from .forms import *
from django.db.models import Avg

# Create your views here.
def home(request):
     
     query = request.GET.get("title")
     allBooks = None
     if query:
        allBooks = Book.objects.filter(name__icontains=query)
     else:
        allBooks = Book.objects.all() #select * from Book
     
     context={
        "books": allBooks,
     }
     return render(request, 'main/index.html',context)
    
#detail page
def detail(request, id):
    book= Book.objects.get(id=id) #select * from Book where id=id
    reviews = Review.objects.filter(book=id).order_by("-comment")
    average= reviews.aggregate(Avg("rating"))["rating__avg"]  
    if average == None:
        average=0
    average = round(average , 2)
    context={
        "book": book,
        "reviews": reviews,
        "average": average
    }
    return render(request, 'main/details.html',context)

# add books to the database
def add_books(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                form = BookForm(request.POST or None)

                #check if the form is valid
                if form.is_valid():
                     data = form.save(commit=False)
                     data.save()
                     return redirect("main:home")
            else:
                form = BookForm()
            return render(request, 'main/addbooks.html', {"form":form,"controller": "Add Books"})

        #if they are not admin
        else:
            return redirect("main:home")
    
    # if they are not loggedin
    return redirect("accounts:login")

                                                   

# edit the book
def edit_books(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            #get the book links with id
            book=Book.objects.get(id=id)
            #form check
            if request.method == "POST":
                form = BookForm( request.POST or None,instance=book)
                #create if form is valid
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:detail", id)
            else:
                form = BookForm(instance=book)
            return render(request, 'main/addbooks.html', {'form':form, "controller": "Edit Books"})
        #if they are not admin
        else:
            return redirect("main:home")
    
    # if they are not loggedin
    return redirect("accounts:login")

#delete books
def delete_books(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:    
            #get the movies
            book = Book.objects.get(id=id)

            #delete the movies
            book.delete()
            return redirect("main:home")
        #if they are not admin
        else:
            return redirect("main:home")
    
    # if they are not loggedin
    return redirect("accounts:login")

def add_review(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST["comment"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.book = book
                data.save()
                return redirect("main:detail", id)
        else:
            form = ReviewForm()
        return render(request, 'main/details.html' ,{'form': form})
    else:
        return redirect("accounts:login")

# edit the review
def edit_review(request, book_id, review_id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=book_id)
        #reviews
        review = Review.objects.get(book=book, id=review_id)

        #check if the review was done by the logged in user
        if request.user == review.user:
            #grant permission
            if request.method == "POST":
                form = ReviewForm(request.POST , instance=review )
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10 or data.rating < 0):
                       error="out or range.Please select rating from 0 to 10."
                       return render(request,'main/editreview.html', {"error": error, " form": form})
                    else:
                       data.save()
                       return redirect("main:detail", book_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'main/editreview.html',{"form": form})
        else:
            return redirect("main:detail", book_id)
    else:
        return redirect("accounts:login")

#delete reviews
def delete_review(request, book_id, review_id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=book_id)
        #reviews
        review = Review.objects.get(book=book, id=review_id)

        #check if the review was done by the logged in user
        if request.user == review.user:
            #grant permission to delete
            review.delete()
        else:
            return redirect("main:detail", book_id)
    else:
        return redirect("accounts:login")
                

