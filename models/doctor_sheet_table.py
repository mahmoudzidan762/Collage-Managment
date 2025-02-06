from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import json


class DoctorSheetTable(models.Model):
    _name = 'doctor.sheet.table'

    opposite = fields.Many2one('doctor.sheet')
    students_name = fields.Many2one('op.student', string='اسم الطالب')
    students_domain = fields.Char(compute='get_students_domain')
    mid_term_exam = fields.Float(string="ميد تيرم")
    practical_exam = fields.Float(string="الاعمال الفصلية")
    final_exam = fields.Float(string="النظري النهائي")
    total_practical_marks = fields.Float(string="المجموع الكلي للاعمال الفصلية")
    total_theoretical_marks = fields.Float(string="النظري الكلي")
    total_marks = fields.Float(string="المجموع الكلي")
    percentage = fields.Float(string="النسبة المؤية")
    grade = fields.Char(string='الرمز')

    @api.onchange('students_name', 'opposite.doc_subjects')
    def get_students_domain(self):
        for rec in self:
            students = self.env['op.student'].search(
                [('doctor_subject.doctor_name.name', '=', rec.opposite.doc_id.name),
                 ('doctor_subject.subject_name', '=', rec.opposite.doc_subjects.name)])
            rec.students_domain = json.dumps([('id', 'in', students.ids)])


class Student(models.Model):
    _inherit = 'op.student'

    student_to_subject = fields.Many2many('op.subject', 'student_subject_rel', 'student_id', 'subject_id',
                                          string='Student subjects')
    doctor_name = fields.Many2one('op.faculty', string='Doctor')
    doctor_subject = fields.One2many('doctor.subject', 'student_id', string='Student subjects')
    mid_term_exam = fields.Float(string="ميد تيرم")
    practical_exam = fields.Float(string="الاعمال الفصلية")
    final_exam = fields.Float(string="النظري النهائي")
    total_practical_marks = fields.Float(string="المجموع الكلي للاعمال الفصلية")
    total_theoretical_marks = fields.Float(string="النظري الكلي")
    total_marks = fields.Float(string="المجموع الكلي")
    percentage = fields.Float(string="النسبة المؤية")
    grade = fields.Char(string='الرمز')


class Subject(models.Model):
    _inherit = 'op.subject'

    subject_to_student = fields.Many2many('op.student', 'student_subject_rel', 'subject_id', 'student_id',
                                          string='Subject students')
    doctor_name = fields.Many2one('op.faculty', string='Doctor')
    doctor_name_domain = fields.Char(compute='get_doctor_name_domain')
    subject_faculty_ids = fields.Many2many('op.faculty', string='Faculty(s)')



    @api.onchange('opposite.doc_subjects')
    def get_doctor_name_domain(self):
        for rec in self:
            ids = []
            for doc in rec.subject_faculty_ids:
                ids.append(doc.id)
            rec.doctor_name_domain = json.dumps([('id', 'in', ids)])
