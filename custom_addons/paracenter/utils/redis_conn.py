# -*- encoding: utf-8 -*-

import redis
from odoo import tools


conn = redis.Redis(host=tools.config.get('redis_host', 'localhost'),
                   port=int(tools.config.get('redis_port', 6379)),
                   db=int(tools.config.get('redis_dbindex', 0)),
                   password=tools.config.get('redis_pass', None))
