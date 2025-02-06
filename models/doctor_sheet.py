from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import json


class DoctorSheet(models.Model):
    _name = 'doctor.sheet'
    _rec_name = 'doc_id'

    doc_id = fields.Many2one('op.faculty', string='اسم الدكتور')
    doc_id2 = fields.Many2one('op.faculty', readonly='1', related='doc_id', string='اسم الدكتور')
    user_id = fields.Many2one('res.users')
    doc_subjects = fields.Many2one('op.subject', string='المواد', default=None)
    doc_subjects_domain = fields.Char(compute='get_doc_subjects_domain')
    doctor_sheet = fields.One2many('doctor.sheet.table', 'opposite', string="طلابي", default=None)
    name_seq = fields.Char(default=lambda self: ('New'))

    @api.onchange('doc_id')
    def re_fill_fields(self):
        print('---------------------------------->>', self.user_id.id)
        self.doctor_sheet = None
        self.doc_subjects = None
        self.user_id = None

    @api.onchange('doc_subjects')
    def onchange_doc_subjects(self):
        self.doctor_sheet = [(5, 0, 0)]
        stu = self.env['doctor.subject'].search(
            [('doctor_name', '=', self.doc_id.id), ('subject_name', '=', self.doc_subjects.id)])
        for i in stu:
            self.doctor_sheet = [(0, 0, {
                'students_name': i.student_id.id,
                'mid_term_exam': i.mid_term_exam,
                'final_exam': i.final_exam,
                'total_practical_marks': i.total_practical_marks,
                'practical_exam': i.practical_exam,
                'total_theoretical_marks': i.total_theoretical_marks,
                'total_marks': i.total_marks,
                'percentage': i.percentage,
                'grade': i.grade,
            })]

    @api.onchange('doc_id')
    def get_doc_subjects_domain(self):
        for rec in self:
            ids = []
            subjects = self.env['op.faculty'].search([('id', '=', rec.doc_id.id)]).faculty_subject_ids
            for sub in subjects:
                ids.append(sub.id)
            rec.doc_subjects_domain = json.dumps([('id', 'in', ids)])

    @api.model
    def create(self, vals):
        if vals.get('name_seq', ('New')) == ('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('doctor.sheet.sequence') or ('New')
        result = super(DoctorSheet, self).create(vals)
        return result

    @api.model
    def write(self, vals):
        result = super(DoctorSheet, self).write(vals)
        for i in self.doctor_sheet:
            i.students_name.doctor_subject.write({
                'mid_term_exam': i.mid_term_exam,
                'final_exam': i.final_exam,
                'total_practical_marks': i.total_practical_marks,
                'practical_exam': i.practical_exam,
                'total_theoretical_marks': i.total_theoretical_marks,
                'total_marks': i.total_marks,
                'percentage': i.percentage,
                'grade': i.grade,
            })
        return result
