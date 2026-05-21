import sys
try:
    import spade
    print("SPADE imported successfully")
    print(f"SPADE version: {spade.__version__}")
    sys.exit(0)
except Exception as e:
    print(f"Error importing SPADE: {e}")
    sys.exit(1)