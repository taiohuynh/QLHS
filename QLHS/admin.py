from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from QLHS import app, db, dao
from QLHS.models import HocSinh, Lop
from flask_login import logout_user, current_user
from flask import redirect, request
from QLHS.models import UserRoleEnum


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app, name='QUẢN Lý HỌC SINH', template_mode='bootstrap4', index_view=MyAdminIndex())


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.NGUOIQUANTRI


class MyPupilView(AuthenticatedAdmin):
    column_list = ['id', 'ho', 'ten', 'gioitinh', 'ngaysinh']
    column_searchable_list = ['ten']
    column_filters = ['ten', 'gioitinh']
    can_export = True
    can_view_details = True


class MyClassView(AuthenticatedAdmin):
    column_list = ['name', 'products']


class MyLogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(MyClassView(Lop, db.session))
admin.add_view(MyPupilView(HocSinh, db.session))
admin.add_view(MyLogoutView(name='Đăng xuất'))
