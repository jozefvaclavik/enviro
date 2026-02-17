# Trifle

Trifle is a time-series analytics platform for storing and analysing metrics over time.

Enviro can send readings directly to Trifle using the Metrics API.

## Setting up Trifle

1. Open your Trifle instance (for example [Trifle Cloud](https://app.trifle.io)).
2. Create or open the project you want to store Enviro readings in.
3. Create a **project token** with **write** permission.
4. During Enviro provisioning choose **Trifle** and enter:
   - **Trifle API URL**: your Trifle base URL (for example `https://app.trifle.io`)
   - **Trifle API token**: the project token from step 3

> Note: enter only the base URL. Enviro automatically posts to `/api/v1/metrics`.

## Message format

Enviro sends an HTTP `POST` request to `/api/v1/metrics` with a JSON body in this format:

```json
{
  "key": "enviro-office",
  "at": "2026-02-17T14:24:24Z",
  "values": {
    "count": 1,
    "temperature": 26.12,
    "humidity": 54.71917,
    "pressure": 1014.99
  }
}
```

- `key`: board nickname from provisioning.
- `at`: reading timestamp in UTC (`YYYY-MM-DDTHH:MM:SSZ`).
- `values`: metric values for the reading. Enviro includes `count=1` plus finite numeric sensor readings.

If Trifle responds with `201` then Enviro will delete its local cached copy of that reading.

View the list of sensor readings provided by each board: [Enviro Indoor](../boards/enviro-indoor.md), [Enviro Grow](../boards/enviro-grow.md), [Enviro Weather](../boards/enviro-weather.md), [Enviro Urban](../boards/enviro-urban.md).
