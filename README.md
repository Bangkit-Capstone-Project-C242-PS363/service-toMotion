# Motion API Documentation

## Base URLs

- Development: `http://localhost:8080`
- Production: `https://signmaster-tomotion-kji5w4ybbq-et.a.run.app`

## Endpoints

### Convert to Motion

```bash
POST /tomotion
Content-Type: application/json
```

Converts input data to motion format.

#### Request Body

```json
{
    "data": string
}
```

#### Response

```json
{
    "error": boolean,
    "message": string,
    "url": string
}
```

#### Example Response

```json
{
  "error": false,
  "message": "Data received",
  "url": "motion_url_here"
}
```

#### Notes

- The endpoint expects JSON data in the request body
- Returns a URL to the processed motion data
