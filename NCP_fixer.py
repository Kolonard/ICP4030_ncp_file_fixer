# .ncp fixer
# small tool for compibility improve beetwen .ncp files, generated in modern PC and ICP4030.
# 
# Change final of .ncp to correct code with '\r\n' suffix
# 
# This lines 
# N4710 COOLANT OFF\n
# N4715 WPCLEAR\n
# N4720 SPINDLE OFF\n
# N4725 PROGEND\n
# Changed to
# NXXX0 COOLANT OFF\n
# NXXX5 SPINDLE OFF\n
# NXX10 WPCLEAR\n
# NXX15 FASTABS Z0\n
# NXX20 FASTABS X0 Y0\n
# NXX25 PROGEND\n

import os

class ncp_fixer():
    def __init__(self, target_file_path='', fixed_file_prefix='', fixed_file_sufix='__fixed.ncp'):
        self.target_file_path       = target_file_path
        self.fixed_file_path        = target_file_path

        self.fixed_file_prefix      = fixed_file_prefix
        self.fixed_file_sufix       = fixed_file_sufix
        self.program_end_key        = var_with_attr('COOLANT OFF\n', -12)
        self.fileID                 = None
        self.file_lines_list        = None
        self.line_number_step       = 5
        self.correct_lines_list     = ['SPINDLE OFF\n'  ,
                                       'WPCLEAR\n'      ,
                                       'FASTABS Z0\n'   ,
                                       'FASTABS X0 Y0\n',
                                       'PROGEND\n'      ]

    def set_path(self,path):
        self.target_file_path = path
        self.fixed_file_path = self.fixed_file_prefix + self.fixed_file_path[0:-4] + self.fixed_file_sufix
    
    def get_fixed_file_name(self):
        return self.fixed_file_path
    
    def save_fixed_file(self):
        fID = open(self.fixed_file_path, 'w')
        for line in self.file_lines_list:
            fID.write(line)
        fID.close()
    
    def fix(self):
        fID = open(self.target_file_path, 'r');
        self.file_lines_list = list(fID)
        fID.close()

        line_number = 0
        for line in reversed(self.file_lines_list):
            key = str(self.program_end_key)
            val = line[self.program_end_key.len:]
            if val == key:
                ll = line.split(' ')
                line_number = int(line.split(' ')[0][1:])
                break
            else:
                self.file_lines_list.pop()
        for line in self.correct_lines_list:
            line_number += self.line_number_step;
            self.file_lines_list.append('N' + str(line_number) + ' ' + line)
    

    def check_file(self):
        if self.target_file_path[-4:] == '.ncp':
            return os.path.exists(self.target_file_path)
        else:
            return False

    def get_path(self):
        path = input('Enter the absolute path or drag \'*.ncp\' file into the terminal:')
        self.target_file_path = path.replace('\\ ', ' ').strip()
        self.fixed_file_path = self.fixed_file_prefix + self.target_file_path[0:-4] + self.fixed_file_sufix

class var_with_attr():
    def __init__(self,var,len):
        self.var = var
        self.len = len
    def __str__(self):  return self.var
    def __repr__(self): return str(self.__str__())

fixer = ncp_fixer();
while True:
    fixer.get_path();
    if True == fixer.check_file():
        fixer.fix()
        fixer.save_fixed_file()
        break
    else:
        print('Error: File not existed!\r\n')

print('Fix done! New file: ' + fixer.get_fixed_file_name())