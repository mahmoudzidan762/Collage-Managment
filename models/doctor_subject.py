from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import json


class DoctorSubject(models.Model):
    _name = 'doctor.subject'

    student_id = fields.Many2one('op.student')
    subject_name = fields.Many2one('op.subject', string='Subject Name')
    doctor_name = fields.Many2one('op.faculty', string='Doctor Name')
    doctor_name_domain = fields.Char(compute='get_doctor_name_domain')
    mid_term_exam = fields.Float(string="ميد تيرم")
    practical_exam = fields.Float(string="الاعمال الفصلية")
    final_exam = fields.Float(string="النظري النهائي")
    total_practical_marks = fields.Float(string="المجموع الكلي للاعمال الفصلية")
    total_theoretical_marks = fields.Float(string="النظري الكلي")
    total_marks = fields.Float(string="المجموع الكلي")
    percentage = fields.Float(string="النسبة المؤية")
    grade = fields.Char(string='الرمز')


    @api.onchange('subject_name')
    def get_doctor_name_domain(self):
        for rec in self:
            ids = []
            subject = self.env['op.subject'].search([('name', '=', rec.subject_name.name)])
            for doc in subject.subject_faculty_ids:
                ids.append(doc.id)
            rec.doctor_name_domain = json.dumps([('id', 'in', ids)])
