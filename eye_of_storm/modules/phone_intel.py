"""Phone Number Intelligence Module — Phase: INVESTIGATE"""
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from modules import BaseModule
from utils.banner import print_result

class PhoneIntelModule(BaseModule):
    """Validate phone number and extract carrier, region, and timezone."""
    def run(self) -> dict:
        results = {"number": self.target, "valid": False}
        self.info(f"[PHONE] Querying: {self.target}")
        try:
            parsed = phonenumbers.parse(self.target, None)
            valid  = phonenumbers.is_valid_number(parsed)
            results.update({
                "valid":        valid,
                "e164":         phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                "country_code": parsed.country_code,
                "region":       geocoder.description_for_number(parsed, "en"),
                "carrier":      carrier.name_for_number(parsed, "en"),
                "timezones":    list(timezone.time_zones_for_number(parsed)),
                "number_type":  str(phonenumbers.number_type(parsed)),
            })
            for k, v in results.items():
                if k not in ("number", "valid"):
                    print_result(k.replace("_", " ").title(), str(v), color="cyan")
        except Exception as e:
            results["error"] = str(e); self.error(str(e))
        return results
