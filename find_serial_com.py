import sys
import getopt
import csv
import serial.tools.list_ports

USAGE = '''-h --help         print this help doc.
    --database
    --db           insert database file. required.
    --description
    --des          set description. only one.
    --vid          set vendor id.
    --pid          set product id.
    --serial_number
    --SN           set Serial Number.
    --location     set location info. <bus>-<port>[-<port>...]'''

database_list = []
record_list = []
serial_list = []

description = None

def usage():
  print(USAGE)

class DictMissingAllow(dict):
  def __missing__(self, key):
    return None

def mk_dictionary():
  for file in database_list:
    with open(file) as csvfile:
      dictReader = csv.DictReader(csvfile, delimiter=',')
      for row in dictReader:
        allow_missing_row = DictMissingAllow(row)
        row_tuple = (allow_missing_row["description"],
                     allow_missing_row["vid"],
                     allow_missing_row["pid"],
                     allow_missing_row["serial_number"],
                     allow_missing_row["location"])
        record_list.append(row_tuple)

def read_serials():
  plist = list(serial.tools.list_ports.comports())
  for obj in plist:
    serial_tuple = (obj.device, obj.description, obj.vid, obj.pid, obj.serial_number, obj.location)
    serial_list.append(serial_tuple)

def get_result():
  result_list = []
  additional_list = []
  for record in record_list:
    if description is not None and record[0].find(description) >= 0:
      additional_list.append(record)

  for device in serial_list:
    if description is not None and device[1].find(description) >= 0:
      result_list.append(device[0])
    elif(device[5] is not None):
      for additional in additional_list:
        add = (additional[1] is None or len(additional[1]) == 0 or int(additional[1]) == device[2]) and \
              (additional[2] is None or len(additional[2]) == 0 or int(additional[2]) == device[3]) and \
              (additional[3] is None or len(additional[3]) == 0 or additional[3] == device[4]) and \
              (additional[4] is None or len(additional[4]) == 0 or device[5].find(additional[4]) >= 0)
        if(add):
          result_list.append(device[0])

  print(' '.join(result_list))

def search():
  mk_dictionary()
  read_serials()

  get_result()

def main():
  global description

  if(len(sys.argv) == 1):
    sys.exit(2)

  try:
    opts, args = getopt.getopt(sys.argv[1:], "h",
    ["help=",
     "database=", "db=",
     "description=", "des="])
  except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

  # print(opts)
  help = False
  for opt, arg in opts:
    if opt in ['-h', '--help']:
      help = True
    elif opt in ['--database', '--db']:
      database_list.append(arg)
    elif opt in ['--description', '--des']:
      description = arg

  if(help==True):
    usage()
  else:
    search()

if __name__ == "__main__":
    main()