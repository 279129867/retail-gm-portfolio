"""直播盈亏平衡模型：一场直播的漏斗、边际贡献与保本场观"""

DEFAULTS = dict(
    exposure=120000,      # 场观曝光
    enter_rate=0.12,      # 曝光→进入直播间
    stay_rate=0.55,       # 进入→停留超过 60 秒
    click_rate=0.12,      # 停留→点商品卡
    pay_rate=0.03,        # 点卡→下单
    atv=5200,             # 直播客单价
    gm=0.34,              # 直播品综合毛利率
    ad_cost=8000,         # 单场投流
    host_cost=1200,       # 主播单场
    ops_cost=900,         # 运营 + 中控单场
    rent_alloc=1500,      # 场地设备摊销
    sample_cost=700,      # 样机与损耗
    refund_rate=0.28,     # 退款退货率（直播家居品类高退货）
    sessions=12,          # 月场次
)


def run(**kw):
    p = dict(DEFAULTS); p.update(kw)
    enter = p['exposure'] * p['enter_rate']
    stay = enter * p['stay_rate']
    click = stay * p['click_rate']
    orders = click * p['pay_rate']
    gmv = orders * p['atv']
    net = gmv * (1 - p['refund_rate'])
    gp = net * p['gm']
    fixed = p['ad_cost'] + p['host_cost'] + p['ops_cost'] + p['rent_alloc'] + p['sample_cost']
    op = gp - fixed
    gmv_per_exposure = p['enter_rate'] * p['stay_rate'] * p['click_rate'] * p['pay_rate'] * p['atv']
    be_gmv = fixed / p['gm'] if p['gm'] > 0 else float('inf')
    be_orders = be_gmv / p['atv']
    be_exposure = be_gmv / gmv_per_exposure if gmv_per_exposure > 0 else float('inf')
    return dict(
        enter=enter, stay=stay, click=click, orders=orders,
        gmv=gmv, net_gmv=net, gross_profit=gp, fixed=fixed, op_profit=op,
        margin=op / net if net else 0,
        gmv_per_1k_exposure=gmv_per_exposure * 1000,
        be_gmv=be_gmv, be_orders=be_orders, be_exposure=be_exposure,
        cac=fixed / orders if orders else float('inf'),
        month_op=op * p['sessions'], month_gmv=gmv * p['sessions'],
    )
