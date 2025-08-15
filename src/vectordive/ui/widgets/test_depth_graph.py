import pytest
from unittest.mock import MagicMock, patch
from vectordive.ui.widgets.depth_graph import DepthGraph

@pytest.fixture
def depth_graph():
    with patch('vectordive.ui.widgets.depth_graph.pqt.PlotWidget', autospec=True) as MockPlotWidget:
        mock_widget = MockPlotWidget.return_value
        dg = DepthGraph()
        dg.depthgraph = mock_widget  # Use the mocked widget
        return dg, mock_widget

def test_clear_graph_calls_clear_and_sets_ranges(depth_graph):
    dg, mock_widget = depth_graph

    # Patch methods on the instance
    dg.clear = MagicMock()
    dg.setXRange = MagicMock()
    dg.setYRange = MagicMock()

    dg.clear_graph()

    dg.clear.assert_called_once()
    dg.setXRange.assert_called_once_with(0, 60)
    dg.setYRange.assert_called_once_with(0, 100)
    
if __name__ == "__main__":
    pytest.main([__file__])
# This will run the tests when the script is executed directly.
# You can also run the tests using pytest from the command line:
# pytest test_depth_graph.py        