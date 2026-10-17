"""GEOINT — Geographic Intelligence Module — Phase: ANALYSE"""
from modules import BaseModule
from utils.banner import print_result

class GeointModule(BaseModule):
    """Analyse GPS coordinates and generate map/satellite links."""
    def run(self) -> dict:
        coords = self.target
        results = {"input": coords, "links": {}}
        self.info(f"[GEOINT] Analysing coordinates: {coords}")
        try:
            lat, lon = [float(x.strip()) for x in coords.split(",")]
            results["latitude"]  = lat
            results["longitude"] = lon
            results["links"] = {
                "Google Maps":    f"https://www.google.com/maps?q={lat},{lon}",
                "Google Satellite": f"https://www.google.com/maps/@{lat},{lon},18z/data=!3m1!1e3",
                "OpenStreetMap":  f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=15",
                "What3Words":     f"https://what3words.com/map?lat={lat}&lng={lon}",
            }
            for name, link in results["links"].items():
                print_result(name, link, color="cyan")
        except Exception as e:
            self.warn("Input must be 'latitude, longitude' (e.g. 48.8566, 2.3522)")
            results["error"] = str(e)
        return results
