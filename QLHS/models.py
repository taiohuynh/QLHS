from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean, Null
from sqlalchemy.orm import relationship
from QLHS import db, app
from flask_login import UserMixin
import enum
from datetime import datetime


class UserRoleEnum(enum.Enum):
    NHANVIEN = 1
    GIAOVIEN = 2
    NGUOIQUANTRI = 3


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class NguoiDung(BaseModel, UserMixin):
    __tablename__ = 'NguoiDung'

    ho = Column(String(50), nullable=True)
    ten = Column(String(20), nullable=False)
    namsinh = Column(DateTime, nullable=True)
    gioitinh = Column(String(10), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRoleEnum))

    nguoiquantri = relationship('NguoiQuanTri', backref='nguoidung', lazy=True)
    nhanvien = relationship('NhanVien', backref='nguoidung', lazy=True)
    giaovien = relationship('GiaoVien', backref='nguoidung', lazy=True)

    def __str__(self):
        return self.ten


class NhanVien(BaseModel):
    __tablename__ = 'NhanVien'

    nguoidung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    phieutiepnhanhocsinh = relationship('PhieuTiepNhanHocSinh', backref='giaovien', lazy=True)


class GiaoVien(BaseModel):
    __tablename__ = 'GiaoVien'

    nguoidung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    phieudiem = relationship('PhieuDiem', backref='giaovien', lazy=True)


class NguoiQuanTri(BaseModel):
    __tablename__ = 'NguoiQuanTri'

    nguoidung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    quydinhsisolop = relationship('QuyDinhSiSoLop', backref='nguoiquantri', lazy=True)
    quydinhtuoitiepnhan = relationship('QuyDinhTuoiTiepNhan', backref='nguoiquantri', lazy=True)


class HocKy(BaseModel):
    __tablename__ = 'HocKy'

    ten = Column(String(50), nullable=False, unique=True)
    namhoc = Column(String(50), nullable=False)
    thoigianbatdau = Column(DateTime, nullable=True, default=datetime.now())
    thoigianketthuc = Column(DateTime, nullable=True)
    phieudiem = relationship('PhieuDiem', backref='hocky', lazy=True)

    def __str__(self):
        return self.name


class MonHoc(BaseModel):
    __tablename__ = 'MonHoc'

    ten = Column(String(20), nullable=True)
    phieudiem = relationship('PhieuDiem', backref='monhoc', lazy=True)

    def __str__(self):
        return self.ten


class Khoi(BaseModel):
    __tablename__ = 'Khoi'

    ten = Column(String(20), nullable=False)
    lop = relationship('Lop', backref='khoi', lazy=True)

    def __str__(self):
        return self.ten


class QuyDinhSiSoLop(BaseModel):
    __tablename__ = 'QuyDinhSiSoLop'

    siso = Column(Integer, nullable=False)
    nguoiquantri_id = Column(Integer, ForeignKey(NguoiQuanTri.id), nullable=False)


class Lop(BaseModel):
    __tablename__ = 'Lop'

    ten = Column(String(50), nullable=False, unique=True)
    khoi_id = Column(Integer, ForeignKey(Khoi.id), nullable=True)
    phieudiem = relationship('PhieuDiem', backref='lop', lazy=True)

    def __str__(self):
        return self.ten


class HocSinh(BaseModel, UserMixin):
    __tablename__ = 'HocSinh'

    ten = Column(String(10), nullable=False)
    ho = Column(String(50), nullable=False)
    gioitinh = Column(String(10), nullable=False)
    ngaysinh = Column(DateTime, nullable=False)
    email = Column(String(10), nullable=True)
    diachi = Column(String(10), nullable=True)
    sdt = Column(String(10), nullable=True)
    lop_id = Column(Integer, ForeignKey(Lop.id), nullable=True)
    phieudiem = relationship('PhieuDiem', backref='hocsinh', lazy=True)

    def __str__(self):
        return self.ten


class QuyDinhTuoiTiepNhan(BaseModel):
    __tablename__ = 'QuyDinhTuoiTiepNhan'

    tuoitiepnhan = Column(Integer, nullable=False)
    nguoiquantri_id = Column(Integer, ForeignKey(NguoiQuanTri.id), nullable=False)


class PhieuTiepNhanHocSinh(BaseModel):
    __tablename__ = 'PhieuTiepNhanHocSinh'

    ngaynhan = Column(DateTime, nullable=False, default=datetime.now())
    nhanvien_id = Column(Integer, ForeignKey(NhanVien.id), nullable=False)
    hocsinh_id = Column(Integer, ForeignKey(HocSinh.id), nullable=False)


class PhieuDiem(BaseModel):
    __tablename__ = 'PhieuDiem'

    ngaylapphieu = Column(DateTime, nullable=False, default=datetime.now())
    lop_id = Column(Integer, ForeignKey(Lop.id), nullable=False)
    hocsinh_id = Column(Integer, ForeignKey(HocSinh.id), nullable=False)
    giaovien_id = Column(Integer, ForeignKey(GiaoVien.id), nullable=False)
    monhoc_id = Column(Integer, ForeignKey(MonHoc.id), nullable=False)
    hocky_id = Column(Integer, ForeignKey(HocKy.id), nullable=False)
    diem_id = relationship('Diem', backref='phieudiem', lazy=True)


class Diem(BaseModel):
    __tablename__ = 'Diem'

    diem = Column(Float, nullable=False)
    loaidiem = Column(String(10), nullable=False)
    phieudiem_id = Column(Integer, ForeignKey(PhieuDiem.id), nullable=False)


if __name__ == "__main__":
    from QLHS import app

    with app.app_context():
        db.create_all()

        import hashlib

        n1 = NguoiDung(ten='Quản Trị Viên', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                       user_role=UserRoleEnum.NGUOIQUANTRI)
        n2 = NguoiDung(ho='Lê Thị Hồng', ten='Tuyết', username='tuyetlth', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                       user_role=UserRoleEnum.GIAOVIEN)
        n3 = NguoiDung(ho='Hồ Hướng', ten='Thiên', username='thienhh', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                       user_role=UserRoleEnum.GIAOVIEN)
        n4 = NguoiDung(ho='Dương Hữu', ten='Thành', username='thanhdh', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                       user_role=UserRoleEnum.GIAOVIEN)
        n5 = NguoiDung(ho='Lê Quang', ten='Hiếu', username='hieulq', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                       user_role=UserRoleEnum.GIAOVIEN)
        n6 = NguoiDung(ho='Lê Thị Cẩm', ten='Tú', username='tultc', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                       user_role=UserRoleEnum.NHANVIEN)
        db.session.add_all([n1, n2, n3, n4, n5, n6])
        db.session.commit()

        nqt = NguoiQuanTri(nguoidung_id=1)
        db.session.add(nqt)
        db.session.commit()

        nv = NhanVien(nguoidung_id=6)
        db.session.add(nv)
        db.session.commit()

        gv1 = GiaoVien(nguoidung_id=2)
        gv2 = GiaoVien(nguoidung_id=3)
        gv3 = GiaoVien(nguoidung_id=4)
        gv4 = GiaoVien(nguoidung_id=5)
        db.session.add_all([gv1, gv2, gv3, gv4])
        db.session.commit()

        h1 = HocKy(ten='Học Kỳ III - 2021-2022', namhoc='2021-2022')
        h2 = HocKy(ten='Học Kỳ I - 2022-2023', namhoc='2022-2023')
        h3 = HocKy(ten='Học Kỳ II - 2022-2023', namhoc='2022-2023')
        h4 = HocKy(ten='Học Kỳ III - 2022-2023', namhoc='2022-2023')
        h5 = HocKy(ten='Học Kỳ I - 2023-2024', namhoc='2023-2024')
        db.session.add_all([h1, h2, h3, h4, h5])
        db.session.commit()

        m1 = MonHoc(ten="Toán")
        m2 = MonHoc(ten="Văn")
        m3 = MonHoc(ten="Anh")
        m4 = MonHoc(ten="Lý")
        m5 = MonHoc(ten="Hóa")
        m6 = MonHoc(ten="Sinh")
        db.session.add_all([m1, m2, m3, m4, m5, m6])
        db.session.commit()

        k1 = Khoi(ten='Khối 10')
        k2 = Khoi(ten='Khối 11')
        k3 = Khoi(ten='Khối 12')
        db.session.add_all([k1, k2, k3])
        db.session.commit()

        l1 = Lop(ten='10A1', khoi_id='1')
        l2 = Lop(ten='11A1', khoi_id='2')
        l3 = Lop(ten='12A1', khoi_id='3')
        l4 = Lop(ten='12A2', khoi_id='3')
        db.session.add_all([l1, l2, l3, l4])
        db.session.commit()

        hs1 = HocSinh(ho='Nguyễn Văn', ten='Tấn', gioitinh='Nam', ngaysinh=datetime(2007, 2, 14), lop_id=1)
        hs2 = HocSinh(ho='Lê Thị', ten='Tuyết', gioitinh='Nữ', ngaysinh=datetime(2007, 1, 3), lop_id=1)
        hs3 = HocSinh(ho='Phan Văn', ten='Minh', gioitinh='Nam', ngaysinh=datetime(2007, 3, 23), lop_id=1)
        hs4 = HocSinh(ho='Nguyễn Mạnh', ten='Cường', gioitinh='Nam', ngaysinh=datetime(2007, 11, 3), lop_id=1)
        hs5 = HocSinh(ho='Lê Thị Diệu', ten='Trinh', gioitinh='Nữ', ngaysinh=datetime(2006, 12, 5), lop_id=2)
        hs6 = HocSinh(ho='Phạm Thị Hoài', ten='Thương', gioitinh='Nữ', ngaysinh=datetime(2006, 9, 18), lop_id=2)
        hs7 = HocSinh(ho='Nguyễn Hồ', ten='Long', gioitinh='Nam',ngaysinh=datetime(2005, 9, 2), lop_id=3)
        hs8 = HocSinh(ho='Đoàn Trung', ten='Phong', gioitinh='Nam', ngaysinh=datetime(2005, 11, 6), lop_id=3)
        hs9 = HocSinh(ho='Lê Văn', ten='Phôn', gioitinh='Nam', ngaysinh=datetime(2005, 1, 3), lop_id=4)
        hs10 = HocSinh(ho='Tạ Thị', ten='Mai', gioitinh='Nữ', ngaysinh=datetime(2005, 4, 25), lop_id=4)
        db.session.add_all([hs1, hs2, hs3, hs4, hs5, hs6, hs7, hs8, hs9, hs10])
        db.session.commit()




        # p1 = Product(name='iPad Pro 2022', price=24000000, category_id=2,
        #              image="https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg")


    # class Pupil(db.Model, UserMixin):
    #     id = Column(Integer, primary_key=True, autoincrement=True)
    #     firstname = Column(String(10), nullable=False)
    #     lastname = Column(String(20), nullable=False)
    #     phone = Column(String(10), nullable=False)
    # class Semester(db.Model):
    #     id = Column(Integer, primary_key=True, autoincrement=True)
    #     schoolyear = Column(String(50), nullable=False, unique=True)
    #     fromdate = Column(DateTime)
    #     todate = Column(DateTime)
    #
    #     def __str__(self):
    #         return self.name
    # class Classroom(db.Model):
    #     id = Column(Integer, primary_key=True, autoincrement=True)
    #     name = Column(String(50), nullable=False, unique=True)
    #     amount = Column(String(50), nullable=False, unique=True)
    #
    #     def __str__(self):
    #         return self.name
    # class Score(BaseModel):
    #     id = Column(Integer, primary_key=True, autoincrement=True)
    #     score = Column(String(10), nullable=False)
    #     scoretype = Column(String(10), nullable=False)
    #     user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    #     semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
# class ScoreDetails(BaseModel):
#     quantity = Column(Integer, default=0)
#     price = Column(Float, default=0)
#     receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
#     product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
# class Comment(BaseModel):
#     content = Column(String(255), nullable=False)
#     created_date = Column(DateTime, default=datetime.now())
#     user_id = Column(Integer, ForeignKey(User.id), nullable=False)
#     product_id = Column(Integer, ForeignKey(Product.id), nullable=False)