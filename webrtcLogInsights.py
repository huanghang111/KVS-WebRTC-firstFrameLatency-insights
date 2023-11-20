import glob
import json
import re
import xlsxwriter
import datetime

logNo = 0
xlsxFileName = 'webrtcTs '+ str(datetime.datetime.now()) +'.xlsx'
lastIsNotRedudant = True
repeatKey = "sender report"  # some key words will repeat many times and we only need extract the first one, such as 'sender report'

def read_files(file_name, stringlist):
  # Get a list of all files that match file_name
  log_files = glob.glob(file_name)
  logNo = len(log_files)
  print("There are " + str(logNo) + " log files.")
  # Iterate over the list of log files
  results = []
  for log_file in log_files:
    results = results + read_lines(log_file,stringlist)
  return results

def read_lines(file_name, stringlist):
  # Read a log file and read line by line.
  # Output a list of items. Each item is also a list: [No., timestamp, key word, line content, log level]
  results = []
  lastIsNotRedudant = True
  with open(file_name, "r") as f:
    for line in f:
      for string in stringlist:
        ts, loglevel = ['','']
        if re.search(string, line) and string != repeatKey:
          ts, loglevel = readTimestamp(line)
          results.append([findKey(string), ts,string, line, loglevel])
          lastIsNotRedudant = True
        if string == repeatKey and re.search(string, line) and lastIsNotRedudant and line.find('sender report no frames sent')==-1:
          ts, loglevel = readTimestamp(line)
          results.append([findKey(string), ts, string, line, loglevel])
          lastIsNotRedudant = False
  return results

def findKey(keyWord):
  for item in list(config['keywords'].keys()):
    if config['keywords'][item] == keyWord:
      return item

def readTimestamp(line):
  # In each line of WebRTC C SDK logs, the timestamp should always be the first two parts, which are separated by space. Example is shown as follows:
  # E.g. "2023-01-10 02:30:09 VERBOSE signalingClientStateChanged(): Signaling client state changed to 8 - 'Connecting'"
  # E.g. '2023-01-10 02:30:50 DEBUG   receiveLwsMessage(): Client received message of type: SDP_OFFER\n'
  splitLine = line.split(' ')
  date = splitLine[0]
  time = splitLine[1]
  loglevel = splitLine[2]
  return [date+ ' ' + time, loglevel]

def read_config(fileName):
  with open(fileName, "r") as f:
    data = f.read()
  data = json.loads(data)
  return data

def xlsx_export(selectedItemList):
  # Create a workbook and add a worksheet.
  workbook = xlsxwriter.Workbook(xlsxFileName)
  worksheet = workbook.add_worksheet('sheet1')
  # Set the width of each column.
  worksheet.set_column("A:A", 5)
  worksheet.set_column("B:B", 15)
  worksheet.set_column("C:C", 25)
  worksheet.set_column("D:E", 10)
  worksheet.set_column("F:F", 50)
  worksheet.set_column("H:H", 20)
  # Add a bold format to use to highlight cells.
  bold = workbook.add_format({"bold": True})
  # Add a format for device timestamp.
  deviceF = workbook.add_format()
  deviceF.set_font_color('blue')
  # Define first row.
  worksheet.write(0,0, "No.", bold)
  worksheet.write(0,1, "步骤/Steps", bold)
  worksheet.write(0,2, "说明/Detail", bold)
  worksheet.write(0,3, "来源/Source", bold)
  worksheet.write(0,4, "Log Level", bold)
  worksheet.write(0,5, "日志关键词/Key Words in Log", bold)
  worksheet.write(0,6, "分类/Category", bold)
  worksheet.write(0,7, "时间戳/Timestamp", bold)
  # Define keyword columns.
  for key in list(config['keywords'].keys()):
    worksheet.write(int(key),0, key)
    worksheet.write(int(key),5, config['keywords'][key])
  # Write items into excel
  totalNo = 1
  lastKey = 0
  for item in selectedItemList:
    if int(item[0]) < lastKey:
      totalNo += 1
    worksheet.write(int(item[0]), 7+totalNo-1, item[1])
    lastKey = int(item[0])

  workbook.close()
  return 0

def fill_details(fileName, configuration):
  workbook = xlsxwriter.Workbook(fileName)
  worksheet = workbook.get_worksheet_by_name('sheet1')
  '''
  todo
  '''
  return 0


if __name__ == "__main__":
  config = read_config("configuration.json")
  file_name_pattern = config['logs_namePattern']
  keyword_list = list(config['keywords'].values())
  results = read_files(file_name_pattern, keyword_list)
  if results == []:
    print("Nothing found.")
  '''
  for result in results:
    print(result)
  '''
  xlsx_export(results)