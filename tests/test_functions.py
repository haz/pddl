#
# Copyright 2021-2023 WhiteMech
#
# ------------------------------
#
# This file is part of pddl.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#

"""This module contains tests for PDDL functions."""
import pytest

from pddl.core import Function
from pddl.logic.functions import TotalCost, Metric
from pddl.logic.helpers import variables


class TestFunctionSimpleInitialisation:
    """Test simple function initialisation."""

    def setup_method(self):
        """Set up the tests."""
        self.a, self.b = variables("a b")
        self.function = Function("f", self.a, self.b)

    def test_name(self):
        """Test name getter."""
        assert self.function.name == "f"

    def test_variables(self):
        """Test terms getter."""
        assert self.function.terms == (self.a, self.b)

    def test_arity(self):
        """Test arity property."""
        assert self.function.arity == 2

    def test_to_equal(self):
        """Test to equal."""
        other = Function("f", self.a, self.b)
        assert self.function == other

    def test_to_str(self):
        """Test to string."""
        assert str(self.function) == f"({self.function.name} {self.a} {self.b})"

    def test_to_repr(self):
        """Test to repr."""
        assert (
            repr(self.function) == f"Function({self.function.name}, {self.a}, {self.b})"
        )


class TestTotalCost:
    """Test total cost function."""

    def setup_method(self):
        """Set up the tests."""
        self.predicate = TotalCost()

    def test_name(self):
        """Test name getter."""
        assert self.predicate.name == "total-cost"


class TestMetric:
    """Test metric."""

    def setup_method(self):
        """Set up the tests."""
        self.a, self.b = variables("a b")
        self.function = Function("f", self.a, self.b)
        self.maximize_metric = Metric(self.function, Metric.MAXIMIZE)
        self.minimize_metric = Metric(self.function, Metric.MINIMIZE)

    def test_function_maximize(self):
        """Test function getter for maximize metric."""
        assert self.maximize_metric.function == self.function

    def test_function_minimize(self):
        """Test function getter for minimize metric."""
        assert self.minimize_metric.function == self.function

    def test_optimization_maximize(self):
        """Test optimization getter for maximize metric."""
        assert self.maximize_metric.optimization == Metric.MAXIMIZE

    def test_optimization_minimize(self):
        """Test optimization getter for minimize metric."""
        assert self.minimize_metric.optimization == Metric.MINIMIZE

    def test_wrong_optimization(self):
        """Test wrong optimization."""
        with pytest.raises(
            AssertionError,
            match="Optimization metric not recognized.",
        ):
            Metric(self.function, "other")

    def test_to_equal(self):
        """Test to equal."""
        other = Metric(Function("f", self.a, self.b), Metric.MINIMIZE)
        assert self.minimize_metric == other

    def test_to_str(self):
        """Test to string."""
        assert str(self.maximize_metric) == f"{self.maximize_metric.optimization} {self.maximize_metric.function}"

    def test_to_repr(self):
        """Test to repr."""
        assert (
            repr(self.minimize_metric) == f"Metric(({self.function.name} {self.a} {self.b}), minimize)"
        )
