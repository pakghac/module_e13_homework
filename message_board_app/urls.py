from django.urls import path

from message_board_app.views import MessageList, MessageDetail, MessageCreate, ResponseCreate, MessageResponseList, \
    ResponseList, MessageResponseDetail, MessageResponseAccept, MessageResponseDelete, CategoryList, \
    subscribe_to_category, unsubscribe_from_category

urlpatterns = [
    path('messages', MessageList.as_view()),
    path('messages/<int:pk>', MessageDetail.as_view(), name='message_detail'),
    path('messages/create', MessageCreate.as_view()),

    path('responses_to_my_messages', MessageResponseList.as_view()),
    path('my_responses', ResponseList.as_view()),
    path('responses_to_my_messages/<int:pk>', MessageResponseDetail.as_view()),
    path('responses_to_my_messages/<int:pk>/accept', MessageResponseAccept.as_view(
        success_url='/board/responses_to_my_messages'), name='accept'),
    path('response_create', ResponseCreate.as_view(), name='response_create'),
    path('responses_to_my_messages/<int:pk>/delete', MessageResponseDelete.as_view(), name='delete'),
    path('categories', CategoryList.as_view()),
    path('subscribe/<int:pk>', subscribe_to_category, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe_from_category, name='unsubscribe'),
]
