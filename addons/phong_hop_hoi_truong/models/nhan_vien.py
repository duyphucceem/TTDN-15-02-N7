from odoo import models, fields, api

class NhanVien(models.Model):
    _name = "nhan_vien"
    _description = "Nhân viên"
    _rec_name = 'ma_nhan_vien'

    ma_nhan_vien = fields.Char(string="Mã Nhân Viên", required=True, copy=False, index=True, unique=True)
    ho_ten = fields.Char(string="Họ và Tên", required=True)
    ngay_sinh = fields.Date(string="Ngày Sinh")
    gioi_tinh = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
    ], string="Giới Tính", default='male')
    so_dien_thoai = fields.Char(string="Số Điện Thoại")
    email = fields.Char(string="Email")
    chuc_vu = fields.Selection([
        ('nhan_vien', 'Nhân viên'),
        ('quan_ly', 'Quản lý'),
        ('ky_thuat', 'Kỹ thuật viên'),
    ], string="Chức vụ", default="nhan_vien")
    
    lich_su_dat_phong_ids = fields.One2many("lich_su_dat_phong", "nhan_vien_id", string="Lịch sử đặt phòng")
    bao_tri_ids = fields.One2many("quan_ly_bao_tri", "nhan_vien_id", string="Lịch sử bảo trì")
    trang_thai = fields.Selection([
        ('working', 'Đang Làm Việc'),
        ('on_leave', 'Đang Nghỉ Phép')
    ], string="Trạng Thái", default='working')

    @api.depends('ngay_sinh')
    def _compute_tuoi(self):
        for rec in self:
            if rec.ngay_sinh:
                rec.tuoi = fields.Date.today().year - rec.ngay_sinh.year
            else:
                rec.tuoi = 0

    tuoi = fields.Integer(string="Tuổi", compute="_compute_tuoi", store=True)

    def action_set_working(self):
        """ Cập nhật trạng thái nhân viên về 'working' khi nhấn nút Lưu """
        for record in self:
            if record.trang_thai != 'on_leave':
                record.trang_thai = 'working'