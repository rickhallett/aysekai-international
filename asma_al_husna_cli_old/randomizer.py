import secrets
import hashlib
import time
import os
import threading
from typing import List, Any, Optional
from dataclasses import dataclass


@dataclass
class EntropySource:
    """Represents a source of entropy for randomness"""

    name: str
    value: bytes
    weight: float = 1.0


class UltraRandomizer:
    """
    High-grade pseudo-random number generator combining multiple entropy sources
    for the most truly random selection possible on consumer hardware.
    """

    def __init__(self):
        self.entropy_sources: List[EntropySource] = []
        self._seed_pool = bytearray(256)  # 2048-bit entropy pool

    def add_entropy_source(self, name: str, value: bytes, weight: float = 1.0):
        """Add a new entropy source to the randomizer"""
        self.entropy_sources.append(EntropySource(name, value, weight))

    def collect_system_entropy(self) -> None:
        """Collect entropy from various system sources"""
        # 1. High-precision time (nanosecond)
        time_ns = time.time_ns()
        time_bytes = time_ns.to_bytes(8, "big")
        self.add_entropy_source("time_nanosecond", time_bytes, 1.0)

        # 2. Cryptographically secure random
        crypto_random = secrets.token_bytes(32)
        self.add_entropy_source("crypto_random", crypto_random, 2.0)

        # 3. OS-level random
        os_random = os.urandom(32)
        self.add_entropy_source("os_random", os_random, 2.0)

        # 4. Process and thread information
        process_info = f"{os.getpid()}{threading.current_thread().ident}".encode()
        self.add_entropy_source("process_thread", process_info, 0.5)

        # 5. Memory address randomization (ASLR)
        obj = object()
        memory_addr = id(obj).to_bytes(8, "big")
        self.add_entropy_source("memory_address", memory_addr, 0.5)

        # 6. Performance counter
        perf_counter = int(time.perf_counter_ns()).to_bytes(8, "big")
        self.add_entropy_source("perf_counter", perf_counter, 1.0)

    def add_user_entropy(self, user_input: str) -> None:
        """Add entropy from user input"""
        # Hash user input with SHA-256
        user_hash = hashlib.sha256(user_input.encode("utf-8")).digest()
        self.add_entropy_source("user_input", user_hash, 1.5)

        # Additional hash with time salt
        time_salt = str(time.time_ns()).encode()
        salted_hash = hashlib.sha256(user_input.encode() + time_salt).digest()
        self.add_entropy_source("user_input_salted", salted_hash, 1.0)

    def _mix_entropy(self) -> bytes:
        """Mix all entropy sources using XOR and hashing"""
        # Initialize with crypto random
        mixed = bytearray(secrets.token_bytes(64))

        # XOR mix all entropy sources
        for source in self.entropy_sources:
            # Expand or contract source to 64 bytes
            expanded = bytearray()
            while len(expanded) < 64:
                # Hash the source value with counter for expansion
                hash_input = source.value + len(expanded).to_bytes(4, "big")
                expanded.extend(hashlib.sha512(hash_input).digest())

            # Apply weighted XOR
            for i in range(64):
                weight_byte = int(source.weight * expanded[i % len(expanded)])
                mixed[i] ^= weight_byte & 0xFF

        # Final mixing passes
        for _ in range(3):
            mixed = bytearray(hashlib.sha512(mixed).digest())
            # Rotate bytes
            mixed = mixed[1:] + mixed[:1]

        return bytes(mixed)

    def _fisher_yates_shuffle(self, items: List[Any], random_gen) -> List[Any]:
        """Perform Fisher-Yates shuffle with given random generator"""
        shuffled = items.copy()
        n = len(shuffled)

        for i in range(n - 1, 0, -1):
            j = random_gen.randbelow(i + 1)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]

        return shuffled

    def ultra_shuffle(self, items: List[Any], user_input: str) -> List[Any]:
        """
        Perform ultra-random shuffle combining all entropy sources.
        This is as close to true randomness as possible on consumer hardware.
        """
        # Collect all entropy
        self.collect_system_entropy()
        self.add_user_entropy(user_input)

        # Mix entropy
        mixed_entropy = self._mix_entropy()

        # Create a deterministic random generator from mixed entropy
        # Use secrets.SystemRandom seeded with our entropy
        class SeededRandom:
            def __init__(self, seed: bytes):
                self.seed = seed
                self.counter = 0

            def randbelow(self, n: int) -> int:
                """Generate random number below n using our entropy"""
                # Use counter to ensure different values each call
                hash_input = self.seed + self.counter.to_bytes(8, "big")
                self.counter += 1

                # Generate more bytes than needed for better distribution
                hash_output = hashlib.sha512(hash_input).digest()

                # Convert to integer and reduce modulo n
                # Use rejection sampling for uniform distribution
                bytes_needed = (n.bit_length() + 7) // 8 + 1
                while True:
                    value = int.from_bytes(hash_output[:bytes_needed], "big")
                    if value < n * (256**bytes_needed // n):
                        return value % n
                    # Rehash for new attempt
                    hash_input = hash_output + b"retry"
                    hash_output = hashlib.sha512(hash_input).digest()

        # Create seeded random generator
        random_gen = SeededRandom(mixed_entropy)

        # Perform multiple shuffle passes for extra randomness
        result = items.copy()

        # First pass: Fisher-Yates with our entropy
        result = self._fisher_yates_shuffle(result, random_gen)

        # Second pass: Crypto-random shuffle
        class CryptoRandom:
            def randbelow(self, n: int) -> int:
                return secrets.randbelow(n)

        crypto_gen = CryptoRandom()
        result = self._fisher_yates_shuffle(result, crypto_gen)

        # Third pass: Mix of both
        final_gen = SeededRandom(mixed_entropy + secrets.token_bytes(32))
        result = self._fisher_yates_shuffle(result, final_gen)

        return result

    def select_one(self, items: List[Any], user_input: str) -> Any:
        """Select one item using ultra-random selection"""
        if not items:
            raise ValueError("Cannot select from empty list")

        # For single selection, we still shuffle but take first element
        # This ensures the selection process remains consistent
        shuffled = self.ultra_shuffle(items, user_input)
        return shuffled[0]

    def get_entropy_report(self) -> str:
        """Generate a report of entropy sources used"""
        report = "Entropy Sources:\n"
        for source in self.entropy_sources:
            entropy_bits = len(source.value) * 8
            report += (
                f"- {source.name}: {entropy_bits} bits (weight: {source.weight})\n"
            )

        total_bits = sum(len(s.value) * 8 for s in self.entropy_sources)
        report += f"\nTotal entropy collected: {total_bits} bits"

        return report
