"""Thread-safe session logger with optional encryption"""

import threading
import csv
import json
import fcntl
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import uuid

from cryptography.fernet import Fernet

from ..utils.validators import InputValidator
from ..core.exceptions import AysekaiError


class SecureSessionLogger:
    """Thread-safe session logger with optional encryption"""

    def __init__(self, log_dir: Path, encrypt: bool = False):
        """
        Initialize secure session logger.

        Args:
            log_dir: Directory to store log files
            encrypt: Enable encryption for log entries
        """
        self.log_dir = log_dir
        self.log_file = log_dir / "sessions.log"
        self.encrypt = encrypt
        self._lock = threading.Lock()

        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Initialize encryption if enabled
        if self.encrypt:
            self._init_encryption()

        # Ensure log file exists with headers
        self._ensure_log_file()

    def _init_encryption(self) -> None:
        """Initialize or load encryption key"""
        key_file = self.log_dir / ".key"

        if key_file.exists():
            # Load existing key
            with open(key_file, "rb") as f:
                key = f.read()
            self.cipher = Fernet(key)
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)

            # Set restrictive permissions (owner read/write only)
            os.chmod(key_file, 0o600)

            self.cipher = Fernet(key)

    def _ensure_log_file(self) -> None:
        """Ensure log file exists with proper headers"""
        if not self.encrypt and not self.log_file.exists():
            # Create CSV with headers
            headers = [
                "timestamp",
                "user",
                "prompt",
                "name_number",
                "name_transliteration",
                "session_id",
            ]

            with open(self.log_file, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)

    def log_session(
        self, user: str, prompt: str, name_number: int, name_transliteration: str
    ) -> None:
        """
        Log a meditation session with thread safety.

        Args:
            user: User identifier
            prompt: User's intention/prompt
            name_number: Number of the selected name (1-99)
            name_transliteration: Transliteration of the selected name
        """
        with self._lock:
            # Sanitize inputs
            prompt = InputValidator.sanitize_prompt(prompt)
            user = user[:100] if user else "anonymous"  # Limit length

            # Prepare log entry
            entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "user": user,
                "prompt": prompt,
                "name_number": name_number,
                "name_transliteration": name_transliteration,
                "session_id": self._generate_session_id(),
            }

            # Write with file locking
            self._write_log_entry(entry)

    def _write_log_entry(self, entry: Dict[str, Any]) -> None:
        """
        Write log entry with file locking.

        Args:
            entry: Log entry dictionary
        """
        mode = "a" if self.log_file.exists() else "w"

        with open(self.log_file, mode, encoding="utf-8", newline="") as f:
            # Acquire exclusive lock
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)

            try:
                if self.encrypt:
                    # Encrypt and write as hex
                    json_data = json.dumps(entry)
                    encrypted = self.cipher.encrypt(json_data.encode())
                    f.write(encrypted.hex() + "\n")
                else:
                    # Write as CSV
                    writer = csv.DictWriter(f, fieldnames=entry.keys())

                    # Write header for new file
                    if mode == "w" or f.tell() == 0:
                        writer.writeheader()

                    writer.writerow(entry)

            finally:
                # Always release lock
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    def _generate_session_id(self) -> str:
        """
        Generate unique session ID.

        Returns:
            UUID string for session identification
        """
        return str(uuid.uuid4())

    def read_encrypted_logs(self) -> list[Dict[str, Any]]:
        """
        Read and decrypt log entries (utility method).

        Returns:
            List of decrypted log entries

        Raises:
            AysekaiError: If decryption fails
        """
        if not self.encrypt:
            raise AysekaiError("Logger is not configured for encryption")

        if not self.log_file.exists():
            return []

        entries = []

        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        # Decrypt hex-encoded data
                        encrypted_bytes = bytes.fromhex(line)
                        decrypted = self.cipher.decrypt(encrypted_bytes)
                        entry = json.loads(decrypted)
                        entries.append(entry)
                    except Exception as e:
                        # Log corruption or key mismatch
                        raise AysekaiError(f"Failed to decrypt log entry: {e}")

        return entries
