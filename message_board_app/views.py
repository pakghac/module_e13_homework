from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from message_board_app.models import Message, Response, Category
from message_board_app.filters import ResponseFilter
from message_board_app.forms import ResponseForm
from message_board import settings


# Create your views here.
def index(request):
    return render(
        request,
        'index.html',
        context={},
    )


class MessageList(ListView):
    model = Message
    template_name = 'message_list.html'
    context_object_name = 'messages'


class MessageDetail(DetailView):
    model = Message
    template_name = 'message_detail.html'
    context_object_name = 'message'


class MessageCreate(LoginRequiredMixin, CreateView):
    model = Message
    template_name = 'message_create.html'
    fields = ['category', 'title', 'content']


    def form_valid(self, form):
        form.instance.messageAuthor = self.request.user
        return super().form_valid(form)


class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    template_name = 'response_create.html'
    fields = ['text']

    def form_valid(self, form):
        form.instance.responseAuthor = self.request.user
        form.instance.message = Message.objects.get(pk=self.request.GET.get('message_id'))
        return super().form_valid(form)


class ResponseList(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'response_list.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return Response.objects.filter(responseAuthor=self.request.user)


class MessageResponseList(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'response_to_message_list.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return Response.objects.filter(message__messageAuthor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ResponseFilter(self.request.GET, queryset=self.get_queryset(), user=self.request.user)
        return context


class MessageResponseDetail(LoginRequiredMixin, DetailView):
    model = Response
    template_name = 'response_to_message_detail.html'
    context_object_name = 'response'

    def get_queryset(self):
        return Response.objects.filter(message__messageAuthor=self.request.user)


class MessageResponseAccept(LoginRequiredMixin, UpdateView):
    model = Response
    form_class = ResponseForm

    def form_valid(self, form):
        response = form.save(commit=False)
        if response.message.messageAuthor == self.request.user:
            response.isAccepted = True
        response.save()
        return super().form_valid(form)

class MessageResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    success_url = '/board/responses_to_my_messages'
    def delete(self, request, *args, **kwargs):
        response = self.get_object()
        if response.message.messageAuthor == self.request.user:
            success_url = self.get_success_url()
            response.delete()
            return http.HttpResponseRedirect(success_url)
        else:
            return http.HttpResponseForbidden("Нельзя удалить этот отклик")

class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


@login_required
def subscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'mail/subscribed.html',
            {
                'category': category,
                'user': user,
            },
        )

        msg = EmailMultiAlternatives(
            subject='Уведомление о подписке',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email, ],
        )

        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)

    return redirect('/board/categories')


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
        email = user.email
        html = render_to_string(
            'mail/unsubscribed.html',
            {
                'category': category,
                'user': user,
            },
        )

        msg = EmailMultiAlternatives(
            subject='Уведомление об отписке',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email, ],
        )

        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)

    return redirect('/board/categories')
