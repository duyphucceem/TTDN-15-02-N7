from odoo import models, fields, api, exceptions
from datetime import timedelta

class DonMuonPhong(models.Model):
    _name = 'don_muon_phong'
    _description = 'Đơn mượn phòng'

    ten_don_muon = fields.Char(string="Tên Đơn Mượn", required=True)
    phong_hop_id = fields.Many2one(
        'danh_sach_phong_hop',
        string='Phòng họp',
        required=True,
        domain="[('trang_thai', '=', 'available')]"  # Chỉ hiển thị phòng có trạng thái 'available'
    )
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên mượn phòng", required=True, ondelete='cascade')
    thoi_gian_bat_dau = fields.Datetime(string="Thời gian bắt đầu", required=True)
    thoi_gian_ket_thuc = fields.Datetime(string="Thời gian kết thúc", required=True)
    trang_thai = fields.Selection([
        ('pending', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('cancelled', 'Đã hủy')
    ], string="Trạng thái", default='pending')
    muc_dich_su_dung = fields.Text(string="Mục đích sử dụng")

    lich_su_dat_phong_ids = fields.One2many('lich_su_dat_phong', 'don_muon_phong_id', string="Lịch sử đặt phòng")

    @api.constrains('phong_hop_id', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc')
    def _check_room_availability(self):
        """ Kiểm tra phòng có bị trùng lịch không ( trừ các phòng đã hủy) """
        for record in self:
            # Kiểm tra xem phòng có đang được sử dụng hoặc đang bảo trì không
            if record.phong_hop_id.trang_thai in ['booked', 'maintenance']:
                raise exceptions.ValidationError("Phòng họp này hiện đang sử dụng hoặc đang bảo trì. Vui lòng chọn phòng khác.")
            
            overlapping_bookings = self.env['lich_su_dat_phong'].search([
                ('phong_hop_id', '=', record.phong_hop_id.id),
                ('thoi_gian_bat_dau', '<', record.thoi_gian_ket_thuc),
                ('thoi_gian_ket_thuc', '>', record.thoi_gian_bat_dau),
                ('id', '!=', record.id),
                ('trang_thai', 'in', ['pending', 'confirmed',])
            ], limit=5)
            if overlapping_bookings:
                raise exceptions.ValidationError("Phòng họp đã bị đặt trong khoảng thời gian này.")

    def action_confirm(self):
        """ Xác nhận đơn mượn phòng """
        for record in self:
            if record.trang_thai == 'pending':
                record.trang_thai = 'confirmed'
            elif record.trang_thai == 'cancelled':
                record.trang_thai = 'cancelled'  
            self.env['lich_su_dat_phong'].create_history(record)
            if record.trang_thai == 'confirmed':
                record.phong_hop_id.trang_thai = 'booked'

    def action_cancel(self):
        """ Hủy đơn mượn phòng """
        for record in self:
            record.trang_thai = 'cancelled'
            # Trả phòng về trạng thái 'available'
            record.phong_hop_id.trang_thai = 'available'

    def _check_time_constraints(self):
        """ Kiểm tra thời gian bắt đầu phải trước thời gian kết thúc và thời gian cách nhau tối đa 6 giờ """
        for record in self:
            if record.thoi_gian_bat_dau >= record.thoi_gian_ket_thuc:
                raise exceptions.ValidationError("Thời gian bắt đầu phải trước thời gian kết thúc.")
            
            # Kiểm tra khoảng cách giữa thời gian bắt đầu và kết thúc
            delta = record.thoi_gian_ket_thuc - record.thoi_gian_bat_dau
            if delta > timedelta(hours=6):  # Giới hạn tối đa 6 giờ
                raise exceptions.ValidationError("Thời gian kết thúc không được cách thời gian bắt đầu quá 6 giờ.")
    

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.ten_phong))  # Hiển thị tên phòng thay vì ID
        return result
