"""
Last-Mile Delivery Route Optimization
--------------------------------------
Simulates a delivery hub dispatching a vehicle to N customer stops in a city.
Compares:
  1) "As-received" order  — stops visited in the order they arrived (baseline)
  2) Nearest-neighbor optimized route — a simple greedy heuristic
  3) 2-opt improvement pass on top of the nearest-neighbor route

Outputs:
  - route_comparison.png   (map of both routes)
  - distance_savings.png   (bar chart comparing total distance)
  - results_summary.csv    (per-stop coordinates + summary stats)
  - printed summary stats (distance saved, % improvement, est. fuel/time savings)
"""

import random
import math
import csv
import matplotlib.pyplot as plt

random.seed(7)

# ---------------------------------------------------------------------------
# 1. Generate a synthetic delivery hub + 20 customer stops (lat/lon offsets
#    in km from hub, to keep the math simple and avoid needing real geo data)
# ---------------------------------------------------------------------------
HUB = (0.0, 0.0)
N_STOPS = 20

stops = []
for i in range(N_STOPS):
    x = random.uniform(-12, 12)
    y = random.uniform(-12, 12)
    stops.append({"id": f"ORD-{100+i}", "x": x, "y": y})


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def route_distance(route_coords):
    total = 0.0
    prev = HUB
    for pt in route_coords:
        total += dist(prev, pt)
        prev = pt
    total += dist(prev, HUB)  # return to hub
    return total


# ---------------------------------------------------------------------------
# 2. Baseline: visit stops in the order orders arrived
# ---------------------------------------------------------------------------
baseline_order = stops[:]
baseline_coords = [(s["x"], s["y"]) for s in baseline_order]
baseline_dist = route_distance(baseline_coords)


# ---------------------------------------------------------------------------
# 3. Nearest-neighbor heuristic
# ---------------------------------------------------------------------------
def nearest_neighbor_route(stops):
    remaining = stops[:]
    route = []
    current = HUB
    while remaining:
        nxt = min(remaining, key=lambda s: dist(current, (s["x"], s["y"])))
        route.append(nxt)
        current = (nxt["x"], nxt["y"])
        remaining.remove(nxt)
    return route


nn_order = nearest_neighbor_route(stops)
nn_coords = [(s["x"], s["y"]) for s in nn_order]
nn_dist = route_distance(nn_coords)


# ---------------------------------------------------------------------------
# 4. 2-opt improvement pass on the nearest-neighbor route
# ---------------------------------------------------------------------------
def two_opt(order):
    coords = [HUB] + [(s["x"], s["y"]) for s in order] + [HUB]
    improved = True
    while improved:
        improved = False
        for i in range(1, len(coords) - 2):
            for j in range(i + 1, len(coords) - 1):
                a, b, c, d = coords[i - 1], coords[i], coords[j], coords[j + 1]
                if dist(a, b) + dist(c, d) > dist(a, c) + dist(b, d):
                    coords[i:j + 1] = coords[i:j + 1][::-1]
                    improved = True
    return coords[1:-1]  # strip hub start/end


two_opt_coords = two_opt(nn_order)
two_opt_dist = route_distance(two_opt_coords)

# ---------------------------------------------------------------------------
# 5. Results
# ---------------------------------------------------------------------------
savings_km = baseline_dist - two_opt_dist
savings_pct = (savings_km / baseline_dist) * 100
AVG_SPEED_KMH = 25          # typical last-mile delivery vehicle speed in dense areas
FUEL_PER_KM = 0.08          # liters/km assumption for a delivery two-wheeler/van

time_saved_min = (savings_km / AVG_SPEED_KMH) * 60
fuel_saved_l = savings_km * FUEL_PER_KM

print("=" * 60)
print("LAST-MILE DELIVERY ROUTE OPTIMIZATION — RESULTS")
print("=" * 60)
print(f"Stops delivered per route     : {N_STOPS}")
print(f"Baseline route distance       : {baseline_dist:.2f} km")
print(f"Nearest-neighbor route        : {nn_dist:.2f} km")
print(f"Nearest-neighbor + 2-opt      : {two_opt_dist:.2f} km")
print("-" * 60)
print(f"Total distance saved          : {savings_km:.2f} km ({savings_pct:.1f}%)")
print(f"Estimated time saved/route    : {time_saved_min:.1f} minutes")
print(f"Estimated fuel saved/route    : {fuel_saved_l:.2f} liters")
print("=" * 60)

# ---------------------------------------------------------------------------
# 6. Save results to CSV
# ---------------------------------------------------------------------------
with open("results_summary.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["metric", "value"])
    writer.writerow(["stops", N_STOPS])
    writer.writerow(["baseline_distance_km", round(baseline_dist, 2)])
    writer.writerow(["nearest_neighbor_distance_km", round(nn_dist, 2)])
    writer.writerow(["two_opt_distance_km", round(two_opt_dist, 2)])
    writer.writerow(["distance_saved_km", round(savings_km, 2)])
    writer.writerow(["distance_saved_pct", round(savings_pct, 1)])
    writer.writerow(["est_time_saved_min", round(time_saved_min, 1)])
    writer.writerow(["est_fuel_saved_l", round(fuel_saved_l, 2)])
    writer.writerow([])
    writer.writerow(["stop_id", "x_km", "y_km"])
    for s in stops:
        writer.writerow([s["id"], round(s["x"], 2), round(s["y"], 2)])

# ---------------------------------------------------------------------------
# 7. Plot: baseline vs optimized route on a map
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))

for ax, coords, title, dist_val, color in [
    (axes[0], baseline_coords, f"Baseline (as-received)\n{baseline_dist:.1f} km", baseline_dist, "#d9534f"),
    (axes[1], two_opt_coords, f"Optimized (NN + 2-opt)\n{two_opt_dist:.1f} km", two_opt_dist, "#2e7d32"),
]:
    path = [HUB] + coords + [HUB]
    xs = [p[0] for p in path]
    ys = [p[1] for p in path]
    ax.plot(xs, ys, "-o", color=color, linewidth=1.5, markersize=5, zorder=2)
    ax.scatter([HUB[0]], [HUB[1]], color="#1F4E78", s=180, marker="s", zorder=3, label="Hub")
    for i, p in enumerate(coords):
        ax.annotate(str(i + 1), (p[0], p[1]), fontsize=7, ha="center", va="center",
                    xytext=(0, 6), textcoords="offset points")
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xlabel("km (east-west)")
    ax.set_ylabel("km (north-south)")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_aspect("equal")
    ax.grid(alpha=0.25)

plt.tight_layout()
plt.savefig("route_comparison.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# 8. Plot: distance comparison bar chart
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5))
labels = ["Baseline\n(as-received)", "Nearest\nNeighbor", "NN + 2-opt\n(final)"]
values = [baseline_dist, nn_dist, two_opt_dist]
colors = ["#d9534f", "#f0ad4e", "#2e7d32"]
bars = ax.bar(labels, values, color=colors, width=0.55)
for bar, v in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 0.3, f"{v:.1f} km",
            ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("Total route distance (km)")
ax.set_title(f"Route Distance by Method — {savings_pct:.1f}% reduction achieved", fontsize=12, fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("distance_savings.png", dpi=150)
plt.close()

print("\nSaved: route_comparison.png, distance_savings.png, results_summary.csv")
