import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from packing_utils import describe_packability

from autofill_utils import get_item_as_tuple_by_reference, load_data


class PaczkerPro(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.items = []
        self.db = load_data("example.csv")
        
        self.title("PaczkerPro")
        self.geometry("1000x600")

        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        left_frame = ttk.Frame(main_frame)
        right_frame = ttk.Frame(main_frame)

        left_frame.grid(row=0, column=0, sticky="nsew")
        right_frame.grid(row=0, column=1, sticky="nsew")

        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=6, uniform="main")
        main_frame.columnconfigure(1, weight=4, uniform="main")

        form_frame = ttk.Frame(left_frame)
        list_frame = ttk.Frame(left_frame)

        form_frame.grid(row=0, column=0, sticky="nsew")
        list_frame.grid(row=1, column=0, sticky="nsew")

        left_frame.rowconfigure(0, weight=0)
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)

        self.ref_var = tk.StringVar()
        self.ref_var.trace_add('write', self.on_ref_change)

        ref_label = ttk.Label(form_frame, text="Reference:")
        self.ref_entry = ttk.Entry(form_frame, textvariable=self.ref_var)

        ref_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ref_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        form_frame.columnconfigure(0, weight=0)
        form_frame.columnconfigure(1, weight=1)

        dim1_label = ttk.Label(form_frame, text="X1 [cm]:")
        self.dim1_entry = ttk.Entry(form_frame)

        dim2_label = ttk.Label(form_frame, text="X2 [cm]:")
        self.dim2_entry = ttk.Entry(form_frame)

        dim3_label = ttk.Label(form_frame, text="X3 [cm]:")
        self.dim3_entry = ttk.Entry(form_frame)

        weight_label = ttk.Label(form_frame, text="Weight [kg]:")
        self.weight_entry = ttk.Entry(form_frame)

        dim1_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.dim1_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        dim2_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.dim2_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        dim3_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.dim3_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        weight_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.weight_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.quantity_var = tk.StringVar(value="1")
        quantity_label = ttk.Label(form_frame, text="Qty:")
        quantity_frame = ttk.Frame(form_frame)
        quantity_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        quantity_frame.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        minus_button = ttk.Button(quantity_frame, text="-", command=self.decrement_quantity)
        
        quantity_display_label = ttk.Label(
            quantity_frame, 
            textvariable=self.quantity_var, 
            width=4,
            anchor="center"
        )
        
        plus_button = ttk.Button(quantity_frame, text="+", command=self.increment_quantity)
        
        minus_button.grid(row=0, column=0, sticky="w")
        quantity_display_label.grid(row=0, column=1, padx=5)
        plus_button.grid(row=0, column=2, sticky="w")

        add_button = ttk.Button(
            form_frame, 
            text="Add item to the list", 
            command=self.add_item
        )
        add_button.grid(row=6, column=1, padx=5, pady=10, sticky="e")

        columns = ('Ref', 'Dim1', 'Dim2', 'Dim3', 'Weight')
        
        self.tree = ttk.Treeview(
            list_frame, 
            columns=columns, 
            show='headings'
        )

        scrollbar = ttk.Scrollbar(
            list_frame, 
            orient=tk.VERTICAL, 
            command=self.tree.yview
        )
        
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.heading('Ref', text='Reference')
        self.tree.column('Ref', width=150)
        
        self.tree.heading('Dim1', text='x1')
        self.tree.column('Dim1', width=50, anchor="center")
        
        self.tree.heading('Dim2', text='x2')
        self.tree.column('Dim2', width=50, anchor="center")
        
        self.tree.heading('Dim3', text='x3')
        self.tree.column('Dim3', width=50, anchor="center")
        
        self.tree.heading('Weight', text='Weight')
        self.tree.column('Weight', width=50, anchor="center")

        delete_button = ttk.Button(
            list_frame, 
            text="Delete selected", 
            command=self.delete_item
        )

        delete_all_button = ttk.Button(
            list_frame, 
            text="Delete all", 
            command=self.delete_all_items
        )
        
        self.tree.grid(row=0, column=0, columnspan=2, sticky='nsew')
        scrollbar.grid(row=0, column=2, sticky='ns')
        delete_button.grid(row=1, column=0, pady=5, sticky="w", padx=5)
        delete_all_button.grid(row=1, column=1, pady=5, columnspan=2, sticky="e", padx=5)
        
        
        list_frame.rowconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=0)
        list_frame.columnconfigure(0, weight=1)
        list_frame.columnconfigure(1, weight=1)
        list_frame.columnconfigure(2, weight=0)

        self.output_text = tk.Text(
            right_frame, 
            state='disabled', 
            wrap='word',
            font=("Helvetica", 10)
        )

        output_scrollbar = ttk.Scrollbar(
            right_frame, 
            orient=tk.VERTICAL, 
            command=self.output_text.yview
        )

        self.output_text.configure(yscrollcommand=output_scrollbar.set)

        self.output_text.grid(row=0, column=0, sticky='nsew')
        output_scrollbar.grid(row=0, column=1, sticky='ns')

        right_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.columnconfigure(1, weight=0)

        self.update_list()


    def increment_quantity(self):
        """
        Increments quantity.
        """
        self.quantity_var.set(str(int(self.quantity_var.get()) + 1))


    def decrement_quantity(self):
        """
        Decrement quantity.
        """
        current_qty = int(self.quantity_var.get())
        if current_qty > 1:
            self.quantity_var.set(current_qty - 1)


    def on_ref_change(self, var, index, mode):
        """
        Checks if given reference is present in csv file and autofills dimensions if so.
        """
        item_as_tuple = get_item_as_tuple_by_reference(self.db, self.ref_var.get())
        if item_as_tuple:
            self.fill_form(*item_as_tuple, including_ref=False)
        else:
            self.clear_form(including_ref=False)

    def add_item(self):
        """ 
        Adds item to the list.
        """
        ref = str(self.ref_entry.get())
        if not ref:
            messagebox.showerror(title="Input error", message="No Reference.")
            return

        try:
            dim1 = float(self.dim1_entry.get().replace(',', '.'))
            dim2 = float(self.dim2_entry.get().replace(',', '.'))
            dim3 = float(self.dim3_entry.get().replace(',', '.'))
            weight = float(self.weight_entry.get().replace(',', '.'))
            qty = int(self.quantity_var.get())
        
        except ValueError:
            messagebox.showerror(title="Input error", message="One of number fileds was filled incorrectly.")
            return

        item_as_tuple = (ref, dim1, dim2, dim3, weight)
        for _ in range(qty): self.items.append(item_as_tuple)

        self.clear_form()
        self.update_list()

    
    def fill_form(self, ref, dim1, dim2, dim3, weight, including_ref = False):
        """
        Fills form with given data.
        """
        self.clear_form(including_ref=including_ref)
        if including_ref: self.ref_entry.insert(0, ref)
        self.dim1_entry.insert(0, dim1)
        self.dim2_entry.insert(0, dim2)
        self.dim3_entry.insert(0, dim3)
        self.weight_entry.insert(0, weight)


    def clear_form(self, including_ref = True):
        """ 
        Clears all form's entry widgets. 
        """
        if including_ref: self.ref_entry.delete(0, 'end')
        self.dim1_entry.delete(0, 'end')
        self.dim2_entry.delete(0, 'end')
        self.dim3_entry.delete(0, 'end')
        self.weight_entry.delete(0, 'end')
        self.quantity_var.set("1")

    
    def update_list(self):
        """ 
        Updates list widget with self.items content 
        and calls self.update_output.
        """
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item_tuple in self.items:
            self.tree.insert('', 'end', values=item_tuple)

        self.update_output()

    
    def delete_item(self):
        """ 
        Deletes selected items from self.items. 
        Calls self.update_list(). 
        """
        ids = self.tree.selection()

        if not ids:
            messagebox.showerror(title="Selection error", message="Nothing was selected.")

        for id in ids:

            try:

                item_as_tuple_str = tuple(self.tree.item(id, 'values'))

                ref = str(item_as_tuple_str[0])
                dim1 = float(item_as_tuple_str[1])
                dim2 = float(item_as_tuple_str[2])
                dim3 = float(item_as_tuple_str[3])
                weight = float(item_as_tuple_str[4])
                item_as_tuple = (ref, dim1, dim2, dim3, weight)

                self.items.remove(item_as_tuple)

            except Exception as e:
                messagebox.showerror(title="Deletion error", message=f"ERROR: {e}")

        self.update_list()

    def delete_all_items(self):
        """
        Deletes all items. 
        """
        self.items.clear()
        self.update_list()

    
    def update_output(self):
        """ 
        Updates packability description. 
        """
        if not self.items:
            output_string = "No items added..."
        else:
            output_string = describe_packability(self.items)

        self.output_text.config(state='normal')
        self.output_text.delete('1.0', 'end')
        self.output_text.insert('1.0', output_string)
        self.output_text.config(state='disabled')
        

if __name__ == "__main__":

    app = PaczkerPro()

    app.mainloop()
