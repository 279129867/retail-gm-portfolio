"""全域 GMV 归因：渠道 ROI、增量 ROI、结构占比与边际 ROI"""

CHANNELS = [
    dict(name='自然到店', cost=0, gmv=1680000, incremental_gmv=1680000),
    dict(name='线上投放', cost=86000, gmv=760000, incremental_gmv=266000),
    dict(name='老客转介绍', cost=18000, gmv=520000, incremental_gmv=340000),
    dict(name='整装渠道', cost=42000, gmv=610000, incremental_gmv=210000),
]


def run(channels=None):
    ch = channels or CHANNELS
    total_gmv = sum(c['gmv'] for c in ch)
    total_cost = sum(c['cost'] for c in ch)
    total_inc = sum(c['incremental_gmv'] for c in ch)
    rows = []
    for c in ch:
        rows.append(dict(
            channel=c['name'], gmv=c['gmv'], cost=c['cost'],
            share=c['gmv'] / total_gmv if total_gmv else 0,
            roi=(c['gmv'] / c['cost']) if c['cost'] else None,
            inc_roi=(c['incremental_gmv'] / c['cost']) if c['cost'] else None,
            cac=(c['cost'] / c['incremental_gmv']) if c['incremental_gmv'] and c['cost'] else None,
        ))
    return dict(
        rows=rows, total_gmv=total_gmv, total_cost=total_cost,
        total_incremental=total_inc,
        blended_roi=(total_gmv / total_cost) if total_cost else None,
        blended_inc_roi=(total_inc / total_cost) if total_cost else None,
    )


def rank_by_inc_roi(result):
    paid = [r for r in result['rows'] if r['inc_roi'] is not None]
    return sorted(paid, key=lambda r: -r['inc_roi'])
