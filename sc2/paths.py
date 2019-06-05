import logging
import os
import platform
import re
from pathlib import Path
from collections import namedtuple

logger = logging.getLogger(__name__)

BASEDIR = {
    "Windows": "C:/Program Files (x86)/StarCraft II",
    "Darwin": "/Applications/StarCraft II",
    "Linux": "~/StarCraftII",
    "WineLinux": "~/.wine/drive_c/Program Files (x86)/StarCraft II",
}

USERPATH = {
    "Windows": "\\Documents\\StarCraft II\\ExecuteInfo.txt",
    "Darwin": "/Library/Application Support/Blizzard/StarCraft II/ExecuteInfo.txt",
    "Linux": None,
    "WineLinux": None,
}

BINPATH = {
    "Windows": "SC2_x64.exe",
    "Darwin": "SC2.app/Contents/MacOS/SC2",
    "Linux": "SC2_x64",
    "WineLinux": "SC2_x64.exe",
}

CWD = {"Windows": "Support64", "Darwin": None, "Linux": None, "WineLinux": "Support64"}

PF = os.environ.get("SC2PF", platform.system())

class Version(namedtuple("Version",
    ["game_version", "build_version", "data_version", "binary"])):
  """Represents a single version of the game."""
  pass


def version_dict(versions):
  return {ver.build_version: ver for ver in versions}


# https://github.com/Blizzard/s2client-proto/blob/master/buildinfo/versions.json
# Generate with bin/gen_versions.py
VERSIONS = version_dict([
    Version("3.13.0", 52910, "8D9FEF2E1CF7C6C9CBE4FBCA830DDE1C", None),
    Version("3.14.0", 53644, "CA275C4D6E213ED30F80BACCDFEDB1F5", None),
    Version("3.15.0", 54518, "BBF619CCDCC80905350F34C2AF0AB4F6", None),
    Version("3.15.1", 54518, "6EB25E687F8637457538F4B005950A5E", None),
    Version("3.16.0", 55505, "60718A7CA50D0DF42987A30CF87BCB80", None),
    Version("3.16.1", 55958, "5BD7C31B44525DAB46E64C4602A81DC2", None),
    Version("3.17.0", 56787, "DFD1F6607F2CF19CB4E1C996B2563D9B", None),
    Version("3.17.1", 56787, "3F2FCED08798D83B873B5543BEFA6C4B", None),
    Version("3.17.2", 56787, "C690FC543082D35EA0AAA876B8362BEA", None),
    Version("3.18.0", 57507, "1659EF34997DA3470FF84A14431E3A86", None),
    Version("3.19.0", 58400, "2B06AEE58017A7DF2A3D452D733F1019", None),
    Version("3.19.1", 58400, "D9B568472880CC4719D1B698C0D86984", None),
    Version("4.0.0", 59587, "9B4FD995C61664831192B7DA46F8C1A1", None),
    Version("4.1.0", 60196, "1B8ACAB0C663D5510941A9871B3E9FBE", None),
    Version("4.1.1", 60321, "5C021D8A549F4A776EE9E9C1748FFBBC", None),
    Version("4.1.2", 60321, "33D9FE28909573253B7FC352CE7AEA40", None),
    Version("4.1.3", 60321, "F486693E00B2CD305B39E0AB254623EB", None),
    Version("4.1.4", 60321, "2E2A3F6E0BAFE5AC659C4D39F13A938C", None),
    Version("4.2.0", 62347, "C0C0E9D37FCDBC437CE386C6BE2D1F93", None),
    Version("4.2.1", 62848, "29BBAC5AFF364B6101B661DB468E3A37", None),
    Version("4.2.2", 63454, "3CB54C86777E78557C984AB1CF3494A0", None),
    Version("4.3.0", 64469, "C92B3E9683D5A59E08FC011F4BE167FF", None),
    Version("4.3.1", 65094, "E5A21037AA7A25C03AC441515F4E0644", None),
    Version("4.3.2", 65384, "B6D73C85DFB70F5D01DEABB2517BF11C", None),
    Version("4.4.0", 65895, "BF41339C22AE2EDEBEEADC8C75028F7D", None),
    Version("4.4.1", 66668, "C094081D274A39219061182DBFD7840F", None),
    Version("4.5.0", 67188, "2ACF84A7ECBB536F51FC3F734EC3019F", None),
    Version("4.5.1", 67188, "6D239173B8712461E6A7C644A5539369", None),
    Version("4.6.0", 67926, "7DE59231CBF06F1ECE9A25A27964D4AE", None),
    Version("4.6.1", 67926, "BEA99B4A8E7B41E62ADC06D194801BAB", None),
    Version("4.6.2", 69232, "B3E14058F1083913B80C20993AC965DB", None),
    Version("4.7.0", 70154, "8E216E34BC61ABDE16A59A672ACB0F3B", None),
    Version("4.7.1", 70154, "94596A85191583AD2EBFAE28C5D532DB", None),
    Version("4.8.0", 71061, "760581629FC458A1937A05ED8388725B", None),
    Version("4.8.1", 71523, "FCAF3F050B7C0CC7ADCF551B61B9B91E", None),
    Version("4.8.2", 71663, "FE90C92716FC6F8F04B74268EC369FA5", None),
    Version("4.8.3", 72282, "0F14399BBD0BA528355FF4A8211F845B", None),
    Version("4.8.4", 73286, "CD040C0675FD986ED37A4CA3C88C8EB5", None),
    Version("4.8.5", 73559, "B2465E73AED597C74D0844112D582595", None),
    Version("4.8.6", 73620, "AA18FEAD6573C79EF707DF44ABF1BE61", None),
    Version("4.9.0", 74071, "70C74A2DCA8A0D8E7AE8647CAC68ACCA", None),
])

def get_env():
    # TODO: Linux env conf from: https://github.com/deepmind/pysc2/blob/master/pysc2/run_configs/platforms.py
    return None



def latest_executeble(versions_dir, version):
    versions = {int(p.name[4:]): p for p in versions_dir.iterdir() if p.is_dir() and p.name.startswith("Base")}
    # latest = max(versions.items())
    # version, path = latest

    path = versions[version]

    if version < 55958:
        logger.critical(f"Your SC2 binary is too old. Upgrade to 3.16.1 or newer.")
        exit(1)
    return path / BINPATH[PF]


class _MetaPaths(type):
    """"Lazily loads paths to allow importing the library even if SC2 isn't installed."""
    def __setup(self):
        if PF not in BASEDIR:
            logger.critical(f"Unsupported platform '{PF}'")
            exit(1)

        try:
            self.VERSION = 73286
            self.NEW_PROTO = False
            self.DATA_VERSION = VERSIONS[self.VERSION].data_version

            base = os.environ.get("SC2PATH")
            if base is None and USERPATH[PF] is not None:
                einfo = str(Path.home().expanduser()) + USERPATH[PF]
                if os.path.isfile(einfo):
                    with open(einfo) as f:
                        content = f.read()
                    if content:
                        base = re.search(r" = (.*)Versions", content).group(1)
                        if not os.path.exists(base):
                            base = None
            if base is None:
                base = BASEDIR[PF]
            self.BASE = Path(base).expanduser()
            self.EXECUTABLE = latest_executeble(self.BASE / "Versions", self.VERSION)
            self.CWD = self.BASE / CWD[PF] if CWD[PF] else None

            self.REPLAYS = self.BASE / "Replays"


            if (self.BASE / "maps").exists():
                self.MAPS = self.BASE / "maps"
            else:
                self.MAPS = self.BASE / "Maps"
        except FileNotFoundError as e:
            logger.critical(f"SC2 installation not found: File '{e.filename}' does not exist.")
            exit(1)

    def __getattr__(self, attr):
        self.__setup()
        return getattr(self, attr)

class Paths(metaclass=_MetaPaths):
    """Paths for SC2 folders, lazily loaded using the above metaclass."""
