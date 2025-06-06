import pytest
from app.worker import add

def test_add_task():
    """
    Tests the basic Celery 'add' task to ensure the worker is processing tasks.
    """
    # Queue the task
    task_result = add.delay(5, 10)
    
    # Wait for the result with a timeout
    result = task_result.get(timeout=10)
    
    # Assert the result
    assert result == 15 