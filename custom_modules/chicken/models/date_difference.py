# import re
# from datetime import strptime, date
# # class DateDifference:
# #     def  __init__ (self, start_date, end_date):
# #         self.fmt = '%Y-%m-%d'
# #         self.s_date = re.search('\d{4}-\d{2}-\d{2}', str(start_date))
# #         self.e_date = re.search('\d{4}-\d{2}-\d{2}', str(end_date))
# #         self.d2 = strptime(self.e_date.group(), fmt).date()
# #         self.d1 = strptime(self.s_date.group(), fmt).date()
# #         self.date_difference = self.e_date - self.s_date
#
# def custom_date_difference(start_date, end_date):
#     fmt = '%Y-%m-%d'
#     s_date = re.search('\d{4}-\d{2}-\d{2}', str(start_date))
#     e_date = re.search('\d{4}-\d{2}-\d{2}', str(end_date))
#     d2 = datetime.strptime(e_date.group(), fmt).date()
#     d1 = datetime.strptime(s_date.group(), fmt).date()
#     date_difference = d2 - d1
#     return int(date_difference.days())
#
