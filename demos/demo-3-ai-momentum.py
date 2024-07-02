#######################################################################################
#   这是一个AI生成的量化交易代码，基于TongsQuant平台。
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

class MomentumTradingStrategy(Strategy):
    def __init__(self, log_fn, p_df, p_pc, p_rc, p_ec, tick_ts):
        super().__init__(log_fn, p_df, p_pc, p_rc, p_ec, tick_ts)
        self.ec = p_ec
        self.pc = p_pc
        info = "START & ASSET: {}".format(self.ec.get_collateral())
        self.log(info)  # 将对应的信息记录在日志文件中

        self.total_volume = 100    # 下单金额
        self.cfg_slip_ratio = 0.1  # 该参数用于模拟滑点
        self.cfg_fee_ratio = 0.0005 # 交易购买费用的预设比率

        self.momentum_period = 14  # 动量计算周期
        self.historical_prices = []
        self.ls = POS_NONE

    # 算法整体部分
    def algorithm(self, td, backtest_end) -> float:
        if(backtest_end):
            return 0

        profit = 0
        poi_list = []
        current_price = td.tick_data[0].price
        # 获取历史数据
        self.historical_prices.append(current_price)
        if len(self.historical_prices) < self.momentum_period:
            return profit
        if len(self.historical_prices) > self.momentum_period:
            self.historical_prices.pop(0)

        # 计算动量
        momentum = current_price - self.historical_prices[0]

        # 开仓策略
        if self.ls == POS_NONE:
            if momentum > 0:
                self.ls = POS_LONG
            elif momentum < 0:
                self.ls = POS_SHORT

            if self.ls != POS_NONE:
                print("---> IN -----> C M", current_price, momentum)
                poi = PosOrderInfo()
                poi.ts = td.tick_data[0].ts
                poi.market = td.tick_data[0].market
                poi.price = current_price
                poi.ls = self.ls
                poi.size = self.total_volume / current_price
                poi.size = self.ec.size_adjust(td.tick_data[0].market, poi.size)
                poi_list.append(poi)
                pos_set = PosSet(poi_list, self.total_volume, self.cfg_slip_ratio, self.cfg_fee_ratio) 
                self.pc.add_pos(pos_set)
        else:
            # 平仓策略
            if (self.ls == POS_LONG and momentum < 0) or (self.ls == POS_SHORT and momentum > 0):
                print("---> OUT -----> C M", current_price, momentum)                    
                poi = PosOrderInfo()
                poi.ts = td.tick_data[0].ts
                poi.market = td.tick_data[0].market
                poi.price = current_price
                poi.ls = self.ls
                poi_list.append(poi)

                profit = self.pc.get_all_prof(poi_list)
                self.pc.close_all() #可以单独平一个PosSet的部分仓位 
                self.pc.remove_closed() #清除已经全部关闭的PosSet
                self.ls = POS_NONE
        return profit

if __name__ == "__main__":
    # 这一开关用于模拟交易结果，实际交易时，将True更改为False即可。
    is_backtest = True   

    # 交易品种，与交易所提供的名称相对应。
    markets = ["BTCUSDT"]
    # 自行保管API密钥，代码部署在你自己的服务器上。
    api_key = ExchApiKey()
    api_key.key = "KEY"
    api_key.secret = "SECRET"
    api_key.passphrase = "PASS"

    if is_backtest:
        ec = ExConnBinaFutureBackTest(markets)
    else:
        ec = ExConnOkx("Okx_MomentumTradingStrategy.log", api_key)  
    df = DataFeeder(ec, markets)
    pc = PosController("Pos_MomentumTradingStrategy.log", ec)
    rc = ReturnCurve()
    strategy = MomentumTradingStrategy("MomentumTradingStrategy.log", df, pc, rc, ec, 60*60)

    initial_asset = ec.get_collateral()
    print("Initial ASSET: ", initial_asset)    
    start_time = time.time()
    strategy.run()
    end_time = time.time()
    print("Time Used: ", end_time - start_time)

    if is_backtest:
        plt.plot(rc.by_day())
        plt.get_current_fig_manager().set_window_title('TongsQuant')
        plt.title("Return Curve")
        plt.xlabel("Day")
        plt.ylabel("USD")
        plt.show()