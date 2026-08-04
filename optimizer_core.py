"""
冶炼厂阵列组件优化核心计算模型
包含冷却速度、单件/批量生产模拟和最优配置枚举
"""
import math

def floor_cool(raw):
    """向下取整并保证下限为2"""
    return max(2, math.floor(raw))

def simulate_batch(N, r, p, c, o, s, h, margin=1.0):
    """
    离散模拟生产 N 件的总时间（含冷却）
    返回总时间，若配置无效返回 inf
    """
    raw = (5 + 8*c) * (1 - 0.10*o + 0.07*h)
    c_cool = floor_cool(raw)
    if c_cool >= r:
        return float('inf')
    t_prod = p / (1 + 0.25*o)
    delta_H = (r - c_cool) * t_prod
    C_max = 100 + 25*s
    if delta_H > C_max - margin + 1e-9:
        return float('inf')
    heat = 0.0
    total_time = 0.0
    for _ in range(N):
        if heat + delta_H > C_max:
            cool_need = heat + delta_H - C_max
            cool_time = cool_need / c_cool
            total_time += cool_time
            heat = C_max - delta_H
        total_time += t_prod
        heat += delta_H
    return total_time

def find_optimal(N, r, p, total_slots=60, margin=1.0):
    """
    枚举所有组件组合，返回最优配置字典
    """
    best_time = float('inf')
    best_config = None
    for c in range(total_slots + 1):
        for o in range(total_slots - c + 1):
            for s in range(total_slots - c - o + 1):
                for h in range(total_slots - c - o - s + 1):
                    T = simulate_batch(N, r, p, c, o, s, h, margin)
                    if T < best_time:
                        best_time = T
                        best_config = (c, o, s, h)
    if best_config is None:
        return None
    c, o, s, h = best_config
    raw = (5 + 8*c) * (1 - 0.10*o + 0.07*h)
    c_cool = floor_cool(raw)
    t_prod = p / (1 + 0.25*o)
    delta_H = (r - c_cool) * t_prod
    C_max = 100 + 25*s
    return {
        'c': c, 'o': o, 's': s, 'h': h,
        't_prod': t_prod,
        'c_cool': c_cool,
        'delta_H': delta_H,
        'C_max': C_max,
        'total_time': best_time,
        'N': N,
        'total_components': c+o+s+h
    }
