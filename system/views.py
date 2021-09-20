from django.shortcuts import render

# Create your views here.
from braces.views import FormInvalidMessageMixin, FormValidMessageMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import *
from .models import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
import datetime

# Create your views here.
class RegisterUser(SuccessMessageMixin, FormView):

    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    success_message = 'Your account has been created! You are now able to log in'

    def form_valid(self, form):
        form.instance.author = self.request.user
        user_name = form.cleaned_data.get('username')
        form.save()
        return super(RegisterUser, self).form_valid(form)

class ChangePasswordView(LoginRequiredMixin, FormValidMessageMixin, FormInvalidMessageMixin, FormView):

    form_class = PasswordChangeForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('login')

    def get_form_valid_message(self):
        return 'Your password was successfully updated!'

    def get_form_invalid_message(self):
        return 'Please correct the error below.'

    def form_valid(self, form):
        form.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

class HomePage(LoginRequiredMixin, ListView):

    model = Room
    template_name = 'home.html'
    context_object_name = 'rooms'

    def get_context_data(self, **kwargs):
        kwargs['reservations'] = Reservation.objects.order_by('date')
        kwargs['today'] = datetime.date.today()
        return super(HomePage, self).get_context_data(**kwargs)

class AddRoom(LoginRequiredMixin, CreateView):

    model = Room
    template_name = 'add_room.html'
    form_class = CreateModifyRoom
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ModifyRoom(LoginRequiredMixin, UpdateView):

    model = Room
    template_name = 'modify_room.html'
    form_class = CreateModifyRoom
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        self.room = get_object_or_404(Room, pk=kwargs['pk'])
        return super(ModifyRoom, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        modifyRoom = self.get_object()
        user = self.request.user
        return user in modifyRoom.owners.all()

    def get_context_data(self, **kwargs):
        kwargs['room'] = Room.objects.get(pk=self.room.id)
        return super(ModifyRoom, self).get_context_data(**kwargs)

class DeleteRoom(LoginRequiredMixin, DeleteView):

    model = Room
    success_url = '/'
    template_name = 'delete_room_confirm.html'

class RoomView(LoginRequiredMixin, DetailView):

    model = Room
    pk_url_kwarg = 'pk'
    template_name = 'show_room.html'

    def dispatch(self, request, *args, **kwargs):
        self.room = get_object_or_404(Room, pk=kwargs['pk'])
        return super(RoomView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['room'] = Room.objects.get(pk=self.room.id)
        kwargs['reservations'] = Reservation.objects.filter(room=self.room)
        return super(RoomView, self).get_context_data(**kwargs)

class MakeReservation(LoginRequiredMixin, CreateView):

    model = Reservation
    template_name = 'add_reservation.html'
    form_class = CreateUpdateReservation
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateReservation(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Reservation
    template_name = 'modify_reservation.html'
    form_class = CreateUpdateReservation
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        self.reservation = get_object_or_404(Reservation, pk=kwargs['pk'])
        return super(UpdateReservation, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        reservation = self.get_object()
        if self.request.user == reservation.user:
            return True
        return False

class DeleteReservation(LoginRequiredMixin, DeleteView):

    model = Reservation
    success_url = '/'
    template_name = 'delete_reservation_confirm.html'