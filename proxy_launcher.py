import customtkinter as ctk
import tkinter.messagebox as messagebox
import subprocess
import threading
import requests
import time
import sys
import os
import base64

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("dark-blue")
MAIN_FONT = "Archangelsk"

class ProxyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Proxy Automator Pro")
        self.geometry("850x680") 
        self.resizable(False, False)
        self.configure(fg_color="#f0f2f5")

        self.repo_var = ctk.StringVar(value="")
        self.browser_var = ctk.StringVar(value=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe")
        self.profile_var = ctk.StringVar(value="Profile 1")
        self.stealth_var = ctk.BooleanVar(value=True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="white")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="Proxy", font=ctk.CTkFont(family=MAIN_FONT, size=24, weight="bold"), text_color="#1a1a1a")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 30))

        self.btn_dash = ctk.CTkButton(self.sidebar, text=" Dashboard", fg_color="#f0f2f5", text_color="#1a1a1a", hover_color="#e4e6e9", anchor="w", font=ctk.CTkFont(family=MAIN_FONT, size=14), command=self.show_dashboard)
        self.btn_dash.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.btn_settings = ctk.CTkButton(self.sidebar, text=" Settings", fg_color="transparent", text_color="gray", hover_color="#e4e6e9", anchor="w", font=ctk.CTkFont(family=MAIN_FONT, size=14), command=self.show_settings)
        self.btn_settings.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.dashboard_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.settings_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        self.build_dashboard()
        self.build_settings()
        self.show_dashboard()

    def get_gh_path(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        local_gh = os.path.join(base_path, "gh.exe")
        if os.path.exists(local_gh):
            return f'"{local_gh}"'
        return "gh"

    def build_dashboard(self):
        self.dashboard_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        header_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        header_frame.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(header_frame, text="Dashboard", font=ctk.CTkFont(family=MAIN_FONT, size=28, weight="bold"), text_color="#1a1a1a")
        title.grid(row=0, column=0, sticky="w")
        
        profile_menu = ctk.CTkOptionMenu(header_frame, values=["Profile 1", "Profile 2", "Profile 3", "Profile 4", "Profile 5"], variable=self.profile_var, fg_color="#1a1a1a", button_color="#333333", button_hover_color="#4d4d4d", font=ctk.CTkFont(family=MAIN_FONT, size=13))
        profile_menu.grid(row=0, column=1, sticky="e")

        self.card_ip = ctk.CTkFrame(self.dashboard_frame, corner_radius=20, fg_color="white")
        self.card_ip.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="nsew")
        ctk.CTkLabel(self.card_ip, text="Current IP", font=ctk.CTkFont(family=MAIN_FONT, size=14), text_color="gray").pack(pady=(15, 0))
        self.lbl_ip = ctk.CTkLabel(self.card_ip, text="Offline", font=ctk.CTkFont(family=MAIN_FONT, size=22, weight="bold"), text_color="#1a1a1a")
        self.lbl_ip.pack(pady=(5, 5))
        self.lbl_ping = ctk.CTkLabel(self.card_ip, text="Latency: - ms", font=ctk.CTkFont(family=MAIN_FONT, size=12), text_color="gray")
        self.lbl_ping.pack(pady=(0, 10))

        self.card_loc = ctk.CTkFrame(self.dashboard_frame, corner_radius=20, fg_color="white")
        self.card_loc.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.card_loc, text="Location", font=ctk.CTkFont(family=MAIN_FONT, size=14), text_color="gray").pack(pady=(20, 5))
        self.lbl_loc = ctk.CTkLabel(self.card_loc, text="Offline", font=ctk.CTkFont(family=MAIN_FONT, size=18, weight="bold"), text_color="#1a1a1a")
        self.lbl_loc.pack(pady=(0, 20))

        self.card_isp = ctk.CTkFrame(self.dashboard_frame, corner_radius=20, fg_color="white")
        self.card_isp.grid(row=1, column=2, padx=(10, 0), pady=10, sticky="nsew")
        ctk.CTkLabel(self.card_isp, text="Provider (ISP)", font=ctk.CTkFont(family=MAIN_FONT, size=14), text_color="gray").pack(pady=(20, 5))
        self.lbl_isp = ctk.CTkLabel(self.card_isp, text="Offline", font=ctk.CTkFont(family=MAIN_FONT, size=18, weight="bold"), text_color="#1a1a1a")
        self.lbl_isp.pack(pady=(0, 20))

        self.btn_check_ip = ctk.CTkButton(self.dashboard_frame, text="Refresh Status", fg_color="#ffffff", text_color="#1a1a1a", hover_color="#f0f2f5", border_width=1, border_color="#d1d5db", font=ctk.CTkFont(family=MAIN_FONT, size=13), command=self.check_ip_status)
        self.btn_check_ip.grid(row=2, column=0, columnspan=3, pady=10)

        control_frame = ctk.CTkFrame(self.dashboard_frame, corner_radius=20, fg_color="white")
        control_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(5, 0))
        control_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(control_frame, text="Instance Controls", font=ctk.CTkFont(family=MAIN_FONT, size=20, weight="bold"), text_color="#1a1a1a").grid(row=0, column=0, columnspan=2, pady=(15, 10))

        btn_create = ctk.CTkButton(control_frame, text="Deploy Server", fg_color="#1a1a1a", text_color="white", hover_color="#333333", height=45, corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT, size=14, weight="bold"), command=self.create_server)
        btn_create.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        btn_tunnel = ctk.CTkButton(control_frame, text="Connect & Launch Browser", fg_color="#1a1a1a", text_color="white", hover_color="#333333", height=45, corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT, size=14, weight="bold"), command=self.launch_tunnel_and_browser)
        btn_tunnel.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        btn_destroy = ctk.CTkButton(control_frame, text="Destroy Instance", fg_color="#f9fafb", text_color="#1a1a1a", hover_color="#f3f4f6", border_width=1, border_color="#d1d5db", height=45, corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT, size=14, weight="bold"), command=self.delete_server)
        btn_destroy.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 15), sticky="ew")

    def build_settings(self):
        self.settings_frame.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(self.settings_frame, text="Settings", font=ctk.CTkFont(family=MAIN_FONT, size=28, weight="bold"), text_color="#1a1a1a")
        title.grid(row=0, column=0, sticky="w", pady=(0, 15))

        wizard_card = ctk.CTkFrame(self.settings_frame, corner_radius=20, fg_color="white")
        wizard_card.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        wizard_card.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(wizard_card, text="Quick Setup Wizard", font=ctk.CTkFont(family=MAIN_FONT, size=18, weight="bold"), text_color="#1a1a1a").grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 10))

        btn_auth = ctk.CTkButton(wizard_card, text="1. Connect GitHub Account", fg_color="#f9fafb", text_color="#1a1a1a", hover_color="#f3f4f6", border_width=1, border_color="#d1d5db", height=40, font=ctk.CTkFont(family=MAIN_FONT, size=13, weight="bold"), command=self.auth_github)
        btn_auth.grid(row=1, column=0, padx=(20, 10), pady=(0, 20), sticky="ew")

        btn_setup = ctk.CTkButton(wizard_card, text="2. Auto-Setup Repository", fg_color="#1a1a1a", text_color="white", hover_color="#333333", height=40, font=ctk.CTkFont(family=MAIN_FONT, size=13, weight="bold"), command=self.auto_setup_repo)
        btn_setup.grid(row=1, column=1, padx=(10, 20), pady=(0, 20), sticky="ew")

        settings_card = ctk.CTkFrame(self.settings_frame, corner_radius=20, fg_color="white")
        settings_card.grid(row=2, column=0, sticky="nsew", pady=5)
        settings_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(settings_card, text="GitHub Repository (user/repo):", font=ctk.CTkFont(family=MAIN_FONT, size=14, weight="bold"), text_color="#1a1a1a").grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        self.repo_entry = ctk.CTkEntry(settings_card, textvariable=self.repo_var, width=400, height=35, fg_color="#f9fafb", text_color="#1a1a1a", border_color="#d1d5db", placeholder_text="e.g. username/proxy-auto")
        self.repo_entry.grid(row=1, column=0, sticky="w", padx=20)

        ctk.CTkLabel(settings_card, text="Browser Executable Path:", font=ctk.CTkFont(family=MAIN_FONT, size=14, weight="bold"), text_color="#1a1a1a").grid(row=2, column=0, sticky="w", padx=20, pady=(15, 5))
        browser_entry = ctk.CTkEntry(settings_card, textvariable=self.browser_var, width=500, height=35, fg_color="#f9fafb", text_color="#1a1a1a", border_color="#d1d5db")
        browser_entry.grid(row=3, column=0, sticky="w", padx=20)
        
        stealth_switch = ctk.CTkSwitch(settings_card, text="Enable Anti-Detect Stealth Mode (Block WebRTC Leaks)", variable=self.stealth_var, onvalue=True, offvalue=False, font=ctk.CTkFont(family=MAIN_FONT, size=13, weight="bold"), text_color="#1a1a1a", progress_color="#1a1a1a", button_color="#ffffff", button_hover_color="#e5e5e5")
        stealth_switch.grid(row=4, column=0, sticky="w", padx=20, pady=(15, 5))

        info_text = "Stealth mode injects Chromium flags to hide your real IP and prevent fingerprinting."
        ctk.CTkLabel(settings_card, text=info_text, text_color="gray", font=ctk.CTkFont(family=MAIN_FONT, size=12)).grid(row=5, column=0, sticky="w", padx=20, pady=(0, 20))

    def show_dashboard(self):
        self.settings_frame.grid_forget()
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")
        self.btn_dash.configure(fg_color="#f0f2f5", text_color="#1a1a1a")
        self.btn_settings.configure(fg_color="transparent", text_color="gray")

    def show_settings(self):
        self.dashboard_frame.grid_forget()
        self.settings_frame.grid(row=0, column=0, sticky="nsew")
        self.btn_settings.configure(fg_color="#f0f2f5", text_color="#1a1a1a")
        self.btn_dash.configure(fg_color="transparent", text_color="gray")

    def run_cmd(self, cmd, background=False):
        if background:
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(cmd, shell=True)

    def auth_github(self):
        msg = ("Authorization Guide:\n\n"
               "1. A console will open.\n"
               "2. Select 'GitHub.com'\n"
               "3. Select 'HTTPS'\n"
               "4. Select 'Yes' to authenticate Git\n"
               "5. Select 'Login with a web browser'\n\n"
               "IMPORTANT: The tool will request 'codespace' permissions. Please allow it.\n\n"
               "Copy the 8-digit code, paste it into the browser, and click Authorize.")
        messagebox.showinfo("Step 1: Authorization", msg)
        gh = self.get_gh_path()
        self.run_cmd(f'start cmd /k "{gh} auth login -s codespace"')

    def auto_setup_repo(self):
        def setup():
            try:
                gh = self.get_gh_path()
                result = subprocess.run(f'{gh} api user -q ".login"', capture_output=True, text=True, shell=True)
                username = result.stdout.strip()
                
                if not username:
                    messagebox.showerror("Error", "Not logged in! Please complete Step 1 first.")
                    return

                repo_name = "proxy-auto"
                full_repo = f"{username}/{repo_name}"
                
                subprocess.run(f'{gh} repo create {repo_name} --public', capture_output=True, shell=True)
                
                readme_text = "# Proxy Auto\nRepository automatically initialized for Codespaces."
                readme_b64 = base64.b64encode(readme_text.encode('utf-8')).decode('utf-8')
                init_cmd = f'{gh} api -X PUT repos/{full_repo}/contents/README.md -f message="Initial commit" -f content="{readme_b64}"'
                subprocess.run(init_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                self.repo_var.set(full_repo)
                messagebox.showinfo("Success", f"Repository {full_repo} successfully created and initialized!\n\nYou can now return to the Dashboard and Deploy your server.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to setup repository: {str(e)}")

        threading.Thread(target=setup, daemon=True).start()

    def create_server(self):
        repo = self.repo_var.get().strip()
        if not repo:
            messagebox.showerror("Error", "Repository is missing. Go to Settings and run the Auto-Setup Repository.")
            return
        messagebox.showinfo("Deploying", "Press 'Enter' in the console if prompted for Machine Type.")
        gh = self.get_gh_path()
        self.run_cmd(f'start cmd /k "{gh} codespace create -R {repo}"')

    def launch_tunnel_and_browser(self):
        repo = self.repo_var.get().strip()
        browser = self.browser_var.get().strip()
        profile_name = self.profile_var.get().replace(" ", "_").lower()
        gh = self.get_gh_path()
        
        tunnel_cmd = f'start cmd /k "{gh} codespace ssh -R {repo} -- -D 1080 -N"'
        subprocess.Popen(tunnel_cmd, shell=True)
        
        def launch_br():
            time.sleep(3) 
            flags = f'--proxy-server="socks5://127.0.0.1:1080" --user-data-dir="C:\\proxy_{profile_name}"'
            if self.stealth_var.get():
                flags += ' --force-webrtc-ip-handling-policy=disable_non_proxied_udp --enforce-webrtc-ip-permission-check --disable-features=WebRtcHideLocalIpsWithMdns'

            launch_cmd = f'"{browser}" {flags}'
            self.run_cmd(launch_cmd, background=True)
            self.check_ip_status()

        threading.Thread(target=launch_br, daemon=True).start()

    def delete_server(self):
        gh = self.get_gh_path()
        self.run_cmd(f"{gh} codespace delete --all --force", background=True)
        messagebox.showinfo("Destroyed", "All instances have been terminated.")
        self.lbl_ip.configure(text="Offline", text_color="#1a1a1a")
        self.lbl_loc.configure(text="Offline")
        self.lbl_isp.configure(text="Offline")
        self.lbl_ping.configure(text="Latency: - ms", text_color="gray")

    def check_ip_status(self):
        self.lbl_ip.configure(text="Checking...", text_color="gray")
        self.lbl_loc.configure(text="Checking...", text_color="gray")
        self.lbl_isp.configure(text="Checking...", text_color="gray")
        self.lbl_ping.configure(text="Latency: checking...", text_color="gray")

        def fetch():
            try:
                proxies = {'http': 'socks5h://127.0.0.1:1080', 'https': 'socks5h://127.0.0.1:1080'}
                start_time = time.time()
                response = requests.get('http://ip-api.com/json/', proxies=proxies, timeout=10)
                ping_ms = int((time.time() - start_time) * 1000)
                
                data = response.json()
                
                if data.get("status") == "success":
                    self.lbl_ip.configure(text=data.get("query", "Unknown"), text_color="#22c55e")
                    self.lbl_loc.configure(text=f"{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}")
                    self.lbl_isp.configure(text=data.get("isp", "Unknown"))
                    
                    ping_color = "#22c55e" if ping_ms < 150 else ("#eab308" if ping_ms < 300 else "#ef4444")
                    self.lbl_ping.configure(text=f"Latency: {ping_ms} ms", text_color=ping_color)
                else:
                    raise Exception("API Error")
            except Exception:
                self.lbl_ip.configure(text="Failed", text_color="#ef4444")
                self.lbl_loc.configure(text="Tunnel Offline")
                self.lbl_isp.configure(text="Tunnel Offline")
                self.lbl_ping.configure(text="Latency: Error", text_color="#ef4444")

        threading.Thread(target=fetch, daemon=True).start()

if __name__ == "__main__":
    app = ProxyApp()
    app.mainloop()