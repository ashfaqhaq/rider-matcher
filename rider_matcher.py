import csv
import json
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class MatchState(TypedDict):
    requests: list[dict[str, str]]
    drivers: list[dict[str, str]]
    matches: list[dict]


def match_drivers(state: MatchState) -> dict:
    matches = []
    for request in state["requests"]:
        candidates = [
            driver for driver in state["drivers"]
            if driver["request_id"] == request["request_id"]
            and driver["driver_status"] == "available"
        ]
        candidates.sort(key=lambda driver: (
            float(driver["road_pickup_minutes"]),
            float(driver["straight_line_km"]),
            driver["driver_id"],
        ))
        best = candidates[0] if candidates else None
        matches.append({
            "request_id": request["request_id"],
            "driver_id": best["driver_id"] if best else None,
            "road_pickup_minutes": float(best["road_pickup_minutes"]) if best else None,
        })
    return {"matches": matches}


graph = StateGraph(MatchState)
graph.add_node("match_drivers", match_drivers)
graph.add_edge(START, "match_drivers")
graph.add_edge("match_drivers", END)
matcher = graph.compile()


def main():
    data_dir = Path(__file__).resolve().parent / "data"
    with (data_dir / "uber_ride_requests_test_set.csv").open(encoding="utf-8-sig", newline="") as file:
        requests = list(csv.DictReader(file))
    with (data_dir / "uber_candidate_drivers_snapshot.csv").open(encoding="utf-8-sig", newline="") as file:
        drivers = list(csv.DictReader(file))
    result = matcher.invoke({"requests": requests, "drivers": drivers, "matches": []})
    print(json.dumps(result["matches"], indent=2))


if __name__ == "__main__":
    main()
