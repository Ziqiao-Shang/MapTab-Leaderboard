#!/usr/bin/env python3
"""Generate leaderboard table HTML fragments and full index.html for MapTab."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Colors (LaTeX)
FC, CC, IC, SB, BH = "#FDEEF4", "#E8F0E8", "#FFF4E5", "#E7F3FF", "#D9D9D9"
MC = "#E8E4F0"  # MixColor for QA Map+Vertex


def fmt_cell(v):
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v)


def td(val, best=False, cls=""):
    c = f' class="lb-num{" lb-best" if best else ""}{" "+cls if cls else ""}"'
    s = fmt_cell(val)
    inner = f"<strong>{escape(s)}</strong>" if best else escape(s)
    return f"<td{c}>{inner}</td>"


def tdl(val):
    return f'<td class="lb-model">{escape(val)}</td>'


def route_row(model, typ, vals, best_mask):
    # vals: 15 numbers (5 groups x 3)
    parts = [tdl(model), f'<td class="lb-type">{escape(typ)}</td>']
    for i, v in enumerate(vals):
        parts.append(td(v, best=bool(best_mask[i])))
    return "<tr>" + "".join(parts) + "</tr>"


# Route planning: (model, type, 15 values, 15 bool best)
route_metro_os = [
    ("Qwen3-VL-8B-Instruct", "Instruct", [2.75, 17.58, 67, 25.69, 46.44, 1018, 21.25, 41.30, 785, 19.31, 39.31, 728, 4.69, 21.87, 137], [0] * 15),
    ("Qwen3-VL-8B-Thinking", "Thinking", [5.12, 20.99, 132, 31.69, 49.76, 1276, 38.00, 57.06, 1669, 23.75, 41.69, 948, 6.38, 22.93, 194], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("Qwen3-VL-2B-Instruct", "Instruct", [0.94, 15.14, 26, 9.88, 27.61, 371, 6.63, 23.85, 232, 7.00, 26.91, 289, 2.00, 17.82, 58], [0] * 15),
    ("Qwen2.5-VL-7B-Instruct", "Instruct", [0.94, 15.02, 21, 14.00, 31.20, 535, 11.69, 28.32, 441, 7.94, 20.77, 318, 3.38, 18.09, 101], [0] * 15),
    ("Phi-3.5-Vision-Instruct-4B", "Instruct", [0.06, 10.40, 1, 10.87, 27.92, 402, 6.63, 22.14, 208, 2.75, 12.27, 99, 0.81, 12.94, 13], [0] * 15),
    ("Phi-4-Multimodal-Instruct-6B", "Instruct", [0.00, 9.75, 0, 2.13, 12.52, 66, 2.13, 11.78, 85, 1.75, 9.51, 52, 0.44, 9.02, 7], [0] * 15),
    ("InternVL3-8B-Instruct", "Instruct", [0.13, 13.98, 2, 10.50, 29.57, 414, 12.81, 31.83, 488, 9.00, 24.73, 377, 1.75, 17.0, 68], [0] * 15),
    ("Qwen3-VL-30B-A3B-Instruct", "Instruct", [3.31, 19.26, 102, 23.69, 44.33, 961, 22.56, 43.58, 914, 19.00, 40.03, 724, 6.75, 26.22, 218], [0] * 15),
    ("Qwen3-VL-32B-Instruct", "Instruct", [6.31, 22.23, 181, 31.87, 54.45, 1270, 32.12, 54.54, 1339, 28.50, 50.06, 1181, 6.56, 24.43, 187], [0] * 15),
    ("Qwen3-VL-32B-Thinking", "Thinking", [13.31, 29.43, 437, 31.81, 54.94, 1276, 44.12, 62.77, 2078, 26.56, 51.48, 1060, 9.19, 28.89, 278], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
]

route_metro_cs = [
    ("GPT-4o", "Instruct", [6.63, 25.61, 205, 42.38, 64.07, 2112, 40.69, 62.40, 1944, 35.63, 55.51, 1630, 11.31, 31.11, 398], [0] * 15),
    ("GPT-4.1", "Instruct", [7.94, 25.52, 235, 48.56, 67.07, 2523, 46.81, 65.18, 2413, 41.81, 62.88, 2038, 14.06, 35.98, 515], [0] * 15),
    ("Gemini-3-Flash-Preview", "Instruct", [37.06, 57.15, 2046, 74.75, 84.99, 5345, 73.06, 83.37, 5171, 69.19, 76.14, 4765, 53.87, 65.84, 3294], [1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1]),
    ("Doubao-Seed-1-6-251015-w/o", "No-Thinking", [8.13, 24.60, 233, 46.94, 66.98, 2394, 48.06, 66.95, 2533, 40.56, 62.11, 2088, 13.81, 35.61, 494], [0] * 15),
    ("Doubao-Seed-1-6-251015-Thinking", "Thinking", [12.06, 30.49, 461, 74.38, 86.23, 4996, 74.00, 85.68, 4964, 76.06, 83.41, 5029, 22.03, 42.48, 984], [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0]),
    ("Qwen-VL-Plus-w/o", "No-Thinking", [4.81, 21.83, 133, 36.88, 58.69, 1643, 38.25, 58.59, 1706, 31.62, 52.92, 1355, 6.94, 27.69, 229], [0] * 15),
    ("Qwen-VL-Plus-Thinking", "Thinking", [10.75, 29.11, 349, 61.50, 76.62, 3576, 62.19, 76.42, 3648, 45.75, 64.46, 2318, 16.38, 37.44, 582], [0] * 15),
]

route_travel_os = [
    ("Qwen3-VL-8B-Instruct", "Instruct", [19.29, 42.50, 1190, 44.05, 61.66, 3051, 43.33, 61.39, 3008, 34.52, 55.56, 2330, 15.65, 40.97, 869], [0] * 15),
    ("Qwen3-VL-8B-Thinking", "Thinking", [22.62, 45.94, 1345, 74.17, 82.41, 5319, 82.68, 88.54, 6268, 33.15, 55.60, 2088, 12.74, 38.10, 705], [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("Qwen3-VL-2B-Instruct", "Instruct", [8.45, 34.30, 500, 11.25, 32.35, 763, 19.17, 45.68, 1210, 12.14, 40.47, 787, 3.15, 30.69, 164], [0] * 15),
    ("Qwen2.5-VL-7B-Instruct", "Instruct", [7.68, 30.48, 431, 21.07, 38.15, 1322, 24.82, 42.02, 1508, 15.60, 37.47, 902, 4.70, 28.84, 235], [0] * 15),
    ("Phi-3.5-Vision-Instruct-4B", "Instruct", [0.12, 20.00, 8, 12.20, 34.81, 778, 9.82, 31.87, 620, 4.46, 23.21, 263, 1.31, 22.68, 81], [0] * 15),
    ("Phi-4-Multimodal-Instruct-6B", "Instruct", [0.42, 19.26, 21, 7.20, 17.63, 479, 5.30, 15.93, 318, 1.73, 9.36, 115, 1.43, 18.96, 63], [0] * 15),
    ("InternVL3-8B-Instruct", "Instruct", [6.61, 29.21, 309, 29.58, 49.69, 1821, 29.40, 50.16, 1865, 13.57, 36.78, 933, 2.50, 24.28, 136], [0] * 15),
    ("Qwen3-VL-30B-A3B-Instruct", "Instruct", [17.86, 44.15, 1098, 50.95, 65.36, 3458, 53.75, 67.71, 3747, 38.45, 58.02, 2738, 9.70, 37.93, 578], [0] * 15),
    ("Qwen3-VL-32B-Instruct", "Instruct", [36.90, 57.44, 2431, 64.52, 76.16, 4704, 68.39, 78.99, 5184, 52.56, 69.18, 3770, 21.67, 47.34, 1299], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]),
    ("Qwen3-VL-32B-Thinking", "Thinking", [39.17, 58.84, 2650, 69.76, 79.60, 5149, 91.79, 94.55, 7287, 42.32, 62.99, 2931, 19.94, 46.73, 1201], [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0]),
]

route_travel_cs = [
    ("GPT-4o", "Instruct", [16.85, 40.98, 930, 65.06, 75.84, 4651, 62.74, 74.11, 4467, 46.07, 63.07, 3069, 12.08, 38.07, 675], [0] * 15),
    ("GPT-4.1", "Instruct", [20.30, 43.24, 1226, 74.82, 82.98, 5571, 70.89, 79.84, 5211, 54.70, 69.59, 3917, 15.06, 40.67, 862], [0] * 15),
    # Travel Gemini: Map-only all; Edge DS only; Map+Vertex2 all
    ("Gemini-3-Flash-Preview", "Instruct", [60.00, 73.20, 4469, 98.27, 98.38, 8190, 94.40, 94.87, 7757, 78.51, 82.40, 6459, 43.51, 60.11, 3250], [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1]),
    ("Doubao-Seed-1-6-251015-w/o", "No-Thinking", [33.04, 54.15, 2193, 73.51, 82.16, 5425, 76.85, 84.04, 5812, 56.25, 71.46, 4031, 25.48, 49.54, 1610], [0] * 15),
    ("Doubao-Seed-1-6-251015-Thinking", "Thinking", [38.45, 58.46, 2735, 98.39, 98.87, 8178, 97.86, 98.47, 8127, 83.15, 89.08, 6672, 25.30, 48.90, 1678], [0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0]),
    ("Qwen-VL-Plus-w/o", "No-Thinking", [30.60, 52.64, 1935, 64.23, 76.45, 4656, 69.64, 79.78, 5133, 53.99, 70.07, 3842, 22.92, 47.65, 1417], [0] * 15),
    ("Qwen-VL-Plus-Thinking", "Thinking", [38.27, 58.94, 2539, 64.35, 76.53, 4670, 94.23, 96.04, 7570, 56.19, 70.84, 4042, 23.21, 47.18, 1481], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
]


def emit_route_table():
    h = []
    h.append('<table class="lb-table">')
    h.append("<thead><tr>")
    h.append('<th rowspan="2" class="lb-th-model">Model</th><th rowspan="2" class="lb-th-type">Type</th>')
    h.append(f'<th colspan="3" style="background:{FC}">Map-only</th>')
    h.append(f'<th colspan="3" style="background:{CC}">Edge-only</th>')
    h.append(f'<th colspan="3" style="background:{IC}">Map+Edge</th>')
    h.append(f'<th colspan="3" style="background:{FC}">Map+Edge+Vertex</th>')
    h.append(f'<th colspan="3" style="background:{CC}">Map+Vertex2</th>')
    h.append("</tr><tr>")
    for _ in range(5):
        h.append("<th>EMA</th><th>PMA</th><th>DS</th>")
    h.append("</tr></thead><tbody>")

    def sec(title):
        h.append(f'<tr class="lb-sec"><td colspan="17"><em><strong>{title}</strong></em></td></tr>')

    def sub(title):
        h.append(f'<tr class="lb-subh"><td colspan="17"><em><strong>{title}</strong></em></td></tr>')

    sec("Scenario: MetroMap")
    sub("Open-source Models")
    for m, t, v, b in route_metro_os:
        h.append(route_row(m, t, v, b))
    h.append('<tr class="lb-mid"><td colspan="17"></td></tr>')
    sub("Closed-source Models")
    for m, t, v, b in route_metro_cs:
        h.append(route_row(m, t, v, b))

    h.append('<tr class="lb-heavy"><td colspan="17"></td></tr>')

    sec("Scenario: TravelMap")
    sub("Open-source Models")
    for m, t, v, b in route_travel_os:
        h.append(route_row(m, t, v, b))
    h.append('<tr class="lb-mid"><td colspan="17"></td></tr>')
    sub("Closed-source Models")
    for m, t, v, b in route_travel_cs:
        h.append(route_row(m, t, v, b))

    h.append("</tbody></table>")
    return "\n".join(h)


def qa_td(v, best=False):
    return td(v, best)


def qa_row(model, typ, vals, best_mask):
    # 12 values
    parts = [tdl(model), f'<td class="lb-type">{escape(typ)}</td>']
    for i, v in enumerate(vals):
        parts.append(qa_td(v, bool(best_mask[i])))
    return "<tr>" + "".join(parts) + "</tr>"


# QA rows: (model, type, 12 floats, 12 bool)
qa_mm_os = [
    ("Qwen3-VL-8B-Instruct", "Instruct", [55.00, 17.50, 73.12, 22.50, 100.0, 7.50, 57.50, 51.88, 86.88, 0.63, 22.50, 38.75], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("Qwen3-VL-8B-Thinking", "Thinking", [53.12, 28.12, 51.25, 56.87, 99.38, 56.87, 79.37, 77.50, 98.12, 7.50, 9.38, 35.63], [0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0]),
    ("Qwen3-VL-2B-Instruct", "Instruct", [8.13, 5.00, 63.12, 3.75, 87.50, 3.12, 26.25, 11.25, 64.38, 0.00, 8.13, 26.87], [0] * 12),
    ("Qwen2.5-VL-7B-Instruct", "Instruct", [48.75, 15.62, 66.25, 15.62, 100.0, 10.00, 44.37, 60.62, 87.50, 1.25, 25.62, 33.12], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("Phi-3.5-Vision-Instruct-4B", "Instruct", [58.13, 18.75, 78.12, 22.50, 100.0, 21.88, 53.75, 66.87, 98.12, 0.63, 21.25, 40.00], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("Phi-4-Multimodal-Instruct-6B", "Instruct", [60.62, 40.62, 80.00, 41.25, 93.13, 42.50, 58.75, 92.50, 99.38, 5.63, 35.63, 49.38], [1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1]),
    ("InternVL3-8B-Instruct", "Instruct", [35.00, 20.62, 65.00, 7.50, 83.13, 3.12, 33.75, 10.00, 70.63, 0.00, 12.50, 28.12], [0] * 12),
    ("Qwen3-VL-30B-A3B-Instruct", "Instruct", [20.62, 16.25, 60.62, 0.63, 68.75, 1.25, 0.00, 1.25, 68.75, 0.00, 11.25, 18.12], [0] * 12),
    ("Qwen3-VL-32B-Instruct", "Instruct", [5.00, 0.00, 38.12, 10.62, 78.12, 3.12, 16.25, 4.37, 73.12, 0.00, 7.50, 23.75], [0] * 12),
    ("Qwen3-VL-32B-Thinking", "Thinking", [26.87, 19.38, 50.00, 5.00, 99.38, 5.00, 21.25, 25.00, 85.62, 0.00, 6.88, 60.62], [0] * 12),
]

qa_mm_cs = [
    ("GPT4-o", "Instruct", [62.50, 13.75, 78.75, 31.87, 100.0, 28.12, 55.63, 78.12, 100.0, 3.75, 29.38, 45.00], [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]),
    ("GPT4.1", "Instruct", [61.88, 26.87, 76.25, 50.62, 99.38, 38.12, 64.38, 83.75, 100.0, 3.12, 25.62, 49.38], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
    ("Gemini-3-Flash-Preview", "Instruct", [59.38, 82.50, 93.13, 91.25, 98.12, 75.62, 88.75, 94.37, 100.0, 48.13, 80.00, 94.37], [0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1]),
    ("Doubao-Seed-1-6-251015-w/o_Thinking", "No-Thinking", [55.63, 20.62, 76.25, 41.88, 100.0, 59.38, 58.13, 86.25, 99.38, 3.75, 49.38, 50.62], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("Doubao-Seed-1-6-251015-Thinking", "Thinking", [54.37, 40.62, 77.50, 72.50, 100.0, 69.37, 96.25, 98.75, 100.0, 27.50, 50.00, 53.12], [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0]),
    ("Qwen-VL-Plus-w/o_Thinking", "No-Thinking", [60.00, 21.88, 78.75, 40.62, 100.0, 40.00, 64.38, 77.50, 97.50, 1.25, 25.62, 40.62], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("Qwen-VL-Plus-Thinking", "Thinking", [57.50, 45.00, 81.87, 68.75, 100.0, 71.25, 90.62, 95.63, 100.0, 13.75, 46.25, 55.63], [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0]),
]

qa_tm_os = [
    ("Qwen3-VL-8B-Instruct", "Instruct", [7.14, 60.12, 52.98, 17.86, 99.40, 45.24, 38.69, 50.60, 61.31, 75.60, 70.24, 14.29], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]),
    ("Qwen3-VL-8B-Thinking", "Thinking", [39.29, 70.83, 52.38, 87.50, 100.0, 39.88, 100.0, 100.0, 100.0, 63.10, 69.05, 13.69], [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0]),
    ("Qwen3-VL-2B-Instruct", "Instruct", [12.50, 58.93, 9.52, 6.00, 94.64, 64.88, 1.19, 46.43, 38.10, 64.29, 67.86, 4.17], [0] * 12),
    ("Qwen2.5-VL-7B-Instruct", "Instruct", [4.76, 65.48, 54.17, 38.10, 99.40, 47.62, 17.26, 87.50, 79.76, 33.93, 68.45, 16.07], [0] * 12),
    ("Phi-3.5-Vision-Instruct-4B", "Instruct", [13.10, 48.21, 59.52, 39.88, 99.40, 41.07, 50.00, 75.60, 77.38, 72.02, 74.40, 10.71], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
    ("Phi-4-Multimodal-Instruct-6B", "Instruct", [44.05, 70.24, 58.93, 78.57, 98.81, 33.93, 96.43, 98.21, 100.0, 73.21, 69.05, 17.86], [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1]),
    ("InternVL3-8B-Instruct", "Instruct", [12.50, 59.52, 35.71, 8.93, 97.62, 49.40, 10.71, 50.00, 51.79, 70.83, 67.86, 4.76], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
    ("Qwen3-VL-30B-A3B-Instruct", "Instruct", [5.95, 50.60, 6.55, 7.74, 86.31, 52.38, 8.93, 44.64, 45.24, 54.76, 35.12, 2.98], [0] * 12),
    ("Qwen3-VL-32B-Instruct", "Instruct", [0.00, 42.26, 14.88, 11.31, 63.69, 38.31, 18.45, 45.83, 47.62, 27.98, 63.69, 5.95], [0] * 12),
    ("Qwen3-VL-32B-Thinking", "Thinking", [8.33, 60.12, 23.21, 1.19, 97.02, 44.64, 10.12, 38.69, 56.55, 69.05, 66.67, 5.95], [0] * 12),
]

qa_tm_cs = [
    ("GPT4-o", "Instruct", [11.31, 63.69, 49.40, 47.02, 100.0, 36.31, 53.57, 99.40, 67.26, 71.43, 73.21, 11.31], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("GPT4.1", "Instruct", [3.57, 69.64, 55.95, 47.02, 100.0, 42.86, 66.07, 100.0, 69.64, 73.21, 77.38, 17.86], [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]),
    ("Gemini-3-Flash-Preview", "Instruct", [45.83, 85.12, 77.98, 97.62, 99.40, 86.31, 100.0, 99.40, 100.0, 85.71, 81.55, 26.19], [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1]),
    ("Doubao-Seed-1-6-251015-w/o_Thinking", "No-Thinking", [22.62, 58.93, 50.00, 63.10, 98.81, 51.79, 54.76, 100.0, 98.81, 66.07, 76.79, 25.60], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
    ("Doubao-Seed-1-6-251015-Thinking", "Thinking", [24.40, 71.43, 55.95, 95.83, 84.52, 71.43, 97.62, 100.0, 100.0, 78.57, 72.02, 22.02], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]),
    ("Qwen-VL-Plus-w/o_Thinking", "No-Thinking", [19.64, 72.02, 52.98, 48.81, 100.0, 35.71, 57.74, 98.81, 82.74, 54.17, 70.24, 19.64], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("Qwen-VL-Plus-Thinking", "Thinking", [24.40, 67.86, 62.50, 98.81, 100.0, 34.52, 100.0, 100.0, 100.0, 69.05, 72.62, 24.40], [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0]),
]


def emit_qa_table():
    h = []
    h.append('<table class="lb-table lb-table-qa">')
    h.append("<thead><tr>")
    h.append('<th rowspan="2" class="lb-th-model">Model</th><th rowspan="2" class="lb-th-type">Type</th>')
    h.append(f'<th colspan="3" style="background:{FC}">Map (M)</th>')
    h.append(f'<th colspan="3" style="background:{CC}">Edge (E)</th>')
    h.append(f'<th colspan="3" style="background:{IC}">Vertex (V)</th>')
    h.append(f'<th colspan="3" style="background:{MC}">Map+Vertex (M+V)</th>')
    h.append("</tr><tr>")
    for _ in range(4):
        h.append("<th>GP</th><th>LP</th><th>SR</th>")
    h.append("</tr></thead><tbody>")

    def sec(title):
        h.append(f'<tr class="lb-sec"><td colspan="14"><strong>{title}</strong></td></tr>')

    def sub(title):
        h.append(f'<tr class="lb-subh"><td colspan="14"><em>{title}</em></td></tr>')

    sec("Scenario: MetroMap")
    sub("Open-source Models")
    for m, t, v, b in qa_mm_os:
        h.append(qa_row(m, t, v, b))
    h.append('<tr class="lb-mid"><td colspan="14"></td></tr>')
    sub("Closed-source Models")
    for m, t, v, b in qa_mm_cs:
        h.append(qa_row(m, t, v, b))

    h.append('<tr class="lb-mid"><td colspan="14"></td></tr>')
    sec("Scenario: TravelMap")
    sub("Open-source Models")
    for m, t, v, b in qa_tm_os:
        h.append(qa_row(m, t, v, b))
    h.append('<tr class="lb-mid"><td colspan="14"></td></tr>')
    sub("Closed-source Models")
    for m, t, v, b in qa_tm_cs:
        h.append(qa_row(m, t, v, b))

    h.append("</tbody></table>")
    return "\n".join(h)


PAGE_STYLE = """
  <style>
    /* ReasonMap-style: light page, narrow reading column, centered blocks */
    body.maptab-body {
      background: #fff;
      color: #222;
    }
    body.maptab-body .navbar {
      background: #fff;
      border-bottom: 1px solid #eee;
      min-height: 2.75rem;
    }
    .maptab-narrow {
      max-width: 820px;
      margin-left: auto;
      margin-right: auto;
    }
    .maptab-hero {
      font-family: 'Noto Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    .maptab-hero .hero-body {
      padding-top: 2.5rem;
      padding-bottom: 1.5rem;
    }
    .maptab-hero .publication-title {
      max-width: 56rem;
      margin-left: auto;
      margin-right: auto;
      text-align: center !important;
      color: #111 !important;
      font-family: 'Google Sans', 'Noto Sans', sans-serif !important;
      font-size: clamp(1.65rem, 4.2vw, 2.85rem) !important;
      font-weight: 700 !important;
      line-height: 1.22;
      letter-spacing: -0.02em;
    }
    .maptab-author-names {
      max-width: 42rem;
      margin: 0 auto 0.6rem;
      text-align: center;
      font-size: clamp(0.92rem, 1.9vw, 1.06rem);
      font-weight: 500;
      color: #333;
      line-height: 1.55;
    }
    .maptab-author-names sup {
      font-size: 0.72em;
      font-weight: 600;
    }
    .maptab-year {
      display: block;
      text-align: center;
      font-size: 1.35rem;
      font-weight: 600;
      color: #222;
      margin: 0.35rem 0 0.85rem;
      letter-spacing: 0.02em;
    }
    .maptab-affiliations {
      max-width: 38rem;
      margin: 0 auto 0.35rem;
      text-align: center;
      font-size: 0.9rem;
      font-weight: 400;
      color: #444;
      line-height: 1.5;
    }
    .maptab-affiliations .affil-line {
      display: block;
      margin-bottom: 0.15rem;
    }
    .maptab-affiliations sup {
      font-size: 0.75em;
      font-weight: 600;
      margin-right: 0.12em;
    }
    .maptab-author-notes {
      max-width: 38rem;
      margin: 0.4rem auto 0;
      text-align: center;
      font-size: 0.84rem;
      font-weight: 400;
      color: #555;
      line-height: 1.5;
    }
    .maptab-author-notes sup {
      font-size: 0.75em;
      font-weight: 600;
    }
    .maptab-note-gap {
      display: inline-block;
      width: 1.35rem;
    }
    .maptab-email {
      font-family: ui-monospace, 'SFMono-Regular', Menlo, Consolas, monospace;
      font-size: 0.95em;
      color: #333;
    }
    .maptab-logo-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      gap: 1.5rem;
      margin-top: 0.85rem;
    }
    .maptab-logo-row figure {
      margin: 0 !important;
    }
    .maptab-link-row {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      align-items: center;
      gap: 0.45rem;
      margin-top: 1rem;
    }
    .maptab-pill {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: #000 !important;
      color: #fff !important;
      border: none !important;
      border-radius: 999px !important;
      padding: 0.42rem 1.1rem !important;
      height: auto !important;
      font-size: 0.8rem !important;
      font-weight: 500 !important;
      font-family: inherit;
      text-decoration: none !important;
      line-height: 1.2;
      box-shadow: none;
    }
    .maptab-pill:hover {
      color: #fff !important;
      background: #1f1f1f !important;
    }
    .maptab-hero .publication-authors {
      max-width: 40rem;
      margin-left: auto;
      margin-right: auto;
    }
    .maptab-hero .publication-links {
      justify-content: center;
    }
    .maptab-teaser {
      background: transparent;
    }
    .maptab-teaser .maptab-teaser-outer {
      max-width: 100%;
      width: 100%;
      padding-left: 1rem;
      padding-right: 1rem;
      margin: 0 auto;
    }
    .maptab-teaser .hero-body {
      padding-top: 0.5rem;
      padding-bottom: 1.25rem;
    }
    .maptab-teaser-img {
      display: block;
      margin: 0 auto;
      width: 60vw;
      max-width: 100%;
      height: auto;
      object-fit: contain;
    }
    .maptab-teaser .content {
      max-width: min(42rem, 90vw);
      margin: 0.85rem auto 0;
      font-size: 0.95rem;
      line-height: 1.55;
      text-align: center;
      color: #444;
    }
    body.maptab-body .section {
      padding-top: 1.75rem;
      padding-bottom: 1.75rem;
      background: transparent;
    }
    body.maptab-body .section h2.title.is-3 {
      font-size: 1.35rem !important;
      font-weight: 600;
      margin-bottom: 0.75rem;
    }
    body.maptab-body #BibTeX pre {
      font-size: 0.78rem;
      border-radius: 6px;
      background: #fff;
      border: 1px solid #eaeaea;
    }
    /* Compact leaderboards: centered like ReasonMap, scroll inside card */
    .maptab-lb-section .container {
      max-width: 880px;
      margin-left: auto;
      margin-right: auto;
    }
    .maptab-lb-section h2.title {
      text-align: center;
    }
    .lb-wrap {
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      margin: 0.75rem auto 0;
      padding: 0.35rem 0.3rem;
      border: 1px solid #e8e8e8;
      border-radius: 6px;
      background: #fff;
      box-shadow: 0 1px 2px rgba(0,0,0,0.04);
      max-width: 100%;
    }
    .lb-table {
      border-collapse: collapse;
      font-size: 0.5rem;
      min-width: max-content;
      width: max-content;
      margin: 0 auto;
      background: #fff;
    }
    .lb-table th, .lb-table td {
      border: 1px solid #c8c8c8;
      padding: 0.12rem 0.2rem;
      vertical-align: middle;
      line-height: 1.25;
    }
    .lb-th-model, .lb-th-type { background: #F2F2F2 !important; font-weight: 600; }
    .lb-model { text-align: left; white-space: nowrap; max-width: 9.5rem; }
    .lb-type { text-align: center; white-space: nowrap; }
    .lb-num { text-align: center; }
    .lb-best { background: #D9D9D9 !important; font-weight: 700; }
    .lb-sec td { background: #E7F3FF !important; text-align: center; font-size: 0.58rem; }
    .lb-subh td { text-align: left; font-style: italic; background: #fafafa !important; font-size: 0.52rem; }
    .lb-mid td { height: 3px; padding: 0; border: none; background: transparent !important; }
    .lb-heavy td { border-top: 2px solid #363636; height: 0; padding: 0; background: transparent !important; }
    .lb-caption {
      font-size: 0.8rem;
      line-height: 1.45;
      text-align: center;
      margin: 0 auto 0.35rem;
      max-width: 44rem;
      color: #444;
    }
    .publication-authors .author-line { display: block; margin-bottom: 0.35rem; }
    body.maptab-body .maptab-pill.is-dark { background: #000; }
    .maptab-abstract h2.title.is-3 {
      text-align: center !important;
      width: 100%;
    }
    .maptab-abstract .content,
    .maptab-abstract h2 {
      max-width: 40rem;
      margin-left: auto;
      margin-right: auto;
    }
    .maptab-bib .title,
    .maptab-bib pre {
      max-width: 40rem;
      margin-left: auto;
      margin-right: auto;
    }
    .maptab-bib h2.title { text-align: center; }
    @media (max-width: 768px) {
      .maptab-teaser-img { width: 92vw; }
      .lb-table { font-size: 0.44rem; }
    }
  </style>
"""

ROUTE_CAPTION = (
    "Evaluation results of various Multimodal Large Language Models (MLLMs) on the MapTab path planning task "
    "<strong>MetroMap</strong> and <strong>TravelMap</strong> scenarios. EMA, PMA, and DS denote Exact Match Accuracy, "
    "Partial Match Accuracy, and Difficulty-aware Score, respectively. Map-only: map information only; Edge-only: edge data only; "
    "Map+Edge: map and edge data; Map+Edge+Vertex: map, edge, and vertex data; Map+Vertex2: map and merged vertex data (Vertex2_tab). "
    "We did not include Edge_tab + Vertex_tab because the comparison between it and Map + Vertex2_tab yielded conclusions consistent "
    "with those from the Map-only and Edge_tab-only control groups, without new findings. "
    "<strong>Bold</strong> values represent the best performance within open-source and closed-source groups, respectively."
)

QA_CAPTION = (
    "Performance of QA tasks across multiple MLLMs in the MetroMap and TravelMap scenarios. Regarding input modalities, M, E, and V "
    "denote Map, Edge_tab, and Vertex_tab, respectively. In the MetroMap scenario, the Vertex_tab paired with the Map input has the "
    "Line column removed to prevent excessive table information from affecting the evaluation of map-table coordination. "
    "Task types are categorized into three classes: Global Perception-based Reasoning Tasks (GP), Local Perception-based Reasoning Tasks (LP), "
    "and Spatial Relationship Judgment Tasks (SR). <strong>Bold</strong> values in the table indicate the best performance among "
    "open-source and closed-source models, respectively."
)

TEASER_BLURB = (
    "MapTab is a comprehensive benchmark designed to evaluate the map understanding and spatial reasoning "
    "capabilities of Vision-Language Models (VLMs). The benchmark focuses on two core tasks: route planning and "
    "map-based question answering, using both metro maps and travel maps."
)

ABSTRACT = """Systematic evaluation of Multimodal Large Language Models (MLLMs) is crucial for advancing  Artificial General Intelligence (AGI). However, existing benchmarks remain insufficient for rigorously assessing their reasoning capabilities under multi-criteria constraints. To bridge this gap, we introduce MapTab, a multimodal benchmark specifically designed to evaluate holistic multi-criteria reasoning in MLLMs via route planning tasks. MapTab requires MLLMs to perceive and ground visual cues from map images alongside route attributes (e.g., Time, Price) from structured tabular data. The benchmark encompasses two scenarios: Metromap, covering metro networks in 160 cities across 52 countries, and Travelmap, depicting 168 representative tourist attractions from 19 countries. In total, MapTab comprises 328 images, 196,800 route planning queries, and 3,936 QA queries, all incorporating 4 key criteria: Time, Price, Comfort, and Reliability. Extensive evaluations across 15 representative MLLMs reveal that current models face substantial challenges in multi-criteria multimodal reasoning. Notably, under conditions of limited visual perception, multimodal collaboration often underperforms compared to unimodal approaches. We believe MapTab provides a challenging and realistic testbed to advance the systematic evaluation of MLLMs."""

BIBTEX = r"""@article{shang2026maptab,
  title={MapTab: Can MLLMs Master Constrained Route Planning?},
  author={Shang, Ziqiao and Ge, Lingyue and Chen, Yang and Tian, Shi-Yu and Huang, Zhenyu and Fu, Wenbo and Li, Yu-Feng and Guo, Lan-Zhe},
  journal={arXiv preprint arXiv:2602.18600},
  year={2026}
}"""


def emit_index_html():
    title = "MapTab: Are MLLMs Ready for Multi-Criteria Route Planning in Heterogeneous Graphs?"
    title_html = escape(title)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="description" content="MapTab: multimodal benchmark for multi-criteria route planning with maps and tables.">
  <meta name="keywords" content="MapTab, MLLM, route planning, multimodal benchmark, heterogeneous graphs">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <link href="https://fonts.googleapis.com/css?family=Google+Sans|Noto+Sans|Castoro" rel="stylesheet">
  <link rel="stylesheet" href="./static/css/bulma.min.css">
  <link rel="stylesheet" href="./static/css/bulma-carousel.min.css">
  <link rel="stylesheet" href="./static/css/bulma-slider.min.css">
  <link rel="stylesheet" href="./static/css/fontawesome.all.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/jpswalsh/academicons@1/css/academicons.min.css">
  <link rel="stylesheet" href="./static/css/index.css">
{PAGE_STYLE}
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script defer src="./static/js/fontawesome.all.min.js"></script>
  <script src="./static/js/bulma-carousel.min.js"></script>
  <script src="./static/js/bulma-slider.min.js"></script>
  <script src="./static/js/index.js"></script>
</head>
<body class="maptab-body">
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <div class="navbar-menu">
      <div class="navbar-start" style="flex-grow: 1; justify-content: center;">
        <a class="navbar-item" href="#">
          <span class="icon"><i class="fas fa-home"></i></span>
        </a>
      </div>
    </div>
  </nav>

  <section class="hero maptab-hero">
    <div class="hero-body">
      <div class="container maptab-narrow">
        <div class="columns is-centered">
          <div class="column has-text-centered">
            <h1 class="title is-1 publication-title">{title_html}</h1>
            <div class="maptab-author-names">
              Ziqiao Shang<sup>1,2†</sup>, Lingyue Ge<sup>1,2†</sup>, Yang Chen<sup>1,2</sup>, Shi-Yu Tian<sup>1,2</sup>, Zhenyu Huang<sup>1,2</sup>,<br>
              Wenbo Fu<sup>1,2</sup>, Yu-Feng Li<sup>1,2</sup>, Lan-Zhe Guo<sup>1,2*</sup>
            </div>
            <span class="maptab-year">2026</span>
            <div class="maptab-affiliations">
              <span class="affil-line"><sup>1</sup>National Key Laboratory for Novel Software Technology, Nanjing University, Nanjing, China</span>
              <span class="affil-line"><sup>2</sup>School of Intelligence Science and Technology, Nanjing University, Suzhou, China</span>
            </div>
            <div class="maptab-author-notes">
              <span><sup>†</sup>Equal contribution</span><span class="maptab-note-gap" aria-hidden="true"></span><span><sup>*</sup>Corresponding author: <span class="maptab-email">guolz@lamda.nju.edu.cn</span></span>
            </div>
            <div class="maptab-logo-row">
              <figure class="image">
                <img src="figure/nanjing_university.jpg" alt="Nanjing University" style="height: 76px; object-fit: contain;">
              </figure>
              <figure class="image">
                <img src="figure/lamda.png" alt="LAMDA" style="height: 76px; object-fit: contain;">
              </figure>
            </div>
            <div class="maptab-link-row">
              <a href="https://arxiv.org/abs/2602.18600" class="maptab-pill" target="_blank" rel="noopener noreferrer">ArXiv</a>
              <a href="https://github.com/Ziqiao-Shang/MapTab" class="maptab-pill" target="_blank" rel="noopener noreferrer">Code</a>
              <a href="https://huggingface.co/datasets/szq-nju/MapTab" class="maptab-pill" target="_blank" rel="noopener noreferrer">Dataset</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="hero teaser maptab-teaser">
    <div class="container maptab-teaser-outer">
      <div class="hero-body">
        <div class="has-text-centered">
          <img class="maptab-teaser-img" src="./figure/fig_1.png" alt="MapTab overview">
        </div>
        <div class="content">
          {escape(TEASER_BLURB)}
        </div>
      </div>
    </div>
  </section>

  <section class="section maptab-abstract">
    <div class="container maptab-narrow">
      <h2 class="title is-3 has-text-centered">Abstract</h2>
      <div class="content has-text-justified">
        {escape(ABSTRACT)}
      </div>
    </div>
  </section>

  <section class="section maptab-lb-section">
    <div class="container">
      <h2 class="title is-3">Route planning leaderboard</h2>
      <p class="lb-caption">{ROUTE_CAPTION}</p>
      <div class="lb-wrap">
{emit_route_table()}
      </div>
    </div>
  </section>

  <section class="section maptab-lb-section">
    <div class="container">
      <h2 class="title is-3">QA leaderboard</h2>
      <p class="lb-caption">{QA_CAPTION}</p>
      <div class="lb-wrap">
{emit_qa_table()}
      </div>
    </div>
  </section>

  <section class="section maptab-bib" id="BibTeX">
    <div class="container maptab-narrow content">
      <h2 class="title">BibTeX</h2>
      <pre><code>{escape(BIBTEX)}</code></pre>
    </div>
  </section>

  <footer class="footer" style="background:transparent;padding:2rem 1rem;">
    <div class="has-text-centered container maptab-narrow">
      <div class="content">
        This website is borrowed from <a href="https://github.com/nerfies/nerfies.github.io">nerfies</a>.
      </div>
    </div>
  </footer>
</body>
</html>
"""


if __name__ == "__main__":
    (ROOT / "_route_table.html").write_text(emit_route_table(), encoding="utf-8")
    (ROOT / "_qa_table.html").write_text(emit_qa_table(), encoding="utf-8")
    (ROOT / "index.html").write_text(emit_index_html(), encoding="utf-8")
    print("Wrote index.html, _route_table.html, _qa_table.html")
