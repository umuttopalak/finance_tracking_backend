from datetime import datetime
from typing import List
from firebase_admin import credentials, initialize_app, db
import os
import json
from pydantic import BaseModel, ValidationError

from models import Category, FinancalItemType, FinancialItem

creds = {
  "type": "service_account",
  "project_id": "finance-tracker-umuttopa-dc40a",
  "private_key_id": "e55eaa319e90f858377672919b53ec32ca66e79f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCsEl4Nq58mkRfo\n3wTgLOePhRRkn/KF3Ii/q2kt68HitGCx/sqUc6ZkzKn6XxI3UbaaAUiYjIL17e7o\n0ifopRPpWPvE9SjfEcgC1X+Vv/7CN+ltxF5ymQ5gOIxDRj0JMQmasVIqmC6+3apU\n6XYAR2gZXBScusksaFMQCdhSrj5zt2CwgCXCcaENrULQ2pFomMjp28khFna8lVJp\n9A4VvOFcuLvj4XHpJTSogRA9EB7FbVMq1R3sEClKfOSKuiQ+jOz2YQqLeEW4LVON\nQLXO6xDYF8vP8WCYo4hs0NPUiBNc7LVKXifFfNaPP8EvtFuqWzsp21aYClS+V9io\ny/RGR8PLAgMBAAECggEAC+y9FJwqQwZ2/BT23OTiDweIxOi8fLuue9qQkD7HVl7H\noZUaQoJ5kBMvOeIzPFXF3nf1lusehJXjUHli1RP1Vsx9rIX6Xll4eMgXrqa6Pq2Y\nRfYSPvxySz5dtPFCigcsm0o1DVIz47LB8cymrzRoN4WywNj8INGBwLVKhu17ZTcG\nYyWv/5nZSAuubKFU4ctLoUNxM8FrTVInGRsqebRWH4JLLt/ozLREaEPq1gtxYmIn\n55hkoelZqbfJxNyY3Xz3yrNYAsnHJWV1qJ6lEjHu+bdfCf+u6/a5wXu4YARRY8AP\nc9eRyrX+5g1tJveAoRgXre/nTB7ZoLyYvFp7Iu4OJQKBgQDzS5gj+SPywb+HYLS0\ngxnoAhUpnjJ6Ro2xeGr+EzZyqHXwmtrYtD3BeFUesqsKmK4b7x6pNLVfH5eUeaf2\ntAlknbSLsK3QLMXbZ9j+YG1XrqJGIOAea3UtkwfztZlgv4/DR1/DHsbbKkqilSjP\nhh/MeiPhXiEZzBdQba0CYzwvZQKBgQC1DqWRaNSXGZ/hjDk/debt8177IFQjYD45\nJeBCZ2XToJHkaScl1AEHkpFIcC5lbWl4vGYDeAVcDcDmwWLDhEyBDLSi7+6IYoyh\nlyVLjpxy8C4kGz2Kx27cYgmbbh10Qi/H+Pm8R5wvQYaJ/njv96mo6QgZhbCviZa9\nnrPUs+BrbwKBgQDU3I/I8YKlMySakl6oDIgO+DuBxRpO5wmzezLJBxA9Muy1TRcq\nQFBDxD9c8184jyrN3+FIk4gYKLDbQ7FT5GLPeDdtfHAmUfXuJ6avsLgZ3f22M69C\njivgauKrNHh0MEXcycacFYJQYGkaZDxnjOanZTmdRVjalDjVso+LJj2TDQKBgHfn\nzUpxTGkM9U8f2EHoyRjI1hwlmtMax9p89PnFFDCE5FmKMfzhXBUxwblhYbiWLwVg\nb4bYk2QVT60CYW/uS+QjD/XgQ+5apZvWR0K0nXOZEFWlHKqtzQNygb5HvIXj11Tt\n1CYWnp7FHF6DAoCZWeic+1o7qXl2+zd0xM+WmIdNAoGBAMqnUF8z07Os1IAXCMuM\nU9k37zCqQ9AFaeArRGrCKULFIzprV1+krUYPTRlfkR0lLWl1Ey6Ya4ruNB2vZLg9\nb9hi1PR0q6kgihaTSmxBHGu60q7xY2wrH+AXpNz/h0A3HkUjE+z+BFcocA6GSQf5\nKbHHd49PgP1aibD7IhEMqpE+\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-57e6l@finance-tracker-umuttopa-dc40a.iam.gserviceaccount.com",
  "client_id": "117370192654918579598",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-57e6l%40finance-tracker-umuttopa-dc40a.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


cred = credentials.Certificate(creds)
initialize_app(cred, {
    'databaseURL': "https://finance-tracker-umuttopa-dc40a-default-rtdb.firebaseio.com/"
})

ref = db.reference()

def save_to_firebase(model, ref_path):
    ref.child(ref_path).set(model)
    
def read_from_firebase(ref_path: str) -> List[dict]:
    data = ref.child(ref_path).get()
    if data:
        return data
    return []

