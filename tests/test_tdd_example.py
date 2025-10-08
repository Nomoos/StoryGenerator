#!/usr/bin/env python3
"""
Test-Driven Development (TDD) Example - Calculator Module

This demonstrates TDD best practices:
- Red: Write failing tests first
- Green: Implement minimal code to pass
- Refactor: Improve code while keeping tests green

This example shows:
- Parameterized tests
- Edge case handling
- Type hints
- Clear test structure
"""


import pytest


# Production Code (would be in src/calculator.py)
class Calculator:
    """A simple calculator demonstrating TDD principles."""

    def add(self, a: int | float, b: int | float) -> int | float:
        """Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b

        Raises:
            TypeError: If arguments are not numbers
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Arguments must be numbers")
        return a + b

    def subtract(self, a: int | float, b: int | float) -> int | float:
        """Subtract b from a.

        Args:
            a: Number to subtract from
            b: Number to subtract

        Returns:
            Difference of a and b

        Raises:
            TypeError: If arguments are not numbers
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Arguments must be numbers")
        return a - b

    def multiply(self, a: int | float, b: int | float) -> int | float:
        """Multiply two numbers."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Arguments must be numbers")
        return a * b

    def divide(self, a: int | float, b: int | float) -> float:
        """Divide a by b.

        Args:
            a: Numerator
            b: Denominator

        Returns:
            Quotient of a and b

        Raises:
            TypeError: If arguments are not numbers
            ZeroDivisionError: If b is zero
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Arguments must be numbers")
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b


# Test Suite
class TestCalculatorAddition:
    """Test suite for addition operation."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        calc = Calculator()
        result = calc.add(2, 3)
        assert result == 5

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        calc = Calculator()
        result = calc.add(-2, -3)
        assert result == -5

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (0, 0, 0),
            (1, 0, 1),
            (0, 1, 1),
            (-1, 1, 0),
            (1.5, 2.5, 4.0),
            (100, 200, 300),
        ],
    )
    def test_add_parameterized(self, a, b, expected):
        """Parameterized test for various addition scenarios."""
        calc = Calculator()
        assert calc.add(a, b) == expected

    def test_add_invalid_type_raises_error(self):
        """Test that invalid types raise TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError, match="Arguments must be numbers"):
            calc.add("2", 3)

        with pytest.raises(TypeError):
            calc.add(2, None)


class TestCalculatorSubtraction:
    """Test suite for subtraction operation."""

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (5, 3, 2),
            (0, 0, 0),
            (-5, -3, -2),
            (3, 5, -2),
            (10.5, 5.5, 5.0),
        ],
    )
    def test_subtract_parameterized(self, a, b, expected):
        """Parameterized test for subtraction."""
        calc = Calculator()
        assert calc.subtract(a, b) == expected


class TestCalculatorMultiplication:
    """Test suite for multiplication operation."""

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (2, 3, 6),
            (0, 5, 0),
            (-2, 3, -6),
            (-2, -3, 6),
            (0.5, 2, 1.0),
        ],
    )
    def test_multiply_parameterized(self, a, b, expected):
        """Parameterized test for multiplication."""
        calc = Calculator()
        assert calc.multiply(a, b) == expected


class TestCalculatorDivision:
    """Test suite for division operation."""

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (6, 2, 3.0),
            (5, 2, 2.5),
            (-6, 2, -3.0),
            (6, -2, -3.0),
            (-6, -2, 3.0),
        ],
    )
    def test_divide_parameterized(self, a, b, expected):
        """Parameterized test for division."""
        calc = Calculator()
        assert calc.divide(a, b) == expected

    def test_divide_by_zero_raises_error(self):
        """Test that division by zero raises ZeroDivisionError."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            calc.divide(5, 0)

    def test_divide_invalid_type_raises_error(self):
        """Test that invalid types raise TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide("10", 2)


# Fixtures Example
@pytest.fixture
def calculator():
    """Fixture providing a Calculator instance."""
    return Calculator()


class TestCalculatorWithFixtures:
    """Demonstrate test fixtures to reduce duplication."""

    def test_chained_operations(self, calculator):
        """Test multiple operations in sequence."""
        result = calculator.add(5, 3)
        result = calculator.multiply(result, 2)
        result = calculator.subtract(result, 4)
        assert result == 12

    def test_order_of_operations_independence(self, calculator):
        """Test that operations work in any order."""
        # Test A
        result1 = calculator.multiply(2, 3)
        result1 = calculator.add(result1, 4)

        # Test B - same result, different order
        result2 = calculator.add(6, 4)

        assert result1 == result2 == 10


if __name__ == "__main__":
    # Allow running this file directly for quick testing
    pytest.main([__file__, "-v", "--tb=short"])
