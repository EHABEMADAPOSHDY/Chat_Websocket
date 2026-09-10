from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import ChatmessageCreateForm
from .models import ChatGroup


User = get_user_model()


@login_required
def chat_view(request, chatroom_name='public-chat'):

    chat_group = get_object_or_404(
        ChatGroup,
        group_name=chatroom_name
    )

    chat_messages = chat_group.chat_messages.all()[:30]

    form = ChatmessageCreateForm()

    other_user = None

    if chat_group.is_private:
        other_user = (
            chat_group.members
            .exclude(id=request.user.id)
            .first()
        )

    context = {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
    }

    return render(
        request,
        'a_rtchat/chat.html',
        context
    )


@login_required
def get_or_create_chatroom(request, username):

    # منع المستخدم من فتح محادثة مع نفسه
    if request.user.username == username:
        return redirect('home')

    # المستخدم الذي نريد محادثته
    other_user = get_object_or_404(
        User,
        username=username
    )

    # البحث عن ChatGroup موجود بالفعل
    chatroom = (
        ChatGroup.objects
        .filter(
            is_private=True,
            members=request.user
        )
        .filter(
            members=other_user
        )
        .first()
    )

    # لو مفيش ChatGroup نعمل واحد جديد
    if chatroom is None:

        chatroom = ChatGroup.objects.create(
            is_private=True
        )

        chatroom.members.add(
            request.user,
            other_user
        )

    # فتح صفحة المحادثة
    return redirect(
        'chatroom',
        chatroom_name=chatroom.group_name
    )