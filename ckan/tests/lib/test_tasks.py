# -*- coding: utf-8 -*-
import logging
from nose.tools import raises

import ckan.tests.helpers as helpers
import ckan.lib.task as task

log = logging.getLogger(__name__)


def fake_function():
    return 42


class TestTasks(object):

    def setup(self):
        task.clear_tasks('low')
        task.clear_tasks('medium')
        task.clear_tasks('high')

    def test_simple_async(self):
        task.async(fake_function, [])
        assert task.task_count('medium') == 1

    @raises(ValueError)
    def test_failing_async_bad_priority(self):
        task.async(fake_function, [], priority="immediately")

    def test_queue_size(self):
        task.async(fake_function, [], priority='low')
        task.async(fake_function, [], priority='low')
        task.async(fake_function, [], priority='low')
        assert task.task_count('low') == 3
        task.clear_queue('low')
        assert task.task_count('low') == 0

    @raises(ValueError)
    def test_queue_size_invalid(self):
        assert task.task_count('immediately') == 0

    def test_queue_size(self):
        task.async(fake_function, [], priority='low')
        task.async(fake_function, [], priority='medium')
        task.async(fake_function, [], priority='high')
        assert task.task_count() == 3
