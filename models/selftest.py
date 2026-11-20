"""不依赖 Streamlit 的自检：打印三个模型的基准结果"""
from models import unit_economics, live_breakeven, gmv_attribution, rank_by_inc_roi
from models.unit_economics import verdict


def main():
    r = unit_economics()
    print('【单店单元经济】')
    print('  月销 %.0f 元 / 坪效 %.0f 元 / 人效 %.0f 元' % (r['gmv_month'], r['pfsm'], r['per_head']))
    print('  月经营利润 %.0f 元 / 净利率 %.1f%%' % (r['op_profit'], r['npm'] * 100))
    print('  盈亏平衡月销 %.0f 元 / 安全边际 %.1f%%' % (r['be_sales'], r['margin_of_safety'] * 100))
    print('  静态回本 %.1f 个月 —— %s' % (r['payback'], verdict(r)))

    b = live_breakeven()
    print('\n【直播盈亏平衡】')
    print('  单场 GMV %.0f / 净额 %.0f 元 / 毛利 %.0f 元 / 成本 %.0f 元 / 利润 %.0f 元' % (b['gmv'], b['net_gmv'], b['gross_profit'], b['fixed'], b['op_profit']))
    print('  保本场观 %.0f 人次 / 保本 GMV %.0f 元 / 单均获客 %.0f 元' % (b['be_exposure'], b['be_gmv'], b['cac']))

    a = gmv_attribution()
    print('\n【全域 GMV 归因】')
    for row in a['rows']:
        roi = '—' if row['roi'] is None else '%.2f' % row['roi']
        inc = '—' if row['inc_roi'] is None else '%.2f' % row['inc_roi']
        print('  %-6s 占比 %5.1f%%　ROI %5s　增量 ROI %5s' % (row['channel'], row['share'] * 100, roi, inc))
    print('  合计 GMV %.0f 元，投放 %.0f 元，混算 ROI %.2f，混算增量 ROI %.2f' % (
        a['total_gmv'], a['total_cost'], a['blended_roi'], a['blended_inc_roi']))
    top = rank_by_inc_roi(a)[0]
    print('  增量效率最高渠道：%s（增量 ROI %.2f）' % (top['channel'], top['inc_roi']))


if __name__ == '__main__':
    main()
