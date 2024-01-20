import math
from flask import render_template, request, redirect, session, jsonify
import dao
from QLHS import app, login, db
from flask_login import login_user, logout_user, login_required, current_user

from QLHS.models import HocSinh


@app.route('/addpupil', methods=['get', 'post'])
def addpupil():
    if current_user.is_authenticated:
        err_msg = ''
        hs = dao.load_hocsinh()

        if request.method.__eq__('POST'):
            ho = request.form['lastname']
            ten = request.form['firstname']
            gioitinh = request.form['sex']
            ngaysinh = request.form['birth']
            diachi = request.form['address']
            sdt = request.form['phone']
            email = request.form['mail']
            if (dao.tinh_tuoihocsinh(ngaysinh) <= 20) and (dao.tinh_tuoihocsinh(ngaysinh) >= 15):
                dao.add_hocsinh(ho=ho, ten=ten, gioitinh=gioitinh, ngaysinh=ngaysinh, email=email, diachi=diachi, sdt=sdt)
                err_msg = 'Thêm học sinh thành công'
            else:
                err_msg = 'Thêm thất bại! Độ tuổi học sinh không phù hợp!'
        return render_template('addpupil.html', err_msg=err_msg, hocsinh=hs)
    return render_template('addpupil.html')


@app.route('/admin/login', methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/search', methods=['get', 'post'])
def search():
    hocsinh_info = dao.load_hocsinh_info()
    return render_template('search.html', hocsinh_info=hocsinh_info)


@app.route('/classlist', methods=['get', 'post'])
def classlist():
    if current_user.is_authenticated:
        err_msg = ''
        if request.method == 'POST':
            try:
                mahs = int(request.form.get('mahs'))
                lop_id = request.form.get('lop')
                hocsinh = HocSinh.query.get(mahs)
                if hocsinh:
                    dao.update_lopcuahocsinh(mahs, lop_id)
                    err_msg = 'Cập nhật lớp của học sinh thành công'
                    # hocsinh_info = dao.load_hocsinh_newinfo()
                else:
                    err_msg = 'Học sinh không tồn tại'
            except Exception as e:
                print(f"Lỗi khi xử lý yêu cầu: {e}")
                err_msg = 'Đã có lỗi xảy ra'
        return render_template('classlist.html', err_msg=err_msg)
    return render_template('classlist.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/login", methods=['get', 'post'])
def login_user_process():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

        next = request.args.get('next')
        return redirect("/" if next is None else next)

    return render_template('login.html')


@app.route('/logout')
def process_logout_user():
    logout_user()
    return redirect("/login")


@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = ""
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(ten=request.form.get('ten'),
                             username=request.form.get('username'),
                             password=password)
            except:
                err_msg = 'Hệ thống đang bị lỗi!'
            else:
                return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)



