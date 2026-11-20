"""Streamlit 页面：三个模型，输入即假设，右侧即结论"""
import pandas as pd
import streamlit as st

from models import unit_economics, live_breakeven, gmv_attribution, rank_by_inc_roi
from models.unit_economics import verdict

st.set_page_config(page_title='零售总经理 · 三模型', layout='wide')
st.title('三个能当场算的模型')
st.caption('全部为可改假设，非任何公司真实经营数据。改一个输入，结论立即重算。')

tabs = st.tabs(['单店单元经济', '直播盈亏平衡', '全域 GMV 归因'])

with tabs[0]:
    c1, c2, c3 = st.columns(3)
    area = c1.number_input('门店面积（㎡）', value=420, step=10)
    rent = c2.number_input('月租金（元）', value=25200, step=1000)
    head = c3.number_input('人员编制（人）', value=9, step=1)
    hr = c1.number_input('人均月人力成本（元）', value=6500, step=500)
    gm = c2.slider('综合毛利率', 0.20, 0.55, 0.37, 0.01)
    sales = c3.number_input('月均销售额（元）', value=780000, step=10000)
    atv = c1.number_input('客单价（元/单）', value=8600, step=100)
    cvr = c2.slider('到店转化率', 0.05, 0.45, 0.21, 0.01)
    capex = c3.number_input('建店总投入（元）', value=1550000, step=10000)

    r = unit_economics(area=area, rent=rent, head=head, hr=hr, gm=gm,
                       sales=sales, atv=atv, cvr=cvr, deco=capex - 500000, prep=120000, stock=380000)
    m = st.columns(4)
    m[0].metric('月经营利润', '%.0f 元' % r['op_profit'])
    m[1].metric('净利率', '%.1f%%' % (r['npm'] * 100))
    m[2].metric('盈亏平衡月销', '%.0f 元' % r['be_sales'])
    m[3].metric('静态回本期', '%.1f 个月' % r['payback'])
    st.info(verdict(r) + '；安全边际 %.1f%%' % (r['margin_of_safety'] * 100))
    st.dataframe(pd.DataFrame([
        ['月成交单数（单）', round(r['units'], 1)],
        ['月到店客流（人次）', round(r['traffic'])],
        ['月坪效（元/㎡）', round(r['pfsm'])],
        ['年坪效（元/㎡）', round(r['pfsm_year'])],
        ['人均月产出（元）', round(r['per_head'])],
        ['租金占销售额比', '%.1f%%' % (r['rent_ratio'] * 100)],
        ['月固定费用（元）', round(r['fixed'])],
        ['月变动费用（元）', round(r['variable'])],
        ['保本月单数（单）', round(r['be_units'], 1)],
        ['年投资回报率', '%.1f%%' % (r['roi'] * 100)],
    ], columns=['指标', '结果']).astype(str), hide_index=True, width='stretch')

with tabs[1]:
    c1, c2, c3 = st.columns(3)
    exposure = c1.number_input('单场曝光', value=120000, step=5000)
    enter = c2.slider('曝光→进入', 0.02, 0.30, 0.12, 0.01)
    stay = c3.slider('进入→停留 60 秒', 0.20, 0.80, 0.55, 0.01)
    click = c1.slider('停留→点商品卡', 0.02, 0.40, 0.12, 0.01)
    pay = c2.slider('点卡→下单', 0.005, 0.20, 0.03, 0.005)
    latv = c3.number_input('直播客单价（元）', value=5200, step=100)
    lgm = c1.slider('直播毛利率', 0.15, 0.55, 0.34, 0.01)
    ad = c2.number_input('单场投流（元）', value=8000, step=500)
    sessions = c3.number_input('月场次', value=12, step=1)
    refund = c1.slider('退款退货率', 0.0, 0.5, 0.28, 0.01)

    b = live_breakeven(exposure=exposure, enter_rate=enter, stay_rate=stay,
                       click_rate=click, pay_rate=pay, atv=latv, gm=lgm,
                       ad_cost=ad, refund_rate=refund)
    m = st.columns(4)
    m[0].metric('单场 GMV', '%.0f 元' % b['gmv'])
    m[1].metric('单场利润', '%.0f 元' % b['op_profit'])
    m[2].metric('保本场观', '%.0f 人次' % b['be_exposure'])
    m[3].metric('单均获客成本', '%.0f 元' % b['cac'])
    st.info('月 %d 场：GMV %.0f 元，利润 %.0f 元' % (sessions, b['month_gmv'], b['month_op']))
    st.dataframe(pd.DataFrame([
        ['进入直播间（人）', round(b['enter'])],
        ['停留 60 秒（人）', round(b['stay'])],
        ['点商品卡（人）', round(b['click'])],
        ['成交单数（单）', round(b['orders'], 1)],
        ['毛利（元）', round(b['gross_profit'])],
        ['单场固定成本（元）', round(b['fixed'])],
        ['保本 GMV（元）', round(b['be_gmv'])],
        ['每千次曝光产出（元）', round(b['gmv_per_1k_exposure'])],
    ], columns=['漏斗节点 / 指标', '结果']).astype(str), hide_index=True, width='stretch')

with tabs[2]:
    st.caption('投放只为增量付费：ROI 看总量，增量 ROI 才是决策依据。')
    a = gmv_attribution()
    df = pd.DataFrame([dict(
        渠道=x['channel'], 成交额=round(x['gmv']), 投放=round(x['cost']),
        占比='%.1f%%' % (x['share'] * 100),
        ROI=('—' if x['roi'] is None else round(x['roi'], 2)),
        增量ROI=('—' if x['inc_roi'] is None else round(x['inc_roi'], 2)),
    ) for x in a['rows']])
    st.dataframe(df.astype(str), hide_index=True, width='stretch')
    st.bar_chart(df.set_index('渠道')['成交额'])
    st.success('合计 GMV %.0f 元　混算 ROI %.2f　混算增量 ROI %.2f　增量效率最高：%s' % (
        a['total_gmv'], a['blended_roi'], a['blended_inc_roi'],
        rank_by_inc_roi(a)[0]['channel']))
