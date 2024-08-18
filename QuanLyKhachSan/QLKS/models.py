from django.db import models
import datetime

# Create your models here.
class NVarCharField(models.Field):
    """
    Custom field for storing Unicode strings with variable length.
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 255)
        super(NVarCharField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'nvarchar(%s)' % self.max_length

class LoaiPhong(models.Model):
    MaLoai = models.AutoField(primary_key = True)
    TenLoai = NVarCharField(max_length = 50, blank = False)
    SucChua = models.IntegerField(blank = False)
    GiaMotNgay = models.FloatField(blank = False)

class Phong(models.Model):
    SoPhong = models.IntegerField(primary_key = True)
    TinhTrang = NVarCharField(max_length = 50, blank = False)
    HinhAnh = NVarCharField(max_length = 50, blank = False)
    MaLoai = models.ForeignKey(LoaiPhong,  on_delete = models.CASCADE, related_name = 'FK_Phong_LoaiPhong')

class NhanVien(models.Model):
    MaNhanVien = models.AutoField(primary_key = True)
    HoTen = NVarCharField(max_length = 100, blank = False)
    ChucVu = NVarCharField(max_length = 50, blank = False)
    SDT = NVarCharField(max_length = 20, blank = False)
    Email = NVarCharField(max_length = 100, null = True)
    NgayVaoLam = models.DateField(default = datetime.date.today)

class KhachHang(models.Model):
    MaKhachHang = models.AutoField(primary_key = True)
    TenKhachHang = NVarCharField(max_length = 100, blank = False)
    DiaChi = models.TextField(blank = False)
    SDT = NVarCharField(max_length = 20, blank = False)
    Email = NVarCharField(max_length = 100, null = True)

class HoaDon(models.Model):
    MaHoaDon = models.AutoField(primary_key = True)
    NgayXuat = models.DateTimeField(default = datetime.datetime.now())
    TongTien = models.FloatField(default = 0)
    MaNhanVien = models.ForeignKey(NhanVien,  on_delete = models.CASCADE, related_name = 'FK_HoaDon_NhanVien')
    MaKhachHang = models.ForeignKey(KhachHang,  on_delete = models.CASCADE, related_name = 'FK_HoaDon_KhachHang')

class DonDatPhong(models.Model):
    MaDonDatPhong = models.AutoField(primary_key = True)
    NgayNhanPhong = models.DateTimeField(default = datetime.datetime.now())
    NgayTraPhong = models.DateTimeField(blank = False)
    TongTienPhong = models.FloatField(default = 0)
    TongTienDichVu = models.FloatField(default = 0)
    TinhTrang = NVarCharField(max_length = 50, blank = False)
    MaHoaDon = models.ForeignKey(HoaDon,  on_delete = models.CASCADE, related_name = 'FK_DonDatPhong_HoaDon')
    SoPhong = models.ForeignKey(Phong,  on_delete = models.CASCADE, related_name = 'FK_DonDatPhong_Phong')

class DichVu(models.Model):
    MaDichVu = models.AutoField(primary_key = True)
    TenDichVu = NVarCharField(max_length = 100, blank = False)
    Gia = models.FloatField(blank = False)
    MoTa = models.TextField(null = True)

class DonDatDichVu(models.Model):
    MaDonDatDichVu = models.AutoField(primary_key = True)
    SoLuong = models.IntegerField(default = 1)
    TongTien = models.FloatField(default = 0)
    NgayDat = models.DateTimeField(default = datetime.datetime.now())
    MaDonDatPhong = models.ForeignKey(DonDatPhong,  on_delete = models.CASCADE, related_name = 'FK_DonDatDichVu_DonDatPhong')
    MaDichVu = models.ForeignKey(DichVu,  on_delete = models.CASCADE, related_name = 'FK_DonDatDichVu_DichVu')

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    tentk = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  
    role = models.CharField(max_length=255)
    manv = models.ForeignKey(NhanVien, on_delete=models.CASCADE, related_name='FK_Account_NhanVien', null = True)
    makh = models.ForeignKey(KhachHang, on_delete=models.CASCADE, related_name='FK_Account_KhachHang', null = True)