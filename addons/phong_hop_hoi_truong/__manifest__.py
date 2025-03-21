# -*- coding: utf-8 -*-
{
    'name': "phong_hop_hoi_truong",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/lich_su_dat_phong.xml',
        'views/don_muon_phong.xml',
        'views/danh_sach_phong_hop.xml',
        'views/quan_ly_bao_tri.xml',
        'views/nhan_vien.xml',
        'views/thong_ke_phong_hop.xml',
        'views/thiet_bi_phong_hop.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}