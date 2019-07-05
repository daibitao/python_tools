# stockinfo

import easyquotation as eq
import curses
import os

"""
'name': '上海机场', 
'code': '600009', 
'now': 79.62, 
'close': 82.86, 
'open': 82.58, 
'volume': 15573200.0, 
'bid_volume': 7792400, 
'ask_volume': 7766600.0, 
'bid1': 79.61, 
'bid1_volume': 13800, 
'bid2': 79.6, 
'bid2_volume': 18200, 
'bid3': 79.59, 
'bid3_volume': 900, 
'bid4': 79.58, 
'bid4_volume': 300, 
'bid5': 79.57, 
'bid5_volume': 2800, 
'ask1': 79.7, 
'ask1_volume': 34900, 
'ask2': 79.71, 
'ask2_volume': 3700, 
'ask3': 79.75, 
'ask3_volume': 100, 
'ask4': 79.77, 
'ask4_volume': 100, 
'ask5': 79.79, 
'ask5_volume': 200, 
'最近逐笔成交': '11:30:01/79.62/9/M/71702/29293|11:29:58/79.61/1/S/7961/29280|11:29:55/79.61/8/S/63689/29263|11:29:52/79.61/7/S/55727/29254|11:29:49/79.66/4/B/31864/29243|11:29:45/79.62/20/M/159260/29233', 
'datetime': datetime.datetime(2019, 7, 4, 11, 34, 52), 
'涨跌': -3.24, 
'涨跌(%)': -3.91, 
'high': 82.58, 
'low': 79.2, 
'价格/成交量(手)/成交额': '79.62/155732/1253830025', 
'成交量(手)': 15573200, 
'成交额(万)': 1253830000.0, 
'turnover': 1.42, 
'PE': 33.32, 
'unknown': '', 
'high_2': 82.58, 
'low_2': 79.2, 
'振幅': 4.08, 
'流通市值': 870.63, 
'总市值': 1534.24, 
'PB': 5.18, 
'涨停价': 91.15, 
'跌停价': 74.57}
"""

stock_info_string = ['name','code','cur_price','new_open','old_close','change','change(%)','high','low']
#stock_info_string1 = ['code','now','open','close','涨跌','涨跌(%)','high','low']

class StockInfo:
    
    def __init__(self):

        self.handle = eq.use('qq')
        self.stock_info={}
        self.stock_list_info={}
        self.stock_info_string_dict={'name'     :'name',
								'code'     :'code',
								'cur_price':'now',
								'old_close':'close',
								'new_open' :'open',
								'change'   :'涨跌',
								'change(%)':'涨跌(%)',
								'high'     :'high',
								'low'      :'low'}

    def single_stock_info(self, stock_id):

        self.stock_info = self.handle.real(stock_id)[stock_id]
        return self.stock_info

    def multi_stock_info(self, stock_id_list):
        
        self.stock_list_info = self.handle.stocks(stock_id_list)
        return self.stock_list_info

    def form_stock_string(self,stock_info):
        list=[]
        for s in stock_info_string:
            value = stock_info[self.stock_info_string_dict[s]]
            list.append(str(value))
        return list


    def test(test):
        stock_id='600009'
        stock_id_list=['600009','300357']
        stock = StockInfo() 
        stock.single_stock_info(stock_id)
        stock.multi_stock_info(stock_id_list)
        print(stock.stock_list_info)

class Display:
   
    def __init__(self):
        self.stdscr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        self.stdscr.timeout(10)

    def __del__(self):
        self.stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def add_str_xy(self,x,y,string):
        self.stdscr.addstr(x,y,str(string))

    def add_str(self,string):
        self.stdscr.addstr(string)

    def clear_str(self):
        self.stdscr.clear()

    def refresh_str(self):
        self.stdscr.refresh()

    def getch(self):
        self.ext = self.stdscr.getch()

    def timeout_open(self):
        self.stdscr.timeout(10)

    def timeout_close(self):
        self.stdscr.timeout()

    def form_x_line_string(self,x,string):
        y=0
        for s in string:
            self.add_str_xy(x,y,s)
            y+=10

    def input_string(self):
        #pass
        self.stdscr.clear()
       
        self.stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

        editwin = curses.newwin(5,30, 2,1)
        rectangle(self.stdscr, 1,0, 1+5+1, 1+30+1)
        self.stdscr.refresh()

        box = Textbox(editwin)

        # Let the user edit until Ctrl-G is struck.
        box.edit()

        # Get resulting contents
        message = box.gather()
         
        return message


def test_single_stock(stock_id):
    
    stock = StockInfo()

    display = Display()


    while True:

        stock_info = stock.single_stock_info(stock_id)

        display.clear_str()
        
        # add string 
        display.form_x_line_string(0,stock_info_string)
        
        display.form_x_line_string(1,stock.form_stock_string(stock_info))    

        display.refresh_str()

        #exit
        display.getch()
        if display.ext == ord('q'):
            break

def test_multi_stock(stock_id_list):
        
    stock = StockInfo()

    display = Display()

    while True:

        stock_info_dict = stock.multi_stock_info(stock_id_list)

        display.clear_str()
        
        # add string 
        display.form_x_line_string(0,stock_info_string)
        
        for i in range(len(stock_id_list)):
            stock_info = stock_info_dict[stock_id_list[i]]
            display.form_x_line_string(i+1,stock.form_stock_string(stock_info))    

        display.refresh_str()

        #exit
        display.getch()
        if display.ext == ord('q'):
            break
   

def test_multi_stock1(stock_id_list):
        
    stock = StockInfo()

    display = Display()


    while True:

        stock_info_dict = stock.multi_stock_info(stock_id_list)

        display.clear_str()
        
        # add string 
        display.form_x_line_string(0,stock_info_string)
        
        for i in range(len(stock_id_list)):
            stock_info = stock_info_dict[stock_id_list[i]]
            display.form_x_line_string(i+1,stock.form_stock_string(stock_info))    

        display.refresh_str()

        #exit
        display.getch()
        if display.ext == ord('q'):
            break
   
        elif display.ext == ord('a'):
            display.stdscr.timeout(5000)
            newid = input_string()
            stock_id_list.append(newid)
            display.stdscr.timeout(10)
            
        elif display.ext == ord('d'):
            pass

if __name__=='__main__':
   
    #test_single_stock('600009')
    test_multi_stock(['600009',
						'300357',
						'000876',
						'603609',
						'300015',
						'603899',
						'600887'])


