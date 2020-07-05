import pytest
import random
from rezume.sections import Section, ResumeBase


class TestSection:
    def test_instantiation_with_elements(self):
        section = Section()
        assert len(section) == 0

        section = Section(["elem1", "elem2"])
        assert len(section) == 2

    def test_items_are_iterable(self):
        section = Section([1, 2, 3])
        items = list(section)
        assert items and len(items) == 3

        section = Section()
        section.add(1)
        section.add(2)
        items = list(section)
        assert items and len(items) == 2

    @pytest.mark.parametrize("elems", [["elem"], [1, 2], [(1,), (2, 3), (4, 5, 6)]])
    def test_element_addition(self, elems):
        section = Section()
        assert len(section) == 0

        for elem in elems:
            section.add(elem)

        assert len(section) == len(elems)

    @pytest.mark.parametrize("elems", [["elem"], [1, 2], [(1,), (2, 3), (4, 5, 6)]])
    def test_element_removal(self, elems):
        section = Section(elems)
        elem = random.choice(elems)
        assert elem in section

        section.discard(elem)
        assert elem not in section

    def test_duplicate_item_replace_old_item(self):
        section = Section([1, 2, 3, 4, 5])
        assert len(section) == 5

        section.add(5)
        assert len(section) == 5

    def test_generate_key_returns_given_item_by_default(self):
        # _generate_key returns a key to uniquely identify items within a
        # section; by default items themselves serve as the key; derived
        # classes can return other unique objects
        section, item = Section(), (1, 2, "boys")
        key = section._generate_key(item)
        assert key is item


class TestResumeBase:
    class SectionA:
        name = "A"

    class SectionB:
        name = "B"

    def test_is_subscriptable_for_items(self):
        base = ResumeBase()
        base.add(TestResumeBase.SectionA())
        base.add(TestResumeBase.SectionB())
        assert base["A"] is not None
