
DATE_FORMAT = "YYYY-MM-DD"
CONSTRUCTION_STAGES = [
    "Foundation",
    "Structure-GF",
    "Structure-I_Floor",
    "Structure-II_Floor",
    "Structure-III_Floor",
    "Structure-IV_Floor",
    "Plastering",
    "Finishing",
    "External Works",
    "Others"
]

PAYMENT_MODES = ["Cash", "UPI", "Bank Transfer",]

# CEMENT
DEFAULT_CEMENT_VENDOR = "CHOWDESHWARI STEEL & CEMENT TRADERS"
DEFAULT_CEMENT_COMPANY = "RAMCO SUPERCRETE CEMENT"
DEFAULT_CEMENT_COST_PER_BAG = 360.00

# BRICKS
DEFAULT_BRICK_VENDOR = "SRS ENTERPRISES"
BRICK_SIZE_COST = {
    "4-INCH" : 29.00,
    "6-INCH" : 35.00
}

# STEEL
DEFAULT_STEEL_VENDOR = "CHOWDESHWARI STEEL & CEMENT TRADERS"
STEEL_CATEGORIES = ["Steel", "Binding Wire"]
DEFAULT_STEEL_COST_PER_KG = 64.00
DEFAULT_BINDING_WIRE_COST_PER_BUNDLE = 2000.00
STEEL_SIZES_COST = {
        "TMT 8mm": 45.25,
        "TMT 10mm": 48.94,
        "TMT 12mm": 51.50,
        "TMT 16mm": 55.11,
        "TMT 20mm": 58.38
    }

# SAND
DEFAULT_SAND_VENDOR = "VISWANATHA SAND SUPPLIERS"
SAND_TYPES_COST = {"DOUBLE_WASHED" : 18000.00, "SINGLE_WASHED": 16500.00}

# STONE
DEFAULT_STONE_VENDOR = "VISWANATHA SAND SUPPLIERS"
STONES_TYPES_COST = {"20mm" : 12500.00, "40mm": 15000.00}

# LABOUR
LABOUR_TYPE = ["Steel Bending", "Civil", "Concrete Gang", "Others"]

# ELECTRIC
ELECTRIC_CATEGORY = ["Wiring", "Fittings", "Temporary EB", "Labor", "Other"]

# PLUMBING
PLUMBING_CATEGORY = ["Pipes", "Fittings", "Sanitary", "Labor", "Water Tank", "Other"]

# PAINTING
PAINTING_CATEGORY = ["Paint", "Primer", "Putty", "Labor", "Tools", "Other"]

# MISCELLANEOUS_EXPENSE
MISCELLANEOUS_EXPENSE_CATEGORIES = {
        "Architect Fee": [
            "Design Consultation", "Blueprint / Drawings", "Site Visits", "Approval Charges", "Other"
        ],
        "Excavation": [
            "JCB / Machine Rent", "Manual Labour", "Soil Removal", "Transport", "Other"
        ],
        "Readymix Concrete": [
            "RMC Material", "Pumping Charges", "Transport", "Labour Support", "Other"
        ],
        "House Plan": [
            "2D Plan", "3D Elevation", "Structural Design", "Government Approval", "Other"
        ],
        "Site Cleaning Setup": [
            "Initial Cleaning", "Debris Removal", "Temporary Setup", "Water Arrangement", "Other"
        ],
        "Loan Process": [
            "Processing Fee", "Legal Charges", "Documentation", "Valuation Charges", "Other"
        ],
        "Miscellaneous": [
            "Small Purchases", "Unexpected Expenses", "Repairs", "Tips / Support Payments", "Other"
        ]
    }