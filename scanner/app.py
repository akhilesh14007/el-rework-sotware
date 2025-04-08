import os
import shutil
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

# Machines and their EL folder paths
ALL_SHIFT_PATHS = {
    "ShiftA": [
        r"\\192.168.0.230\thinkEYE\ThinkEyes_EL",
        r"\\192.168.0.251\thinkeye el1\ThinkEyes_EL"
    ],
    "ShiftB": [
        r"\\192.168.0.230\thinkEYE\ThinkEyes_EL",
        r"\\192.168.0.251\thinkeye el1\ThinkEyes_EL"
    ],
}


def get_current_date_folder():
    now = datetime.now()
    return now.strftime(r"%Y_%m\%m_%d")


def build_all_ng_paths(panel_number):
    """
    Build all possible NG image paths from both machines and both shifts.
    """
    date_folder = get_current_date_folder()
    extensions = ["jpg", "jpeg", "png"]
    possible_paths = []

    for shift, machine_paths in ALL_SHIFT_PATHS.items():
        for base_folder in machine_paths:
            ng_folder = os.path.join(base_folder, date_folder, shift, "NG")
            for ext in extensions:
                full_path = os.path.join(ng_folder, f"{panel_number}.{ext}")
                possible_paths.append(full_path)

    return possible_paths


@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None

    if request.method == "POST":
        panel_number = request.form.get("panel_number", "").strip()
        if panel_number:
            for path in build_all_ng_paths(panel_number):
                if os.path.exists(path):
                    destination = os.path.join("static", "images", os.path.basename(path))
                    os.makedirs(os.path.dirname(destination), exist_ok=True)
                    shutil.copy(path, destination)
                    image_url = f"/static/images/{os.path.basename(path)}?v={datetime.now().timestamp()}"
                    break

    return render_template("index.html", image_url=image_url)


if __name__ == "__main__":
    app.run(debug=True)
