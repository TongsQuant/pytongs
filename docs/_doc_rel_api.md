
# pytongs Class/Struct member & function


|  C++   | Python  |
|  ----  | ----  |
| std::string  | str |
| double  | float |
 


## Class/Struct: Strategy

**Constructor:** `Strategy(std::string, DataFeeder *, PosController *, ReturnCurve *, ExConn *, u_long)`

**Public Members:**

**Public Functions:**

  - `log(std::string info)` → `void`
  - `run()` → `void`




## Class/Struct: ExchApiKey

**Constructor:** `ExchApiKey()`

**Public Members:**

  - `key`: `std::string`
  - `secret`: `std::string`
  - `passphrase`: `std::string`
  - `extra`: `std::string`

**Public Functions:**


## Class/Struct: ExConn

**Constructor:** `ExConn()`

**Public Members:**

**Public Functions:**
  - `sure_put_order_market_price(std::string market, POS_LS ls, double size)` → `bool`
  - `sure_close_order_market_price(std::string market, POS_LS ls, double size)` → `bool`
  - `get_pos(std::string market)` → `PosOrderInfo`
  - `close_all_pos(std::string market)` → `bool`
  - `avg_day_price(std::string market)` → `double`
  - `get_historical_price(const std::string market, int sec_res, long start_time, long stop_time)` → `double`
  - `get_historical_price_list(const std::string market, int sec_res, long start_time, long stop_time)` → `std::vector<double>`
  - `get_last_trade_price(const std::string market)` → `double`
  - `get_orderbook(const std::string market, int depth)` → `OrderBook`
  - `get_collateral()` → `double`
  - `get_tick(std::string market)` → `TickDataOne`
  - `get_min_size(std::string market)` → `double`
  - `check_min_size_vol(std::string market, double size, double vol)` → `bool`
  - `spot_get_balance(std::string market)` → `double`
  - `spot_order_market(std::string market, POS_LS ls, double size)` → `bool`


## Class/Struct: HistoricalTickRecord

**Public Members:**

  - `time_str`: `std::string`
  - `ts`: `std::time_t`
  - `open`: `double`
  - `close`: `double`
  - `low`: `double`
  - `high`: `double`
  - `volume`: `double`

**Public Functions:**




## Class/Struct: OrderBook

**Public Members:**

  - `depth`: `int`
  - `market`: `std::string`
  - `sizes_ask`: `std::vector<double>`
  - `sizes_bid`: `std::vector<double>`
  - `prices_ask`: `std::vector<double>`
  - `prices_bid`: `std::vector<double>`

**Public Functions:**




## Class/Struct: TickDataOne

**Public Members:**

  - `ts`: `long`
  - `market`: `std::string`
  - `price`: `double`
  - `volume_ask`: `double`
  - `volume_bid`: `double`

**Public Functions:**




## Class/Struct: TickDataAll

**Public Members:**

  - `ts`: `long`
  - `tick_data`: `std::vector<TickDataOne>`

**Public Functions:**




## Class/Struct: PosOrderInfo

**Constructor:** `PosOrderInfo()`

**Public Members:**

  - `ts`: `long`
  - `ls`: `POS_LS`
  - `market`: `std::string`
  - `price`: `double`
  - `size`: `double`
  - `unclosed_size`: `double`
  - `open_price`: `double`
  - `close_price`: `double`
  - `pnl`: `double`
  - `status`: `uint`
  - `open_id`: `std::string`
  - `close_id`: `std::string`

**Public Functions:**




## Class/Struct: ReturnCurve

**Constructor:** `ReturnCurve()`

**Public Members:**

  - `m_maxdown_high_mark`: `uint`
  - `m_maxdown_low_mark`: `uint`
  - `m_maxdown_ratio`: `double`
  - `m_sharpe_ratio`: `double`

**Public Functions:**

  - `add(AssetPoint ap)` → `void`
  - `clear()` → `void`
  - `size()` → `size_t`
  - `get_ts_list()` → `std::vector<long>`
  - `get_asset_list()` → `std::vector<double>`
  - `get_total_return()` → `double`
  - `by_day()` → `std::vector<double>`
  - `get_last_asset()` → `double`
  - `get_init_asset()` → `double`
  - `get_performance()` → `std::string`
  - `get_tabled_raw()` → `std::string`




## Class/Struct: DataFeeder

**Public Members:**

**Public Functions:**

  - `get_tick_data()` → `TickDataAll`
  - `get_past_avg_price(long secs_from_now, long secs_peroid, int sec_res, uint market_index)` → `double`
  - `get_past_price(long secs_from_now, uint market_index)` → `double`
  - `get_market_name(uint index)` → `std::string`
  - `get_market_nums()` → `uint`




## Class/Struct: PosSet

**Constructor:** `PosSet()`

**Public Members:**

**Public Functions:**




## Class/Struct: PosController

**Constructor:** `PosController(std::string, ExConn *)`

**Public Members:**

**Public Functions:**

  - `all_pos_str(std::vector<PosOrderInfo> order_info)` → `std::string`
  - `get_pos_size0(uint index)` → `double`
  - `close_pos_with_size0(uint index, std::vector<PosOrderInfo> poi)` → `double`
  - `get_pos_prof(uint index, std::vector<PosOrderInfo> order_info)` → `double`
  - `get_pos_exp_prof(uint index)` → `double`
  - `get_pos_interval(uint index, long ts)` → `long`
  - `size()` → `size_t`
  - `get_all_vol(uint market_index)` → `double`
  - `order_str(uint index, std::vector<PosOrderInfo> order_info)` → `std::string`
  - `close_all()` → `void`
  - `close_one(uint index)` → `void`
  - `add_pos(PosSet pos)` → `void`
  - `remove_closed()` → `void`
  - `get_all_prof(std::vector<PosOrderInfo> order_info)` → `double`



## Class/Struct: SodCfg

**Constructor:** `SodCfg()`

**Public Members:**

  - `btc_dramatics_rate`: `double`
  - `catch_rate`: `double`
  - `check_interval`: `long`
  - `check_count_max`: `uint`
  - `end_interval`: `long`
  - `in_interval`: `long`
  - `fee_ratio`: `double`
  - `slip_ratio`: `double`
  - `max_full_down`: `double`
  - `pos_ratio`: `double`
  - `vol_div`: `double`
  - `prof_ratio`: `double`
  - `min_order_size`: `double`
  - `min_order_vol`: `double`

**Public Functions:**

