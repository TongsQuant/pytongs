#######################################################################################
#
#   示例：如何开仓和平仓。
#        algorithm()必须返回本轮的收益，它是回测时ReturnCurve的收益数据的来源。
#        实盘时，真正的收益通过self.ec.get_collateral()获取【无仓位时】。
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

    def algorithm(self, td, backtest_end) -> float:
        profit = 0
        poi_list = []
        for i in range(2):      # PosSet可以放置多个交易对象的下单数据，同时下单
            poi = PosOrderInfo()
            poi.ts = td.tick_data[i].ts
            poi.market = td.tick_data[i].market
            poi.price = td.tick_data[i].price
            poi.ls = POS_LONG
            poi.size = self.m_full_vol / td.tick_data[i].price
            poi.size = self.ec.size_adjust(td.tick_data[i].market, poi.size)
            poi_list.append(poi)

        # 平之前仓位
        # 收益的计算，需要使用poi_list里面的当前价格
        profit = self.pc.get_all_prof(poi_list)
        self.pc.close_all() #也可以单独平一个PosSet的部分仓位 
        self.pc.remove_closed() #清除已经完全关闭的PosSet

        # 开仓
        pos_set = PosSet(poi_list, self.m_full_vol, self.cfg_slip_ratio, self.cfg_fee_ratio) 
        self.pc.add_pos(pos_set)
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
    stra = StraEasyMoney("StraEasyMoney.log", df, pc, rc, ec, 60)

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