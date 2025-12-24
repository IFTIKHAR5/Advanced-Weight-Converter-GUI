# converter.py
"""
Weight conversion logic module
"""
import datetime

# Conversion factors relative to 1 kilogram
CONVERSION_FACTORS = {
    'kg': 1.0,            # Kilogram (base unit)
    'g': 1000.0,          # Gram
    'mg': 1000000.0,      # Milligram
    'oz': 35.274,         # Ounce
    'lb': 2.20462,        # Pound
    't': 0.001,           # Metric Ton
    'st': 0.157473,       # Stone
    'ct': 5000.0,         # Carat
    'gr': 15432.3584,     # Grain
    'lt': 0.000984207,    # Long Ton (UK)
    'stn': 0.00110231     # Short Ton (US)
}

# Unit display names
UNIT_NAMES = {
    'kg': 'Kilograms',
    'g': 'Grams',
    'mg': 'Milligrams',
    'oz': 'Ounces',
    'lb': 'Pounds',
    't': 'Metric Tons',
    'st': 'Stones',
    'ct': 'Carats',
    'gr': 'Grains',
    'lt': 'Long Tons (UK)',
    'stn': 'Short Tons (US)'
}

# Unit symbols
UNIT_SYMBOLS = {
    'kg': 'kg',
    'g': 'g',
    'mg': 'mg',
    'oz': 'oz',
    'lb': 'lb',
    't': 't',
    'st': 'st',
    'ct': 'ct',
    'gr': 'gr',
    'lt': 'lt',
    'stn': 'stn'
}

class WeightConverter:
    """Handles weight conversion operations"""
    
    def __init__(self):
        self.history = []
        self.max_history = 10
    
    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert weight from one unit to another
        """
        if from_unit not in CONVERSION_FACTORS or to_unit not in CONVERSION_FACTORS:
            raise ValueError(f"Invalid unit.")
        
        # Convert to kilograms first, then to target unit
        value_in_kg = value / CONVERSION_FACTORS[from_unit]
        converted_value = value_in_kg * CONVERSION_FACTORS[to_unit]
        
        return converted_value
    
    def add_to_history(self, value: float, from_unit: str, results: dict, timestamp=None):
        """
        Add a conversion to history
        """
        if timestamp is None:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        history_entry = {
            'timestamp': timestamp,
            'value': value,
            'from_unit': from_unit,
            'results': results.copy()
        }
        
        self.history.insert(0, history_entry)
        
        # Keep only last max_history entries
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
    
    def get_history(self) -> list:
        """Get conversion history"""
        return self.history
    
    def clear_history(self):
        """Clear conversion history"""
        self.history = []
    
    def format_result(self, value: float, unit: str, decimal_places: int = 3) -> str:
        """
        Format a conversion result with proper unit name
        """
        if unit in UNIT_SYMBOLS:
            unit_symbol = UNIT_SYMBOLS[unit]
        else:
            unit_symbol = unit
            
        # Format with appropriate decimal places
        if value == 0:
            formatted_value = "0"
        elif abs(value) < 0.000001:
            formatted_value = f"{value:.2e}"
        elif abs(value) < 0.001:
            formatted_value = f"{value:.6f}"
        elif abs(value) < 1:
            formatted_value = f"{value:.4f}"
        elif abs(value) < 1000:
            formatted_value = f"{value:.{decimal_places}f}"
        else:
            # For large numbers, use comma separators
            formatted_value = f"{value:,.{decimal_places}f}"
            
        return f"{formatted_value} {unit_symbol}"