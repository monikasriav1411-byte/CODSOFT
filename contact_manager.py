import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import re

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("📱 Contact Manager")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # Modern color scheme
        self.bg_color = "#f5f6fa"
        self.primary_color = "#5f27cd"
        self.secondary_color = "#341f97"
        self.accent_color = "#00d2d3"
        self.success_color = "#10ac84"
        self.danger_color = "#ee5a6f"
        self.card_bg = "#ffffff"
        self.text_dark = "#2c3e50"
        self.text_light = "#7f8c8d"
        
        # Load contacts
        self.contacts = self.load_contacts()
        self.selected_index = None
        
        self.setup_ui()
        self.refresh_table()
        
    def setup_ui(self):
        # Configure root background
        self.root.config(bg=self.bg_color)
        
        # ==================== HEADER ====================
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=90)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_font = font.Font(family="Segoe UI", size=28, weight="bold")
        subtitle_font = font.Font(family="Segoe UI", size=11)
        
        tk.Label(header_frame, text="📱 Contact Manager", 
                font=title_font, bg=self.primary_color, 
                fg="white").pack(pady=(15, 0))
        
        tk.Label(header_frame, text="Manage your contacts efficiently", 
                font=subtitle_font, bg=self.primary_color, 
                fg="#e0e0e0").pack()
        
        # ==================== MAIN CONTAINER ====================
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=25, pady=20)
        
        # ==================== TOP SECTION - FORM ====================
        form_card = tk.Frame(main_container, bg=self.card_bg, relief="flat", bd=0)
        form_card.pack(fill="x", pady=(0, 20))
        
        # Add subtle shadow effect
        shadow = tk.Frame(main_container, bg="#d0d0d0", height=2)
        shadow.place(x=25, y=185, width=950)
        
        # Form header
        form_header = tk.Frame(form_card, bg=self.secondary_color, height=50)
        form_header.pack(fill="x")
        form_header.pack_propagate(False)
        
        tk.Label(form_header, text="✏️ Contact Information", 
                font=("Segoe UI", 14, "bold"),
                bg=self.secondary_color, fg="white").pack(side="left", padx=20)
        
        # Form content
        form_content = tk.Frame(form_card, bg=self.card_bg)
        form_content.pack(fill="x", padx=20, pady=20)
        
        # Row 1: Name and Phone
        row1 = tk.Frame(form_content, bg=self.card_bg)
        row1.pack(fill="x", pady=(0, 15))
        
        self.create_labeled_entry(row1, "Full Name *", "name_entry", width=35)
        self.create_labeled_entry(row1, "Phone Number *", "phone_entry", width=25)
        
        # Row 2: Email and Address
        row2 = tk.Frame(form_content, bg=self.card_bg)
        row2.pack(fill="x", pady=(0, 15))
        
        self.create_labeled_entry(row2, "Email Address", "email_entry", width=35)
        
        # Address field
        addr_container = tk.Frame(row2, bg=self.card_bg)
        addr_container.pack(side="left", padx=10)
        
        tk.Label(addr_container, text="Full Address", 
                font=("Segoe UI", 10, "bold"),
                bg=self.card_bg, fg=self.text_dark).pack(anchor="w", pady=(0, 5))
        
        self.address_entry = tk.Entry(addr_container, 
                                     font=("Segoe UI", 10),
                                     relief="solid", bd=1, width=50)
        self.address_entry.pack()
        
        # Button row
        button_frame = tk.Frame(form_content, bg=self.card_bg)
        button_frame.pack(fill="x", pady=(10, 0))
        
        button_container = tk.Frame(button_frame, bg=self.card_bg)
        button_container.pack()
        
        self.add_btn = self.create_modern_button(button_container, "➕ Add Contact", 
                                                 self.success_color, self.add_contact)
        self.add_btn.pack(side="left", padx=5)
        
        self.update_btn = self.create_modern_button(button_container, "✏️ Update", 
                                                    self.accent_color, self.update_contact)
        self.update_btn.pack(side="left", padx=5)
        
        self.delete_btn = self.create_modern_button(button_container, "🗑️ Delete", 
                                                    self.danger_color, self.delete_contact)
        self.delete_btn.pack(side="left", padx=5)
        
        self.clear_btn = self.create_modern_button(button_container, "🔄 Clear Form", 
                                                   self.text_light, self.clear_form)
        self.clear_btn.pack(side="left", padx=5)
        
        # Initially disable update and delete
        self.update_btn.config(state="disabled")
        self.delete_btn.config(state="disabled")
        
        # ==================== BOTTOM SECTION - TABLE ====================
        table_card = tk.Frame(main_container, bg=self.card_bg, relief="flat", bd=0)
        table_card.pack(fill="both", expand=True)
        
        # Table header
        table_header = tk.Frame(table_card, bg=self.secondary_color, height=50)
        table_header.pack(fill="x")
        table_header.pack_propagate(False)
        
        header_left = tk.Frame(table_header, bg=self.secondary_color)
        header_left.pack(side="left", fill="y")
        
        tk.Label(header_left, text="📋 Contact List", 
                font=("Segoe UI", 14, "bold"),
                bg=self.secondary_color, fg="white").pack(side="left", padx=20, pady=10)
        
        self.count_label = tk.Label(header_left, text="(0 contacts)", 
                                    font=("Segoe UI", 10),
                                    bg=self.secondary_color, fg="#e0e0e0")
        self.count_label.pack(side="left")
        
        # Search box in header
        search_frame = tk.Frame(table_header, bg=self.secondary_color)
        search_frame.pack(side="right", padx=20)
        
        tk.Label(search_frame, text="🔍", font=("Segoe UI", 14),
                bg=self.secondary_color, fg="white").pack(side="left", padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.search_contacts())
        
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                     font=("Segoe UI", 10), relief="solid", 
                                     bd=1, width=25)
        self.search_entry.pack(side="left")
        
        # Table with Treeview
        table_container = tk.Frame(table_card, bg=self.card_bg)
        table_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Configure Treeview style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Contact.Treeview",
                       background=self.card_bg,
                       foreground=self.text_dark,
                       rowheight=35,
                       fieldbackground=self.card_bg,
                       borderwidth=0,
                       font=("Segoe UI", 10))
        style.map("Contact.Treeview",
                 background=[("selected", self.accent_color)])
        
        style.configure("Contact.Treeview.Heading",
                       background=self.primary_color,
                       foreground="white",
                       relief="flat",
                       font=("Segoe UI", 11, "bold"))
        style.map("Contact.Treeview.Heading",
                 background=[("active", self.secondary_color)])
        
        # Create Treeview
        columns = ("Name", "Phone", "Email", "Address")
        self.tree = ttk.Treeview(table_container, columns=columns, 
                                show="headings", style="Contact.Treeview",
                                selectmode="browse")
        
        # Define headings
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone Number")
        self.tree.heading("Email", text="Email Address")
        self.tree.heading("Address", text="Address")
        
        # Define column widths
        self.tree.column("Name", width=200, anchor="w")
        self.tree.column("Phone", width=150, anchor="w")
        self.tree.column("Email", width=250, anchor="w")
        self.tree.column("Address", width=300, anchor="w")
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_container, orient="vertical", 
                           command=self.tree.yview)
        hsb = ttk.Scrollbar(table_container, orient="horizontal", 
                           command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
    def create_labeled_entry(self, parent, label_text, attr_name, width=30):
        container = tk.Frame(parent, bg=self.card_bg)
        container.pack(side="left", padx=10)
        
        label = tk.Label(container, text=label_text, 
                        font=("Segoe UI", 10, "bold"),
                        bg=self.card_bg, fg=self.text_dark)
        label.pack(anchor="w", pady=(0, 5))
        
        entry = tk.Entry(container, font=("Segoe UI", 10),
                        relief="solid", bd=1, width=width)
        entry.pack()
        
        setattr(self, attr_name, entry)
    
    def create_modern_button(self, parent, text, color, command):
        btn = tk.Button(parent, text=text, font=("Segoe UI", 10, "bold"),
                       bg=color, fg="white", relief="flat", cursor="hand2",
                       command=command, bd=0, padx=20, pady=10,
                       activebackground=color, activeforeground="white")
        
        # Hover effects
        btn.bind("<Enter>", lambda e, b=btn, c=color: self.on_button_hover(b, c, True))
        btn.bind("<Leave>", lambda e, b=btn, c=color: self.on_button_hover(b, c, False))
        
        return btn
    
    def on_button_hover(self, button, color, entering):
        if button["state"] == "disabled":
            return
        
        if entering:
            rgb = self.hex_to_rgb(color)
            new_rgb = tuple(min(255, c + 20) for c in rgb)
            new_color = f'#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}'
            button.config(bg=new_color)
        else:
            button.config(bg=color)
    
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def refresh_table(self):
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add contacts
        for contact in self.contacts:
            self.tree.insert("", "end", values=(
                contact["name"],
                contact["phone"],
                contact["email"],
                contact["address"]
            ))
        
        # Update count
        self.count_label.config(text=f"({len(self.contacts)} contacts)")
    
    def on_tree_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        item = selected_items[0]
        values = self.tree.item(item, "values")
        
        # Find contact by phone (unique identifier)
        for idx, contact in enumerate(self.contacts):
            if contact["phone"] == values[1]:
                self.selected_index = idx
                self.populate_form(contact)
                break
    
    def populate_form(self, contact):
        # Clear and fill form
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, contact["name"])
        
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, contact["phone"])
        
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, contact["email"])
        
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, contact["address"])
        
        # Enable update and delete buttons
        self.update_btn.config(state="normal")
        self.delete_btn.config(state="normal")
    
    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()
        
        # Validation
        if not name or not phone:
            messagebox.showwarning("Required Fields", 
                                 "Name and Phone Number are required!")
            return
        
        if not self.validate_phone(phone):
            messagebox.showwarning("Invalid Phone", 
                                 "Please enter a valid phone number (10+ digits)!")
            return
        
        if email and not self.validate_email(email):
            messagebox.showwarning("Invalid Email", 
                                 "Please enter a valid email address!")
            return
        
        # Check duplicate
        for contact in self.contacts:
            if contact["phone"] == phone:
                messagebox.showwarning("Duplicate Contact", 
                                     "A contact with this phone number already exists!")
                return
        
        # Add contact
        new_contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }
        
        self.contacts.append(new_contact)
        self.save_contacts()
        self.refresh_table()
        self.clear_form()
        
        messagebox.showinfo("Success", 
                          f"Contact '{name}' added successfully!")
    
    def update_contact(self):
        if self.selected_index is None:
            messagebox.showwarning("No Selection", 
                                 "Please select a contact to update!")
            return
        
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()
        
        # Validation
        if not name or not phone:
            messagebox.showwarning("Required Fields", 
                                 "Name and Phone Number are required!")
            return
        
        if not self.validate_phone(phone):
            messagebox.showwarning("Invalid Phone", 
                                 "Please enter a valid phone number!")
            return
        
        if email and not self.validate_email(email):
            messagebox.showwarning("Invalid Email", 
                                 "Please enter a valid email address!")
            return
        
        # Update contact
        self.contacts[self.selected_index] = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }
        
        self.save_contacts()
        self.refresh_table()
        self.clear_form()
        
        messagebox.showinfo("Success", 
                          f"Contact '{name}' updated successfully!")
    
    def delete_contact(self):
        if self.selected_index is None:
            messagebox.showwarning("No Selection", 
                                 "Please select a contact to delete!")
            return
        
        contact_name = self.contacts[self.selected_index]["name"]
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{contact_name}'?"):
            self.contacts.pop(self.selected_index)
            self.save_contacts()
            self.refresh_table()
            self.clear_form()
            
            messagebox.showinfo("Success", 
                              f"Contact '{contact_name}' deleted successfully!")
    
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        
        self.selected_index = None
        self.update_btn.config(state="disabled")
        self.delete_btn.config(state="disabled")
        
        # Clear tree selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)
    
    def search_contacts(self):
        search_term = self.search_var.get().lower().strip()
        
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filter and display
        filtered = [c for c in self.contacts 
                   if search_term in c["name"].lower() 
                   or search_term in c["phone"]
                   or search_term in c["email"].lower()]
        
        for contact in filtered:
            self.tree.insert("", "end", values=(
                contact["name"],
                contact["phone"],
                contact["email"],
                contact["address"]
            ))
        
        # Update count
        self.count_label.config(text=f"({len(filtered)} contacts)")
    
    def validate_phone(self, phone):
        # Remove spaces and common separators
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        # Check if it's all digits and at least 10 characters
        return cleaned.isdigit() and len(cleaned) >= 10
    
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def load_contacts(self):
        try:
            with open("contacts.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_contacts(self):
        with open("contacts.json", "w") as f:
            json.dump(self.contacts, f, indent=2)

def main():
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()