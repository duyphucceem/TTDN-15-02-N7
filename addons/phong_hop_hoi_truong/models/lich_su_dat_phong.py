from odoo import models, fields, api
from datetime import timedelta

class LichSuDatPhong(models.Model):
    _name = "lich_su_dat_phong"
    _description = "Lịch sử đặt phòng"

    phong_hop_id = fields.Many2one("danh_sach_phong_hop", string="Phòng họp", required=True)
    nhan_vien_id = fields.Many2one("nhan_vien", string="Người đặt", required=True)
    thoi_gian_bat_dau = fields.Datetime(string="Thời gian bắt đầu", required=True)
    thoi_gian_ket_thuc = fields.Datetime(string="Thời gian kết thúc", required=True)
    don_muon_phong_id = fields.Many2one('don_muon_phong', string="Đơn mượn phòng")
    
    trang_thai = fields.Selection([
        ('dang_dien_ra', 'Đang diễn ra'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy'),
        ('confirmed', 'Đã xác nhận'),
    ], string="Trạng thái", default="dang_dien_ra")

    @api.model
    def create_history(self, don_muon_phong):
        """ Kiểm tra trước khi tạo lịch sử """
        existing_history = self.search([
            ('don_muon_phong_id', '=', don_muon_phong.id),
            ('trang_thai', '=', 'confirmed')
        ], limit=1)
        if not existing_history:
            self.create({
                'don_muon_phong_id': don_muon_phong.id,
                'nhan_vien_id': don_muon_phong.nhan_vien_id.id,
                'phong_hop_id': don_muon_phong.phong_hop_id.id,
                'thoi_gian_bat_dau': don_muon_phong.thoi_gian_bat_dau,
                'thoi_gian_ket_thuc': don_muon_phong.thoi_gian_ket_thuc,
                'trang_thai': don_muon_phong.trang_thai
            })

    @api.constrains('thoi_gian_bat_dau', 'thoi_gian_ket_thuc')
    def _check_time_constraints(self):
        """ Kiểm tra thời gian bắt đầu phải trước thời gian kết thúc và thời gian cách nhau tối đa 4 giờ """
        for record in self:
            if record.thoi_gian_bat_dau >= record.thoi_gian_ket_thuc:
                raise exceptions.ValidationError("Thời gian bắt đầu phải trước thời gian kết thúc.")
            
            # Kiểm tra khoảng cách giữa thời gian bắt đầu và kết thúc
            delta = record.thoi_gian_ket_thuc - record.thoi_gian_bat_dau
            if delta > timedelta(hours=4):
                raise exceptions.ValidationError("Thời gian kết thúc không được cách thời gian bắt đầu quá 4 giờ.")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.ten_phong))  # Hiển thị tên phòng thay vì ID
        return result