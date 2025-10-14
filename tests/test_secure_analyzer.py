import pytest
from unittest.mock import patch, MagicMock
from secure_analyzer import renew_token  # Adjust import path if in a package

@pytest.fixture
def mock_renewal():
    """Mock external renewal function if renew_token calls one."""
    with patch('secure_analyzer.external_renew_service') as mock:
        mock.return_value = True  # Assume successful renewal
        yield mock

class TestRenewToken:
    """Test suite for renew_token function."""
    
    def test_successful_renewal(self, mock_renewal, capsys):
        """Test successful case: present lease_duration, verify TTL print and return."""
        lease_data = {'lease_duration': 3600}
        expected_ttl = 3600
        expected_print = f"Token renewed with TTL: {expected_ttl}"
        
        result = renew_token(lease_data)
        
        assert result == expected_ttl
        captured = capsys.readouterr()
        assert expected_print in captured.out
        mock_renewal.assert_called_once_with(expected_ttl)  # If applicable

    def test_missing_key(self, capsys):
        """Test error for completely missing lease_duration key."""
        lease_data = {}
        
        with pytest.raises(KeyError, match="'lease_duration'"):  # Or ValueError if wrapped
            renew_token(lease_data)
        
        captured = capsys.readouterr()
        assert "Missing required key: lease_duration" in captured.out  # If error prints

    def test_misnamed_key(self, capsys):
        """Test error for mis-named key (e.g., typo), covering same error path."""
        lease_data = {'lease_duraton': 3600}  # Typo in key name
        
        with pytest.raises(KeyError, match="'lease_duration'"):
            renew_token(lease_data)
        
        # Ensures coverage of dict access failure regardless of input

    @pytest.mark.parametrize("duration, expected", [
        (0, 0),  # Zero TTL: immediate expiry edge
        (-1, ValueError),  # Negative: invalid, expect exception
        (86400, 86400),  # Large positive for full logic
    ])
    def test_edge_conditions(self, duration, expected, mock_renewal, capsys):
        """Parametrized tests for edge cases in lease_duration handling."""
        if isinstance(expected, type) and issubclass(expected, Exception):
            lease_data = {'lease_duration': duration}
            with pytest.raises(expected, match="Invalid lease duration"):
                renew_token(lease_data)
        else:
            lease_data = {'lease_duration': duration}
            result = renew_token(lease_data)
            assert result == expected
            captured = capsys.readouterr()
            assert f"Token renewed with TTL: {expected}" in captured.out

    def test_renewal_failure(self, capsys):
        """Test if renewal logic fails (e.g., mock returns False), covering error branch."""
        mock_renewal.return_value = False  # Patch to fail
        lease_data = {'lease_duration': 3600}
        
        with pytest.raises(RuntimeError, match="Renewal failed"):
            renew_token(lease_data)
