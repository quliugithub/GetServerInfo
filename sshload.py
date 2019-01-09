# _*_ coding: utf-8 _*_
# import paramiko
import paramiko
import sys
from openpyxl import Workbook  # 导入包
import time



def get_info(hostip):
    Info_Dict = {}
    private_key=paramiko.RSAKey.from_private_key(open("/root/.ssh/id_rsa"))
    transport = paramiko.Transport((hostip,10022))
    transport.connect(username='root',pkey=private_key)
    s = paramiko.SSHClient()
    s._transport = transport
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    Info_List = []
    stdin, stout, stderr = s.exec_command('date +%F')
    Date = stout.read().decode().replace("\n", "")
    Info_List.append(Date)
    Info_List.append(hostip)
    
    Info_List.append('√')
    Info_List.append('√')
    Info_List.append('')
    
    stdin, stout, stderr = s.exec_command('top -bi -n 1|grep  Cpu|awk -F "[ ]+" "{print \$8}"')
    Cpu_usage = stout.read().decode().replace("\n", "")
    Info_List.append(Cpu_usage)
    
    stdin, stout, stderr = s.exec_command('free -mh|grep Mem|awk -F "[ ]+" "{print \$2}"')
    Mem_Total = stout.read().decode().replace("\n", "")
    stdin, stout, stderr = s.exec_command('free -mh|grep Mem|awk -F "[ ]+" "{print \$4}"')
    Mem_Free = stout.read().decode().replace("\n", "")
    Mem_Usage = Mem_Free + "/" + Mem_Total
    Info_List.append(Mem_Usage)
    
    stdin, stout, stderr = s.exec_command('df -h|grep -w / |awk -F "[ ]+" "{print \$5}"')
    SystemDiskUsage = stout.read().decode().replace("\n", "")
    Info_List.append(SystemDiskUsage)
    
    stdin, stout, stderr = s.exec_command('df -h|grep data|awk -F "[ ]+" "{print \$5}"')
    DataDiskUsage = stout.read().decode().replace("\n", "")
    Info_List.append(DataDiskUsage)
    s._transport.close()
    return Info_List



iplist = []
info_Dict ={}
wb = Workbook()  # 新建一个表格文件
# wb.add_sheet(u'sheet1', cell_overwrite_ok=True)
sheet = wb.get_active_sheet()  # 也可以通过wb.create_sheet(title="new sheet")来创建一个新的sheet

# 快捷写，一行行录入数据，提供一个list或者tuple或者词典都可以
sheet.append(["日期", "服务器ip", "日志检查", "进程检查", "数据库表空间", "cpu空闲率", "内存使用率(可用/总共)", "系统磁盘空间使用率", "数据磁盘空间使用率"])

for line in open('/tmp/iplist'):
    line = line.strip('\n')
    iplist.append(line)

for ip in iplist:
    info = get_info(ip)
    #info = info_Dict[ip]
    sheet.append([info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8]])   #自动填写下一行

dt = time.strftime("%Y%m%d%H%M%S", time.localtime())
wb.save(dt + ".xls")

    # for i in range(len(ip)):
    #     a = GetServerInfo(ip[i])
   #     write_excel()
