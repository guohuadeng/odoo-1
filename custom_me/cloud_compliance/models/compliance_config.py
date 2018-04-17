# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
from . import custom_models
from collections import OrderedDict
_logger = logging.getLogger(__name__)

class Cloud_Compliance_Config(models.Model):
    """云合规xmlrpc连接配置"""
    _name = 'setting.config'
    _inherit = 'res.config.settings'
    _description = 'Cloud Compliance Config'

    #以下配置皆是目标系统中的相关信息
    default_user_name = fields.Char(default_model="goods.list")   #用户登陆名，形如xxxx@example.com & admin

    default_user_pwd = fields.Char(default_model="goods.list") # 用户登录密码

    default_user_dbname = fields.Char(default_model="goods.list")  # 用户登陆数据库名

    default_url_post = fields.Char(default_model="goods.list") # 输入目标url地址