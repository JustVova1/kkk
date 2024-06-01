import os
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkthemes import ThemedTk

# Конічний рух 
class MyApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.k1 = 0.25
        self.k2 = 1.55
        self.k3 = 0.35
        self.delta_t = 0.1
        self.start_time = 0
        self.end_time = 500
        self.selected_option = tk.StringVar(value="ax1")
       
       
        self.init_ui()

    def init_ui(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NW)

        self.right_frame = ttk.Frame(main_frame)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW)

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        input_group_box = ttk.LabelFrame(left_frame, text='Параметри')
        input_group_box.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NW)

        labels_and_entries = [
            ('k1:', self.k1, 'input_k1'),
            ('k2:', self.k2, 'input_k2'),
            ('k3:', self.k3, 'input_k3'),
            ('Δt:', self.delta_t, 'input_delta_t'),
            ('Початковий час:', self.start_time, 'input_start_time'),
            ('Кінцевий час:', self.end_time, 'input_end_time'),
        ]

        self.checkbox1_var1 = tk.BooleanVar(value=True)
        self.checkbox2_var1 = tk.BooleanVar(value=True)
        self.checkbox3_var1 = tk.BooleanVar(value=True)
        self.checkbox1_var2 = tk.BooleanVar(value=True)
        self.checkbox2_var2 = tk.BooleanVar(value=True)
        self.checkbox3_var2 = tk.BooleanVar(value=True)
        self.checkbox4_var2 = tk.BooleanVar(value=True)

        for i, (label_text, value, entry_attr) in enumerate(labels_and_entries):
            ttk.Label(input_group_box, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=5, padx=5)
            entry = ttk.Entry(input_group_box)
            entry.insert(0, str(value))
            entry.grid(row=i, column=1, pady=5, padx=5)
            setattr(self, entry_attr, entry)

        button_group_box = ttk.LabelFrame(left_frame, text='Побудова')
        button_group_box.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NW)

        buttons = [
            ('Побудувати графіки ω(t)', self.app_plot_omega),
            ('Побудувати графіки λ(t)', self.app_plot_lambda),
            ('Побудувати траєкторії λi(λj)', self.app_plot_lambda_2d)
        ]

        for text, command in buttons:
            ttk.Button(button_group_box, text=text, command=command).pack(anchor=tk.W, pady=5, padx=5)

        save_buttons_group_box = ttk.LabelFrame(button_group_box, text='Збереження')
        save_buttons_group_box.pack(padx=10, pady=20, fill=tk.BOTH, expand=True)

        save_buttons = [
            ('Зберегти ω(t) в CSV', self.app_save_omega),
            ('Зберегти λ(t) в CSV', self.app_save_lambda)
        ]

        for text, command in save_buttons:
            ttk.Button(save_buttons_group_box, text=text, command=command).pack(anchor=tk.W, pady=5, padx=5)



        select_box = ttk.LabelFrame(left_frame, text='Вибір графіка')
        select_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=tk.EW)

        checkbox_group1 = ttk.LabelFrame(select_box, text='Проекція кутової швидкості')
        checkbox_group1.grid(row=0, column=0, sticky=tk.NW, padx=10, pady=10)

        checkboxes1 = [
            ("ω1(t)", self.checkbox1_var1),
            ("ω2(t)", self.checkbox2_var1),
            ("ω3(t)", self.checkbox3_var1)
        ]

        for idx, (text, variable) in enumerate(checkboxes1):
            ttk.Checkbutton(checkbox_group1, text=text, variable=variable).grid(row=idx, column=0, padx=5, pady=2)

        checkbox_group2 = ttk.LabelFrame(select_box, text='Кватерніон')
        checkbox_group2.grid(row=0, column=1, sticky=tk.NW, padx=10, pady=10)

        checkboxes2 = [
            ("λ1(t)", self.checkbox1_var2),
            ("λ2(t)", self.checkbox2_var2),
            ("λ3(t)", self.checkbox3_var2),
            ("λ4(t)", self.checkbox4_var2)
        ]

        for idx, (text, variable) in enumerate(checkboxes2):
            ttk.Checkbutton(checkbox_group2, text=text, variable=variable).grid(row=idx, column=0, padx=5, pady=2)

        radio_group_box = ttk.LabelFrame(select_box, text='Траєкторії')
        radio_group_box.grid(row=0, column=2, padx=10, pady=10, sticky=tk.EW)

        radiobuttons = [
            ("λ1 vs λ0", "ax1"),
            ("λ2 vs λ0", "ax2"),
            ("λ3 vs λ0", "ax3")
        ]

        for idx, (text, value) in enumerate(radiobuttons):
            ttk.Radiobutton(radio_group_box, text=text, variable=self.selected_option, value=value).grid(row=idx, column=0, sticky=tk.W, padx=5, pady=5)
       

   
    def get_selected_checkboxes(self, checkbox_vars):
        return [var.get() for var in checkbox_vars]

    def app_save_omega(self):
        if 'omega_data' in self.__dict__:
            # Перевірка і створення папки data, якщо вона не існує
            if not os.path.exists('data'):
                os.makedirs('data')
            
            file_path = os.path.join('data', 'omega.csv')
            signal_calculator = SignalCalculator(self.k1, self.k2, self.k3, self.delta_t, self.start_time, self.end_time,  self.right_frame)
            signal_calculator.save_to_csv(file_path, *self.omega_data)
            messagebox.showinfo("Success", "Дані проекцій кутової швидкості успішно збережені в omega.csv")
        else:
            messagebox.showwarning("Error", "Немає даних проекцій кутової швидкості для збереження. Будь ласка, згенеруйте спочатку графік.")

    def app_save_lambda(self):
        if 'lambda_data' in self.__dict__:
            # Перевірка і створення папки data, якщо вона не існує
            if not os.path.exists('data'):
                os.makedirs('data')
            
            file_path = os.path.join('data', 'lambda.csv')
            signal_calculator = SignalCalculator(self.k1, self.k2, self.k3, self.delta_t, self.start_time, self.end_time,  self.right_frame)
            signal_calculator.save_to_csv(file_path, *self.lambda_data)
            messagebox.showinfo("Success", "Дані кватерніонів успішно збережені в lambda.csv")
        else:
            messagebox.showwarning("Error", "Немає даних кватерніонів для збереження. Будь ласка, згенеруйте спочатку графік.")
    def app_plot_lambda_2d(self):
        if self.app_check_input_data():
            for widget in self.right_frame.winfo_children():
                widget.destroy()

            signal_calculator = SignalCalculator(self.k1, self.k2, self.k3, self.delta_t, self.start_time, self.end_time,  self.right_frame)
            signal_calculator.plot_lambda_2d(self.selected_option.get(), self.right_frame)

    def app_check_input_data(self):
        k1_str = self.input_k1.get()
        k2_str = self.input_k2.get()
        k3_str = self.input_k3.get()
        delta_t_str = self.input_delta_t.get()
        start_time_str = self.input_start_time.get()
        end_time_str = self.input_end_time.get()
        try:
            self.k1 = float(k1_str)
            self.k2 = float(k2_str)
            self.k3 = float(k3_str)
            self.delta_t = float(delta_t_str)
            self.start_time = float(start_time_str)
            self.end_time = float(end_time_str)
            
            if self.delta_t == 0:
                messagebox.showwarning("Error", "Δt не може дорівнювати нулю.")
                return False
            
            if self.end_time == 0:
                messagebox.showwarning("Error", "Кінцевий час не може дорівнювати нулю.")
                return False
            
            return True
        except ValueError:
            messagebox.showwarning("Error", "Будь ласка, введіть правильні числові значення в усі поля введення.")
            return False

    def get_selected_checkboxes(self, checkbox_vars):
        # Функція повертає тільки вибрані чекбокси
        selected = [var.get() for var in checkbox_vars if var.get()]
        return selected

    def app_plot_omega(self):
        if self.app_check_input_data():
            for widget in self.right_frame.winfo_children():
                widget.destroy()

            selected_checkboxes = self.get_selected_checkboxes([self.checkbox1_var1, self.checkbox2_var1, self.checkbox3_var1])
            if selected_checkboxes:  # Перевірка, чи є вибрані чекбокси
                signal_calculator = SignalCalculator(self.k1, self.k2, self.k3, self.delta_t, self.start_time, self.end_time,  self.right_frame)
                self.omega_data = signal_calculator.plot_omega(self.right_frame, selected_checkboxes)
            else:
                messagebox.showwarning("Error", "Не вибрано жодного  ω. Будь ласка, встановіть хоча б один прапорець для побудови графіка.")

    def app_plot_lambda(self):
        if self.app_check_input_data():
            for widget in self.right_frame.winfo_children():
                widget.destroy()

            selected_checkboxes = self.get_selected_checkboxes([self.checkbox1_var2, self.checkbox2_var2, self.checkbox3_var2, self.checkbox4_var2])
            if selected_checkboxes:  # Перевірка, чи є вибрані чекбокси
                signal_calculator = SignalCalculator(self.k1, self.k2, self.k3, self.delta_t, self.start_time, self.end_time,  self.right_frame)
                self.lambda_data = signal_calculator.plot_lambda(self.right_frame, selected_checkboxes)
            else:
                messagebox.showwarning("Error", "Не вибрано жодного  λ. Будь ласка, встановіть хоча б один прапорець для побудови графіка.")
class SignalCalculator:
    def __init__(self, k1, k2, k3, delta_t, start_time, end_time,  right_frame):
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.delta_t = delta_t
        self.end_time = end_time
        self.start_time = start_time
        self.right_frame = right_frame
        self.current_fig = None
        self.canvas = None

    def calculate_omega_values(self):
        time_steps = np.arange(self.start_time, self.end_time + self.delta_t, self.delta_t)
        omega1 = self.k2 * np.sin(self.k3) * np.sin(self.k1 * time_steps)
        omega2 = self.k2 * np.sin(self.k3) * np.cos(self.k1 * time_steps)
        omega3 = self.k1 + self.k2 * np.cos(self.k3)
        omega3 = np.full(time_steps.shape, omega3)
        return time_steps, omega1, omega2, omega3

    def calculate_lambda_values(self):
        time_steps = np.arange(self.start_time, self.end_time + self.delta_t, self.delta_t)
        lambda0 = np.cos(self.k3 / 2) * np.cos(((self.k2 + self.k1) / 2) * time_steps)
        lambda1 = np.sin(self.k3 / 2) * np.cos(((self.k2 - self.k3) / 2) * time_steps)
        lambda2 = np.sin(self.k3 / 2) * np.sin(((self.k2 - self.k3) / 2) * time_steps)
        lambda3 = np.cos(self.k3 / 2) * np.sin(((self.k2 + self.k3) / 2) * time_steps)
        return time_steps, lambda0, lambda1, lambda2, lambda3

    def plot_lambda_2d(self, ax_to_plot, right_frame):
        time_steps,lambda0, lambda1, lambda2, lambda3 = self.calculate_lambda_values()
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)

        if ax_to_plot == "ax1":
            ax.plot(lambda0, lambda1)
            ax.set_xlabel('λ0')
            ax.set_ylabel('λ1')
            ax.set_title('Траєкторія λ1 vs λ0')
        elif ax_to_plot == "ax2":
            ax.plot(lambda0, lambda2)
            ax.set_xlabel('λ0₀')
            ax.set_ylabel('λ2')
            ax.set_title('Траєкторія λ2 vs λ0')
        elif ax_to_plot == "ax3":
            ax.plot(lambda0, lambda3)
            ax.set_xlabel('λ0')
            ax.set_ylabel('λ3')
            ax.set_title('Траєкторія λ3 vs λ0')

        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_plot(self, selected_option):
        self.plot_lambda_2d(selected_option)

    def plot_omega(self, right_frame, selected_checkboxes):
        time_steps, omega1, omega2, omega3 = self.calculate_omega_values()
        
        sns.set_theme(style="darkgrid")

        plot_indices = [i for i, selected in enumerate(selected_checkboxes) if selected]
        subplot_count = len(plot_indices)
        
        # Динамічно визначаємо figsize в залежності від кількості підграфіків
        fig_height = 2 * subplot_count if subplot_count > 0 else 4
        fig = plt.figure(figsize=(10, fig_height))

        for i, idx in enumerate(plot_indices):
            ax = fig.add_subplot(subplot_count, 1, i + 1)
            if idx == 0:
                ax.plot(time_steps, omega1, label='ω1', color='b', linestyle='-', linewidth=2)
                ax.set_ylabel('ω1', fontsize=10)
            elif idx == 1:
                ax.plot(time_steps, omega2, label='ω2', color='g', linestyle='-', linewidth=2)
                ax.set_ylabel('ω2', fontsize=10)
            elif idx == 2:
                ax.plot(time_steps, omega3, label='ω3', color='r', linestyle='-', linewidth=2)
                ax.set_ylabel('ω3', fontsize=10)
            ax.set_xlabel('Час, с', fontsize=10)
            ax.grid(True)
            ax.legend(loc='best')

        plt.tight_layout(pad=1.0)  # Зменшення відступів

        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        return time_steps, omega1, omega2, omega3

    def plot_lambda(self, right_frame, selected_checkboxes):
        time_steps, lambda0, lambda1, lambda2, lambda3 = self.calculate_lambda_values()

        sns.set_theme(style="darkgrid")

        plot_indices = [i for i, selected in enumerate(selected_checkboxes) if selected]
        subplot_count = len(plot_indices)
        
        # Динамічно визначаємо figsize в залежності від кількості підграфіків
        fig_height = 4 * subplot_count if subplot_count > 0 else 4
        fig = plt.figure(figsize=(8, fig_height))

        for i, idx in enumerate(plot_indices):
            ax = fig.add_subplot(subplot_count, 1, i + 1)
            if idx == 0:
                ax.plot(time_steps, lambda0, label='λ0', color='b', linestyle='-', linewidth=2)
                ax.set_ylabel('λ0', fontsize=10)
            elif idx == 1:
                ax.plot(time_steps, lambda1, label='λ1', color='g', linestyle='-', linewidth=2)
                ax.set_ylabel('λ1', fontsize=10)
            elif idx == 2:
                ax.plot(time_steps, lambda2, label='λ2', color='r', linestyle='-', linewidth=2)
                ax.set_ylabel('λ2', fontsize=10)
            elif idx == 3:
                ax.plot(time_steps, lambda3, label='λ3', color='m', linestyle='-', linewidth=2)
                ax.set_ylabel('λ3', fontsize=10)
            ax.set_xlabel('Час, с', fontsize=10)
            ax.grid(True)
            ax.legend(loc='best')

        plt.tight_layout(pad=1.0) 

        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        return time_steps, lambda0, lambda1, lambda2, lambda3


    def save_to_csv(self, filename, time_steps, *data):
        time_data = np.array([time_steps]).T
        data_array = np.column_stack(data)
        np.savetxt(filename, np.concatenate((time_data, data_array), axis=1), delimiter=',', fmt='%.3f', header='Time,' + ','.join([f'Data_{i+1}' for i in range(len(data))]), comments='')



if __name__ == "__main__":
    root = ThemedTk(theme="breeze") 
    app = MyApp(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
