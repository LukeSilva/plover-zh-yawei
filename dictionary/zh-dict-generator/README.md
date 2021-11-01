# CORPUS Sources 語料庫的來源:

Taiwanese 台灣的:
https://language.moe.gov.tw/001/Upload/files/SITE_CONTENT/M0001/PRIMARY/shrest2-2.htm?open

Click on 下載, download the .zip file, unextract it. Open .dbf file with libreoffice, it is encoded with the Big 5 encoding. Save it as a .csv file encoded with utf8 in `corpus/tw.csv`

下載.zip檔, 解壓, 用libreoffice把裡面的.dbf檔打開, 開時要選大五碼這個交換碼. 存成utf-8的.csv檔, 在`corpus/tw.csv`

Chinese 中國的:
http://corpus.zhonghuayuwen.org/Resources.aspx
Click on 现代汉语语料库词频表, download the .xls file. Save it as a utf8 encoded csv file in `corpus/cn.csv`


Finally, download cedict, save as cedict_ts.u8, and remove the comment heading at the top

# Build dictionaries:
First run main.py to generate the parts (goes in build/), and then combine.py to combine the dictionary parts together into usable files (goes in out/).
