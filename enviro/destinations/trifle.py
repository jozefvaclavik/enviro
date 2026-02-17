from enviro import logging
from enviro.constants import UPLOAD_SUCCESS, UPLOAD_FAILED
import urequests
import ujson
import config

def is_valid_metric_value(value):
  # Skip bools and non-numeric types; keep only finite numbers.
  if isinstance(value, bool):
    return False

  if not isinstance(value, (int, float)):
    return False

  if isinstance(value, float):
    if value != value:  # NaN
      return False
    if value == float("inf") or value == float("-inf"):
      return False

  return True

def log_destination():
  logging.info(f"> uploading cached readings to Trifle: {config.trifle_url}")

def upload_reading(reading):
  """
  Upload reading to Trifle API.
  Sends nickname as key, all numeric sensor readings as values with count=1.
  """
  trifle_url = (config.trifle_url or "").strip().rstrip("/")
  trifle_token = (config.trifle_token or "").strip()
  url = f"{trifle_url}/api/v1/metrics"
  headers = {
    'Authorization': f'Bearer {trifle_token}',
    'Content-Type': 'application/json'
  }

  # Build values dict with count and all numeric sensor readings
  values = {"count": 1}

  # Add all sensor readings (only numeric values)
  for key, value in reading["readings"].items():
    if is_valid_metric_value(value):
      values[key] = value

  payload = {
    "key": reading["nickname"],
    "at": reading["timestamp"],
    "values": values
  }

  try:
    payload_json = ujson.dumps(payload)
    logging.debug(f"  - trifle request url: {url}")
    logging.debug(f"  - trifle token length: {len(trifle_token)}")
    logging.debug(f"  - trifle payload: {payload_json}")

    # Use explicit JSON string body to avoid urequests `json=` encoding quirks.
    result = urequests.post(url, headers=headers, data=payload_json)
    status_code = result.status_code
    reason = result.reason
    response_body = None
    try:
      response_body = result.text
    except Exception:
      try:
        response_body = result.content
      except Exception:
        response_body = "<unavailable>"
    result.close()

    if status_code == 201:
      return UPLOAD_SUCCESS

    logging.debug(f"  - upload issue ({status_code} {reason}) body={response_body}")
  except Exception as e:
    logging.debug(f"  - exception uploading: {e}")

  return UPLOAD_FAILED
