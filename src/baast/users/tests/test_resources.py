# -*- coding: utf-8 -*-
from unittest import TestCase


class UserContextTest(TestCase):
    def _make_one(self):
        from ..resources import UserContext
        return UserContext()

    def test_new(self):
        """新規作成
        """
        context = self._make_one()
        context.new()

    def test_load(self):
        """既存データをロード
        """
        context = self._make_one()
        context.load(1)

    def test_update(self):
        """更新
        """
        context = self._make_one()
        context.new()
        context.update(**{'first_name': 'a'})

    def test_delete(self):
        """削除
        """
        context = self._make_one()
        context.new()
        self.assert_(not context._core.is_deleted)
        context.delete()
        self.assert_(context._core.is_deleted)

    def test_copy(self):
        """コピー
        """
        context = self._make_one()
        context.new()
        context.update(
            first_name='first name',
            )
        copied_context = context.copy()
        self.assertEqual(context._core.first_name, copied_context._core.first_name)

    def test_save(self):
        """保存
        """
        context = self._make_one()
        context.new()
        context.save()
        new_context = self._make_one()
        new_context.load(context._core.id)
        self.assertEqual(context._core, new_context._core)
