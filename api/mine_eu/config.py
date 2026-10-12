"""Runtime settings, read once from the environment."""
from dataclasses import dataclass, field
import os
from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class Settings:
    database_url: str = ''
    admin_token: str = ''
    legal_dir: Path = PKG_ROOT / 'legal'
    font_dirs: tuple = ('/usr/share/fonts/dejavu', '/usr/share/fonts/truetype/dejavu', '/usr/share/fonts/TTF')
    host: str = '127.0.0.1'
    port: int = 8081
    operator_name: str = 'Decision Models (operator of mine.decisionmodels.io)'
    operator_address: str = ''
    rate_per_ip_hour: int = 5
    rate_global_day: int = 50
    max_body: int = 64 * 1024
    # Not secret: bounds the in-memory preview limiter (requests per IP per minute).
    preview_per_minute: int = 30
    extra: dict = field(default_factory=dict)

    @classmethod
    def from_env(cls, env=os.environ):
        s = cls()
        s.database_url = env.get('DATABASE_URL', '').strip()
        s.admin_token = env.get('ADMIN_TOKEN', '').strip()
        if env.get('LEGAL_DIR'):
            s.legal_dir = Path(env['LEGAL_DIR'])
        if env.get('FONT_DIR'):
            s.font_dirs = (env['FONT_DIR'],) + s.font_dirs
        s.host = env.get('API_HOST', s.host)
        s.port = int(env.get('API_PORT', s.port))
        s.operator_name = env.get('OPERATOR_NAME', s.operator_name)
        s.operator_address = env.get('OPERATOR_ADDRESS', s.operator_address)
        s.rate_per_ip_hour = int(env.get('RATE_PER_IP_HOUR', s.rate_per_ip_hour))
        s.rate_global_day = int(env.get('RATE_GLOBAL_DAY', s.rate_global_day))
        return s
