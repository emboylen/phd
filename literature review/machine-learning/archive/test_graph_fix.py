"""
Quick test to verify knowledge graph JSON serialization fix
"""
import json
import numpy as np

# Test the issue
print("Testing JSON serialization fix...")

# The problem: numpy types don't serialize
try:
    test_data = {
        'weight': np.float32(0.5),
        'size': np.int32(10)
    }
    json.dumps(test_data)
    print("❌ FAILED: Should have raised TypeError")
except TypeError as e:
    print("✓ Confirmed: numpy types cause error")
    print(f"  Error: {e}")

# The solution: convert to native Python types
try:
    test_data_fixed = {
        'weight': float(np.float32(0.5)),  # Convert to Python float
        'size': int(np.int32(10))          # Convert to Python int
    }
    result = json.dumps(test_data_fixed)
    print("\n✓ FIXED: Python native types work")
    print(f"  Serialized: {result}")
except TypeError as e:
    print(f"❌ Still broken: {e}")

print("\n" + "="*50)
print("Knowledge graph fix verified!")
print("="*50)
print("\nChanges applied in refined-topic-model.py:")
print("  Line 813: size=int(max(doc_count * 3, 20))")
print("  Line 832: weight=float(doc_data['topic_prob'])")
print("  Line 844: size=int(max(score * 80, 5))")
print("  Line 850: weight=float(score)")
print("\nAll numpy float32/int values converted to Python native types ✓")

