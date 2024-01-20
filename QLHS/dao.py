from datetime import datetime

from QLHS.models import Lop, HocSinh, NguoiDung, Khoi, PhieuDiem, HocKy
from QLHS import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func


def add_hocsinh(ho, ten, gioitinh, ngaysinh, email, diachi, sdt):
    hs = HocSinh(ho=ho, ten=ten, gioitinh=gioitinh, ngaysinh=ngaysinh, email=email, diachi=diachi, sdt=sdt)
    db.session.add(hs)
    db.session.commit()


def tinh_tuoihocsinh(ngaysinh):
    today = datetime.today()
    birthdate = datetime.strptime(ngaysinh, '%Y-%m-%d')  # Điều chỉnh định dạng ngày sinh tùy theo định dạng thực tế
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def load_hocsinh():
    return HocSinh.query.all()


def load_hocsinh_info():
    return (db.session.query(HocSinh, Lop, Khoi). \
        join(Lop, HocSinh.lop_id == Lop.id). \
        join(Khoi, Lop.khoi_id == Khoi.id). \
        order_by(HocSinh.id.asc()).all())


def load_hocsinh_newinfo():
    return (db.session.query(HocSinh, Lop, Khoi). \
        join(Lop, HocSinh.lop_id == Lop.id). \
        join(Khoi, Lop.khoi_id == Khoi.id). \
        order_by(HocSinh.id.asc()).all())


def load_mahocsinh():
    return HocSinh.query.all()


def update_lopcuahocsinh(mahs, lop_id):
    try:
        mahs = int(mahs)
        lop_id = int(lop_id)
        hocsinh = db.session.query(HocSinh).filter(HocSinh.id == mahs).first()
        if hocsinh:

            db.session.query(HocSinh).filter(HocSinh.id.__eq__(mahs)).update({'lop_id': lop_id})
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Lỗi khi cập nhật lớp của học sinh: {e}")
        db.session.rollback()
        return False


def count_hocsinhlop(lop_id):
    return db.session.query(func.count(HocSinh.id)).filter_by(Lop.category_id.__eq__(lop_id=lop_id)).scalar()


def get_user_by_id(id):
    return NguoiDung.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return NguoiDung.query.filter(NguoiDung.username.__eq__(username.strip()),
                             NguoiDung.password.__eq__(password)).first()


def add_user(ten, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = NguoiDung(ten=ten, username=username, password=password)

    db.session.add(u)
    db.session.commit()

