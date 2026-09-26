"""Test eksportu pakietu - regresja braku J w __init__.py."""
import topologic


def test_all_operators_exported():
    assert hasattr(topologic, "twist")
    assert hasattr(topologic, "defect")
    assert hasattr(topologic, "resonance")
    assert hasattr(topologic, "J")
    assert hasattr(topologic, "anomaly")
    assert hasattr(topologic, "resonance_m")


def test_all_list_matches_exports():
    assert set(topologic.__all__) == {"twist", "defect", "anomaly", "resonance", "resonance_m", "J"}
