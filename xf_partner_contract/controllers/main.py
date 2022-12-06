# -*- coding: utf-8 -*-

import base64

import json
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.addons.documents.controllers.main import ShareRoute
from odoo.http import request

class DocumentController(ShareRoute):
    @http.route("/documents/upload_attachment/<int:act_id>", type='http', methods=['POST'], auth="user", csrf=False)
    def upload_document_active_id(self,act_id, folder_id, ufile, tag_ids, document_id=False, partner_id=False, owner_id=False):

        files = request.httprequest.files.getlist('ufile')
        if act_id == 0:
            act_id = False
        result = {'success': _("All files uploaded")}
        tag_ids = tag_ids.split(',') if tag_ids else []
        if document_id:
            document = request.env['documents.document'].browse(int(document_id))
            ufile = files[0]
            try:
                data = base64.encodebytes(ufile.read())
                mimetype = ufile.content_type
                document.write({
                    'name': ufile.filename,
                    'datas': data,
                    'mimetype': mimetype,
                })
            except Exception as e:
                logger.exception("Fail to upload document %s" % ufile.filename)
                result = {'error': str(e)}
        else:
            vals_list = []
            for ufile in files:
                try:
                    mimetype = ufile.content_type
                    datas = base64.encodebytes(ufile.read())
                    vals = {
                        'name': ufile.filename,
                        'mimetype': mimetype,
                        'datas': datas,
                        'folder_id': int(folder_id),
                        'tag_ids': tag_ids,
                        'partner_id': int(partner_id),
                        'contract_id': act_id
                    }
                    if owner_id:
                        vals['owner_id'] = int(owner_id)
                    vals_list.append(vals)
                except Exception as e:
                    logger.exception("Fail to upload document %s" % ufile.filename)
                    result = {'error': str(e)}
            cids = request.httprequest.cookies.get('cids', str(request.env.user.company_id.id))
            allowed_company_ids = [int(cid) for cid in cids.split(',')]
            documents = request.env['documents.document'].with_context(allowed_company_ids=allowed_company_ids).create(vals_list)
            result['ids'] = documents.ids

        return json.dumps(result)