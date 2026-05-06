"""
Image EXIF & GPS Extraction Module
Phase: INVESTIGATE
"""

import os
import exifread
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from modules import BaseModule
from utils.banner import print_result


def _dms_to_decimal(dms, ref):
    """Convert GPS DMS tuple to decimal degrees."""
    try:
        d = float(dms[0].num) / float(dms[0].den)
        m = float(dms[1].num) / float(dms[1].den)
        s = float(dms[2].num) / float(dms[2].den)
        decimal = d + m / 60.0 + s / 3600.0
        if ref in ["S", "W"]:
            decimal = -decimal
        return round(decimal, 6)
    except Exception:
        return None


class ExifGPSModule(BaseModule):
    """Extract EXIF metadata and GPS coordinates from image files."""

    def run(self) -> dict:
        results = {
            "file":     self.target,
            "exists":   False,
            "exif":     {},
            "gps":      {},
            "map_url":  None,
        }

        if not os.path.isfile(self.target):
            self.warn(f"File not found: {self.target}")
            results["error"] = "File not found"
            return results

        results["exists"] = True
        self.info(f"[EXIF] Analysing: {self.target}")

        # exifread for raw tags
        try:
            with open(self.target, "rb") as f:
                tags = exifread.process_file(f, details=True)

            for tag, value in tags.items():
                results["exif"][tag] = str(value)
                if self.verbose:
                    print_result(tag, str(value)[:80])
        except Exception as e:
            self.warn(f"exifread error: {e}")

        # PIL for GPS
        try:
            img       = Image.open(self.target)
            exif_data = img._getexif()
            if exif_data:
                gps_info = {}
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "GPSInfo":
                        for gps_tag_id, gps_value in value.items():
                            gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            gps_info[gps_tag] = gps_value

                if gps_info:
                    lat = _dms_to_decimal(
                        gps_info.get("GPSLatitude", []),
                        gps_info.get("GPSLatitudeRef", "N"),
                    )
                    lon = _dms_to_decimal(
                        gps_info.get("GPSLongitude", []),
                        gps_info.get("GPSLongitudeRef", "E"),
                    )
                    if lat and lon:
                        results["gps"] = {"latitude": lat, "longitude": lon}
                        results["map_url"] = (
                            f"https://www.google.com/maps?q={lat},{lon}"
                        )
                        print_result("GPS Latitude",  lat,  color="cyan")
                        print_result("GPS Longitude", lon,  color="cyan")
                        print_result("Google Maps",   results["map_url"], color="green")
                    else:
                        print_result("GPS", "No GPS data found", color="yellow")
        except Exception as e:
            self.warn(f"PIL GPS parse error: {e}")

        return results
