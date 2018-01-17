#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Daspanel CP Web

Daspanel control panel for web

 :copyright: (c) 2017, Abner G Jacobsen.
             All rights reserved.
 :license:   GNU General Public License v3, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function
import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required

bp = Blueprint('system', __name__)


@bp.route('/', methods=['GET'])
@login_required
def home():
    """GET /: render homepage
    """
    return render_template('/modules/system/home.html')

@bp.route('/services/users', methods=['GET'])
@login_required
def services_users():
    """GET /: render credentials info
    """
    return render_template('/modules/system/services_users.html', cfg=current_app.config['DASPANEL'], env=os.environ)


