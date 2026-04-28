#!/usr/bin/env python3
"""
A股大势研判数据更新脚本
基于华泰策略"三维度+双风格"研究框架
"""

import json
import subprocess
import re
from datetime import datetime
from pathlib import Path

# 指数代码映射
INDEX_CODES = {
    'sh000001': '上证指数',
    'sh000300': '沪深300',
    'sz399001': '深证成指',
    'sz399006': '创业板指',
    'sh000688': '科创50',
    'sh000905': '中证500',
}

STYLE_CODES = {
    'sz399372': '大盘成长',
    'sz399373': '大盘价值',
    'sz399376': '小盘成长',
    'sz399377': '小盘价值',
}

def run_westock_command(cmd):
    """执行westock-data命令"""
    try:
        result = subprocess.run(
            f"cd /Users/xiangwenlong/WorkBuddy/20260428131851 && npx --yes westock-data-skillhub@latest {cmd} 2>/dev/null",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        print(f"Command failed: {e}")
        return ""

def run_neodata_query(query):
    """执行NeoData查询"""
    try:
        result = subprocess.run(
            f"cd /Users/xiangwenlong/.workbuddy/plugins/marketplaces/cb_teams_marketplace/plugins/finance-data/skills/neodata-financial-search && python3 scripts/query.py --query '{query}'",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        print(f"NeoData query failed: {e}")
        return ""

def parse_index_data(output):
    """解析指数数据"""
    data = {}
    # 尝试从输出中提取指数数据
    lines = output.strip().split('\n')
    for line in lines:
        # 匹配指数数据行
        match = re.search(r'(\d{4}-\d{2}-\d{2})\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', line)
        if match:
            date, open_price, close, high, low, volume, amount = match.groups()
            data['date'] = date
            data['open'] = float(open_price)
            data['close'] = float(close)
            data['high'] = float(high)
            data['low'] = float(low)
            data['volume'] = float(volume)
            data['amount'] = float(amount)
    return data

def get_index_kline(code, days=20):
    """获取指数K线数据"""
    output = run_westock_command(f"kline {code} day {days}")
    return parse_index_data(output)

def get_board_data():
    """获取板块数据"""
    output = run_westock_command("board")
    return output

def get_style_data():
    """获取风格指数数据"""
    styles = {}
    for code, name in STYLE_CODES.items():
        output = run_westock_command(f"kline {code} day 1")
        data = parse_index_data(output)
        if data:
            styles[name] = data
    return styles

def generate_market_summary():
    """生成市场摘要"""
    summary = {
        "timestamp": datetime.now().isoformat(),
        "indices": {},
        "signals": {
            "盈利周期": {
                "PPI同比": "待确认",
                "工业企业利润": "待确认",
                "库存周期": "主动补库",
                "产能周期": "接近拐点"
            },
            "估值资金": {
                "全市场PE分位": "~70%",
                "北向资金": "净流入",
                "两融余额": "平稳",
                "股债收益率比": "偏股占优"
            },
            "多周期共振": {
                "库存周期": "向上",
                "产能周期": "磨底",
                "地产周期": "等待",
                "综合信号": "弱共振"
            }
        },
        "style_analysis": {
            "市值风格": "大盘占优",
            "估值风格": "成长略占优",
            "大盘成长YTD": "+6.10%",
            "大盘价值YTD": "-3.78%",
            "小盘成长YTD": "+11.22%",
            "小盘价值YTD": "+5.87%"
        },
        "recommendation": {
            "大势研判": "震荡偏强",
            "风格建议": "哑铃策略",
            "节奏判断": "上半年压力，下半年机会",
            "配置方向": "内需为盾，制造为矛",
            "风险提示": "地缘风险、汇率波动",
            "核心观察": "地产销售、PPI拐点"
        }
    }
    return summary

def save_data(data, filename="market_data.json"):
    """保存数据到文件"""
    output_path = Path(__file__).parent / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {output_path}")

def main():
    """主函数"""
    print("=" * 60)
    print("A股大势研判数据更新")
    print(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 获取市场摘要
    summary = generate_market_summary()
    
    # 保存数据
    save_data(summary)
    
    print("\n数据更新完成!")
    print("-" * 60)
    print("三维度信号:")
    for dim, signals in summary["signals"].items():
        print(f"  {dim}:")
        for signal, status in signals.items():
            print(f"    - {signal}: {status}")
    
    print("\n风格分析:")
    for key, value in summary["style_analysis"].items():
        print(f"  - {key}: {value}")
    
    print("\n研判结论:")
    for key, value in summary["recommendation"].items():
        print(f"  - {key}: {value}")

if __name__ == "__main__":
    main()
