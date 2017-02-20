#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Daspanel CP Web

Daspanel control panel for web

 :copyright: (c) 2017, Abner G Jacobsen.
             All rights reserved.
 :license:   GNU General Public License v3, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
import json
from devourer import GenericAPI, APIMethod, APIError

from .forms import (
    NewSiteForm, DeleteSiteForm, EditSiteForm,
    NewUploadHttpForm,
    ServerCmdForm,
    NewVersionForm, DeleteVersionForm, EditVersionForm,
    NewRedirectForm, DeleteRedirectForm, EditRedirectForm
)

bp = Blueprint('sites', __name__)

API_SERVER = 'http://daspanel-api:8080/1.0'

class VersionsApi(GenericAPI):
    add_version  = APIMethod('post', '/{id}/versions')
    del_version  = APIMethod('delete', '/{id}/versions/{version_id}')
    edit_version  = APIMethod('put', '/{id}/versions/{version_id}')
    get_byid = APIMethod('get', '/{id}/versions/{version_id}')

    def __init__(self, server='http://daspanel-api:8080/1.0', auth=None):
        _headers = {
            'pragma': 'no-cache',
            'Connection': 'close',
            'Accept': 'application/json',
            'Authorization': auth,
        }

        super(VersionsApi, self).__init__(
            url = '{}/sites'.format(server),
            auth = None,
            headers = _headers,
            load_json = True,
            throw_on_error = True
        )
        
    def finalize(self, name, result, *args, **kwargs):
        if self.throw_on_error and result.status_code >= 400:
            print(result.content)
            raise APIError(json.loads(result.content)['detail'], response=result.__dict__)
        if self.load_json and not result.status_code == 204:
            return json.loads(result.content)
        return result.content

class HttpServiceApi(GenericAPI):
    gen_config   = APIMethod('get', '/{server_type}/genconfig/{id}')
    del_config   = APIMethod('get', '/{server_type}/delconfig/{id}')
    enable_site  = APIMethod('get', '/{server_type}/activate/{id}')
    disable_site = APIMethod('get', '/{server_type}/deactivate/{id}')
    http_reload  = APIMethod('get', '/{server_type}/reload')

    def __init__(self, server='http://daspanel-api:8080/1.0', auth=None):
        _headers = {
            'pragma': 'no-cache',
            'Connection': 'close',
            'Accept': 'application/json',
            'Authorization': auth,
        }

        super(HttpServiceApi, self).__init__(
            url = '{}/sites/service'.format(server),
            auth = None,
            headers = _headers,
            load_json = True,
            throw_on_error = True
        )
        
    def finalize(self, name, result, *args, **kwargs):
        if self.throw_on_error and result.status_code >= 400:
            print(result.content)
            raise APIError(json.loads(result.content)['detail'], response=result.__dict__)
        if self.load_json and not result.status_code == 204:
            return json.loads(result.content)
        return result.content


class ContentApi(GenericAPI):
    http_zip   = APIMethod('post', '/{id}/remotezip')

    def __init__(self, server='http://daspanel-api:8080/1.0', auth=None):
        _headers = {
            'pragma': 'no-cache',
            'Connection': 'close',
            'Accept': 'application/json',
            'Authorization': auth,
        }

        super(ContentApi, self).__init__(
            url = '{}/sites/content'.format(server),
            auth = None,
            headers = _headers,
            load_json = True,
            throw_on_error = True
        )
        
    def finalize(self, name, result, *args, **kwargs):
        if self.throw_on_error and result.status_code >= 400:
            print(result.content)
            raise APIError(json.loads(result.content)['detail'], response=result.__dict__)
        if self.load_json:
            return json.loads(result.content)
        return result.content


class SitesApi(GenericAPI):
    get_all   = APIMethod('get', '/')
    get_byid  = APIMethod('get', '/{id}')
    add_site  = APIMethod('post', '/')
    del_site  = APIMethod('delete', '/{id}')
    edit_site = APIMethod('put', '/{id}')
    set_defaultversion = APIMethod('put', '/{id}/setdefaultversion/{version_id}')
    clone_version = APIMethod('get', '/{id}/cloneversion/{version_id}')
    redirects_new = APIMethod('post', '/{id}/redirects')
    redirects_del = APIMethod('delete', '/{id}/redirects/{redirect_id}')
    redirects_edit = APIMethod('put', '/{id}/redirects/{redirect_id}')
    redirects_getbyid = APIMethod('get', '/{id}/redirects/{redirect_id}')

    def __init__(self, server='http://daspanel-api:8080/1.0', auth=None):
        _headers = {
            'pragma': 'no-cache',
            'Connection': 'close',
            'Accept': 'application/json',
            'Authorization': auth,
        }

        super(SitesApi, self).__init__(
            url = '{}/sites'.format(server),
            auth = None,
            headers = _headers,
            load_json = True,
            throw_on_error = True
        )
        
    def finalize(self, name, result, *args, **kwargs):
        if self.throw_on_error and result.status_code >= 400:
            #error_msg = "Custom Error when invoking {} with parameters {} {}: {}"
            #params = (name, args, kwargs, result.__dict__)
            #raise APIError(error_msg.format(*params))
            print(result.content)
            raise APIError(json.loads(result.content)['detail'], response=result.__dict__)
        if self.load_json:
            return json.loads(result.content)
        return result.content


@bp.route('/', methods=['GET'])
@login_required
def home():
    """GET /: render homepage
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        result = api.get_all()
        #flash('Consulta bem sucedida!!!', 'message')
    except APIError as err:
        result = {}
        flash(err, 'error')

    for rec in result:
        print(rec)
        print("========================================\n")

    return render_template('/modules/sites/home.html', records=result)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """GET /new: render homepage
    """
    form = NewSiteForm()
    if form.validate_on_submit():
        data = request.form.to_dict()
        data.pop("csrf_token", None)
        api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
        server_api = HttpServiceApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
        try:
            result = api.add_site(payload=data)
            flash('Site criado com sucesso!!!', 'message')
            try:
                cmd_result = server_api.gen_config(server_type='caddy', id=result['_cuid'])
                cmd_result = server_api.enable_site(server_type='caddy', id=result['_cuid'])
                cmd_result = server_api.http_reload(server_type='caddy')
            except APIError as err:
                cmd_result = {}
                flash(str(err), 'error')
            return redirect(url_for('sites.content_fromhttp', recid=result['_cuid']))
            #return redirect(request.args.get('next') or url_for('sites.home'))
        except APIError as err:
            result = {}
            flash(str(err), 'error')

    return render_template('/modules/sites/new.html', form=form)

@bp.route('/delete/<recid>', methods=['GET', 'POST'])
@login_required
def delete(recid):
    """GET/POST /delete: delete site
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        result = api.get_byid(id=recid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.home'))
    form = DeleteSiteForm()
    if form.validate_on_submit():
        try:
            sitename = result['sitedescription']
            server_api = HttpServiceApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
            try:
                cmd_result = server_api.disable_site(server_type='caddy', id=recid)
                cmd_result = server_api.del_config(server_type='caddy', id=recid)
                cmd_result = server_api.http_reload(server_type='caddy')
            except APIError as err:
                cmd_result = {}
                flash(str(err), 'error')
            result = api.del_site(id=recid)
            flash('Site deletado sucesso: ' + ' ' + sitename, 'message')
            return redirect(url_for('sites.home'))
        except APIError as err:
            result = {}
            flash(str(err), 'error')
            return redirect(url_for('sites.delete', recid=recid))
    return render_template('/modules/sites/delete.html', form=form, record=result)

@bp.route('/edit/<recid>', methods=['GET', 'POST'])
@login_required
def edit(recid):
    """GET/POST /edit: edit site
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        result = api.get_byid(id=recid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.home'))
    print(result)
    form = EditSiteForm(request.form, **result)
    if form.validate_on_submit():
        data = request.form.to_dict()
        data.pop("csrf_token", None)
        try:
            sitename = result['sitedescription']
            result = api.edit_site(id=recid, payload=data)
            flash('Site edited with sucess: ' + ' ' + sitename, 'message')
            server_api = HttpServiceApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
            try:
                cmd_result = server_api.disable_site(server_type='caddy', id=recid)
                cmd_result = server_api.gen_config(server_type='caddy', id=recid)
                cmd_result = server_api.enable_site(server_type='caddy', id=recid)
                cmd_result = server_api.http_reload(server_type='caddy')
            except APIError as err:
                cmd_result = {}
                flash(str(err), 'error')
            return redirect(url_for('sites.home'))
        except APIError as err:
            result = {}
            flash(str(err), 'error')
            return redirect(url_for('sites.edit', recid=recid))
    return render_template('/modules/sites/edit.html', form=form, recid=recid)

@bp.route('/content/<recid>/fromhttp', methods=['GET', 'POST'])
@login_required
def content_fromhttp(recid):
    """GET/POST /content: upload ZIP from remote http url
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        result = api.get_byid(id=recid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.home'))

    versions = [(v['_cuid'], v['description']) for v in result['versions']]
    form = NewUploadHttpForm(version=result['active_version'])
    form.version.choices = versions
    #form.version.default = result['active_version']
    #form.process()
    print(request.form.to_dict())
    if form.validate_on_submit():
        data = request.form.to_dict()
        print(data)
        data.pop("csrf_token", None)
        try:
            sitename = result['sitedescription']
            api_content = ContentApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
            upload_result = api_content.http_zip(id=recid, payload=data)
            flash('Site content for \"' + sitename + '\" version \"' + data['version'] + '\" uploaded to: ' + upload_result['location'], 'message')
            print(upload_result)
            return redirect(url_for('sites.home'))
        except APIError as err:
            result = {}
            flash(str(err), 'error')
            return redirect(url_for('sites.content_fromhttp', recid=recid))
    return render_template('/modules/sites/content_uploadfromhttp.html', form=form, recid=recid)

@bp.route('/server/<recid>', methods=['GET', 'POST'])
@login_required
def server_commands(recid):
    """GET/POST /server: server commands for the site
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        result = api.get_byid(id=recid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.home'))

    form = ServerCmdForm(request.form, **result)
    if form.validate_on_submit():
        data = request.form.to_dict()
        data.pop("csrf_token", None)
        if not 'cmd' in data:
            flash("Invalid server command", 'error')
        else:
            server_api = HttpServiceApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
            if data['cmd'] == 'gen-site-config':
                try:
                    cmd_result = server_api.gen_config(server_type=data['server_type'], id=recid)
                    flash("Site configuration generated with success", 'message')
                except APIError as err:
                    cmd_result = {}
                    flash(str(err), 'error')
            elif data['cmd'] == 'enable-site':
                try:
                    cmd_result = server_api.enable_site(server_type=data['server_type'], id=recid)
                    flash("Site enabled with success", 'message')
                except APIError as err:
                    cmd_result = {}
                    flash(str(err), 'error')
            elif data['cmd'] == 'disable-site':
                try:
                    cmd_result = server_api.disable_site(server_type=data['server_type'], id=recid)
                    flash("Site disabled with success", 'message')
                except APIError as err:
                    cmd_result = {}
                    flash(str(err), 'error')
            elif data['cmd'] == 'server-reload':
                try:
                    cmd_result = server_api.http_reload(server_type=data['server_type'])
                    flash("HTTP server reloaded with success", 'message')
                except APIError as err:
                    cmd_result = {}
                    flash(str(err), 'error')

            else:
               flash("Server command not configured: " + data['cmd'], 'error') 
                
        return redirect(url_for('sites.server_commands', recid=recid))

    return render_template('/modules/sites/server_commands.html', form=form, site=result)


@bp.route('/<recid>/versions', methods=['GET'])
@login_required
def site_versions(recid):
    """GET /<recid>/versions: get all versions off an site
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        result = api.get_byid(id=recid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.home'))
    print(result)

    return render_template('/modules/sites/versions.html', records=result, site=result)

@bp.route('/<recid>/versions/new', methods=['GET', 'POST'])
@login_required
def site_versions_new(recid):
    """GET/POST /<recid>/versions/new: create new version for site
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        result = api.get_byid(id=recid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.site_versions', recid=recid))

    form = NewVersionForm()
    if form.validate_on_submit():
        data = request.form.to_dict()
        data.pop("csrf_token", None)
        version_api = VersionsApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
        try:
            result = version_api.add_version(id=recid, payload=data)
            server_api = HttpServiceApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
            try:
                cmd_result = server_api.disable_site(server_type='caddy', id=recid)
                cmd_result = server_api.gen_config(server_type='caddy', id=recid)
                cmd_result = server_api.enable_site(server_type='caddy', id=recid)
                cmd_result = server_api.http_reload(server_type='caddy')
            except APIError as err:
                cmd_result = {}
                flash(str(err), 'error')
            flash('Version ' + data['description'] +' created', 'message')
            return redirect(url_for('sites.site_versions', recid=recid))
        except APIError as err:
            result = {}
            flash(str(err), 'error')

    return render_template('/modules/sites/versions_new.html', form=form, site=result)

@bp.route('/<recid>/versions/<versionid>/delete', methods=['GET', 'POST'])
@login_required
def site_versions_delete(recid, versionid):
    """GET/POST /<recid>/versions/versionid>/delete: delete version of site
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        result = api.get_byid(id=recid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.home'))

    form = DeleteVersionForm()
    if form.validate_on_submit():
        data = request.form.to_dict()
        data.pop("csrf_token", None)
        version_api = VersionsApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
        try:
            result = version_api.del_version(id=recid, version_id=versionid)
            flash('Version  deleted', 'message')
            server_api = HttpServiceApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
            try:
                cmd_result = server_api.disable_site(server_type='caddy', id=recid)
                cmd_result = server_api.gen_config(server_type='caddy', id=recid)
                cmd_result = server_api.enable_site(server_type='caddy', id=recid)
                cmd_result = server_api.http_reload(server_type='caddy')
            except APIError as err:
                cmd_result = {}
                flash(str(err), 'error')
            return redirect(url_for('sites.site_versions', recid=recid))
        except APIError as err:
            result = {}
            flash(str(err), 'error')
            return redirect(url_for('sites.site_versions_delete', recid=recid, versionid=versionid))

    return render_template('/modules/sites/versions_delete.html', form=form, site=result, versionid=versionid)


@bp.route('/<recid>/versions/<versionid>/edit', methods=['GET', 'POST'])
@login_required
def site_versions_edit(recid, versionid):
    """GET/POST /<recid>/versions/versionid>/edit: edit version of site
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        site_result = api.get_byid(id=recid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.home'))

    versions_api = VersionsApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        result = versions_api.get_byid(id=recid, version_id=versionid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.site_versions', recid=recid))

    form = EditVersionForm(request.form, **result)
    if form.validate_on_submit():
        data = request.form.to_dict()
        print(data)
        data.pop("csrf_token", None)
        try:
            result = versions_api.edit_version(id=recid, version_id=versionid, payload=data)
            flash('Version  edited', 'message')
            server_api = HttpServiceApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
            try:
                cmd_result = server_api.disable_site(server_type='caddy', id=recid)
                cmd_result = server_api.gen_config(server_type='caddy', id=recid)
                cmd_result = server_api.enable_site(server_type='caddy', id=recid)
                cmd_result = server_api.http_reload(server_type='caddy')
            except APIError as err:
                cmd_result = {}
                flash(str(err), 'error')
            return redirect(url_for('sites.site_versions', recid=recid))
        except APIError as err:
            result = {}
            flash(str(err), 'error')
            return redirect(url_for('sites.site_versions_edit', recid=recid, versionid=versionid))

    return render_template('/modules/sites/versions_edit.html', form=form, site=site_result, recid=recid, versionid=versionid)


@bp.route('/<recid>/versions/<versionid>/setdefault', methods=['GET'])
@login_required
def site_versions_setdefault(recid, versionid):
    """GET/POST /<recid>/versions/versionid>/setdefault: set version as active
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        site_result = api.set_defaultversion(id=recid, version_id=versionid)
        flash('Active version changed', 'message')
        server_api = HttpServiceApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
        try:
            cmd_result = server_api.disable_site(server_type='caddy', id=recid)
            cmd_result = server_api.gen_config(server_type='caddy', id=recid)
            cmd_result = server_api.enable_site(server_type='caddy', id=recid)
            cmd_result = server_api.http_reload(server_type='caddy')
        except APIError as err:
            cmd_result = {}
            flash(str(err), 'error')
        return redirect(url_for('sites.site_versions', recid=recid))
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.site_versions', recid=recid))

@bp.route('/<recid>/versions/<versionid>/clone', methods=['GET'])
@login_required
def site_versions_clone(recid, versionid):
    """GET/POST /<recid>/versions/versionid>/clone: clone version of site
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        site_result = api.clone_version(id=recid, version_id=versionid)
        flash('Version cloned', 'message')
        server_api = HttpServiceApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
        try:
            cmd_result = server_api.disable_site(server_type='caddy', id=recid)
            cmd_result = server_api.gen_config(server_type='caddy', id=recid)
            cmd_result = server_api.enable_site(server_type='caddy', id=recid)
            cmd_result = server_api.http_reload(server_type='caddy')
        except APIError as err:
            cmd_result = {}
            flash(str(err), 'error')
        return redirect(url_for('sites.site_versions', recid=recid))
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.site_versions', recid=recid))

@bp.route('/<recid>/redirects', methods=['GET'])
@login_required
def site_redirects(recid):
    """GET /<recid>/redirects: get all redirects off an site
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        result = api.get_byid(id=recid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.home'))
    print(result)

    return render_template('/modules/sites/redirects.html', records=result, site=result)

@bp.route('/<recid>/redirects/new', methods=['GET', 'POST'])
@login_required
def site_redirects_new(recid):
    """GET/POST /<recid>/redirects/new: create new redirect for site
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        result = api.get_byid(id=recid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.site_versions', recid=recid))

    versions = [(v['_cuid'], v['description']) for v in result['versions']]
    form = NewRedirectForm(version=result['active_version'])
    form.version.choices = versions

    if form.validate_on_submit():
        data = request.form.to_dict()
        data.pop("csrf_token", None)
        if 'ssl' not in data:
            data['ssl'] = False
        else:
            if data['ssl'] == 'y':
                data['ssl'] = True
            else:
                data['ssl']= False
        print(data)
        try:
            result = api.redirects_new(id=recid, payload=data)
            flash('Redirect ' + data['hosturl'] + '.'  + data['domain'] + ' created', 'message')
            server_api = HttpServiceApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
            try:
                cmd_result = server_api.disable_site(server_type='caddy', id=recid)
                cmd_result = server_api.gen_config(server_type='caddy', id=recid)
                cmd_result = server_api.enable_site(server_type='caddy', id=recid)
                cmd_result = server_api.http_reload(server_type='caddy')
            except APIError as err:
                cmd_result = {}
                flash(str(err), 'error')
            return redirect(url_for('sites.site_redirects', recid=recid))
        except APIError as err:
            result = {}
            flash(str(err), 'error')

    return render_template('/modules/sites/redirects_new.html', form=form, site=result)

@bp.route('/<recid>/redirects/<redirectid>/delete', methods=['GET', 'POST'])
@login_required
def site_redirects_delete(recid, redirectid):
    """GET/POST /<recid>/redirect/<redirectid>/delete: delete redirect of site
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        result = api.get_byid(id=recid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.home'))

    form = DeleteRedirectForm()
    if form.validate_on_submit():
        data = request.form.to_dict()
        data.pop("csrf_token", None)
        try:
            result = api.redirects_del(id=recid, redirect_id=redirectid)
            flash('Redirect  deleted', 'message')
            server_api = HttpServiceApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
            try:
                cmd_result = server_api.disable_site(server_type='caddy', id=recid)
                cmd_result = server_api.gen_config(server_type='caddy', id=recid)
                cmd_result = server_api.enable_site(server_type='caddy', id=recid)
                cmd_result = server_api.http_reload(server_type='caddy')
            except APIError as err:
                cmd_result = {}
                flash(str(err), 'error')
            return redirect(url_for('sites.site_redirects', recid=recid))
        except APIError as err:
            result = {}
            flash(str(err), 'error')
            return redirect(url_for('sites.site_redirects_delete', recid=recid, redirectid=redirectid))

    return render_template('/modules/sites/redirects_delete.html', form=form, site=result, redirectid=redirectid)

@bp.route('/<recid>/redirects/<redirectid>/edit', methods=['GET', 'POST'])
@login_required
def site_redirects_edit(recid, redirectid):
    """GET/POST /<recid>/versions/versionid>/edit: edit version of site
    """
    api = SitesApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
    try:
        site_result = api.get_byid(id=recid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.home'))

    try:
        result = api.redirects_getbyid(id=recid, redirect_id=redirectid)
    except APIError as err:
        result = {}
        flash(str(err), 'error')
        return redirect(url_for('sites.site_redirects', recid=recid))

    versions = [(v['_cuid'], v['description']) for v in site_result['versions']]
    form = EditRedirectForm(request.form, **result)
    form.version.choices = versions

    if form.validate_on_submit():
        data = request.form.to_dict()
        data.pop("csrf_token", None)
        if 'ssl' not in data:
            data['ssl'] = False
        else:
            if data['ssl'] == 'y':
                data['ssl'] = True
            else:
                data['ssl']= False
        print(data)

        try:
            result = api.redirects_edit(id=recid, redirect_id=redirectid, payload=data)
            flash('Redirect edited', 'message')
            server_api = HttpServiceApi(server=API_SERVER, auth=current_app.config['DASPANEL_UUID'])
            try:
                cmd_result = server_api.disable_site(server_type='caddy', id=recid)
                cmd_result = server_api.gen_config(server_type='caddy', id=recid)
                cmd_result = server_api.enable_site(server_type='caddy', id=recid)
                cmd_result = server_api.http_reload(server_type='caddy')
            except APIError as err:
                cmd_result = {}
                flash(str(err), 'error')
            return redirect(url_for('sites.site_redirects', recid=recid))
        except APIError as err:
            result = {}
            flash(str(err), 'error')
            return redirect(url_for('sites.site_redirects_edit', recid=recid, redirectid=redirectid))

    return render_template('/modules/sites/redirects_edit.html', form=form, site=site_result, recid=recid, redirectid=redirectid)


