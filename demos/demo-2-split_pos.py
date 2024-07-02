#######################################################################################
#
#   示例：1）如何管理多个仓位  2）如何根据订单簿决定下单金额
#
#######################################################################################
#
#   使用AI生成代码：https://www.coze.com/s/Zs8r8hKhv/
#
#   TongsQuant是一个Python/C++一体化的量化交易平台。
#   1）高效+便利，Python实现策略代码，C++内核运行。数秒内完成1年的分钟级数据的回测。
#   2）回测即实盘，实盘时代码无需改动
#   3) 离线部署。策略代码、交易所KEY自行保存，无泄漏风险。仅需拷贝一个文件到部署计算机。
#
#   开发资料：https://github.com/TongsQuant/pytongs
#
#######################################################################################

from libpytongs import Strategy, ExConnBinaFutureBackTest, DataFeeder, PosController, ReturnCurve, ExchApiKey, ExConnOkx, PosOrderInfo, PosSet
import matplotlib.pyplot as plt
import time

POS_LONG = 1
POS_SHORT = -1
POS_NONE = 0

class StraEasyMoney(Strategy):
    def __init__(self, log_fn, p_df, p_pc, p_rc, p_ec, tick_ts):
        super().__init__(log_fn, p_df, p_pc, p_rc, p_ec, tick_ts)
        self.ec = p_ec
        self.pc = p_pc
        info = "START & ASSET: {}".format(self.ec.get_collateral())
        self.log(info)  # LOG会记录在文件中

        self.m_full_vol = 100    # 下单金额，实际开发中，可以动态计算
        self.cfg_slip_ratio = 0.1  # 简化为利润减少比率，非价格滑点
        self.cfg_fee_ratio = 0.0005 # 交易所手续费

        self.ls = POS_LONG
        self.count = 0

    def algorithm(self, td, backtest_end) -> float:
        self.count += 1        
        profit = 0        
        if(backtest_end): # //backrtest end, 忽略当前仓位
            return profit

        # 演示目的：可以根据订单薄实际情况，决定下单数量和金额
        if (self.ls == POS_SHORT):
            vol_indi = td.tick_data[0].volume_bid  
        else:
            vol_indi = td.tick_data[0].volume_ask
        if vol_indi < self.m_full_vol:
            vol_indi = self.m_full_vol
        poi_list = []
        for i in range(2):      # PosSet可以放置多个交易对象的下单数据，同时下单
            poi = PosOrderInfo()
            poi.ts = td.tick_data[i].ts
            poi.market = td.tick_data[i].market
            poi.price = td.tick_data[i].price
            poi.ls = self.ls*(1 - i*2)  # 演示目的，一个SET包括了，两个交易对象，分别多空
            poi.size = vol_indi / td.tick_data[i].price
            # size的自动调整，以满足交易所的需求【最小下单数量，最小间隔等】
            # 交易所需求参数，在交易所连接时自动获取
            poi.size = self.ec.size_adjust(td.tick_data[i].market, poi.size)
            poi_list.append(poi)

        # 演示：开仓5次，然后逐个平仓5次
        if (self.count % 10) < 5:
            # 开仓
            pos_set = PosSet(poi_list, self.m_full_vol, self.cfg_slip_ratio, self.cfg_fee_ratio) 
            self.pc.add_pos(pos_set) 
            # print("-->IN PosSet: ", self.pc.size())
        else:               
            # 平一个PosSet的所有仓位，里面有两个交易对象的仓位
            # 一个PosSet的仓位也可以部分平仓，使用close_pos_with_size0
            profit = self.pc.get_pos_prof(0, poi_list)
            self.pc.close_one(0)
            self.pc.remove_closed() #清除已经全部关闭的PosSet
            # print("-->OUT PosSet: ", self.pc.size(), " / Prof: ", profit)
        return profit

if __name__ == "__main__":
    #实盘时，更改True为False即可
    is_backtest = True   

    #交易对象，使用交易所提供的名称
    markets = ["BTCUSDT", "ETHUSDT"]
    #自行保管交易所KEY，代码部署在自己的服务器
    key = ExchApiKey()
    key.key = "KEY"
    key.secret = "SECRET"
    key.passphrase = "PASS"

    if is_backtest:
        ec = ExConnBinaFutureBackTest(markets)
    else:
        ec = ExConnOkx("OKX_EasyMoney.log", key)  
        # 更换其他交易所：ec= ExConnBina("Bina_EasyMoney.log", key)
    df = DataFeeder(ec, markets)
    pc = PosController("POS_EasyMoney.log", ec)
    rc = ReturnCurve()
    stra = StraEasyMoney("StraEasyMoney.log", df, pc, rc, ec, 600)

    # 取保证金余额。有仓位时，交易所算法有差异。可统一为在空仓时获取，实时维护收益和杠杆率，做风险管理
    asset_init = ec.get_collateral()
    print("ASSET: ", asset_init)    
    time_start = time.time()
    stra.run()
    time_end = time.time()
    print("Time Used: ", time_end - time_start)
    # print("Return: ", rc.get_tabled_raw())

    if is_backtest:
        plt.plot(rc.by_day())
        plt.get_current_fig_manager().set_window_title('TongsQuant')
        plt.title("Return Curve")
        plt.xlabel("Day")
        plt.ylabel("USD")
        plt.show()