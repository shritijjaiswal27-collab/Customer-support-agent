# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

def track_package(tracking_id: str) -> dict:
    """Get the tracking status and details for a package.

    Args:
        tracking_id: The unique identifier for the shipment package.

    Returns:
        A dictionary with the package status, current location, and estimated delivery date (ETA).
    """
    statuses = {
        "12345": {"status": "In Transit", "location": "Chicago, IL", "eta": "Tomorrow"},
        "67890": {"status": "Delivered", "location": "Austin, TX", "eta": "Delivered yesterday"},
        "abcde": {"status": "Pending", "location": "Warehouse, CA", "eta": "In 3 days"},
    }
    return statuses.get(
        tracking_id,
        {"status": "Unknown", "location": "N/A", "eta": "N/A", "message": f"Tracking ID {tracking_id} not found."}
    )


def calculate_shipping_rates(weight_lbs: float, destination: str = None) -> dict:
    """Calculate the estimated shipping rate for a package.

    Args:
        weight_lbs: Weight of the package in pounds.
        destination: The destination city, state, or region (optional).

    Returns:
        A dictionary with the estimated cost, shipping method, and delivery timeframe.
    """
    base_rate = 5.0
    per_pound = 2.0
    cost = base_rate + (weight_lbs * per_pound)
    
    dest_str = destination if destination else "Standard Domestic"
    
    return {
        "estimated_cost_usd": round(cost, 2),
        "destination": dest_str,
        "weight_lbs": weight_lbs,
        "shipping_method": "Ground",
        "estimated_delivery_days": 3 if weight_lbs < 10 else 5
    }
