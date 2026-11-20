"""单店单元经济模型：坪效、人效、盈亏平衡、静态回本期"""

DEFAULTS = dict(
    area=420, rent=25200, head=9, hr=6500, gm=0.37,
    comm=0.025, deliv=0.08, hq=0.02, util=8000, mkt=22000,
    sales=780000, atv=8600, cvr=0.21,
    deco=1050000, prep=120000, stock=380000,
)


def run(**kw):
    p = dict(DEFAULTS); p.update(kw)
    gp = p['sales'] * p['gm']
    var_rate = p['comm'] + p['deliv'] + p['hq']
    var = p['sales'] * var_rate
    fixed = p['rent'] + p['head'] * p['hr'] + p['util'] + p['mkt']
    op = gp - var - fixed
    capex = p['deco'] + p['prep'] + p['stock']
    cm_rate = p['gm'] - var_rate
    be = fixed / cm_rate if cm_rate > 0 else float('inf')
    return dict(
        gmv_month=p['sales'], units=p['sales'] / p['atv'], traffic=p['sales'] / p['atv'] / p['cvr'],
        pfsm=p['sales'] / p['area'], pfsm_year=p['sales'] / p['area'] * 12,
        per_head=p['sales'] / p['head'], rent_psm=p['rent'] / p['area'],
        rent_ratio=p['rent'] / p['sales'],
        gross_profit=gp, variable=var, fixed=fixed,
        op_profit=op, npm=op / p['sales'], op_year=op * 12,
        capex=capex,
        payback=capex / op if op > 0 else float('inf'),
        roi=op * 12 / capex if capex else float('inf'),
        be_sales=be, be_units=be / p['atv'], be_pfsm=be / p['area'],
        margin_of_safety=(p['sales'] - be) / p['sales'],
    )


def verdict(r):
    pb = r['payback']
    if pb <= 24:
        return '回本周期健康（≤24 个月）'
    if pb <= 36:
        return '回本周期偏长，先压固定费用'
    return '回本周期过长，不建议开此店'
