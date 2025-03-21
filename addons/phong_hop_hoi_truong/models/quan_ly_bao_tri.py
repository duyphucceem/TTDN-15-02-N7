from odoo import models, fields, api

class QuanLyBaoTri(models.Model):
    _name = "quan_ly_bao_tri"
    _description = "Quản lý bảo trì"

    thiet_bi_id = fields.Many2one("thiet_bi_phong_hop", string="Tên thiết bị", required=True)
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên bảo trì", required=True)
    ngay_bao_tri = fields.Date(string="Ngày bảo trì", required=True)
    ghi_chu = fields.Text(string="Ghi chú")
    
    trang_thai = fields.Selection([
        ('dang_bao_tri', 'Đang bảo trì'),
        ('hoan_thanh', 'Hoàn thành'),
    ], string="Trạng thái", default="dang_bao_tri")
    
    # Liên kết phòng thông qua thiết bị
    phong_hop_id = fields.Many2one(related="thiet_bi_id.phong_hop_id", string="Phòng họp", store=True)

    @api.model
    def create(self, vals):
        # Đảm bảo rằng tên thiết bị sẽ được hiển thị khi tạo mới
        res = super(QuanLyBaoTri, self).create(vals)
        return res
