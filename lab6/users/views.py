from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import connection
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from .forms import RegisterForm, UpdateProfileForm
from users.auth_backend import AuthBackend
from .models import Users, Logs
from .roles import get_customer_role_id, get_employee_role_id


class LoginUserView(View):
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = AuthBackend().authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            if user.is_superuser:
                return redirect('/admin/')

            return redirect('main')

        return render(request, template_name=self.template_name,
                      context={'failed': True}, )


def logout_user(request):
    logout(request)
    return redirect('login')


class RegisterUserView(View):
    template_name = 'users/register.html'

    form_class = RegisterForm

    def get(self, request):
        return render(request, 'users/register.html',
                      {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if len(list(Users.objects.raw("SELECT id FROM users "
                                      "WHERE username = %s",
                                      [request.POST['username']]))) > 0:
            return redirect(request.path, request=request)
        if form.is_valid():
            connection.cursor().execute("CALL create_user(username_p => %s, "
                                        "password_p => %s, email_p => %s, "
                                        "name_p => %s, phone_number_p => %s, "
                                        "role_id_p => %s)",
                                        [form.cleaned_data['username'],
                                         form.cleaned_data['password'],
                                         form.cleaned_data['email'],
                                         form.cleaned_data['name'],
                                         form.cleaned_data['phone_number'],
                                         get_customer_role_id()])

            user = authenticate(request, username=request.POST['username'],
                                password=request.POST['password'])

            if user is not None:
                login(request, user)
                return redirect('main')

        return redirect('register')


class UserProfileView(View):
    template_name = 'users/user-profile.html'

    def get(self, request, user_id):
        user = Users.objects.raw("SELECT id, name, email, phone_number "
                                 "FROM users WHERE id = %s", [user_id])
        return render(request, self.template_name, context={'user': user[0]})


class UpdateUserProfileView(View):
    template_name = 'users/update-user-profile.html'
    form_class = UpdateProfileForm

    def get(self, request, user_id):
        if user_id == request.user.id:
            user = Users.objects.raw("SELECT id, name, "
                                     "phone_number, email "
                                     "FROM users WHERE id = %s",
                                     [user_id])
            return render(request, self.template_name, context={
                'user_id': user_id,
                'form': self.form_class(
                    instance=user[0]),
            })

        return HttpResponseForbidden()

    def post(self, request, user_id):
        user = Users.objects.raw("SELECT id, name, "
                                 "phone_number, email "
                                 "FROM users WHERE id = %s",
                                 [user_id])
        form = self.form_class(request.POST,
                               instance=user[0])
        if form.is_valid():
            connection.cursor().execute("CALL update_user_info"
                                        "(id_p => %s, name_p => %s, "
                                        "email_p => %s, "
                                        "phone_number_p => %s)",
                                        [user_id, form.cleaned_data['name'],
                                         form.cleaned_data['email'],
                                         form.cleaned_data['phone_number']])
            form.save(commit=True)

            return redirect('user-profile', user_id=user_id)

        return HttpResponseBadRequest


class UsersView(View):
    template_name = 'users/users-list.html'

    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse('Unauthorized', 401)
        users = Users.objects.raw("SELECT * FROM users")
        return render(request, self.template_name,
                      context={
                          'users': list(users)
                      })


class LogsView(ListView):
    template_name = 'users/logs.html'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(LogsView, self).get(request,
                                             *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LogsView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Logs.objects.raw("SELECT logs.*, users.username FROM logs "
                                "JOIN users ON logs.user_id = users.id "
                                "ORDER BY logs.time DESC")


@user_passes_test(lambda u: u.is_superuser)
def update_user_role(request, user_id):
    connection.cursor().execute("CALL update_user_role(user_id => %s, "
                                "new_role_id => %s)",
                                [user_id, get_employee_role_id()])
    return redirect('user-profile', user_id=user_id)