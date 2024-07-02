#######################################################################################
#
#   示例：系统最基本的用法。程序输出ETH的价格曲线
#
#######################################################################################
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

from libpytongs import Strategy, ExConnBinaFutureBackTest, DataFeeder, PosController, ReturnCurve, ExchApiKey, ExConnOkx
import matplotlib.pyplot as plt

class StraEasyMoney(Strategy):
    def __init__(self, log_fn, p_df, p_pc, p_rc, p_ec, tick_ts):
        super().__init__(log_fn, p_df, p_pc, p_rc, p_ec, tick_ts)
        self.price_list = []
    def algorithm(self, td, backtest_end) -> float:
        profit = 0
        if not backtest_end:
            self.price_list.append(td.tick_data[1].price)
        return profit

if __name__ == "__main__":
    is_backtest = True
    markets = ["BTCUSDT", "ETHUSDT"]
    key = ExchApiKey()
    key.key = "KEY"
    key.secret = "SECRET"
    key.passphrase = "PASS"

    if is_backtest:
        ec = ExConnBinaFutureBackTest(markets)
    else:
        ec= ExConnOkx("OKX_EasyMoney.log", key)

    df = DataFeeder(ec, markets)
    pc = PosController("POS_EasyMoney.log", ec)
    rc = ReturnCurve()
    stra = StraEasyMoney("StraEasyMoney.log", df, pc, rc, ec, 60)
    stra.run()

    if is_backtest:
        plt.plot(stra.price_list)
        plt.show()