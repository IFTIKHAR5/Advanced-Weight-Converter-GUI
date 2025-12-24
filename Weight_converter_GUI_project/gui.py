# #  # gui.py
# """
# GUI components for the weight converter
# """
# import tkinter as tk
# from tkinter import ttk, scrolledtext
# import json
# import os

# # Import from local modules
# from converter import WeightConverter, UNIT_NAMES, CONVERSION_FACTORS
# from utils import (
#     validate_positive_number, show_error, show_info, 
#     copy_to_clipboard, create_tooltip
# )

# class WeightConverterApp:
#     """Main application class"""
    
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Advanced Weight Converter")
#         self.root.geometry("700x630")  # Further reduced height since status bar removed
#         self.root.minsize(600, 530)
        
#         # Initialize StringVars BEFORE creating widgets
#         self.input_value = tk.StringVar(value="1")
#         self.input_unit = tk.StringVar(value='kg')
        
#         # Initialize converter
#         self.converter = WeightConverter()
        
#         # Configuration - KEEP decimal places but no dropdown
#         self.decimal_places = 3  # Fixed to 3 decimal places
        
#         # Load saved settings
#         self.load_settings()
        
#         # Setup GUI
#         self.setup_styles()
#         self.create_widgets()
#         self.setup_bindings()
        
#         # Set initial focus
#         self.value_entry.focus()
#         self.value_entry.select_range(0, tk.END)
    
#     def setup_styles(self):
#         """Configure ttk styles"""
#         self.style = ttk.Style()
#         self.style.theme_use('clam')
        
#         # Configure button colors
#         self.style.configure('Convert.TButton', foreground='white', background='#4CAF50', font=('Arial', 10, 'bold'))
#         self.style.map('Convert.TButton', background=[('active', '#45a049')])
        
#         self.style.configure('Clear.TButton', foreground='white', background='#f44336')
#         self.style.map('Clear.TButton', background=[('active', '#da190b')])
        
#         # Configure Notebook style
#         self.style.configure('TNotebook', background='#f0f0f0')
#         self.style.configure('TNotebook.Tab', padding=[10, 5])
    
#     def create_widgets(self):
#         """Create all GUI widgets"""
#         # Create main container with padding
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
#         # Configure grid weights
#         self.root.columnconfigure(0, weight=1)
#         self.root.rowconfigure(0, weight=1)
#         main_frame.columnconfigure(1, weight=1)
        
#         # Title
#         title_label = ttk.Label(main_frame, text="Advanced Weight Converter", 
#                                font=('Arial', 16, 'bold'))
#         title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
#         # Input Section
#         input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
#         input_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
#         input_frame.columnconfigure(1, weight=1)
        
#         # Value input
#         ttk.Label(input_frame, text="Value:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
#         self.value_entry = ttk.Entry(input_frame, textvariable=self.input_value, width=20)
#         self.value_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
#         # Input unit selection
#         ttk.Label(input_frame, text="Convert from:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
#         self.input_combobox = ttk.Combobox(input_frame, textvariable=self.input_unit, 
#                                           values=list(UNIT_NAMES.keys()), 
#                                           state='readonly', width=15)
#         self.input_combobox.grid(row=0, column=3, sticky=tk.W)
        
#         # Output unit selection
#         output_frame = ttk.LabelFrame(main_frame, text="Output Units", padding="10")
#         output_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
#         # Create checkboxes for output units
#         self.output_unit_vars = {}
#         checkboxes_frame = ttk.Frame(output_frame)
#         checkboxes_frame.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E))
        
#         units = list(UNIT_NAMES.items())
#         half = len(units) // 2
        
#         # Left column
#         for i, (unit_code, unit_name) in enumerate(units[:half]):
#             var = tk.BooleanVar(value=True)
#             self.output_unit_vars[unit_code] = var
#             cb = ttk.Checkbutton(checkboxes_frame, text=f"{unit_name} ({unit_code})",
#                                 variable=var)
#             cb.grid(row=i, column=0, sticky=tk.W, padx=(0, 20))
        
#         # Right column
#         for i, (unit_code, unit_name) in enumerate(units[half:]):
#             var = tk.BooleanVar(value=True)
#             self.output_unit_vars[unit_code] = var
#             cb = ttk.Checkbutton(checkboxes_frame, text=f"{unit_name} ({unit_code})",
#                                 variable=var)
#             cb.grid(row=i, column=1, sticky=tk.W)
        
#         # Selection buttons
#         selection_buttons = ttk.Frame(output_frame)
#         selection_buttons.grid(row=1, column=0, columnspan=4, pady=(10, 0))
        
#         ttk.Button(selection_buttons, text="Select All", 
#                   command=self.select_all_units).pack(side=tk.LEFT, padx=2)
#         ttk.Button(selection_buttons, text="Deselect All", 
#                   command=self.deselect_all_units).pack(side=tk.LEFT, padx=2)
#         ttk.Button(selection_buttons, text="Common Units", 
#                   command=self.select_common_units).pack(side=tk.LEFT, padx=2)
        
#         # Create Notebook for Results and History tabs
#         self.notebook = ttk.Notebook(main_frame)
#         self.notebook.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
#         # Results Tab
#         results_tab = ttk.Frame(self.notebook, padding="5")
#         self.notebook.add(results_tab, text="Results")
        
#         # Results text widget with scrollbar
#         self.results_text = scrolledtext.ScrolledText(results_tab, font=('Courier', 10), height=10)
#         self.results_text.pack(fill=tk.BOTH, expand=True)
#         self.results_text.config(state=tk.DISABLED)
        
#         # History Tab
#         history_tab = ttk.Frame(self.notebook, padding="5")
#         self.notebook.add(history_tab, text="History")
        
#         # History text widget
#         self.history_text = scrolledtext.ScrolledText(history_tab, font=('Courier', 9), height=8)
#         self.history_text.pack(fill=tk.BOTH, expand=True)
#         self.history_text.config(state=tk.DISABLED)
        
#         # History control buttons
#         history_buttons = ttk.Frame(history_tab)
#         history_buttons.pack(fill=tk.X, pady=(5, 0))
#         ttk.Button(history_buttons, text="Clear History", command=self.clear_history).pack(side=tk.LEFT, padx=5)
        
#         # Control buttons - CONVERT BUTTON IS HERE
#         buttons_frame = ttk.Frame(main_frame)
#         buttons_frame.grid(row=4, column=0, columnspan=4, pady=(15, 0))
        
#         # CONVERT BUTTON (GREEN)
#         self.convert_btn = ttk.Button(buttons_frame, text="Convert", style='Convert.TButton',
#                                      command=self.perform_conversion, width=12)
#         self.convert_btn.pack(side=tk.LEFT, padx=5)
        
#         # CLEAR BUTTON (RED)
#         ttk.Button(buttons_frame, text="Clear", style='Clear.TButton',
#                   command=self.clear_form, width=10).pack(side=tk.LEFT, padx=5)
        
#         # COPY BUTTON
#         ttk.Button(buttons_frame, text="Copy Results",
#                   command=self.copy_results, width=12).pack(side=tk.LEFT, padx=5)
        
#         # NO STATUS BAR - COMPLETELY REMOVED
        
#         # Add initial messages
#         self.results_text.config(state=tk.NORMAL)
#         self.results_text.insert(tk.END, "Enter a value, select units, and click 'Convert'")
#         self.results_text.config(state=tk.DISABLED)
        
#         self.history_text.config(state=tk.NORMAL)
#         self.history_text.insert(tk.END, "Conversion history will appear here")
#         self.history_text.config(state=tk.DISABLED)
    
#     def setup_bindings(self):
#         """Set up keyboard bindings"""
#         # Bind Enter key to perform conversion
#         self.root.bind('<Return>', lambda e: self.perform_conversion())
#         self.root.bind('<Escape>', lambda e: self.clear_form())
#         self.root.bind('<Control-c>', lambda e: self.copy_results())
        
#         # Bind focus events
#         self.value_entry.bind('<FocusIn>', lambda e: self.value_entry.select_range(0, tk.END))
    
#     def perform_conversion(self):
#         """Perform conversion and update results - CALLED BY CONVERT BUTTON"""
#         # Get input value
#         input_str = self.input_value.get().strip()
        
#         # Clear previous results
#         self.results_text.config(state=tk.NORMAL)
#         self.results_text.delete(1.0, tk.END)
        
#         # Validate input
#         if not input_str:
#             self.results_text.insert(tk.END, "Please enter a value to convert")
#             self.results_text.config(state=tk.DISABLED)
#             return
        
#         if not validate_positive_number(input_str):
#             self.results_text.insert(tk.END, "Error: Please enter a valid positive number")
#             self.results_text.config(state=tk.DISABLED)
#             return
        
#         try:
#             value = float(input_str)
#             from_unit = self.input_unit.get()
            
#             # Get selected output units
#             selected_units = [unit for unit, var in self.output_unit_vars.items() 
#                             if var.get() and unit != from_unit]
            
#             if not selected_units:
#                 self.results_text.insert(tk.END, "No output units selected")
#                 self.results_text.config(state=tk.DISABLED)
#                 return
            
#             # Perform conversions
#             results = {}
#             for unit in selected_units:
#                 try:
#                     converted = self.converter.convert(value, from_unit, unit)
#                     results[unit] = converted
#                 except Exception as e:
#                     results[unit] = str(e)
            
#             # Display results
#             self.display_results(value, from_unit, results)
            
#             # Automatically add to history
#             self.add_to_history(value, from_unit, results)
            
#         except Exception as e:
#             self.results_text.insert(tk.END, f"Error: {str(e)}")
#             self.results_text.config(state=tk.DISABLED)
    
#     def display_results(self, value: float, from_unit: str, results: dict):
#         """Display conversion results"""
#         self.results_text.config(state=tk.NORMAL)
#         self.results_text.delete(1.0, tk.END)
        
#         # Display input value
#         input_unit_name = UNIT_NAMES.get(from_unit, from_unit)
#         self.results_text.insert(tk.END, f"Converting {value} {input_unit_name}:\n")
#         self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        
#         # Display results
#         for unit, result in sorted(results.items()):
#             if isinstance(result, (int, float)):
#                 formatted = self.converter.format_result(result, unit, self.decimal_places)
#                 unit_name = UNIT_NAMES.get(unit, unit)
#                 self.results_text.insert(tk.END, f"  • {unit_name.ljust(20)}: {formatted}\n")
#             else:
#                 unit_name = UNIT_NAMES.get(unit, unit)
#                 self.results_text.insert(tk.END, f"  • {unit_name.ljust(20)}: Error - {result}\n", 'error')
        
#         self.results_text.config(state=tk.DISABLED)
#         self.results_text.tag_config('error', foreground='red')
    
#     def clear_form(self):
#         """Clear the input form"""
#         self.input_value.set("1")
#         self.input_unit.set('kg')
#         self.results_text.config(state=tk.NORMAL)
#         self.results_text.delete(1.0, tk.END)
#         self.results_text.insert(tk.END, "Enter a value, select units, and click 'Convert'")
#         self.results_text.config(state=tk.DISABLED)
#         self.value_entry.focus()
#         self.value_entry.select_range(0, tk.END)
    
#     def copy_results(self):
#         """Copy results to clipboard"""
#         text = self.results_text.get(1.0, tk.END).strip()
#         if text and not text.startswith("Please enter") and not text.startswith("Error:") and not text.startswith("Enter a value"):
#             copy_to_clipboard(text, self.root)
#             show_info("Results copied to clipboard!", self.root)
#         else:
#             show_error("No valid results to copy", self.root)
    
#     def add_to_history(self, value: float, from_unit: str, results: dict):
#         """Add current conversion to history automatically"""
#         valid_results = {}
#         for unit, result in results.items():
#             if isinstance(result, (int, float)):
#                 valid_results[unit] = result
        
#         if valid_results:
#             self.converter.add_to_history(value, from_unit, valid_results)
#             self.update_history_display()
    
#     def update_history_display(self):
#         """Update the history display"""
#         history = self.converter.get_history()
#         self.history_text.config(state=tk.NORMAL)
#         self.history_text.delete(1.0, tk.END)
        
#         if not history:
#             self.history_text.insert(tk.END, "No conversion history yet.")
#         else:
#             for i, entry in enumerate(history, 1):
#                 timestamp = entry['timestamp']
#                 value = entry['value']
#                 from_unit = entry['from_unit']
#                 from_unit_name = UNIT_NAMES.get(from_unit, from_unit)
                
#                 self.history_text.insert(tk.END, f"{i}. [{timestamp}]\n")
#                 self.history_text.insert(tk.END, f"   {value} {from_unit_name} →\n")
                
#                 count = 0
#                 for unit, result in entry['results'].items():
#                     if count < 5:
#                         if isinstance(result, (int, float)):
#                             formatted = self.converter.format_result(result, unit, 3)
#                             unit_name = UNIT_NAMES.get(unit, unit)
#                             self.history_text.insert(tk.END, f"     {unit_name}: {formatted}\n")
#                             count += 1
                
#                 if len(entry['results']) > 5:
#                     remaining = len(entry['results']) - 5
#                     self.history_text.insert(tk.END, f"     ... and {remaining} more\n")
                
#                 self.history_text.insert(tk.END, "-" * 50 + "\n")
        
#         self.history_text.config(state=tk.DISABLED)
    
#     def clear_history(self):
#         """Clear conversion history"""
#         self.converter.clear_history()
#         self.update_history_display()
    
#     def select_all_units(self):
#         """Select all output units"""
#         for var in self.output_unit_vars.values():
#             var.set(True)
    
#     def deselect_all_units(self):
#         """Deselect all output units"""
#         for var in self.output_unit_vars.values():
#             var.set(False)
    
#     def select_common_units(self):
#         """Select common weight units"""
#         common_units = ['kg', 'g', 'lb', 'oz', 't', 'st']
#         for unit, var in self.output_unit_vars.items():
#             var.set(unit in common_units)
    
#     def save_settings(self):
#         """Save application settings"""
#         settings = {
#             'selected_units': {unit: var.get() for unit, var in self.output_unit_vars.items()}
#         }
        
#         try:
#             with open('converter_settings.json', 'w') as f:
#                 json.dump(settings, f)
#         except:
#             pass
    
#     def load_settings(self):
#         """Load application settings"""
#         try:
#             if os.path.exists('converter_settings.json'):
#                 with open('converter_settings.json', 'r') as f:
#                     settings = json.load(f)
                
#                 saved_units = settings.get('selected_units', {})
#                 for unit, selected in saved_units.items():
#                     if unit in self.output_unit_vars:
#                         self.output_unit_vars[unit].set(selected)
#         except:
#             pass     



# gui.py - CLEAN MODERN VERSION
"""
GUI components for the weight converter - Clean Modern Design
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import os

# Import from local modules
from converter import WeightConverter, UNIT_NAMES, CONVERSION_FACTORS
from utils import (
    validate_positive_number, show_error, show_info, 
    copy_to_clipboard
)

class WeightConverterApp:
    """Main application class with clean modern UI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Weight Converter")
        self.root.geometry("750x700")  # Adjusted size to prevent overflow
        self.root.minsize(700, 600)
        
        # Set window background
        self.root.configure(bg='#f8f9fa')
        
        # Color scheme
        self.colors = {
            'primary': '#3498db',      # Blue
            'secondary': '#2ecc71',    # Green
            'accent': '#e74c3c',       # Red
            'dark': '#2c3e50',         # Dark blue
            'light': '#ecf0f1',        # Light gray
            'background': '#f8f9fa',   # Off-white
            'card': '#ffffff',         # White cards
            'text': '#2c3e50',         # Dark text
            'border': '#dfe6e9'        # Light border
        }
        
        # Initialize StringVars
        self.input_value = tk.StringVar(value="1")
        self.input_unit = tk.StringVar(value='kg')
        
        # Initialize converter
        self.converter = WeightConverter()
        
        # Configuration
        self.decimal_places = 3
        
        # Load saved settings
        self.load_settings()
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.setup_bindings()
        
        # Set initial focus
        self.value_entry.focus()
        self.value_entry.select_range(0, tk.END)
    
    def setup_styles(self):
        """Configure modern ttk styles"""
        self.style = ttk.Style()
        
        # Use 'clam' theme for better styling control
        self.style.theme_use('clam')
        
        # Configure colors
        self.style.configure('Title.TLabel', 
                           font=('Arial', 18, 'bold'),
                           foreground=self.colors['dark'],
                           background=self.colors['background'])
        
        self.style.configure('Card.TLabelframe',
                           background=self.colors['card'],
                           foreground=self.colors['dark'],
                           relief='flat',
                           borderwidth=2)
        
        self.style.configure('Card.TLabelframe.Label',
                           font=('Arial', 10, 'bold'),
                           foreground=self.colors['primary'],
                           background=self.colors['card'])
        
        self.style.configure('Input.TLabel',
                           font=('Arial', 9),
                           foreground=self.colors['text'],
                           background=self.colors['card'])
        
        self.style.configure('Convert.TButton',
                           font=('Arial', 10, 'bold'),
                           foreground='white',
                           background=self.colors['secondary'],
                           borderwidth=0,
                           padding=8)
        self.style.map('Convert.TButton',
                      background=[('active', '#27ae60')])
        
        self.style.configure('Clear.TButton',
                           font=('Arial', 10),
                           foreground='white',
                           background=self.colors['accent'],
                           borderwidth=0,
                           padding=8)
        self.style.map('Clear.TButton',
                      background=[('active', '#c0392b')])
        
        self.style.configure('Action.TButton',
                           font=('Arial', 9),
                           foreground=self.colors['primary'],
                           background=self.colors['light'],
                           borderwidth=1,
                           padding=5)
        self.style.map('Action.TButton',
                      background=[('active', '#d5dbdb')])
        
        # Configure Notebook
        self.style.configure('Modern.TNotebook',
                           background=self.colors['background'])
        self.style.configure('Modern.TNotebook.Tab',
                           font=('Arial', 9, 'bold'),
                           padding=[10, 4],
                           background=self.colors['light'],
                           foreground=self.colors['text'])
        self.style.map('Modern.TNotebook.Tab',
                      background=[('selected', self.colors['primary'])],
                      foreground=[('selected', 'white')])
        
        # Configure Checkbuttons
        self.style.configure('Modern.TCheckbutton',
                           font=('Arial', 8),
                           background=self.colors['card'],
                           foreground=self.colors['text'])
        
        # Configure Combobox
        self.style.configure('Modern.TCombobox',
                           fieldbackground='white',
                           background='white',
                           foreground=self.colors['text'],
                           borderwidth=1)
        
        # Configure Entry
        self.style.configure('Modern.TEntry',
                           fieldbackground='white',
                           foreground=self.colors['text'],
                           borderwidth=1)
    
    def create_widgets(self):
        """Create all GUI widgets with clean design"""
        # Create main container with less padding to prevent overflow
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title - SIMPLIFIED
        title_label = ttk.Label(main_frame, 
                               text="Weight Converter",
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 15))
        
        # Input Section - COMPACT
        input_frame = ttk.LabelFrame(main_frame, text="Input", 
                                    style='Card.TLabelframe', padding="10")
        input_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Value input
        ttk.Label(input_frame, text="Value:", 
                 style='Input.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.value_entry = ttk.Entry(input_frame, textvariable=self.input_value, 
                                    width=18, style='Modern.TEntry',
                                    font=('Arial', 10))
        self.value_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        # Input unit selection
        ttk.Label(input_frame, text="From:", 
                 style='Input.TLabel').grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        
        self.input_combobox = ttk.Combobox(input_frame, textvariable=self.input_unit, 
                                          values=list(UNIT_NAMES.keys()), 
                                          state='readonly', width=15,
                                          style='Modern.TCombobox',
                                          font=('Arial', 9))
        self.input_combobox.grid(row=0, column=3, sticky=tk.W)
        
        # Output Units Section - COMPACT
        output_frame = ttk.LabelFrame(main_frame, text="Output Units", 
                                     style='Card.TLabelframe', padding="10")
        output_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Create checkboxes for output units in a MORE COMPACT grid
        self.output_unit_vars = {}
        checkboxes_frame = ttk.Frame(output_frame)
        checkboxes_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        units = list(UNIT_NAMES.items())
        
        # Create 4 columns layout for better space usage
        cols = 4
        rows = (len(units) + cols - 1) // cols
        
        for idx, (unit_code, unit_name) in enumerate(units):
            row = idx % rows
            col = idx // rows
            
            var = tk.BooleanVar(value=True)
            self.output_unit_vars[unit_code] = var
            
            cb = ttk.Checkbutton(checkboxes_frame, text=f"{unit_name}",
                                variable=var, style='Modern.TCheckbutton')
            cb.grid(row=row, column=col, sticky=tk.W, padx=5, pady=3)
        
        # Quick selection buttons - SIMPLIFIED
        selection_frame = ttk.Frame(output_frame)
        selection_frame.grid(row=rows, column=0, columnspan=cols, pady=(10, 0))
        
        ttk.Button(selection_frame, text="Select All", 
                  command=self.select_all_units, style='Action.TButton', width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(selection_frame, text="Deselect All", 
                  command=self.deselect_all_units, style='Action.TButton', width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(selection_frame, text="Common Units", 
                  command=self.select_common_units, style='Action.TButton', width=10).pack(side=tk.LEFT, padx=2)
        
        # Action Buttons - ADDED CONVERT AND CLEAR BUTTONS
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=4, pady=(10, 0))
        
        # CONVERT BUTTON - ADDED
        self.convert_btn = ttk.Button(buttons_frame, text="Convert",
                                     command=self.perform_conversion,
                                     style='Convert.TButton',
                                     width=12)
        self.convert_btn.pack(side=tk.LEFT, padx=5)
        
        # CLEAR BUTTON - ADDED
        ttk.Button(buttons_frame, text="Clear",
                  command=self.clear_form,
                  style='Clear.TButton',
                  width=12).pack(side=tk.LEFT, padx=5)
        
        # COPY BUTTON
        ttk.Button(buttons_frame, text="Copy Results",
                  command=self.copy_results,
                  style='Action.TButton',
                  width=12).pack(side=tk.LEFT, padx=5)
        
        # Results and History Notebook - COMPACT
        notebook_frame = ttk.Frame(main_frame)
        notebook_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        notebook_frame.rowconfigure(0, weight=1)
        notebook_frame.columnconfigure(0, weight=1)
        
        self.notebook = ttk.Notebook(notebook_frame, style='Modern.TNotebook', height=250)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Results Tab
        results_tab = ttk.Frame(self.notebook, padding="8")
        self.notebook.add(results_tab, text="Results")
        
        # Results text widget - REMOVED WELCOME MESSAGE
        self.results_text = scrolledtext.ScrolledText(results_tab, 
                                                     font=('Courier New', 9),
                                                     bg='white',
                                                     fg=self.colors['text'],
                                                     height=10)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.results_text.config(state=tk.DISABLED)
        
        # Set initial message - SIMPLE
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, "Enter value, select units, and click 'Convert'")
        self.results_text.config(state=tk.DISABLED)
        
        # History Tab
        history_tab = ttk.Frame(self.notebook, padding="8")
        self.notebook.add(history_tab, text="History")
        
        # History text widget
        self.history_text = scrolledtext.ScrolledText(history_tab,
                                                     font=('Courier New', 8),
                                                     bg='white',
                                                     fg=self.colors['text'],
                                                     height=10)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        self.history_text.config(state=tk.DISABLED)
        
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, "Conversion history will appear here")
        self.history_text.config(state=tk.DISABLED)
        
        # History control buttons
        history_buttons = ttk.Frame(history_tab)
        history_buttons.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(history_buttons, text="Clear History",
                  command=self.clear_history,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
    
    def setup_bindings(self):
        """Set up keyboard bindings"""
        # Bind Enter key to perform conversion
        self.root.bind('<Return>', lambda e: self.perform_conversion())
        self.root.bind('<Escape>', lambda e: self.clear_form())
        self.root.bind('<Control-c>', lambda e: self.copy_results())
        
        # Bind focus events
        self.value_entry.bind('<FocusIn>', lambda e: self.value_entry.select_range(0, tk.END))
    
    def perform_conversion(self):
        """Perform conversion and update results"""
        # Get input value
        input_str = self.input_value.get().strip()
        
        # Clear previous results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        # Validate input
        if not input_str:
            self.results_text.insert(tk.END, "Please enter a value to convert")
            self.results_text.config(state=tk.DISABLED)
            return
        
        if not validate_positive_number(input_str):
            self.results_text.insert(tk.END, "Error: Please enter a valid positive number")
            self.results_text.config(state=tk.DISABLED)
            return
        
        try:
            value = float(input_str)
            from_unit = self.input_unit.get()
            
            # Get selected output units
            selected_units = [unit for unit, var in self.output_unit_vars.items() 
                            if var.get() and unit != from_unit]
            
            if not selected_units:
                self.results_text.insert(tk.END, "No output units selected")
                self.results_text.config(state=tk.DISABLED)
                return
            
            # Perform conversions
            results = {}
            for unit in selected_units:
                try:
                    converted = self.converter.convert(value, from_unit, unit)
                    results[unit] = converted
                except Exception as e:
                    results[unit] = str(e)
            
            # Display results
            self.display_results(value, from_unit, results)
            
            # Automatically add to history
            self.add_to_history(value, from_unit, results)
            
        except Exception as e:
            self.results_text.insert(tk.END, f"Error: {str(e)}")
            self.results_text.config(state=tk.DISABLED)
    
    def display_results(self, value: float, from_unit: str, results: dict):
        """Display conversion results"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        # Display input value
        input_unit_name = UNIT_NAMES.get(from_unit, from_unit)
        self.results_text.insert(tk.END, f"Converting {value} {input_unit_name}:\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Display results
        for unit, result in sorted(results.items()):
            if isinstance(result, (int, float)):
                formatted = self.converter.format_result(result, unit, self.decimal_places)
                unit_name = UNIT_NAMES.get(unit, unit)
                self.results_text.insert(tk.END, f"  • {unit_name.ljust(20)}: {formatted}\n")
            else:
                unit_name = UNIT_NAMES.get(unit, unit)
                self.results_text.insert(tk.END, f"  • {unit_name.ljust(20)}: Error - {result}\n", 'error')
        
        self.results_text.config(state=tk.DISABLED)
        self.results_text.tag_config('error', foreground='red')
    
    def clear_form(self):
        """Clear the input form"""
        self.input_value.set("1")
        self.input_unit.set('kg')
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Enter value, select units, and click 'Convert'")
        self.results_text.config(state=tk.DISABLED)
        self.value_entry.focus()
        self.value_entry.select_range(0, tk.END)
    
    def copy_results(self):
        """Copy results to clipboard"""
        text = self.results_text.get(1.0, tk.END).strip()
        if text and not text.startswith("Please enter") and not text.startswith("Error:") and not text.startswith("Enter value"):
            copy_to_clipboard(text, self.root)
            show_info("Results copied to clipboard!", self.root)
        else:
            show_error("No valid results to copy", self.root)
    
    def add_to_history(self, value: float, from_unit: str, results: dict):
        """Add current conversion to history automatically"""
        valid_results = {}
        for unit, result in results.items():
            if isinstance(result, (int, float)):
                valid_results[unit] = result
        
        if valid_results:
            self.converter.add_to_history(value, from_unit, valid_results)
            self.update_history_display()
    
    def update_history_display(self):
        """Update the history display"""
        history = self.converter.get_history()
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        if not history:
            self.history_text.insert(tk.END, "No conversion history yet.")
        else:
            for i, entry in enumerate(history, 1):
                timestamp = entry['timestamp']
                value = entry['value']
                from_unit = entry['from_unit']
                from_unit_name = UNIT_NAMES.get(from_unit, from_unit)
                
                self.history_text.insert(tk.END, f"{i}. [{timestamp}]\n")
                self.history_text.insert(tk.END, f"   {value} {from_unit_name} →\n")
                
                count = 0
                for unit, result in entry['results'].items():
                    if count < 5:
                        if isinstance(result, (int, float)):
                            formatted = self.converter.format_result(result, unit, 3)
                            unit_name = UNIT_NAMES.get(unit, unit)
                            self.history_text.insert(tk.END, f"     {unit_name}: {formatted}\n")
                            count += 1
                
                if len(entry['results']) > 5:
                    remaining = len(entry['results']) - 5
                    self.history_text.insert(tk.END, f"     ... and {remaining} more\n")
                
                self.history_text.insert(tk.END, "-" * 50 + "\n")
        
        self.history_text.config(state=tk.DISABLED)
    
    def clear_history(self):
        """Clear conversion history"""
        self.converter.clear_history()
        self.update_history_display()
    
    def select_all_units(self):
        """Select all output units"""
        for var in self.output_unit_vars.values():
            var.set(True)
    
    def deselect_all_units(self):
        """Deselect all output units"""
        for var in self.output_unit_vars.values():
            var.set(False)
    
    def select_common_units(self):
        """Select common weight units"""
        common_units = ['kg', 'g', 'lb', 'oz', 't', 'st']
        for unit, var in self.output_unit_vars.items():
            var.set(unit in common_units)
    
    def save_settings(self):
        """Save application settings"""
        settings = {
            'selected_units': {unit: var.get() for unit, var in self.output_unit_vars.items()}
        }
        
        try:
            with open('converter_settings.json', 'w') as f:
                json.dump(settings, f)
        except:
            pass
    
    def load_settings(self):
        """Load application settings"""
        try:
            if os.path.exists('converter_settings.json'):
                with open('converter_settings.json', 'r') as f:
                    settings = json.load(f)
                
                saved_units = settings.get('selected_units', {})
                for unit, selected in saved_units.items():
                    if unit in self.output_unit_vars:
                        self.output_unit_vars[unit].set(selected)
        except:
            pass