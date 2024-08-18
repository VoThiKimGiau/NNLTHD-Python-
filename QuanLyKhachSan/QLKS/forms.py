from django import forms
from django.utils import timezone
from django.db import models
from .models import HoaDon, NhanVien, KhachHang, DonDatPhong, Phong, DonDatDichVu, DichVu, Account, LoaiPhong

# 11 - Võ Thị Kim Giàu
class NhanVienChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.HoTen

class KhachHangChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.TenKhachHang

class ThemHoaDonForm(forms.Form):
    nhanVien = NhanVienChoiceField(queryset=NhanVien.objects.all(), label='Nhân viên')
    khachHang = KhachHangChoiceField(queryset=KhachHang.objects.all(), label='Khách hàng')
    ngayXuat = forms.DateTimeField(label='Ngày xuất hóa đơn',
                                   input_formats=['%d/%m/%Y %H:%M:%S'],
                                   initial=timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M:%S'))
    tongTien = forms.FloatField(min_value=0, label='Tổng tiền', widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = super().clean()
        maNV = cleaned_data.get('maNV')
        maKH = cleaned_data.get('maKH')
        ngayXuat = cleaned_data.get('ngayXuat')

        try:
            HoaDon.objects.get(MaNhanVien=maNV, MaKhachHang=maKH, NgayXuat=ngayXuat)
            raise forms.ValidationError("Hóa đơn đã tồn tại")
        except HoaDon.DoesNotExist:
            return cleaned_data

    def save(self):
        HoaDon.objects.create(
            MaNhanVien=self.cleaned_data['nhanVien'],
            MaKhachHang=self.cleaned_data['khachHang'],
            NgayXuat=self.cleaned_data['ngayXuat'],
            TongTien=self.cleaned_data['tongTien'],
        )

class HoaDonChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.MaHoaDon

class PhongChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.SoPhong

class ThemDonDatPhongForm(forms.Form):
    maDonDatPhong = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    maHoaDon = HoaDonChoiceField(queryset=HoaDon.objects.all(), label='Mã hóa đơn')
    soPhong = PhongChoiceField(queryset=Phong.objects.all(), label='Số phòng')
    ngayNhan = forms.DateTimeField(label='Ngày nhận phòng',
                                   input_formats=['%d/%m/%Y %H:%M'],
                                   initial=timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M'))
    ngayTra = forms.DateTimeField(label='Ngày trả phòng',
                                   input_formats=['%d/%m/%Y %H:%M'],
                                   initial=timezone.localtime(timezone.now() + timezone.timedelta(days=1)).strftime('%d/%m/%Y %H:%M'))
    tongTienPhong = forms.FloatField(min_value=0, label='Tổng tiền phòng', widget=forms.HiddenInput(), initial=0)
    tongTienDichVu = forms.FloatField(min_value=0, label='Tổng tiền dịch vụ', widget=forms.HiddenInput(), initial=0)
    TT_choice = (
        ("Đang sử dụng","Đang sử dụng"),
        ("Đã thanh toán","Đã thanh toán"),
        )
    tinhTrang = forms.ChoiceField(choices = TT_choice, initial="Đang sử dụng", label = 'Tình trạng')

    def clean(self):
        cleaned_data = super().clean()
        maDonDatPhong = cleaned_data.get('maDonDatPhong')
        maHoaDon = cleaned_data.get('maHoaDon')
        soPhong = cleaned_data.get('soPhong')
        ngayNhan = cleaned_data.get('ngayNhan')
        ngayTra = cleaned_data.get('ngayTra')
        tongTienPhong = cleaned_data.get('tongTienPhong')
        tongTienDichVu = cleaned_data.get('tongTienDichVu')
        tinhTrang = cleaned_data.get('tinhTrang')

        try:
            DonDatPhong.objects.get(MaHoaDon = maHoaDon, SoPhong = soPhong)
            raise forms.ValidationError("Đơn đặt phòng đã tồn tại")
        except DonDatPhong.DoesNotExist:
            return cleaned_data

    def save(self):
        listDV = DonDatDichVu.objects.all()
        listHD = HoaDon.objects.all()
        phong = Phong.objects.get(SoPhong=self.cleaned_data['soPhong'].SoPhong)
        soNgay = (self.cleaned_data['ngayTra'] - self.cleaned_data['ngayNhan']).days
        sumTDV = 0
        for dv in listDV:
            if dv.MaDonDatPhong.MaDonDatPhong == self.cleaned_data['maDonDatPhong']:
                sumTDV = sumTDV + dv.TongTienDichVu
        don_dat_phong = DonDatPhong.objects.create(
            MaHoaDon=self.cleaned_data['maHoaDon'],
            SoPhong=self.cleaned_data['soPhong'],
            NgayNhanPhong=self.cleaned_data['ngayNhan'],
            NgayTraPhong=self.cleaned_data['ngayTra'],
            TongTienPhong=phong.MaLoai.GiaMotNgay * soNgay,
            TongTienDichVu=sumTDV,
            TinhTrang=self.cleaned_data['tinhTrang'],
            )
        for hoa_don in listHD:
            if hoa_don.MaHoaDon == don_dat_phong.MaHoaDon.MaHoaDon:
                hoa_don.TongTien = hoa_don.TongTien + don_dat_phong.TongTienPhong + don_dat_phong.TongTienDichVu
                hoa_don.save()


# 34 - Phan Văn Từ Pháp
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

class ThemTaiKhoanForm(forms.Form):
    tentk = forms.CharField(max_length=255, label='Tên Tài Khoản')
    username = forms.CharField(max_length=255, label='Username')
    password = forms.CharField(max_length=255, label='Password', widget=forms.PasswordInput())
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Role')
    nhanVien = NhanVienChoiceField(queryset=NhanVien.objects.all(), label='Nhân viên', required=False)
    khachHang = KhachHangChoiceField(queryset=KhachHang.objects.all(), label='Khách hàng', required=False)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        role = cleaned_data.get('role')
        nhanVien = cleaned_data.get('nhanVien')
        khachHang = cleaned_data.get('khachHang')

        # Check for duplicate username
        if Account.objects.filter(username=username).exists():
            self.add_error('username', 'Tài khoản đã tồn tại')

        # Ensure the correct fields are filled based on the role
        if role == 'admin' and not nhanVien:
            self.add_error('nhanVien', 'Nhân viên is required for admin role')
        if role == 'customer' and not khachHang:
            self.add_error('khachHang', 'Khách hàng is required for customer role')

        return cleaned_data

    def save(self):
        role = self.cleaned_data['role']
        account = Account.objects.create(
            tentk=self.cleaned_data['tentk'],
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            role=role,
            manv=self.cleaned_data['nhanVien'] if role == 'admin' else None,
            makh=self.cleaned_data['khachHang'] if role == 'customer' else None,
        )
        return account
class SuaTaiKhoanForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Role")
    manv = NhanVienChoiceField(queryset=NhanVien.objects.all(), label="Nhân viên", required=False)
    makh = KhachHangChoiceField(queryset=KhachHang.objects.all(), label="Khách hàng", required=False)

    class Meta:
        model = Account
        fields = ['tentk', 'username', 'password', 'role', 'manv', 'makh']
        labels = {
            'tentk': 'Tên tài khoản',
            'username': 'Username',
            'password': 'Password',
            'Role': 'Role',
            'manv': 'Mã nhân viên',
            'makh': 'Mã khách hàng',
        }

        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        manv = cleaned_data.get('manv')
        makh = cleaned_data.get('makh')

        if role == 'admin' and not manv:
            self.add_error('manv', 'Nhân viên is required for admin role')
        if role == 'customer' and not makh:
            self.add_error('makh', 'Khách hàng is required for customer role')

        return cleaned_data

class XoaTaiKhoanForm(forms.Form):
    confirm = forms.BooleanField(label='Confirm deletion', required=True)

class ThemNhanVienForm(forms.Form):
    HoTen = forms.CharField(max_length=100, label='Họ tên')
    ChucVu = forms.CharField(max_length=50, label='Chức vụ')
    SDT = forms.CharField(max_length=20, label='Số điện thoại')
    Email = forms.EmailField(required=False, label='Email')
    NgayVaoLam = forms.DateField(label='Ngày vào làm')

class SuaNhanVienForm(forms.ModelForm):
    class Meta:
        model = NhanVien
        fields = ['HoTen', 'ChucVu', 'SDT', 'Email', 'NgayVaoLam']
        labels = {
            'HoTen': 'Họ tên',
            'ChucVu': 'Chức vụ',
            'SDT': 'Số điện thoại',
            'Email': 'Email',
            'NgayVaoLam': 'Ngày vào làm',
        }
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

# 41 - Nguyễn Hữu Thông
class ThemKHForm(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = ["TenKhachHang","SDT","Email","DiaChi"]
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance.pk:
            instance.save()
        else:
            instance.save()
        return instance

class DichVuForm(forms.ModelForm):
    
    class Meta:
        model = DichVu
        fields = ["TenDichVu","Gia","MoTa"]
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance.pk:
            instance.save()
        else:
            instance.save()
        return instance
    
class DonDatDichVuForm(forms.ModelForm):
    MaDonDatPhong = forms.ChoiceField(choices=[(dv.MaDonDatPhong,dv.MaDonDatPhong) for dv in DonDatPhong.objects.all()])
    MaDichVu = forms.ChoiceField(choices=[(dv.MaDichVu, dv.TenDichVu) for dv in DichVu.objects.all()])
    SoLuong = forms.IntegerField(min_value=1)
    TongTien = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    class Meta:
        model = DonDatDichVu
        fields = ["SoLuong",  "TongTien","NgayDat","MaDonDatPhong", "MaDichVu"]
      
        
        
    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['MaDonDatPhong'] = DonDatPhong.objects.get(MaDonDatPhong=cleaned_data['MaDonDatPhong'])
        cleaned_data['MaDichVu'] = DichVu.objects.get(MaDichVu=cleaned_data['MaDichVu'])
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        self.tính_tổng_tiền(instance)
        return instance
    
    def tính_tổng_tiền(self, instance):
        instance.TongTien = instance.SoLuong * instance.MaDichVu.Gia
        instance.save()

class TimTheoGia(forms.Form):
    Gia1 = forms.CharField(label='Từ giá', max_length=100)
    Gia2 = forms.CharField(label='Đến giá', max_length=100)

# 31 - Nguyễn Ngọc Ái Nhi
class LoaiPhongForm(forms.ModelForm):
    class Meta:
        model = LoaiPhong
        fields = ["TenLoai","SucChua","GiaMotNgay"]
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance.pk:
            instance.save()
        else:
            instance.save()
        return instance


class PhongForm(forms.ModelForm):
    MaLoai = forms.ChoiceField(choices=[(dv.MaLoai, dv.TenLoai) for dv in LoaiPhong.objects.all()])
    class Meta:
        model = Phong
        fields = ["TinhTrang","HinhAnh","MaLoai"]
    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['MaLoai'] = LoaiPhong.objects.get(MaLoai=cleaned_data['MaLoai'])
        return cleaned_data
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance.pk:
            instance.save()
        else:
            instance.save()
        return instance
