from django.urls import path
from . import views # call to url_shortener/views.py

urlpatterns = [
# 11 - Võ Thị Kim Giàu
path('HoaDonAdmin', views.dsHD, name='HoaDonAdmin'),
path('ThemHoaDon', views.themHoaDon, name='ThemHoaDon'),
path('XoaHoaDon/<int:mahd>/', views.xoaHoaDon, name='XoaHoaDon'),
path('SuaHoaDon/<int:mahd>/', views.suaHoaDon, name='SuaHoaDon'),
path('DonDatPhongAdmin', views.dsDDP, name='DonDatPhongAdmin'),
path('ThemDonDatPhong', views.themDonDatPhong, name='ThemDonDatPhong'),
path('XoaDonDatPhong/<int:maddp>/', views.xoaDonDatPhong, name='XoaDonDatPhong'),
path('SuaDonDatPhong/<int:maddp>/', views.suaDonDatPhong, name='SuaDonDatPhong'),
path('HoaDon', views.hoaDonKH, name='HoaDon'),
path('ThemDonDatPhongKH/<int:soph>/', views.themDonDatPhongKH, name='ThemDonDatPhongKH'),
path('ChiTietPhong/<int:soph>/', views.xemChiTietPhong, name='ChiTietPhong'),
# 34 - Phan Văn Từ Pháp
path('index', views.index, name='homeadmin'),
path('loaiphong', views.listphong, name='loaiphong'),
path('home', views.home, name='home'),
path('dsnv', views.emplist, name='nhanvien'),
path('account', views.acclist, name='taikhoan'),
path('', views.checkLogin, name='Login'),
path('about', views.about, name='about'),
path('services', views.services, name='services'),
path('detailrooms', views.detailrooms, name='detailrooms'),
path('rooms', views.rooms, name='rooms'),
path('contact', views.contact, name='contact'),
path('blog', views.blog, name='blog'),
path('ThemTaiKhoan', views.themTaiKhoan, name='ThemTaiKhoan'),
path('XoaTaiKhoan/<int:id>/', views.xoaTaiKhoan, name='XoaTaiKhoan'),
path('SuaTaiKhoan/<int:id>/', views.suaTaiKhoan, name='SuaTaiKhoan'),
path('ThemNhanVien', views.themNhanVien, name='ThemNhanVien'),
path('XoaNhanVien/<int:id>/', views.xoaNhanVien, name='XoaNhanVien'),
path('SuaNhanVien/<int:id>/', views.suaNhanVien, name='SuaNhanVien'),
path('logout', views.logout_view, name='logout'),
path('admin', views.admin_index, name='admin_index'),  
path('customer', views.customer_home, name='customer_home'),
path('register', views.register, name='register'),
path('searchaccount', views.account_search, name='account_search'),
path('searchemployee', views.nhanvien_search, name='nhanvien_search'),
# 41 - Nguyễn Hữu Thông
path('dskh1', views.dskh1, name='dskh1'),
path('themkh', views.themkh, name='themkh'),
path('xoakh/<int:id>/', views.xoakh, name='xoakh'),
path('suakh/<int:id>/', views.suakh, name='suakh'),
path('dsdv1', views.dsdv1, name='dsdv1'),
path('themdv', views.themdv, name='themdv'),
path('xoadv/<int:id>/', views.xoadv, name='xoadv'),
path('suadv/<int:id>/', views.suadv, name='suadv'),
path('dsddv1', views.dsddv1, name='dsddv1'),
path('themddv', views.themddv, name='themddv'),
path('xoaddv/<int:id>/', views.xoaddv, name='xoaddv'),
path('suaddv/<int:id>/', views.suaddv, name='suaddv'),
path('dsdv2', views.dsdv2, name='dsdv2'),
path('themddv1', views.themddv1, name='themddv1'),
path('Search', views.Search, name='Search'),
# 31 - Nguyễn Ngọc Ái Nhi
path('loaiphong', views.loaiphong, name='loaiphong'),
path('themlp', views.themlp, name='themlp'),
path('xoalp/<int:id>/', views.xoalp, name='xoalp'),
path('sualp/<int:id>/', views.sualp, name='sualp'),
    
path('phong', views.dsp, name='phong'),
path('phongKH', views.dspKH, name='phongKH'),
path('themPH', views.themPH, name='themPH'),
path('xoaPH/<int:id>/', views.xoaPH, name='xoaPH'),
path('suaPH/<int:id>/', views.suaPH, name='suaPH'),
]