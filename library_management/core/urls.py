from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/",views.login,name="login"),
    path("logout/",views.logout_user,name="logout"),
    path("signup/",views.signup,name="signup"),
    path("login/dashboard/<str:user_id>/",views.login_successfull_view,name="dashboard"),
    path("member/books/<int:user_id>/",views.all_books_available_view,name='all_books'),
    path("member/buy/book/<int:user_id>/<int:book_id>/",views.buy_book,name='buy_books'),
    path("member/mybooks/<int:user_id>/",views.my_books,name='my_books'),
    path("member/mybooks/return/<int:user_id>/<int:book_id>/",views.return_my_books,name='return_my_books'),
    path("library/manage/books/<int:user_id>/",views.library_manage_books,name='manage_books'),
    path("library/manage/books/status/<int:book_id>/<int:user_id>/",views.library_update_book_status,name='update_book_status'),
    path("library/manage/books/status/<int:book_id>/<int:user_id>/confirm/",views.library_book_status_update_confirm,name='book_status_update_confirm'),
    path("library/manage/books/<int:user_id>/new/",views.add_new_book,name='add_new_book'),
    path("library/manage/books/<int:user_id>/new/success/",views.add_new_book_success,name='add_new_book_success'),
    path("library/manage/books/<int:book_id>/<int:user_id>/remove/",views.delete_book,name='delete_book'),
    path("library/manage/users/<int:user_id>/",views.library_manage_users,name='manage_users'),
    path("library/manage/users/password/<int:user_id>/<int:main_user_id>/",views.library_update_user_password,name='update_user_password'),
    path("library/manage/users/password/<int:user_id>/<int:main_user_id>/success/",views.library_update_user_password_success,name='update_user_password_success'),
    path("library/manage/users/<int:user_id>/<int:main_user_id>/remove/",views.delete_user,name='delete_user'),
    path("library/manage/users/<int:user_id>/new/",views.add_new_user,name='add_new_user'),
    path("library/manage/users/<int:user_id>/new/success/",views.add_new_user_success,name='add_new_user_success'),



]