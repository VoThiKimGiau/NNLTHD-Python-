from django.shortcuts import render, redirect, get_object_or_404
from .models import LoaiPhong, HoaDon, DonDatPhong, NhanVien, KhachHang, DonDatDichVu, Phong, Account, DichVu
from .forms import ThemHoaDonForm, ThemDonDatPhongForm, LoginForm, ThemKHForm, DichVuForm, ThemTaiKhoanForm, SuaTaiKhoanForm,XoaTaiKhoanForm,ThemNhanVienForm,SuaNhanVienForm,LoaiPhongForm, PhongForm,DonDatDichVuForm, TimTheoGia
import locale
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
import getpass
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.auth.models import User

# Create your views here.
#def index(request):
#	return render(request, 'pages/customer/home.html')
# 11 - Võ Thị Kim Giàu
def list(request):
	data = {
		'DM_loaiphong': LoaiPhong.objects.all(),
		}
	return render(request, 'pages/customer/home.html', data)

def dsHD(request):
	listHD = HoaDon.objects.all()
	for hd in listHD:
		hd.TongTienFormatted = format_currency(hd.TongTien)
	data = {
		'ds_HD': listHD,
		}
	return render(request, 'pages/admin/HoaDonAdmin.html', data)

def themHoaDon(request):
	form = ThemHoaDonForm()
	if request.method == 'POST':
		form = ThemHoaDonForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('HoaDonAdmin')
	return render(request, 'pages/admin/ThemHoaDon.html', {'form' : form})

def xoaHoaDon(request, mahd):
    hoa_don = get_object_or_404(HoaDon, MaHoaDon=mahd)
    hoa_don.TongTienFormatted = format_currency(hoa_don.TongTien)
    if request.method == 'POST':
        hoa_don.delete()
        return redirect('HoaDonAdmin')
    return render(request, 'pages/admin/XoaHoaDon.html', {'hoa_don': hoa_don})

def sumTongTien(hoa_don):
	listDP = DonDatPhong.objects.all()
	sumTT = 0
	for dp in listDP:
		if dp.MaHoaDon.MaHoaDon == hoa_don.MaHoaDon:
			sumTT = sumTT + dp.TongTienPhong + dp.TongTienDichVu
	return float(sumTT)

def suaHoaDon(request, mahd):
	hoa_don = get_object_or_404(HoaDon, MaHoaDon=mahd)
	listNV = NhanVien.objects.all()
	listKH = KhachHang.objects.all()
	hoa_don.TongTienFormatted = format_currency(sumTongTien(hoa_don))
	data = {
		'ds_NV': listNV,
		'ds_KH': listKH,
		'hoa_don': hoa_don,
		}
	if request.method == 'POST':
		# Lấy dữ liệu mới từ form
		MaNhanVien = request.POST['MaNhanVien']
		MaKhachHang = request.POST['MaKhachHang']
		NgayXuat = request.POST['NgayXuat']

		# Lấy instance của NhanVien dựa trên MaNhanVien
		nv_instance = NhanVien.objects.get(MaNhanVien=MaNhanVien)

		# Lấy instance của NhanVien dựa trên MaNhanVien
		kh_instance = KhachHang.objects.get(MaKhachHang=MaKhachHang)

		# Chuyển đổi định dạng ngày tháng
		date_time = datetime.strptime(NgayXuat, '%d/%m/%Y %H:%M:%S')
		formatted_date = date_time.strftime('%Y-%m-%d %H:%M:%S')

		# Cập nhật thông tin hóa đơn
		hoa_don.MaNhanVien = nv_instance
		hoa_don.MaKhachHang = kh_instance
		hoa_don.NgayXuat = formatted_date
		hoa_don.TongTien = sumTongTien(hoa_don)
		hoa_don.save()    
		return redirect('HoaDonAdmin')

	return render(request, 'pages/admin/SuaHoaDon.html', data)

def format_currency(value):
    locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
    return f"{value:,.0f} ₫"


def dsDDP(request):
	listDP = DonDatPhong.objects.all()
	for dp in listDP:
		dp.TongTienPhongFormatted = format_currency(dp.TongTienPhong)
		dp.TongTienDichVuFormatted = format_currency(dp.TongTienDichVu)
	data = {
		'ds_DP': listDP,
		}
	return render(request, 'pages/admin/DonDatPhongAdmin.html', data)

def themDonDatPhong(request):
	form = ThemDonDatPhongForm()
	listDV = DonDatDichVu.objects.all()
	if request.method == 'POST':
		form = ThemDonDatPhongForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('DonDatPhongAdmin')
	return render(request, 'pages/admin/ThemDonDatPhong.html', {'form': form})

def xoaDonDatPhong(request, maddp):
	don_dat_phong = get_object_or_404(DonDatPhong, MaDonDatPhong=maddp)
	don_dat_phong.TongTienPhongFormatted = format_currency(don_dat_phong.TongTienPhong)
	don_dat_phong.TongTienDichVuFormatted = format_currency(don_dat_phong.TongTienDichVu)
	hoa_don = don_dat_phong.MaHoaDon
	if request.method == 'POST':
		don_dat_phong.delete()
		hoa_don.TongTien = sumTongTien(hoa_don)
		hoa_don.save()    
		return redirect('DonDatPhongAdmin')
	return render(request, 'pages/admin/XoaDonDatPhong.html', {'don_dat_phong': don_dat_phong})

def sumTienPhong(don_dat_phong):
    phong = Phong.objects.get(SoPhong=don_dat_phong.SoPhong.SoPhong)
    
    ngay_nhan_phong = datetime.strptime(don_dat_phong.NgayNhanPhong, '%Y-%m-%d %H:%M')
    ngay_tra_phong = datetime.strptime(don_dat_phong.NgayTraPhong, '%Y-%m-%d %H:%M')
    
    soNgay = (ngay_tra_phong - ngay_nhan_phong).days
    
    return float(phong.MaLoai.GiaMotNgay * soNgay)
	

def sumTienDichVu(don_dat_phong):
	listDV = DonDatDichVu.objects.all()
	sumTDV = 0
	for dv in listDV:
		if dv.MaDonDatPhong.MaDonDatPhong == don_dat_phong.MaDonDatPhong:
			sumTDV = sumTDV + dv.TongTien
	return float(sumTDV)

def suaDonDatPhong(request, maddp):
	don_dat_phong = get_object_or_404(DonDatPhong, MaDonDatPhong=maddp)
	listHD = HoaDon.objects.all()
	listPH = Phong.objects.all()
	hoa_don = don_dat_phong.MaHoaDon

	don_dat_phong.TongTienPhongFormatted = format_currency(don_dat_phong.TongTienPhong)
	don_dat_phong.TongTienDichVuFormatted = format_currency(don_dat_phong.TongTienDichVu)

	data = {
		'ds_HD': listHD,
		'ds_PH': listPH,
		'don_dat_phong': don_dat_phong,
		}
	if request.method == 'POST':
		# Lấy dữ liệu mới từ form
		MaHoaDon = request.POST['MaHoaDon']
		SoPhong = request.POST['SoPhong']
		NgayNhanPhong = request.POST['NgayNhanPhong']
		NgayTraPhong = request.POST['NgayTraPhong']
		TinhTrang = request.POST['TinhTrang']

		# Lấy instance của HoaDon dựa trên MaHoaDon
		hd_instance = HoaDon.objects.get(MaHoaDon=MaHoaDon)

		# Lấy instance của SoPhong dựa trên SoPhong
		ph_instance = Phong.objects.get(SoPhong=SoPhong)

		# Chuyển đổi định dạng ngày tháng
		date_time_nhan = datetime.strptime(NgayNhanPhong, '%d/%m/%Y %H:%M')
		formatted_date_nhan = date_time_nhan.strftime('%Y-%m-%d %H:%M')
		date_time_tra = datetime.strptime(NgayTraPhong, '%d/%m/%Y %H:%M')
		formatted_date_tra = date_time_tra.strftime('%Y-%m-%d %H:%M')

		# Cập nhật thông tin
		don_dat_phong.MaHoaDon = hd_instance
		don_dat_phong.SoPhong = ph_instance
		don_dat_phong.NgayNhanPhong = formatted_date_nhan
		don_dat_phong.NgayTraPhong = formatted_date_tra
		don_dat_phong.TongTienPhong = sumTienPhong(don_dat_phong)
		don_dat_phong.TongTienDichVu = sumTienDichVu(don_dat_phong)
		don_dat_phong.TinhTrang = TinhTrang
		don_dat_phong.save()    

		hoa_don.TongTien = sumTongTien(hoa_don)
		hoa_don.save()
		return redirect('DonDatPhongAdmin')

	return render(request, 'pages/admin/SuaDonDatPhong.html', data)

def hoaDonKH(request):
	khach_hang = get_object_or_404(KhachHang, MaKhachHang=1) # Chưa lấy được theo mã khách hàng đang đăng nhập

	if khach_hang is None:
		return render(request, 'pages/customer/home.html')
	
	try:
		ds_HD = HoaDon.objects.filter(MaKhachHang=khach_hang.MaKhachHang)
		hoa_don_data = []
		for hoa_don in ds_HD:
			hoa_don.TongTienFormatted = format_currency(hoa_don.TongTien)
			ds_DP = DonDatPhong.objects.filter(MaHoaDon=hoa_don.MaHoaDon)
			for dp in ds_DP:
				dp.TongTienPhongFormatted = format_currency(dp.TongTienPhong)
				dp.TongTienDichVuFormatted = format_currency(dp.TongTienDichVu)

			ds_DV = DonDatDichVu.objects.filter(MaDonDatPhong__in=[dp.MaDonDatPhong for dp in ds_DP])
			for dv in ds_DV:
				dv.TongTienFormatted = format_currency(dv.TongTien)
				dv.GiaFormatted = format_currency(dv.MaDichVu.Gia)

			hoa_don_data.append({
				'hoa_don': hoa_don,
				'ds_DP': ds_DP,
				'ds_DV': ds_DV,
			})

		nhan_vien = get_object_or_404(NhanVien, MaNhanVien=1)
		data = {
			'khach_hang': khach_hang,
			'nhan_vien': nhan_vien,
			'hoa_don_data': hoa_don_data,
		}
		return render(request, 'pages/customer/HoaDon.html', data)
	except KhachHang.DoesNotExist:
		return render(request, 'pages/admin/HoaDonAdmin.html')

def themDonDatPhongKH(request, soph):
	listDV = DonDatDichVu.objects.all()
	nv_instance = NhanVien.objects.get(MaNhanVien=1)
	kh_instance = KhachHang.objects.get(MaKhachHang=1) #layMaKHTuAccount()
	phong = Phong.objects.get(SoPhong=soph)
	don_dat_phong = None  

	if request.method == 'POST':
		NgayNhan = request.POST['NgayNhanPhong']
		NgayTra = request.POST['NgayTraPhong']
		date_time_nhan = datetime.strptime(NgayNhan, '%d/%m/%Y %H:%M')
		formatted_date_nhan = date_time_nhan.strftime('%Y-%m-%d %H:%M')
		date_time_tra = datetime.strptime(NgayTra, '%d/%m/%Y %H:%M')
		formatted_date_tra = date_time_tra.strftime('%Y-%m-%d %H:%M')

		soNgay = (date_time_tra - date_time_nhan).days

		hoa_don = HoaDon.objects.create(
			MaNhanVien=nv_instance,
			MaKhachHang=kh_instance,
			NgayXuat=timezone.now(),
			TongTien=0,
			)

		don_dat_phong = DonDatPhong.objects.create(
			MaHoaDon=hoa_don,
			SoPhong=phong,
			NgayNhanPhong=formatted_date_nhan,
			NgayTraPhong=formatted_date_tra,
			TongTienPhong=phong.MaLoai.GiaMotNgay * soNgay,
			TongTienDichVu=0,
			TinhTrang="Đang sử dụng",
		)

		sumTDV = 0
		for dv in listDV:
			if dv.MaDonDatPhong == don_dat_phong.MaDonDatPhong:
				sumTDV = sumTDV + dv.TongTienDichVu

		don_dat_phong.TongTienDichVu = sumTDV
		don_dat_phong.TongTienPhongFormatted = format_currency(don_dat_phong.TongTienPhong)
		don_dat_phong.TongDichVuFormatted = format_currency(don_dat_phong.TongTienDichVu)

		hoa_don.TongTien = hoa_don.TongTien + don_dat_phong.TongTienPhong + don_dat_phong.TongTienDichVu
		hoa_don.save()

		data = {
			'hoa_don': hoa_don,
			'phong': phong,
			'don_dat_phong': don_dat_phong,
		}
		return redirect('HoaDon')
	else:
		NgayNhan = timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M')
		NgayTra = timezone.localtime(timezone.now() + timezone.timedelta(days=1)).strftime('%d/%m/%Y %H:%M')

		data = {
			'NgayNhan': NgayNhan,
			'NgayTra': NgayTra,
        }
		return render(request, 'pages/customer/ThemDonDatPhongKH.html', data)

def xemChiTietPhong(request, soph):
	phong = Phong.objects.get(SoPhong=soph)
	phong.MaLoai.GiaMotNgayFormatted = format_currency(phong.MaLoai.GiaMotNgay)
	return render(request, 'pages/customer/ChiTietPhong.html', {'p':phong})

# 34 - Phan Văn Từ Pháp
def index(request):
    return render(request, 'pages/admin/home.html')

def about(request):
    return render(request, 'pages/customer/about.html')

def services(request):
    return render(request, 'pages/customer/services.html')

def detailrooms(request):
    return render(request, 'pages/customer/detailrooms.html')

def rooms(request):
    return render(request, 'pages/customer/rooms.html')

def contact(request):
    return render(request, 'pages/customer/contact.html')

def blog(request):
    return render(request, 'pages/customer/blog.html')
def listphong(request):
	data = {
		'DM_loaiphong': LoaiPhong.objects.all(),
		}
	return render(request, 'pages/admin/LoaiPhong.html', data)
def home(request):
    return render(request, 'pages/customer/home.html')

def emplist(request):
	data = {
		'Lst_Employee': NhanVien.objects.all(),
		}
	return render(request, 'pages/admin/DSNV.html', data)


def acclist(request):
	data = {
		'Lst_Account': Account.objects.all(),
        'Lst_Employee': NhanVien.objects.all(),
		'Lst_Customer': KhachHang.objects.all(),
		}
	return render(request, 'pages/admin/Account.html', data)

def themTaiKhoan(request):
    if request.method == 'POST':
        form = ThemTaiKhoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/QLKS/account') 
    else:
        form = ThemTaiKhoanForm()
    return render(request, 'pages/admin/ThemTaiKhoan.html', {'form': form})
def suaTaiKhoan(request, id):
    account = get_object_or_404(Account, id=id)
    if request.method == 'POST':
        form = SuaTaiKhoanForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('/QLKS/account')
    else:
        form = SuaTaiKhoanForm(instance=account)
    return render(request, 'pages/admin/SuaTaiKhoan.html', {'form': form, 'account': account})

def xoaTaiKhoan(request, id):
    account = get_object_or_404(Account, id=id)
    if request.method == 'POST':
        form = XoaTaiKhoanForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            account.delete()
            return redirect('/QLKS/account')
    else:
        form = XoaTaiKhoanForm()
    return render(request, 'pages/admin/XoaTaiKhoan.html', {'form': form, 'account': account})

def themNhanVien(request):
    if request.method == 'POST':
        form = ThemNhanVienForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            nhanvien = NhanVien(
                HoTen=data['HoTen'],
                ChucVu=data['ChucVu'],
                SDT=data['SDT'],
                Email=data['Email'],
                NgayVaoLam=data['NgayVaoLam']
            )
            nhanvien.save()
            return redirect('/QLKS/dsnv')  # Chuyển hướng đến trang chính sau khi đã tạo thành công
    else:
        form = ThemNhanVienForm()
    return render(request, 'pages/admin/ThemNhanVien.html', {'form': form})

def suaNhanVien(request, id):
    nhanvien = get_object_or_404(NhanVien, MaNhanVien=id)
    if request.method == 'POST':
        form = SuaNhanVienForm(request.POST, instance=nhanvien)
        if form.is_valid():
            form.save()
            return redirect('/QLKS/dsnv')  # Chuyển hướng về trang chính sau khi đã sửa thành công
    else:
        form = SuaNhanVienForm(initial={
            'HoTen': nhanvien.HoTen,
            'ChucVu': nhanvien.ChucVu,
            'SDT': nhanvien.SDT,
            'Email': nhanvien.Email,
            'NgayVaoLam': nhanvien.NgayVaoLam
        })
    return render(request, 'pages/admin/SuaNhanVien.html', {'form': form})

def xoaNhanVien(request, id):
    nhanvien = get_object_or_404(NhanVien, MaNhanVien =id)
    if request.method == 'POST':
        nhanvien.delete()
        return redirect('/QLKS/dsnv')  # Chuyển hướng về trang chính sau khi đã xóa thành công
    return render(request, 'pages/admin/XoaNhanVien.html', {'nhanvien': nhanvien})

def checkLogin(request):
    if request.method == 'POST':
        username1 = request.POST.get('username1')
        password1 = request.POST.get('password1')

        accounts = Account.objects.filter(username=username1, password=password1)
        for account in accounts:
            if account.role == 'admin':
                return redirect('admin_index')
            elif account.role == 'customer':
                return redirect('customer_home')
        
        messages.error(request, 'Invalid username or password')

    return render(request, 'pages/admin/Login.html')

def logout_view(request):
    logout(request)
    return redirect('/QLKS/')
def admin_index(request):
    return render(request, 'pages/admin/home.html')

def customer_home(request):
    return render(request, 'pages/customer/home.html')

def register(request):
    if request.method == 'POST':
        tentk = request.POST.get('tentk')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Kiểm tra xác nhận mật khẩu
        if password != confirm_password:
            messages.error(request, "Mật khẩu và xác nhận mật khẩu không khớp.")
            return redirect('/QLKS/register')

        # Kiểm tra xem người dùng đã tồn tại chưa
        if Account.objects.filter(username=username).exists():
            messages.error(request, "Tên người dùng đã tồn tại.")
            return redirect('/QLKS/register')

        # Tạo tài khoản mới với vai trò mặc định là 'customer'
        account = Account(
            tentk=tentk, 
            username=username, 
            password=password, 
            role='customer'
        )
        account.save()

        messages.success(request, "Tài khoản đã được tạo thành công. Vui lòng đăng nhập.")
        return redirect('/QLKS/')

    return render(request, 'pages/admin/DangKyTaiKhoan.html')

# Tìm kiếm account
def account_search(request):
    query = request.GET.get('q')
    if query:
        Lst_Account = Account.objects.filter(
            Q(tentk__icontains=query) |
            Q(username__icontains=query) |
            Q(role__icontains=query)
        )
    else:
        Lst_Account = Account.objects.all()
    
    return render(request, 'pages/admin/Account.html', {'Lst_Account': Lst_Account})
# Tìm kiếm nhân viên
def nhanvien_search(request):
    query = request.GET.get('q')
    if query:
        Lst_Employee = NhanVien.objects.filter(
            Q(MaNhanVien__icontains=query) |
            Q(HoTen__icontains=query) 
            
        )
    else:
        Lst_Employee = NhanVien.objects.all()
    
    return render(request, 'pages/admin/DSNV.html', {'Lst_Employee': Lst_Employee})

# 41 - Nguyễn Hữu Thông
def dskh1(request):
	data = {
		'DM_khachhang': KhachHang.objects.all(),
	}
	return render(request, 'pages/admin/KhachHang.html', data)

def dsdv1(request):
	data = {
		'DM_dichvu': DichVu.objects.all(),
	}
	return render(request, 'pages/admin/DichVu.html', data)

def dsdv2(request):
	data = {
		'DM_dichvu': DichVu.objects.all(),
	}
	return render(request, 'pages/customer/DichVu.html', data)

def themkh(request):
	form = ThemKHForm()
	if request.method == 'POST':
		form = ThemKHForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/QLKS/dskh1')
	return render(request, 'pages/admin/ThemKH.html', {'form': form,'DM_khachhang': KhachHang.objects.all()})


def xoakh(request, id):
    kh = get_object_or_404(KhachHang, MaKhachHang=id)
    if request.method == 'POST':
        kh.delete()
        return redirect('dskh1')
    return render(request, 'pages/admin/XoaKH.html', {'DM_khachhang': kh})

def suakh(request, id):
    instance = get_object_or_404(KhachHang, MaKhachHang=id)
    form = ThemKHForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dskh1')
    return render(request, 'pages/admin/SuaKH.html', {'form': form, 'DM_khachhang': instance})


def themdv(request):
	form = DichVuForm()
	if request.method == 'POST':
		form = DichVuForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/QLKS/dsdv1')
	return render(request, 'pages/admin/ThemDV.html', {'form': form,'DM_dichvu': DichVu.objects.all()})

def xoadv(request, id):
    dv = get_object_or_404(DichVu, MaDichVu=id)
    if request.method == 'POST':
        dv.delete()
        return redirect('dsdv1')
    return render(request, 'pages/admin/XoaDV.html', {'DM_dichvu': dv})

def suadv(request, id):
    instance = get_object_or_404(DichVu, MaDichVu=id)
    form = DichVuForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dsdv1')
    return render(request, 'pages/admin/SuaDV.html', {'form': form, 'DM_dichvu': instance})

def dsddv1(request):
	data = {
		'DM_dondv': DonDatDichVu.objects.all(),
	}
	return render(request, 'pages/admin/DonDichVu.html', data)

def themddv(request):
	form = DonDatDichVuForm()
	if request.method == 'POST':
		form = DonDatDichVuForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/QLKS/dsddv1')
	return render(request, 'pages/admin/ThemDonDV.html', {'form': form,'DM_dondv': DonDatDichVu.objects.all()})

def themddv1(request):
	form = DonDatDichVuForm()
	if request.method == 'POST':
		form = DonDatDichVuForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/QLKS/dsdv2')
	return render(request, 'pages/customer/ThemDonDV.html', {'form': form,'DM_dondv': DonDatDichVu.objects.all()})


def xoaddv(request, id):
    dv = get_object_or_404(DonDatDichVu, MaDonDatDichVu=id)
    if request.method == 'POST':
        dv.delete()
        return redirect('dsddv1')
    return render(request, 'pages/admin/XoaDonDV.html', {'DM_dondv': dv})

def suaddv(request, id):
    instance = get_object_or_404(DonDatDichVu, MaDonDatDichVu=id)
    form = DonDatDichVuForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dsddv1')
    return render(request, 'pages/admin/SuaDonDV.html', {'form': form, 'DM_dondv': instance})

def Search(request):
    form = TimTheoGia()
    if request.method == 'POST':
        form = TimTheoGia(request.POST)
        if form.is_valid():
              g1 = int(request.POST["Gia1"])
              g2 = request.POST["Gia2"]
              rooms = Phong.objects.all().filter(MaLoai__GiaMotNgay__gte=g1,MaLoai__GiaMotNgay__lte=g2)
              room_count = rooms.count()
              data = {
				'DM_phong': rooms,
				'DM_loaiphong': LoaiPhong.objects.all(),
                'gia':g1,
                'room_count': room_count
            	}
        return render(request,'pages/customer/phong.html', data )
    return render(request, 'pages/customer/TimPhong.html', {'form': form})

# 31 - Nguyễn Ngọc Ái Nhi
def loaiphong(request):
	data = {
		'DM_loaiphong': LoaiPhong.objects.all(),
		}
	return render(request, 'pages/admin/LoaiPhong.html', data)

def dsp(request):
	data = {
		'DM_phong': Phong.objects.all(),
	}
	return render(request,'pages/admin/Phong.html', data)

def dspKH(request):
	data = {
		'DM_phong': Phong.objects.all(),
		'DM_loaiphong': LoaiPhong.objects.all(),
	}
	return render(request,'pages/customer/phong.html', data)

def themlp(request):
	form = LoaiPhongForm()
	if request.method == 'POST':
		form = LoaiPhongForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/QLKS/loaiphong')
	return render(request,'pages/admin/ThemLoai.html', {'form': form,'DM_loaiphong': LoaiPhong.objects.all()})
	
def xoalp(request, id):
    kh = get_object_or_404(LoaiPhong, MaLoai=id)
    if request.method == 'POST':
        kh.delete()
        return redirect('loaiphong')
    return render(request, 'pages/admin/XoaLoai.html', {'DM_loaiphong': kh})

def sualp(request, id):
    instance = get_object_or_404(LoaiPhong, MaLoai=id)
    form = LoaiPhongForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('loaiphong')
    return render(request, 'pages/admin/SuaLoai.html', {'form': form, 'DM_loaiphong': instance})

def themPH(request):
	form = PhongForm()
	if request.method == 'POST':
		form = PhongForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/QLKS/phong')
	return render(request,'pages/admin/ThemPhong.html', {'form': form,'DM_phong': Phong.objects.all()})
	
def xoaPH(request, id):
    kh = get_object_or_404(Phong, SoPhong=id)
    if request.method == 'POST':
        kh.delete()
        return redirect('phong')
    return render(request, 'pages/admin/XoaPhong.html', {'DM_phong': kh})

def suaPH(request, id):
    instance = get_object_or_404(Phong, SoPhong=id)
    form = PhongForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('phong')
    return render(request, 'pages/admin/SuaPhong.html', {'form': form, 'DM_phong': instance})