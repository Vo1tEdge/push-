import os
import requests
import akshare as ak
from datetime import datetime

def get_fund_data():
    """获取012752最新净值和涨跌幅"""
    df = ak.fund_open_fund_info_em(symbol="012752", indicator="单位净值走势")
    df = df.tail(2)  # 取最近两行
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    nav = latest['单位净值']
    change = (nav - prev['单位净值']) / prev['单位净值'] * 100
    return {
        'date': str(latest['净值日期']),
        'nav': nav,
        'change': change
    }

def push_to_wechat(data):
    """推送到微信"""
    token = os.environ.get("PUSHPLUS_TOKEN")
    color = "red" if data['change'] >= 0 else "green"
    content = f"""
    <h3>建信纳斯达克100指数(QDII)C人民币</h3>
    <p>净值日期：{data['date']}</p>
    <p>单位净值：<b>{data['nav']}</b></p>
    <p>日涨跌幅：<font color="{color}"><b>{data['change']:+.2f}%</b></font></p>
    <p style="color:#999;font-size:12px">数据来源：天天基金 | 推送时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    """
    requests.post("https://www.pushplus.plus/send", json={
        "token": token,
        "title": f"纳斯达克100基金日报 {data['change']:+.2f}%",
        "content": content,
        "template": "html"
    })

if __name__ == "__main__":
    data = get_fund_data()
    push_to_wechat(data)
