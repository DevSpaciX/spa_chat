from uuid import uuid4

from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms import TextInput
from django.shortcuts import render, redirect

from django.views import generic, View
from django.views.generic import FormView
from django_filters import rest_framework as filters
from django_filters.widgets import RangeWidget

from room.forms import RoomCreateForm
from room.models import Room, Message


class RoomFilter(filters.FilterSet):
    user_name = filters.CharFilter(field_name='messages__user__username', lookup_expr='icontains', widget=TextInput(attrs={
            'style': 'border: 1px solid black; border-radius: 10px;'
        }))
    email = filters.CharFilter(field_name='messages__user__email', lookup_expr='icontains',widget=TextInput(attrs={
            'style': 'border: 1px solid black; border-radius: 10px;'
        }))
    oldest_first = filters.BooleanFilter(
        widget=forms.RadioSelect(choices=((True, 'Oldest First'), (False, 'Newest First'))),
        label='Oldest First',
        method='filter_oldest_first'
    )

    date_added = filters.DateFromToRangeFilter(
        field_name='date_added',
        widget=RangeWidget(attrs={
            'class': 'dateinput',
            'type': 'date'
        }),
        method="filter_date_added"
    )

    def filter_date_added(self, queryset, name, value):
        start_date = value.start
        end_date = value.stop
        if self.data.get('oldest_first'):
            return queryset.filter(date_added__range=(start_date, end_date))
        else:
            return queryset.filter(date_added__range=(start_date, end_date))

    def filter_oldest_first(self, queryset, name, value):
        if value:
            return queryset.order_by('date_added')
        else:
            return queryset.order_by('-date_added')

    class Meta:
        model = Room
        fields = ['user_name']


class ChatRoomsList(generic.ListView):
    model = Room
    template_name = "homepage.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = RoomFilter(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = RoomFilter(self.request.GET, queryset=queryset)
        return filter.qs.distinct()


class ChatRoomDetail(generic.ListView):
    model = Room
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = Message.objects.all()
        context['messages'] = messages
        return context


@login_required
def room(request, pk):
    room = Room.objects.get(pk=pk)
    messages = Message.objects.filter(room_id=pk)[0:25]

    context = {
        'room': room,
        'messages': messages,
    }

    return render(request, 'room.html', context)


class RoomCreateView(FormView):
    template_name = "room_create.html"
    form_class = RoomCreateForm

    def form_valid(self, form):
        try:
            new_room = form.save(commit=False)
            new_room.save()
            user = self.request.user
            Message.objects.create(
                user=user, room=new_room, text=new_room.main_message, email=user.email
            )
            return redirect("room:room", pk=new_room.pk)

        except ValidationError as e:
            form.add_error('title', e)
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
