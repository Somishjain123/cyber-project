import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import cipher_logic
import time
import random

# Color Palette for Premium Look
B_DARK = "#0f172a"  # Slate 900
B_SENDER = "#1e293b" # Slate 800
B_NETWORK = "#334155" # Slate 700
B_RECEIVER = "#1e293b"
C_ACCENT = "#38bdf8" # Sky 400
C_SENDER = "#10b981" # Emerald 500
C_ATTACK = "#f43f5e" # Rose 500
C_TEXT = "#f8fafc"

class SecureCommSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Message Communication Simulation")
        self.root.geometry("1100x850")
        self.root.configure(bg=B_DARK)
        
        self.current_sub_key = cipher_logic.generate_substitution_key()
        self.original_plaintext = ""
        self.last_used_method = "None"
        
        # State to hold the transmitted message's context (Fixes key-overwrite bug)
        self.transmitted_context = {
            "text": "",
            "method": "None",
            "key": None,
            "shifts": []
        }
        
        self.setup_styles()
        self.create_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=B_DARK)
        style.configure("Section.TFrame", background=B_SENDER)
        style.configure("TLabel", background=B_DARK, foreground=C_TEXT, font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=C_ACCENT)
        style.configure("Sender.TButton", background=C_SENDER, foreground="white", font=("Segoe UI", 10, "bold"))
        style.configure("Attack.TButton", background=C_ATTACK, foreground="white", font=("Segoe UI", 10, "bold"))
        
    def create_layout(self):
        # Title Header
        header_frame = tk.Frame(self.root, bg=B_DARK, pady=10)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="🛡️ SECURE MESSAGE COMMUNICATION SIMULATION", 
                 font=("Segoe UI", 20, "bold"), fg=C_ACCENT, bg=B_DARK).pack()
        tk.Label(header_frame, text="A → ENCRYPT → NETWORK → ATTACKER → RECEIVER", 
                 font=("Consolas", 10), fg="#94a3b8", bg=B_DARK).pack()

        # Main Columns Container
        main_container = tk.Frame(self.root, bg=B_DARK)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.columnconfigure(2, weight=1)

        # --- COLUMN 1: SENDER (A) ---
        sender_frame = tk.LabelFrame(main_container, text="👤 [SENDER A]", font=("Segoe UI", 12, "bold"),
                                     bg=B_SENDER, fg=C_SENDER, padx=10, pady=10)
        sender_frame.grid(row=0, column=0, sticky="nsew", padx=5)
        
        tk.Label(sender_frame, text="Step 1: Type Message", bg=B_SENDER, fg="#cbd5e1").pack(anchor="w")
        self.sender_input = scrolledtext.ScrolledText(sender_frame, height=5, bg="#0f172a", fg="white", 
                                                      font=("Segoe UI", 11), borderwidth=0)
        self.sender_input.pack(fill="x", pady=5)
        self.sender_input.insert("1.0", "HELLO WORLD THIS IS A SECRET MESSAGE")

        # Encryption Config
        config_frame = tk.Frame(sender_frame, bg=B_SENDER)
        config_frame.pack(fill="x", pady=10)
        
        tk.Label(config_frame, text="Caesar Shift:", bg=B_SENDER, fg="white").grid(row=0, column=0, sticky="w")
        self.shift_entry = tk.Entry(config_frame, width=5, bg=B_DARK, fg="white", insertbackground="white")
        self.shift_entry.grid(row=0, column=1, padx=5, pady=2)
        self.shift_entry.insert(0, "3")

        tk.Label(config_frame, text="Multi-Shift Keys:", bg=B_SENDER, fg="white").grid(row=1, column=0, sticky="w")
        self.multi_entry = tk.Entry(config_frame, width=12, bg=B_DARK, fg="white", insertbackground="white")
        self.multi_entry.grid(row=1, column=1, padx=5, pady=2)
        self.multi_entry.insert(0, "3,1,4,2")

        # Send Buttons
        tk.Label(sender_frame, text="Step 2: Choose Security & Send", bg=B_SENDER, fg="#cbd5e1").pack(anchor="w", pady=(10,0))
        btn_caes = tk.Button(sender_frame, text="SEND: Caesar (Weak)", bg="#475569", fg="white", 
                             command=lambda: self.transmit("Caesar"), font=("Segoe UI", 10, "bold"))
        btn_caes.pack(fill="x", pady=2)
        
        btn_sub = tk.Button(sender_frame, text="SEND: Substitution (Weak)", bg="#475569", fg="white", 
                            command=lambda: self.transmit("Substitution"), font=("Segoe UI", 10, "bold"))
        btn_sub.pack(fill="x", pady=2)
        
        btn_secure = tk.Button(sender_frame, text="SEND: Hybrid Secure (Multi+Sub)", bg=C_SENDER, fg="white", 
                               command=lambda: self.transmit("Secure"), font=("Segoe UI", 10, "bold"))
        btn_secure.pack(fill="x", pady=2)

        tk.Button(sender_frame, text="View Current Sub-Key Mapping", bg="#334155", fg=C_ACCENT, 
                  command=self.show_key_mapping, font=("Segoe UI", 9, "italic")).pack(pady=10)

        # --- COLUMN 2: NETWORK / ATTACKER ---
        network_frame = tk.LabelFrame(main_container, text="🌐 [NETWORK / ATTACKER]", font=("Segoe UI", 12, "bold"),
                                      bg=B_NETWORK, fg=C_ATTACK, padx=10, pady=10)
        network_frame.grid(row=0, column=1, sticky="nsew", padx=5)

        tk.Label(network_frame, text="Intercepted Message:", bg=B_NETWORK, fg="#cbd5e1").pack(anchor="w")
        self.network_view = scrolledtext.ScrolledText(network_frame, height=5, bg="#1e293b", fg=C_ATTACK, 
                                                      font=("Consolas", 11), borderwidth=0, state="disabled")
        self.network_view.pack(fill="x", pady=5)

        # Attack Button Frame
        attack_frame = tk.Frame(network_frame, bg=B_NETWORK)
        attack_frame.pack(fill="x", pady=10)
        
        tk.Button(attack_frame, text="BRUTE FORCE ATTACK", bg=C_ATTACK, fg="white", 
                  command=self.attack_brute, font=("Segoe UI", 10, "bold")).pack(fill="x", pady=2)
        
        tk.Button(attack_frame, text="FREQUENCY ANALYSIS", bg="#be123c", fg="white", 
                  command=self.attack_freq, font=("Segoe UI", 10, "bold")).pack(fill="x", pady=2)

        tk.Label(network_frame, text="Attack Result:", bg=B_NETWORK, fg="#cbd5e1").pack(anchor="w", pady=(10,0))
        self.attack_output = scrolledtext.ScrolledText(network_frame, height=8, bg="#0f172a", fg="#94a3b8", 
                                                       font=("Consolas", 10))
        self.attack_output.pack(fill="both", expand=True)
        
        self.status_label = tk.Label(network_frame, text="Status: Waiting for data...", bg=B_NETWORK, 
                                     fg="white", font=("Segoe UI", 10, "italic"))
        self.status_label.pack(pady=5)

        # --- COLUMN 3: RECEIVER (B) ---
        receiver_frame = tk.LabelFrame(main_container, text="👤 [RECEIVER B]", font=("Segoe UI", 12, "bold"),
                                       bg=B_RECEIVER, fg=C_ACCENT, padx=10, pady=10)
        receiver_frame.grid(row=0, column=2, sticky="nsew", padx=5)

        tk.Label(receiver_frame, text="Received Ciphertext:", bg=B_RECEIVER, fg="#cbd5e1").pack(anchor="w")
        self.receiver_view = scrolledtext.ScrolledText(receiver_frame, height=5, bg="#0f172a", fg=C_ACCENT, 
                                                       font=("Consolas", 11), borderwidth=0, state="disabled")
        self.receiver_view.pack(fill="x", pady=5)

        tk.Button(receiver_frame, text="DECRYPT & REVEAL", bg=C_ACCENT, fg="white", 
                  command=self.receive_decrypt, font=("Segoe UI", 10, "bold")).pack(fill="x", pady=10)

        tk.Label(receiver_frame, text="Final Original Message:", bg=B_RECEIVER, fg="#cbd5e1").pack(anchor="w")
        self.final_output = scrolledtext.ScrolledText(receiver_frame, height=8, bg="#0f172a", fg="white", 
                                                      font=("Segoe UI", 11))
        self.final_output.pack(fill="both", expand=True)
        
        # Footer / Explanation
        footer = tk.Frame(self.root, bg=B_DARK, pady=5)
        footer.pack(fill="x")
        self.footer_text = tk.Label(footer, text="System Ready.", bg=B_DARK, fg="#94a3b8", font=("Segoe UI", 9))
        self.footer_text.pack()

    # --- SIMULATION LOGIC ---
    def transmit(self, method):
        msg = self.sender_input.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showwarning("Empty", "Please enter a message first!")
            return
            
        self.original_plaintext = msg
        self.last_used_method = method
        
        # Clear previous states
        self.update_view(self.network_view, "")
        self.update_view(self.receiver_view, "")
        self.final_output.delete("1.0", tk.END)
        self.attack_output.delete("1.0", tk.END)
        self.status_label.config(text="Status: Encrypting...", fg="#fbbf24")
        self.footer_text.config(text=f"Process: Sender A is encrypting message using {method}...")

        # Calculate Ciphertext
        ciphertext = ""
        try:
            if method == "Caesar":
                shift = int(self.shift_entry.get())
                ciphertext = cipher_logic.caesar_encrypt(msg, shift)
            elif method == "Substitution":
                self.current_sub_key = cipher_logic.generate_substitution_key()
                ciphertext = cipher_logic.substitution_encrypt(msg, self.current_sub_key)
            elif method == "Secure":
                shifts = [int(s.strip()) for s in self.multi_entry.get().split(",")]
                self.transmitted_context["shifts"] = shifts # Store for decryption
                # Multi-shift + Substitution (Hybrid)
                temp = cipher_logic.multi_shift_encrypt(msg, shifts)
                ciphertext = cipher_logic.substitution_encrypt(temp, self.current_sub_key)

            # Bundle context with the current transmission (Fixes key overwrite bug)
            self.transmitted_context["text"] = ciphertext
            self.transmitted_context["method"] = method
            self.transmitted_context["key"] = self.current_sub_key.copy() if hasattr(self.current_sub_key, "copy") else self.current_sub_key
        except Exception as e:
            messagebox.showerror("Error", f"Invalid Key Configuration: {e}")
            return

        # SIMULATE DELAY: Movement to Network
        self.root.after(800, lambda: self.show_in_network(ciphertext))

    def show_in_network(self, text):
        self.update_view(self.network_view, text)
        self.status_label.config(text="Status: INTERCEPTED ON NETWORK", fg=C_ATTACK)
        self.footer_text.config(text="Process: Message detected in transmission channel! Attacker can now see it.")
        
        # SIMULATE DELAY: Movement to Receiver
        self.root.after(1200, lambda: self.show_in_receiver(text))

    def show_in_receiver(self, text):
        self.update_view(self.receiver_view, text)
        self.footer_text.config(text="Process: Message successfully reached Receiver B.")

    def attack_brute(self):
        text = self.network_view.get("1.0", tk.END).strip()
        if not text: return
        
        self.attack_output.delete("1.0", tk.END)
        self.attack_output.insert(tk.END, "ATTACKER: Running Brute Force on Caesar assumptions...\n\n")
        
        results = cipher_logic.caesar_brute_force(text)
        found_match = False
        
        for i, (shift, dec, score) in enumerate(results[:10]):
            is_correct = dec.upper() == self.original_plaintext.upper()
            marker = " ✅ CORRECT MATCH!" if is_correct else ""
            self.attack_output.insert(tk.END, f"Shift {shift:02}: {dec[:30]}...{marker}\n")
            if is_correct: found_match = True

        if found_match:
            self.status_label.config(text="Status: ATTACK SUCCESSFUL! ❌ (Message Compromised)", fg=C_ATTACK)
            messagebox.showinfo("Attack Result", f"ATTACK SUCCESSFUL!\n\nAttacker found the original message: \n'{self.original_plaintext}'\n\nMethod: Caesar Brute Force")
        else:
            self.status_label.config(text="Status: ATTACK FAILED! ✅ (Encryption Held)", fg=C_SENDER)
            self.attack_output.insert(tk.END, "\nCRITICAL: No readable English matches found.\nTarget may be using Secure Mode.")

    def attack_freq(self):
        text = self.network_view.get("1.0", tk.END).strip()
        if not text: return
        
        freq_pct, sorted_items = cipher_logic.frequency_analysis(text)
        self.attack_output.delete("1.0", tk.END)
        self.attack_output.insert(tk.END, "ATTACKER: Performing Statistical Frequency Analysis...\n\n")
        self.attack_output.insert(tk.END, "Top Letter Frequencies Found:\n")
        
        for char, count in sorted_items[:5]:
            pct = freq_pct[char]
            self.attack_output.insert(tk.END, f"  Letter '{char}': {pct:.1f}%\n")
            
        self.attack_output.insert(tk.END, "\nATTACKER GUESS (ADVANCED):\n")
        if self.last_used_method == "Substitution":
            self.status_label.config(text="Status: CALCULATING STATISTICAL GUESS...", fg="#fbbf24")
            self.root.update() # Refresh GUI to show status
            
            # Statistical Guess (Improved Hill Climbing version)
            guess = cipher_logic.substitution_attack_solve(text)
            
            self.attack_output.insert(tk.END, "Algorithm: Hill Climbing (Bigram Fitness Analysis)\n")
            self.attack_output.insert(tk.END, f"\n[PREDICTED MESSAGE]:\n{guess}\n")
            self.attack_output.insert(tk.END, "\nNote: Accuracy increases with message length.")
            
            self.status_label.config(text="Status: ANALYSIS COMPLETE ⚠️", fg="#fbbf24")
        else:
            self.attack_output.insert(tk.END, "Data looks highly random. Frequency patterns are successfully masked.\n")
            self.status_label.config(text="Status: ATTACK FAILED! ✅", fg=C_SENDER)

    def receive_decrypt(self):
        cipher_text = self.receiver_view.get("1.0", tk.END).strip()
        if not cipher_text: return
        
        self.footer_text.config(text="Process: Receiver B is applying the shared private key...")
        
        # Simulated delay for decryption process
        self.root.after(500, lambda: self._do_decrypt(cipher_text))

    def _do_decrypt(self, text):
        try:
            # Use the context bundled with the message
            ctx_method = self.transmitted_context["method"]
            ctx_key = self.transmitted_context["key"]
            ctx_shifts = self.transmitted_context["shifts"]
            
            decrypted = ""
            if ctx_method == "Caesar":
                shift = int(self.shift_entry.get())
                decrypted = cipher_logic.caesar_decrypt(text, shift)
            elif ctx_method == "Substitution":
                decrypted = cipher_logic.substitution_decrypt(text, ctx_key)
            elif ctx_method == "Secure":
                # Reverse Hybrid: Decrypt Sub then Decrypt Multi-shift
                temp = cipher_logic.substitution_decrypt(text, ctx_key)
                neg_shifts = [-s for s in ctx_shifts]
                decrypted = cipher_logic.multi_shift_encrypt(temp, neg_shifts)
            
            self.final_output.delete("1.0", tk.END)
            self.final_output.insert(tk.END, decrypted)
            self.footer_text.config(text="Process: Message successfully decrypted by intended receiver.")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed at receiver end: {e}")

    def show_key_mapping(self):
        map_win = tk.Toplevel(self.root)
        map_win.title("Current Substitution Key Mapping")
        map_win.geometry("400x500")
        map_win.configure(bg=B_DARK)
        
        txt = scrolledtext.ScrolledText(map_win, bg=B_DARK, fg=C_ACCENT, font=("Consolas", 10))
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        
        txt.insert(tk.END, "Standard Letter -> Mapped Letter\n")
        txt.insert(tk.END, "-------------------------------\n")
        sorted_keys = sorted(self.current_sub_key.items())
        for k, v in sorted_keys:
            txt.insert(tk.END, f"      {k}         ->      {v}\n")
        txt.config(state="disabled")

    # Helpers
    def update_view(self, widget, content):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", content)
        widget.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureCommSystem(root)
    root.mainloop()
