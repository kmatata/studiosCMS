import datetime

def calculate_consumer_timeout(task_time):
  """
  Calculates the appropriate celery consumer timeout, given the ETA of the task.

  Args:
    task_time: The ETA of the task, as a datetime object.

  Returns:
    The appropriate celery consumer timeout, in seconds.
  """

  now = datetime.datetime.now()
  print(now)
  delta = task_time - now
  print(delta)
  timeout = delta.total_seconds()

  return timeout

if __name__ == "__main__":
  task_time = datetime.datetime.now() + datetime.timedelta(days=1, hours=0, minutes=0)
  timeout = calculate_consumer_timeout(task_time)
  print(f"The appropriate celery consumer timeout is {timeout} seconds.")
