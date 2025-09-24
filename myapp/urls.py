
from django.urls import path, include

from Myapp import views

urlpatterns = [
    path('login_get',views.login_get),
    path('admin_homepage/',views.admin_homepage),
    path('login_post/',views.login_post),
    path('viewcategory/',views.viewcategory),
    path('Addcategory',views.Addcategory),
    path('AddcategoryPost',views.AddcategoryPost),
    path('editcategory/<id>',views.editcategory),
    path('deletecategory/<id>/',views.deletecategory),
    path('viewusers',views.viewusers),
    path('viewbooks',views.viewbooks),
    path('viewtransactions',views.viewtransactions),
    path('viewuserrating',views.viewuserrating),
    path('viewcomplaint',views.viewcomplaint),
    path('sendreply/<id>/',views.sendreply),
    path('sendreplypost/',views.sendreplypost),
    path('change_password',views.change_password),
    path('change_passwordpost/',views.change_passwordpost),

    path('UserHome/',views.UserHome),
    path('registration_user/',views.registration_user),
    path('RegistrationPost/',views.RegistrationPost),
    path('View_profile',views.View_profile),
    path('Update_profile',views.Update_profile),
    path('UpdateProfilePost/',views.UpdateProfilePost),
    path('EditBook/<id>/',views.EditBook),
    path('deleteBook/<id>/',views.deleteBook),
    path('BookEditPost/',views.BookEditPost),
    path('Add_book',views.Add_book),
    path('BookPost/',views.BookPost),
    path('view_request/',views.view_request),
    path('view_status',views.view_status),
    path('ViewPayment/',views.ViewPayment),
    path('searchBook/',views.searchBook),
    path('AddComplaintPost/',views.AddComplaintPost),
    path('DeleteComplaint/<id>/',views.DeleteComplaint),
    path('BookDetails/<id>/',views.BookDetails),
    path('ReviewPost/<id>/',views.ReviewPost),
    path('RequestBook/<id>/',views.RequestBook),
    path('RequestRentBook/<id>/',views.RequestRentBook),
    path('AcceptRequest/<id>/',views.AcceptRequest),
    path('RejectRequest/<id>/',views.RejectRequest),
    path('AcceptRentRequest/<id>/',views.AcceptRentRequest),
    path('RejectRentRequest/<id>/',views.RejectRentRequest),
    path('raz_pay/<amount>/<id>/',views.raz_pay),
    path('raz_pay_rent/<amount>/<id>/',views.raz_pay_rent),
    path('change_passwordpostUser/',views.change_passwordpostUser),
    path('chat/<id>/',views.chat),
    path('chat_view/',views.chat_view),
    path('chat_send/<msg>/',views.chat_send),
    path('User_sendchat/',views.chat),
    path('User_viewchat/',views.User_viewchat),
    path('ViewNotification/',views.ViewNotification),
    path('SendNotificationPost/<id>/',views.SendNotificationPost),
    path('LogOut/',views.LogOut),
    path('AdminHome/',views.AdminHome),






]
