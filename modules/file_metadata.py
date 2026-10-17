"""File Metadata Extraction Module — Phase: RECON"""
import os, subprocess
from modules import BaseModule
from utils.banner import print_result

class FileMetadataModule(BaseModule):
    """Extract metadata from PDF, DOCX, XLSX, images using ExifTool."""
    def run(self) -> dict:
        results = {"file": self.target, "metadata": {}}
        if not os.path.isfile(self.target):
            results["error"] = "File not found"; return results
        self.info(f"[METADATA] Analysing: {self.target}")
        try:
            out = subprocess.check_output(["exiftool", "-json", self.target],
                                          stderr=subprocess.DEVNULL, text=True)
            import json
            data = json.loads(out)
            if data:
                results["metadata"] = data[0]
                for k, v in results["metadata"].items():
                    if k not in ("SourceFile",):
                        print_result(k, str(v)[:80])
        except FileNotFoundError:
            self.warn("exiftool not found — install: sudo apt install libimage-exiftool-perl")
        except Exception as e:
            self.error(str(e))
        return results
