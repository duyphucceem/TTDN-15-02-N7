from odoo import models, fields, api

class DanhSachPhongHop(models.Model):
    _name = "danh_sach_phong_hop"
    _description = "Danh sách phòng họp"

    ten_phong = fields.Char(string="Tên phòng", required=True)
    suc_chua = fields.Integer(string="Sức chứa")
    vi_tri = fields.Char(string="Vị trí")
    trang_thai = fields.Selection([
        ('available', 'Trống'),
        ('using', 'Đang sử dụng'),
        ('maintenance', 'Bảo trì'),
        ('booked', 'Đã đặt'),
    ], string="Trạng thái", default="available")
    hinh_anh_phong_hop = fields.Binary(string='Hình ảnh')
    
    thiet_bi_ids = fields.One2many("thiet_bi_phong_hop", "phong_hop_id", string="Thiết bị")
    lich_su_dat_phong_ids = fields.One2many("lich_su_dat_phong", "phong_hop_id", string="Lịch sử đặt phòng")

    # Trường tính toán số phòng đã sử dụng
    so_phong_da_su_dung = fields.Integer(string="Số phòng đã sử dụng", compute='_compute_so_phong_da_su_dung')
    so_phong_total = fields.Integer(string="Tổng số phòng", compute='_compute_so_phong_total')

    @api.depends('lich_su_dat_phong_ids')
    def _compute_so_phong_da_su_dung(self):
        for record in self:
            record.so_phong_da_su_dung = len(record.lich_su_dat_phong_ids.filtered(lambda l: l.trang_thai == 'confirmed'))


    @api.depends('lich_su_dat_phong_ids')
    def _compute_so_phong_total(self):
        for record in self:
            record.so_phong_total = len(record.env['danh_sach_phong_hop'].search([]))



    @api.depends('lich_su_dat_phong_ids', 'thiet_bi_ids')
    def _compute_room_status(self):
        for record in self:
            if record.lich_su_dat_phong_ids.filtered(lambda r: r.trang_thai == 'confirmed'):
                record.trang_thai = 'using'
            elif record.thiet_bi_ids.filtered(lambda t: t.trang_thai == 'can_bao_tri'):
                record.trang_thai = 'maintenance'
            else:
                record.trang_thai = 'available'

    def release_room(self):
        """ Trả phòng họp về trạng thái 'available' khi kết thúc sử dụng """
        for record in self:
            if record.trang_thai == 'using':
                record.trang_thai = 'available'
                
    @api.onchange('trang_thai')
    def _onchange_trang_thai(self):
        """ Cập nhật trạng thái nhân viên khi có thay đổi """
        if self.trang_thai == 'on_leave':
            # Thực hiện hành động khi nhân viên nghỉ phép
            pass
        elif self.trang_thai == 'using':
            # Thực hiện hành động khi phòng đang được sử dụng
            pass


    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.ten_phong))
        return result
