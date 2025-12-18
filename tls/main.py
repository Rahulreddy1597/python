import os
import glob
import yaml
from datetime import datetime, timedelta, timezone
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Configuration
CONFIG_DIR = "cert_configs"
CERTS_DIR = "certs"

REQUIRED_FIELDS = [
    "common_name", "organization", "organizational_unit",
    "country", "state", "locality",
    "validity_days", "renew_if_expires_in_days", "key"
]

# Helper functions
def fail(msg):
    raise ValueError(msg)


def cert_days_left(cert_path):
    """Return remaining validity of a certificate in days (timezone-aware)."""
    with open(cert_path, "rb") as f:
        cert = x509.load_pem_x509_certificate(f.read(), default_backend())
    now = datetime.now(timezone.utc)
    return (cert.not_valid_after_utc - now).total_seconds() / 86400


def load_cert_cfg(path):
    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        cert = data.get("certificate")
    except Exception as e:
        fail(f"Invalid YAML: {e}")

    if not cert:
        fail("Missing 'certificate' block")

    missing = [f for f in REQUIRED_FIELDS if f not in cert]
    if missing:
        fail(f"Missing fields: {', '.join(missing)}")

    if "size" not in cert["key"]:
        fail("Missing key.size")

    return cert

# cert generation
def generate_cert(c, out_dir):
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=c["key"]["size"],
        backend=default_backend()
    )

    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, c["country"]),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, c["state"]),
        x509.NameAttribute(NameOID.LOCALITY_NAME, c["locality"]),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, c["organization"]),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, c["organizational_unit"]),
        x509.NameAttribute(NameOID.COMMON_NAME, c["common_name"]),
    ])

    now = datetime.now(timezone.utc)

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=c["validity_days"]))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(c["common_name"])]),
            critical=False,
        )
        .sign(key, hashes.SHA256(), default_backend())
    )

    os.makedirs(out_dir, exist_ok=True)

    with open(f"{out_dir}/key.pem", "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    with open(f"{out_dir}/cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"[{c['common_name']}] certificate generated")


def reconcile(cfg_path):
    try:
        c = load_cert_cfg(cfg_path)
    except ValueError as e:
        print(f"ERROR [{cfg_path}]: {e}")
        return

    out_dir = f"{CERTS_DIR}/{c['common_name']}"
    cert_path = f"{out_dir}/cert.pem"

    if not os.path.exists(cert_path):
        generate_cert(c, out_dir)
        return

    try:
        days_left = cert_days_left(cert_path)
    except Exception:
        generate_cert(c, out_dir)
        return

    if days_left < c["renew_if_expires_in_days"]:
        generate_cert(c, out_dir)
    else:
        print(f"[{c['common_name']}] still valid ({days_left:.2f} days left)")



# Entry point
def main():
    os.makedirs(CERTS_DIR, exist_ok=True)

    for path in glob.glob(f"{CONFIG_DIR}/*.yaml"):
        reconcile(path)


if __name__ == "__main__":
    main()
