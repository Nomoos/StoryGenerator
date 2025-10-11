using System;
using Xunit;

namespace StoryGenerator.Tests.Examples
{
    /// <summary>
    /// Test-Driven Development (TDD) Example - Calculator Module
    /// 
    /// This demonstrates TDD best practices in C#:
    /// - Red: Write failing tests first
    /// - Green: Implement minimal code to pass
    /// - Refactor: Improve code while keeping tests green
    /// 
    /// This example shows:
    /// - Parameterized tests with [Theory] and [InlineData]
    /// - Edge case handling
    /// - Nullable reference types
    /// - Clear test structure and naming
    /// - Exception testing
    /// </summary>
    public class TddCalculatorTests
    {
        /// <summary>
        /// Simple calculator for TDD demonstration.
        /// In a real project, this would be in a separate file.
        /// </summary>
        private class Calculator
        {
            public int Add(int a, int b) => a + b;

            public int Subtract(int a, int b) => a - b;

            public int Multiply(int a, int b) => a * b;

            public double Divide(double a, double b)
            {
                if (b == 0)
                {
                    throw new DivideByZeroException("Cannot divide by zero");
                }
                return a / b;
            }
        }

        #region Addition Tests

        [Fact]
        public void Add_TwoPositiveNumbers_ReturnsSum()
        {
            // Arrange
            var calculator = new Calculator();

            // Act
            var result = calculator.Add(2, 3);

            // Assert
            Assert.Equal(5, result);
        }

        [Fact]
        public void Add_TwoNegativeNumbers_ReturnsSum()
        {
            // Arrange
            var calculator = new Calculator();

            // Act
            var result = calculator.Add(-2, -3);

            // Assert
            Assert.Equal(-5, result);
        }

        [Theory]
        [InlineData(0, 0, 0)]
        [InlineData(1, 0, 1)]
        [InlineData(0, 1, 1)]
        [InlineData(-1, 1, 0)]
        [InlineData(100, 200, 300)]
        [InlineData(int.MaxValue - 1, 1, int.MaxValue)]
        public void Add_VariousInputs_ReturnsExpectedSum(int a, int b, int expected)
        {
            // Arrange
            var calculator = new Calculator();

            // Act
            var result = calculator.Add(a, b);

            // Assert
            Assert.Equal(expected, result);
        }

        #endregion

        #region Subtraction Tests

        [Theory]
        [InlineData(5, 3, 2)]
        [InlineData(0, 0, 0)]
        [InlineData(-5, -3, -2)]
        [InlineData(3, 5, -2)]
        [InlineData(10, 5, 5)]
        public void Subtract_VariousInputs_ReturnsExpectedDifference(int a, int b, int expected)
        {
            // Arrange
            var calculator = new Calculator();

            // Act
            var result = calculator.Subtract(a, b);

            // Assert
            Assert.Equal(expected, result);
        }

        #endregion

        #region Multiplication Tests

        [Theory]
        [InlineData(2, 3, 6)]
        [InlineData(0, 5, 0)]
        [InlineData(-2, 3, -6)]
        [InlineData(-2, -3, 6)]
        [InlineData(1, 100, 100)]
        public void Multiply_VariousInputs_ReturnsExpectedProduct(int a, int b, int expected)
        {
            // Arrange
            var calculator = new Calculator();

            // Act
            var result = calculator.Multiply(a, b);

            // Assert
            Assert.Equal(expected, result);
        }

        #endregion

        #region Division Tests

        [Theory]
        [InlineData(6.0, 2.0, 3.0)]
        [InlineData(5.0, 2.0, 2.5)]
        [InlineData(-6.0, 2.0, -3.0)]
        [InlineData(6.0, -2.0, -3.0)]
        [InlineData(-6.0, -2.0, 3.0)]
        public void Divide_VariousInputs_ReturnsExpectedQuotient(double a, double b, double expected)
        {
            // Arrange
            var calculator = new Calculator();

            // Act
            var result = calculator.Divide(a, b);

            // Assert
            Assert.Equal(expected, result, precision: 10);
        }

        [Fact]
        public void Divide_ByZero_ThrowsDivideByZeroException()
        {
            // Arrange
            var calculator = new Calculator();

            // Act & Assert
            var exception = Assert.Throws<DivideByZeroException>(() => calculator.Divide(5, 0));
            Assert.Contains("Cannot divide by zero", exception.Message);
        }

        #endregion

        #region Integration Tests

        [Fact]
        public void ChainedOperations_MultipleSteps_ReturnsCorrectResult()
        {
            // Arrange
            var calculator = new Calculator();

            // Act - (5 + 3) * 2 - 4 = 12
            var result = calculator.Add(5, 3);
            result = calculator.Multiply(result, 2);
            result = calculator.Subtract(result, 4);

            // Assert
            Assert.Equal(12, result);
        }

        [Theory]
        [InlineData(2, 3, 4, 20)]  // (2 + 3) * 4 = 20
        [InlineData(10, 5, 2, 30)]  // (10 + 5) * 2 = 30
        [InlineData(0, 0, 5, 0)]    // (0 + 0) * 5 = 0
        public void ComplexOperation_AddThenMultiply_ReturnsExpectedResult(int a, int b, int c, int expected)
        {
            // Arrange
            var calculator = new Calculator();

            // Act
            var sum = calculator.Add(a, b);
            var result = calculator.Multiply(sum, c);

            // Assert
            Assert.Equal(expected, result);
        }

        #endregion
    }
}
