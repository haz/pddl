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

"""This modules implements PDDL terms."""
import functools
from typing import AbstractSet, Collection, Optional

from pddl.custom_types import name as name_type
from pddl.custom_types import namelike, to_names
from pddl.helpers.base import assert_, ensure_set
from pddl.helpers.cache_hash import cache_hash


@cache_hash
@functools.total_ordering
class Term:
    """A term in a formula."""

    def __init__(
        self, name: namelike, type_tags: Optional[Collection[namelike]] = None
    ):
        """
        Initialize a term.

        :param name: the name for the term.
        :param type_tags: the type tags associated to this term.
        """
        self._name = name_type(name)
        self._type_tags = set(to_names(ensure_set(type_tags)))

    @property
    def name(self) -> str:
        """Get the name."""
        return self._name

    @property
    def type_tags(self) -> AbstractSet[name_type]:
        """Get a set of type tags for this term."""
        return self._type_tags

    def __lt__(self, other):
        """Compare with another term."""
        if isinstance(other, Constant):
            return (self.name, sorted(self.type_tags)) < (
                other.name,
                sorted(other.type_tags),
            )
        else:
            return super().__lt__(other)


# TODO check correctness
class Constant(Term):
    """A constant term."""

    def __init__(self, name: namelike, type_tag: Optional[namelike] = None):
        """
        Initialize a constant.

        :param name: the name.
        :param type_tag: the type tag
        """
        super().__init__(name, type_tags={type_tag} if type_tag is not None else None)

    @property
    def type_tag(self) -> Optional[name_type]:
        """Get the type of this constant."""
        type_tags = self.type_tags
        assert_(len(type_tags) <= 1)
        return next(iter(type_tags)) if len(type_tags) == 1 else None

    def __str__(self) -> str:
        """Get the string representation."""
        return self._name

    def __repr__(self):
        """Get a unique representation of the object."""
        return f"Constant({self.name})"

    def __eq__(self, other) -> bool:
        """Compare with another object."""
        return isinstance(other, Constant) and self.name == other.name

    def __hash__(self):
        """Get the hash."""
        return hash((Constant, self._name))


class Variable(Term):
    """A variable term."""

    def __init__(
        self, name: namelike, type_tags: Optional[Collection[namelike]] = None
    ):
        """
        Initialize the variable.

        :param name: the name.
        :param type_tags: the type tags
        """
        super().__init__(name, type_tags=type_tags)

    def __str__(self) -> str:
        """Get the string representation."""
        return f"?{self._name}"

    def __repr__(self):
        """Get a unique representation of the object."""
        return f"Variable({self.name})"

    def __eq__(self, other) -> bool:
        """Compare with another object."""
        return (
            isinstance(other, Variable)
            and self.name == other.name
            and self.type_tags == other.type_tags
        )

    def __hash__(self) -> int:
        """Get the hash."""
        return hash((Variable, self._name))
