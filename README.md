# pytongs
pythongs是基于TongsQuant C++ Core的Python开发平台。  

* **回测即实盘**

    使用统一框架，回测完成，可立即上线实盘。   
    回测使用完整的含交易费、滑点流程。

* **离线部署**

    仅依赖一个so文件，拷贝到部署机器即可运行。  
    自行保管交易所KEY，避免泄漏  
    策略代码保密  

* **开发高效，运行高效**

    Python/C++一体化构架。  
    Python开发具体策略实现，系统核心运行C++代码。  
    分钟级全年数据（50万+数据），简单策略通常在数秒内可以完成回测。

* **实盘验证**

    实盘长期运行验证  
    多交易所随意切换  
    订单大小随意切分  
    多仓位管理，利润监控  
    完整log机制
  

使用pytongs，只需要复制一个文件【libpytongs.so】到当前目录，Python程序import即可。

~~~
from libpytongs import Strategy, DataFeeder, PosController, ReturnCurve, ExchApiKey, ExConnBina, PosOrderInfo, PosSet
~~~

如果你的ubuntu/wsl已经预装python和openssl，可以立即体验回测效率：

~~~
git clone https://github.com/TongsQuant/pytongs
cd demos
python demo-3-ai-momentum.py
~~~

pytong的Python Class实际调用的是C++的Class。Class的成员变量和函数参数说明请查看docs目录。

使用pytongs创建一个回测实盘一体的代码非常容易，只需要创建一个Class继承Strategy，然后实现其中的algorithm()即可。


~~~
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
~~~

# 其他准备工作

## 1）开发环境

   开发可以使用Ubuntu或者Windows下的WSL Ubuntu。Win11的WSL支持GUI图形输出，可以直接在Win11展示Python回测曲线。
   
   开发环境需要安装openssl 1.1。在Ubuntu 20.04之前的版本安装：
   ~~~
   sudo apt-get install libssl-dev
   ~~~
   22.04之后的版本安装：
   ~~~
   wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb
   sudo dpkg -i libssl1.1_1.1.0g-2ubuntu4_amd64.deb
   ~~~


## 2）交易所配置 

对于永续合约，大部分交易所的都有杠杆、单项/双向持仓以及全仓/逐仓的设置。有的交易所缺省的杠杆为20，部分小币种下单量受限。

建议杠杆设到5，全仓模式，单向持仓模式【不允许对一个交易对象同时持有Long，Short仓位。假如之前持有Long仓位，Short的Order将会减少Long仓位，而不是新建立一个Short仓位】。

pytongs公开接口仅支持单项持仓，如果你要开发双向持仓套取交易所交易补偿费率，请联系我们tongsquant(at)gmail。

## 3）实盘运行环境 

实盘运行环境可以使用Ubuntu轻量级云服务器，成本每年几十美金。可以限制交易所之外的所有IP访问。
同样的，实盘环境需要安装openssl。

因为Python调用了C++代码，若使用Control+Z结束程序时，还有残留。使用“kill -9 进程号”完全结束进程。 “ps -Af”可以查看进程号。

## 4）回测数据

回测数据文件为*.bbdh后缀，内容为时长1一年的分钟级数据，定期更新。请复制至libpytongs.so的目录使用。  

---
---
# 使用TongsQuant定制的GPT轻松开发策略软件

https://www.coze.com/s/Zs8rrXeYS/


# 支持我们

TongsQuant是免费的，你可以使用我们的邀请码注册Binance和OKX，获取10%的交易手续费优惠。我们同时获得推广收益。


BINA邀请码：YNT2CGCI  
URL直达：https://accounts.binance.com/register?ref=YNT2CGCI

![avatar](https://raw.githubusercontent.com/TongsQuant/pytongs/master/img/qr_bina-200.png)

OKX邀请码：TENFORUSER  
URL直达：https://www.okx.com/join/TENFORUSER

![avatar](https://raw.githubusercontent.com/TongsQuant/pytongs/master/img/qr_okx-200.png)

