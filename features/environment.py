import os
import textwrap
import time

import allure
from PIL import Image, ImageDraw, ImageFont

SCREENSHOT_DIR = "screenshots"


def before_scenario(context, scenario):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def after_step(context, step):
    """On a failed step, build a placeholder 'screenshot' and attach it to Allure."""
    if step.status != "failed":
        return

    error = str(step.exception) if step.exception else "No exception message"
    lines = [
        "API TEST FAILURE",
        "",
        f"Scenario: {context.scenario.name}",
        f"Step: {step.keyword} {step.name}",
        "",
        "Error:",
    ] + textwrap.wrap(error, width=95)[:8]

    image = Image.new("RGB", (900, 420), color=(30, 30, 30))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    y = 25
    for i, line in enumerate(lines):
        colour = (255, 80, 80) if i == 0 else (255, 255, 255)
        draw.text((30, y), line, fill=colour, font=font)
        y += 24

    path = os.path.join(SCREENSHOT_DIR, f"failure_{int(time.time() * 1000)}.png")
    image.save(path)

    allure.attach.file(
        path,
        name="API Failure Screenshot",
        attachment_type=allure.attachment_type.PNG,
    )


def after_scenario(context, scenario):
    """Delete any bin the scenario created so the JSONBin account stays clean."""
    client = getattr(context, "client", None)
    bin_id = getattr(context, "bin_id", None)

    if client and bin_id and not getattr(context, "bin_deleted", False):
        try:
            client.delete_bin(bin_id)
        except Exception as exc:  # cleanup must never fail the test run
            print(f"Cleanup warning: could not delete bin {bin_id}: {exc}")
