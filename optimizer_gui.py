"""
冶炼厂阵列最优配比计算器 - 图形界面版
基于 tkinter，无需额外依赖
"""
import tkinter as tk
from tkinter import ttk, messagebox
from optimizer_core import find_optimal

# 预设产品（快速填充）
PRESETS = {
    "思维辅助器": (40, 69.1),
    "神圣机械心脏": (50, 69.1),
    "灵脉回路": (25, 21.0),
    "炼锻钢": (25, 19.8),
    "祝圣石": (10, 14.4)
}

class OptimizerApp:
    def __init__(self, root):
        self.root = root
        root.title("冶炼厂阵列最优配比计算器")
        root.geometry("600x550")
        root.resizable(False, False)

        # ---- 输入区域 ----
        main_frame = ttk.LabelFrame(root, text="输入参数", padding=10)
        main_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(main_frame, text="快速选择产品:").grid(row=0, column=0, sticky="w", pady=2)
        self.preset_var = tk.StringVar()
        self.preset_combo = ttk.Combobox(main_frame, textvariable=self.preset_var,
                                         values=list(PRESETS.keys()), state="readonly")
        self.preset_combo.grid(row=0, column=1, sticky="w", pady=2)
        self.preset_combo.bind("<<ComboboxSelected>>", self.load_preset)

        ttk.Label(main_frame, text="散热量 r (热量/小时):").grid(row=1, column=0, sticky="w", pady=2)
        self.r_entry = ttk.Entry(main_frame, width=15)
        self.r_entry.grid(row=1, column=1, sticky="w", pady=2)
        self.r_entry.insert(0, "50")

        ttk.Label(main_frame, text="基础加工时间 p (小时):").grid(row=2, column=0, sticky="w", pady=2)
        self.p_entry = ttk.Entry(main_frame, width=15)
        self.p_entry.grid(row=2, column=1, sticky="w", pady=2)
        self.p_entry.insert(0, "69.1")

        ttk.Label(main_frame, text="生产件数 N:").grid(row=3, column=0, sticky="w", pady=2)
        self.n_entry = ttk.Entry(main_frame, width=15)
        self.n_entry.grid(row=3, column=1, sticky="w", pady=2)
        self.n_entry.insert(0, "1")

        ttk.Label(main_frame, text="组件总数上限 (默认60):").grid(row=4, column=0, sticky="w", pady=2)
        self.slots_entry = ttk.Entry(main_frame, width=15)
        self.slots_entry.grid(row=4, column=1, sticky="w", pady=2)
        self.slots_entry.insert(0, "60")

        ttk.Label(main_frame, text="安全裕度 margin (建议1.0):").grid(row=5, column=0, sticky="w", pady=2)
        self.margin_entry = ttk.Entry(main_frame, width=15)
        self.margin_entry.grid(row=5, column=1, sticky="w", pady=2)
        self.margin_entry.insert(0, "1.0")

        self.calc_btn = ttk.Button(main_frame, text="计算最优配置", command=self.calculate)
        self.calc_btn.grid(row=6, column=0, columnspan=2, pady=10)

        # ---- 结果显示 ----
        result_frame = ttk.LabelFrame(root, text="计算结果", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.result_text = tk.Text(result_frame, height=15, width=70, state="disabled", wrap="word")
        self.result_text.pack(fill="both", expand=True)

        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief="sunken")
        status_bar.pack(fill="x", side="bottom", padx=5, pady=2)

    def load_preset(self, event=None):
        name = self.preset_var.get()
        if name in PRESETS:
            r, p = PRESETS[name]
            self.r_entry.delete(0, tk.END)
            self.r_entry.insert(0, str(r))
            self.p_entry.delete(0, tk.END)
            self.p_entry.insert(0, str(p))

    def calculate(self):
        try:
            r = float(self.r_entry.get())
            p = float(self.p_entry.get())
            N = int(self.n_entry.get())
            slots = int(self.slots_entry.get()) if self.slots_entry.get() else 60
            margin = float(self.margin_entry.get()) if self.margin_entry.get() else 1.0
        except ValueError:
            messagebox.showerror("输入错误", "请确保所有输入为有效数字")
            return
        if N <= 0 or r <= 0 or p <= 0 or slots <= 0:
            messagebox.showerror("输入错误", "参数必须为正数")
            return

        self.status_var.set("正在计算...")
        self.root.update()

        result = find_optimal(N, r, p, slots, margin)

        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)

        if result is None:
            self.result_text.insert(tk.END, "无可行配置！\n请检查参数（可能 margin 过大或 r/p 不合理）。")
            self.status_var.set("计算完成，无可行配置")
        else:
            out = f"最优组件配置：\n"
            out += f"  冷却 c = {result['c']}\n"
            out += f"  超频 o = {result['o']}\n"
            out += f"  分担 s = {result['s']}\n"
            out += f"  散热 h = {result['h']}\n"
            out += f"  总组件数 = {result['total_components']}\n"
            out += f"\n性能参数：\n"
            out += f"  单件生产时间 = {result['t_prod']:.6f} 小时\n"
            out += f"  实际冷却速度 = {result['c_cool']:.2f} 热量/小时\n"
            out += f"  单件净产热   = {result['delta_H']:.2f} 热量\n"
            out += f"  热容量上限   = {result['C_max']:.2f} 热量\n"
            out += f"  总生产时间   = {result['total_time']:.6f} 小时 (含冷却)\n"
            out += f"  生产件数     = {result['N']}"
            self.result_text.insert(tk.END, out)
            self.status_var.set("计算完成")
        self.result_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizerApp(root)
    root.mainloop()