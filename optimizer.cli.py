"""
冶炼厂阵列最优配比计算器 - 命令行版
用法: python optimizer_cli.py -r 50 -p 69.1 -N 10
"""
import argparse
from optimizer_core import find_optimal

def main():
    parser = argparse.ArgumentParser(description="冶炼厂阵列最优配比计算器")
    parser.add_argument('-r', '--r', type=float, required=True, help="产品每小时散热量 (热量/小时)")
    parser.add_argument('-p', '--p', type=float, required=True, help="基础加工时间 (小时)")
    parser.add_argument('-N', '--N', type=int, required=True, help="生产件数")
    parser.add_argument('--slots', type=int, default=60, help="组件总数上限 (默认60)")
    parser.add_argument('--margin', type=float, default=1.0, help="安全裕度 (默认1.0)")
    args = parser.parse_args()

    result = find_optimal(args.N, args.r, args.p, args.slots, args.margin)
    if result is None:
        print("无可行配置，请检查参数。")
        return

    print("\n最优配置：")
    for key, val in result.items():
        if isinstance(val, float):
            if key in ('t_prod', 'total_time'):
                print(f"  {key:>18}: {val:.6f} 小时")
            elif key in ('delta_H', 'C_max'):
                print(f"  {key:>18}: {val:.2f} 热量")
            elif key == 'c_cool':
                print(f"  {key:>18}: {val:.2f} 热量/小时")
            else:
                print(f"  {key:>18}: {val}")
        else:
            print(f"  {key:>18}: {val}")

if __name__ == "__main__":
    main()